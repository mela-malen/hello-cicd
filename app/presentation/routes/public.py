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

    # Get newsletter selections
    newsletters = {
        'kost': 'nl_kost' in request.form,
        'mindset': 'nl_mindset' in request.form,
        'kunskap': 'nl_kunskap' in request.form,
        'veckans_pass': 'nl_veckans_pass' in request.form,
        'jaine': 'nl_jaine' in request.form,
    }

    result = subscription_service.subscribe(email, name, newsletters)

    if not result.success:
        return render_template(
            "subscribe.html",
            error=result.error,
            email=email,
            name=name,
            newsletters=newsletters,
        )

    return render_template(
        "thank_you.html",
        email=result.subscriber.email,
        name=result.subscriber.name,
        newsletters=result.subscriber.get_newsletters(),
    )
