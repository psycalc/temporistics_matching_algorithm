from flask import Blueprint, render_template, request, jsonify, current_app, redirect, url_for, flash, make_response
from flask_login import login_required, current_user
from ..forms import ProfileForm, EditProfileForm
from ..models import User, UserType
from ..extensions import db
from ..services import get_types_by_typology, get_distance_if_compatible
from ..routes_helper import handle_profile_image_upload
import os
from flask_wtf import FlaskForm
from wtforms import HiddenField

profile_bp = Blueprint('profile', __name__)

class EmptyForm(FlaskForm):
    csrf_token = HiddenField()


def index():
    if current_user.is_authenticated:
        default_typology_name = "Temporistics"
        types = get_types_by_typology(default_typology_name)
        form = EmptyForm()
        return render_template("index.html", types=types, form=form)
    else:
        return redirect(url_for("auth.login"))

profile_bp.add_url_rule('/', view_func=index, methods=['GET'])


@profile_bp.route('/change_language', methods=['POST'])
def change_language():
    COOKIE_NAME = "locale"
    COOKIE_EXPIRATION = 60 * 60 * 24 * 30  # 30 днів
    language = request.form.get("language")

    current_app.logger.info("=" * 50)
    current_app.logger.info("ЗМІНА МОВИ ЗАПИТАНА")
    current_app.logger.info(f"Запитувана мова: {language}")
    current_app.logger.info(f"Поточні cookie: {request.cookies}")
    current_app.logger.info(f"Метод запиту: {request.method}")
    current_app.logger.info(f"Всі form дані: {request.form}")
    current_app.logger.info(f"Заголовки запиту: {request.headers}")
    current_app.logger.info(f"Підтримувані мови: {current_app.config['LANGUAGES']}")

    if language and language in current_app.config["LANGUAGES"]:
        response = make_response(redirect(url_for("profile.index")))
        response.set_cookie(
            COOKIE_NAME,
            language,
            max_age=COOKIE_EXPIRATION,
            path="/",
            httponly=False,
            secure=request.is_secure,
            samesite="Lax"
        )
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        current_app.logger.info(f"Cookie встановлено: {COOKIE_NAME}={language}, max_age={COOKIE_EXPIRATION}")
        current_app.logger.info(f"Всі заголовки відповіді: {response.headers}")
        current_app.logger.info("=" * 50)
        return response
    else:
        current_app.logger.error(
            f"Помилка зміни мови. Мова '{language}' не підтримується. Підтримувані мови: {current_app.config['LANGUAGES']}"
        )
        current_app.logger.info("=" * 50)
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Language change failed. Please select a supported language.",
                }
            ),
            400,
        )


@profile_bp.route('/user/<username>', methods=['GET', 'POST'])
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        flash("You do not have permission to view or edit this profile.", "danger")
        return redirect(url_for("profile.index"))
    form = ProfileForm()
    if request.method == "GET":
        form.email.data = user.email
        if user.user_type:
            form.typology_name.data = user.user_type.typology_name
            form.type_value.data = user.user_type.type_value
        form.city.data = user.city
        form.country.data = user.country
        form.profession.data = user.profession
        form.show_profession.data = user.profession_visible

    if form.validate_on_submit():
        current_app.logger.info(f"Updating user profile: {user.username}")
        current_app.logger.info(f"Current email: {user.email}")
        current_app.logger.info(f"New email from form: {form.email.data}")
        user.email = form.email.data
        user.city = form.city.data
        user.country = form.country.data
        user.profession = form.profession.data
        user.profession_visible = form.show_profession.data
        current_app.logger.info(f"Email after update: {user.email}")
        if not user.user_type:
            user.user_type = UserType(
                typology_name=form.typology_name.data,
                type_value=form.type_value.data,
            )
        else:
            user.user_type.typology_name = form.typology_name.data
            user.user_type.type_value = form.type_value.data
        try:
            db.session.commit()
            current_app.logger.info(f"Email after commit: {user.email}")
            flash("Profile updated successfully.", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating profile: {str(e)}")
            flash(f"An error occurred while updating your profile: {str(e)}. Please try again.", "danger")
        return redirect(url_for("profile.user_profile", username=user.username))

    return render_template("profile.html", user=user, form=form, can_edit=(user == current_user))


@profile_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        from ..services import update_user_profile
        old_image_filename = current_user.profile_image
        update_user_profile(
            current_user,
            username=form.username.data,
            email=form.email.data,
            typology_name=form.typology_name.data,
            type_value=form.type_value.data,
            latitude=form.latitude.data,
            longitude=form.longitude.data,
            city=form.city.data,
            country=form.country.data,
            profession=form.profession.data,
            profession_visible=form.show_profession.data,
            max_distance=form.max_distance.data,
        )
        if form.profile_image.data:
            filename = form.profile_image.data.filename
            ext = os.path.splitext(filename.lower())[1]
            if ext not in [".jpg", ".jpeg", ".png"]:
                flash("Invalid image format. Only JPEG and PNG are supported.", "danger")
                db.session.rollback()
                return render_template("edit_profile.html", form=form)
            if not handle_profile_image_upload(form.profile_image.data, current_user):
                db.session.rollback()
                flash("Error uploading profile image. Please try again.", "danger")
                return render_template("edit_profile.html", form=form)
            if old_image_filename and old_image_filename != current_user.profile_image:
                old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_image_filename)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("profile.user_profile", username=current_user.username))
    else:
        if form.errors:
            print(f"Form validation failed: {form.errors}")
    return render_template("edit_profile.html", form=form)


@profile_bp.route('/check_distance', methods=['GET', 'POST'])
@login_required
def check_distance():
    if request.method == "POST":
        other_username = request.form.get("other_username")
        other_user = User.query.filter_by(username=other_username).first()
        if not other_user:
            flash("User not found", "danger")
            return render_template("check_distance_form.html")
        try:
            dist = get_distance_if_compatible(current_user, other_user)
            return render_template("check_distance_result.html", distance=dist, user=other_user)
        except ValueError as e:
            flash(str(e), "danger")
            return render_template("check_distance_form.html")
    else:
        return render_template("check_distance_form.html")


@profile_bp.route('/nearby_compatibles')
@login_required
def nearby_compatibles():
    users = User.query.filter(User.id != current_user.id).all()
    compatible_list = []
    for u in users:
        if u.latitude is not None and u.longitude is not None and current_user.latitude is not None and current_user.longitude is not None:
            try:
                dist = get_distance_if_compatible(current_user, u)
                compatible_list.append((u, dist))
            except ValueError:
                pass
    compatible_list.sort(key=lambda x: x[1])
    return render_template("nearby_compatibles.html", compatible_list=compatible_list)
