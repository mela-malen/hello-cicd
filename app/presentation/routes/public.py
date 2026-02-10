from flask import Blueprint, render_template, request

from app.business.services.subscription_service import SubscriptionService

bp = Blueprint("public", __name__)

subscription_service = SubscriptionService()


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

    result = subscription_service.subscribe(email, name)

    if not result.success:
        return render_template(
            "subscribe.html",
            error=result.error,
            email=email,
            name=name,
        )

    return render_template(
        "thank_you.html",
        email=result.subscriber.email,
        name=result.subscriber.name,
    )
