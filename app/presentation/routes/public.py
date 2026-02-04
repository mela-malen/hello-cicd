import re
from flask import Blueprint, render_template, request

bp = Blueprint("public", __name__)

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"


def validate_email(email: str) -> tuple[bool, str]:
    if not email or not email.strip():
        return False, "Email is required"
    if not re.match(EMAIL_PATTERN, email.strip()):
        return False, "Invalid email format"
    return True, ""


def normalize_email(email: str) -> str:
    return email.lower().strip()


def normalize_name(name: str | None) -> str:
    if not name or not name.strip():
        return "Subscriber"
    return name.strip()


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/subscribe")
def subscribe():
    return render_template("subscribe.html")


@bp.route("/subscribe/confirm", methods=["POST"])
def subscribe_confirm():
    email = request.form.get("email", "")
    name = request.form.get("name", "")

    is_valid, error = validate_email(email)
    if not is_valid:
        return render_template(
            "subscribe.html",
            error=error,
            email=email,
            name=name,
        )

    normalized_email = normalize_email(email)
    normalized_name = normalize_name(name)

    return render_template(
        "thank_you.html",
        email=normalized_email,
        name=normalized_name,
    )
