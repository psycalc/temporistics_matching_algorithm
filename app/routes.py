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
    abort
)
from flask_login import login_user, logout_user, login_required, current_user
from .forms import RegistrationForm, LoginForm, ProfileForm, EditProfileForm
from .models import User, UserType
from . import db, login_manager
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

main = Blueprint("main", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class EmptyForm(FlaskForm):
    csrf_token = HiddenField()

def get_available_typologies():
    # Предположим, эта функция возвращает список всех доступных типологий динамически.
    # Вы можете реализовать логику получения из базы или конфигурации.
    return ["Temporistics", "Psychosophia", "Amatoric", "Socionics"]

@main.route("/get_types", methods=["GET"])
def get_types():
    typology_name = request.args.get("typology")
    types = get_types_by_typology(typology_name)
    return jsonify({"types": types})

def get_typology_class(typology_name):
    typology_classes = {
        "Temporistics": TypologyTemporistics,
        "Psychosophia": TypologyPsychosophia,
        "Amatoric": TypologyAmatoric,
        "Socionics": TypologySocionics,
    }
    return typology_classes.get(typology_name)

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
    COOKIE_EXPIRATION = 60 * 60 * 24 * 30
    language = request.form.get("language")
    if language and language in current_app.config["LANGUAGES"]:
        response = make_response(redirect(url_for("main.index")))
        response.set_cookie(COOKIE_NAME, language, max_age=COOKIE_EXPIRATION)
        return response
    else:
        current_app.logger.error(
            f"Failed to change language. Supported languages: {current_app.config['LANGUAGES']}"
        )
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

    # Убедимся, что количество entries в form.typologies равно количеству доступных типологий
    while len(form.typologies) < len(available_typologies):
        form.typologies.append_entry()

    # Устанавливаем для каждой типологии её имя и варианты type_value
    for i, subform in enumerate(form.typologies):
        typology_name = available_typologies[i]
        subform.typology_name.data = typology_name  # Ставим имя типологии в hidden_field

        available_types = get_types_by_typology(typology_name)
        if available_types:
            subform.type_value.choices = [(t, t) for t in available_types]
        else:
            subform.type_value.choices = [("No available types", "No available types")]

    if request.method == "POST" and form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        # Создаём UserType для каждой типологии
        last_user_type_id = None
        for subform in form.typologies:
            ut = UserType(
                typology_name=subform.typology_name.data,
                type_value=subform.type_value.data
            )
            db.session.add(ut)
            db.session.commit()
            last_user_type_id = ut.id

        # Привязываем последний созданный user_type к user (просто как пример)
        user.type_id = last_user_type_id
        db.session.commit()

        flash("Your account has been created! You can now log in.", "success")
        return redirect(url_for("main.login"))
    elif request.method == "POST" and not form.validate():
        flash("Registration failed. Please correct the errors below and try again.", "danger")

    return render_template("register.html", title="Register", form=form)

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ("http", "https") and ref_url.netloc == test_url.netloc

@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get("next")
            if not is_safe_url(next_page):
                return abort(400)
            return redirect(next_page) if next_page else redirect(url_for("main.index"))
        else:
            flash("Login Unsuccessful. Please check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)

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

    if form.validate_on_submit():
        user.email = form.email.data
        if not user.user_type:
            user.user_type = UserType(
                typology_name=form.typology_name.data,
                type_value=form.type_value.data
            )
        else:
            user.user_type.typology_name = form.typology_name.data
            user.user_type.type_value = form.type_value.data

        try:
            db.session.commit()
            flash("Profile updated successfully.", "success")
        except Exception:
            db.session.rollback()
            flash("An error occurred while updating your profile. Please try again.", "danger")

        return redirect(url_for("main.user_profile", username=user.username))

    return render_template("profile.html", user=user, form=form)

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
