from flask import (
    Blueprint,
    render_template,
    request,
    jsonify,
    current_app,
    redirect,
    url_for,
    flash,
    make_response,
    abort,
)
from flask_login import login_user, logout_user, login_required, current_user
from .forms import RegistrationForm, LoginForm, ProfileForm, EditProfileForm
from .models import User, UserType
from .extensions import db, login_manager
from .services import get_types_by_typology, calculate_relationship
from .typologies import (
    TypologyTemporistics,
    TypologyPsychosophia,
    TypologyAmatoric,
    TypologySocionics,
)
from flask_wtf import FlaskForm
from wtforms import HiddenField
from urllib.parse import urlparse, urljoin
from app.services import get_distance_if_compatible
from werkzeug.utils import secure_filename
import os
from .routes_helper import handle_profile_image_upload, update_user_typology
from .services import create_user_type, assign_user_type
from .statistics_utils import load_typology_status
from .chat_providers import get_chat_provider

main = Blueprint("main", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class EmptyForm(FlaskForm):
    csrf_token = HiddenField()

def get_available_typologies():
    status = load_typology_status()
    return [name for name, enabled in status.items() if enabled]

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc

@main.route("/get_types", methods=["GET"])
def get_types():
    typology_name = request.args.get("typology")
    types = get_types_by_typology(typology_name)
    return jsonify({"types": types})

@main.route("/calculate", methods=["POST"])
def calculate():
    user1_type = request.form.get("user1")
    user2_type = request.form.get("user2")
    typology_name = request.form.get("typology")

    # Проверяем наличие параметров
    if not user1_type or not user2_type or not typology_name:
        flash("Missing required parameters for calculation.", "danger")
        return render_template("result.html", error="Missing required parameters for calculation."), 200

    # Если все параметры на месте, вызываем calculate_relationship
    relationship_type, comfort_score = calculate_relationship(user1_type, user2_type, typology_name)

    debug = current_app.config["DEBUG"]
    logs = "Debug logs or details can be displayed here."
    return render_template(
        "result.html",
        relationship_type=relationship_type,
        comfort_score=comfort_score,
        user1_type=user1_type,
        user2_type=user2_type,
        typology_name=typology_name,
        request_data=request.form,
        logs=logs,
        debug=debug,
    )

@main.route("/", methods=["GET"])
def index():
    if current_user.is_authenticated:
        default_typology_name = "Temporistics"
        types = get_types_by_typology(default_typology_name)
        form = EmptyForm()
        return render_template("index.html", types=types, form=form)
    else:
        return redirect(url_for("main.login"))

@main.route("/change_language", methods=["POST"])
def change_language():
    COOKIE_NAME = "locale"
    COOKIE_EXPIRATION = 60 * 60 * 24 * 30  # 30 днів
    language = request.form.get("language")
    
    # Розширене логування
    current_app.logger.info("=" * 50)
    current_app.logger.info("ЗМІНА МОВИ ЗАПИТАНА")
    current_app.logger.info(f"Запитувана мова: {language}")
    current_app.logger.info(f"Поточні cookie: {request.cookies}")
    current_app.logger.info(f"Метод запиту: {request.method}")
    current_app.logger.info(f"Всі form дані: {request.form}")
    current_app.logger.info(f"Заголовки запиту: {request.headers}")
    current_app.logger.info(f"Підтримувані мови: {current_app.config['LANGUAGES']}")
    
    if language and language in current_app.config["LANGUAGES"]:
        # Створюємо відповідь
        response = make_response(redirect(url_for("main.index")))
        # Встановлюємо cookie з чітко визначеним шляхом і доменом
        response.set_cookie(
            COOKIE_NAME, 
            language, 
            max_age=COOKIE_EXPIRATION,
            path="/",         # Для всього сайту
            httponly=False,   # Доступний для JavaScript
            secure=request.is_secure,  # Якщо HTTPS, ставимо secure
            samesite="Lax"    # Дозволяє cookie при переході з інших сайтів
        )
        
        # Додаємо заголовки для запобігання кешуванню
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

@main.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    available_typologies = get_available_typologies()
    while len(form.typologies) < len(available_typologies):
        form.typologies.append_entry()

    for i, subform in enumerate(form.typologies):
        typology_name = available_typologies[i]
        subform.typology_name.data = typology_name
        available_types = get_types_by_typology(typology_name)
        if available_types:
            subform.type_value.choices = [(t, t) for t in available_types]
        else:
            subform.type_value.choices = [("No available types", "No available types")]

    if request.method == "POST":
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                city=form.city.data,
                country=form.country.data,
                profession=form.profession.data,
                profession_visible=form.show_profession.data,
            )
            user.set_password(form.password.data)
            db.session.add(user)

            last_user_type = None
            for subform in form.typologies:
                ut = create_user_type(
                    typology_name=subform.typology_name.data,
                    type_value=subform.type_value.data,
                    commit=False
                )
                last_user_type = ut

            if last_user_type:
                user.type_id = last_user_type.id

            # Handle profile image if provided
            if form.profile_image.data:
                if not handle_profile_image_upload(form.profile_image.data, user):
                    # Image upload failed, rollback changes
                    db.session.rollback()
                    flash("Error uploading profile image. Please try again.", "danger")
                    return render_template("register.html", title="Register", form=form)

            # If we got here, everything succeeded
            db.session.commit()
            flash("Your account has been created! You can now log in.", "success")
            return redirect(url_for("main.login"))
        else:
            flash("Registration failed. Please correct the errors below and try again.", "danger")

    return render_template("register.html", title="Register", form=form)

@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    google_enabled = 'google' in current_app.blueprints
    github_enabled = 'github' in current_app.blueprints
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and current_app.user_manager.verify_password(form.password.data, user.password_hash):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page) if next_page else redirect(url_for("main.index"))
        else:
            if request.method == "POST":
                current_app.logger.debug(
                    f"Login form validation failed: {form.errors}"
                )
            # Flash the message and render the template in the same request
            flash("Login Unsuccessful", "danger")
            return render_template(
                "login.html",
                title="Login",
                form=form,
                google_enabled=google_enabled,
                github_enabled=github_enabled,
            )
    return render_template(
        "login.html",
        title="Login",
        form=form,
        google_enabled=google_enabled,
        github_enabled=github_enabled,
    )

@main.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login"))

@main.route("/user/<username>", methods=["GET", "POST"])
@login_required
def user_profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    if user != current_user:
        flash("You do not have permission to view or edit this profile.", "danger")
        return redirect(url_for("main.index"))
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
        # Логування даних для діагностики
        current_app.logger.info(f"Updating user profile: {user.username}")
        current_app.logger.info(f"Current email: {user.email}")
        current_app.logger.info(f"New email from form: {form.email.data}")
        
        # Оновлення email
        user.email = form.email.data
        user.city = form.city.data
        user.country = form.country.data
        user.profession = form.profession.data
        user.profession_visible = form.show_profession.data
        current_app.logger.info(f"Email after update: {user.email}")
        
        # Оновлення типології
        assign_user_type(user,
                        typology_name=form.typology_name.data,
                        type_value=form.type_value.data,
                        commit=False)
            
        try:
            db.session.commit()
            current_app.logger.info(f"Email after commit: {user.email}")
            flash("Profile updated successfully.", "success")
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error updating profile: {str(e)}")
            flash(f"An error occurred while updating your profile: {str(e)}. Please try again.", "danger")
        return redirect(url_for("main.user_profile", username=user.username))

    return render_template("profile.html", user=user, form=form, can_edit=(user == current_user))

@main.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        from .repositories.user_repository import update_user_profile
        old_image_filename = current_user.profile_image

        # Update user profile data (no commit yet)
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
            # Перевіряємо формат зображення перед збереженням
            filename = form.profile_image.data.filename
            ext = os.path.splitext(filename.lower())[1]
            if ext not in [".jpg", ".jpeg", ".png"]:
                flash("Invalid image format. Only JPEG and PNG are supported.", "danger")
                db.session.rollback()
                return render_template("edit_profile.html", form=form)
            
            # Спробуємо обробити зображення
            if not handle_profile_image_upload(form.profile_image.data, current_user):
                # Image upload failed, rollback to revert profile changes as well
                db.session.rollback()
                flash("Error uploading profile image. Please try again.", "danger")
                return render_template("edit_profile.html", form=form)

            # If upload succeeded, remove the old image if different
            if old_image_filename and old_image_filename != current_user.profile_image:
                old_image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], old_image_filename)
                if os.path.exists(old_image_path):
                    os.remove(old_image_path)

        # Commit after all updates (including image)
        db.session.commit()
        flash("Profile updated successfully.", "success")
        return redirect(url_for("main.user_profile", username=current_user.username))
    else:
        # Логування помилок валідації
        if form.errors:
            current_app.logger.debug(
                f"Edit profile form validation failed: {form.errors}"
            )

    # If not a POST or form not valid, just display the form
    return render_template("edit_profile.html", form=form)

@main.route("/check_distance", methods=["GET", "POST"])
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

@main.route("/nearby_compatibles")
@login_required
def nearby_compatibles():
    # Получаем всех пользователей кроме текущего
    users = User.query.filter(User.id != current_user.id).all()
    compatible_list = []

    for u in users:
        # Проверяем наличие координат
        if u.latitude is not None and u.longitude is not None and current_user.latitude is not None and current_user.longitude is not None:
            try:
                dist = get_distance_if_compatible(current_user, u)
                # Если дошли до сюда, значит совместимость есть
                compatible_list.append((u, dist))
            except ValueError:
                # Значит несовместимы, пропускаем
                pass

    # Сортируем по расстоянию
    compatible_list.sort(key=lambda x: x[1])

    # Передаем в шаблон список кортежей (пользователь, расстояние)
    return render_template("nearby_compatibles.html", compatible_list=compatible_list)


@main.route("/chat")
@login_required
def chat():
    return render_template("chat.html")


@main.route("/chat_api", methods=["POST"])
@login_required
def chat_api():
    data = request.get_json()
    message = data.get("message", "") if data else ""
    if not message:
        return jsonify({"reply": "No message provided."}), 400

    provider = get_chat_provider()
    try:
        reply = provider.reply(message)
    except Exception as e:
        current_app.logger.error(f"Chat provider error: {e}")
        reply = "Sorry, I cannot respond right now."
    return jsonify({"reply": reply})
