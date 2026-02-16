from flask import Blueprint, render_template, request, current_app
import logging

from app.business.services.subscription_service import SubscriptionService

bp = Blueprint("public", __name__)

subscription_service = SubscriptionService()

logger = logging.getLogger(__name__)


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/subscribe")
def subscribe():
    return render_template("subscribe.html")


@bp.route("/subscribe/thank-you")
def subscribe_thank_you():
    return render_template("thank_you.html")


@bp.route("/subscribe/confirm", methods=["POST"])
def subscribe_confirm():
    email = request.form.get("email", "")
    name = request.form.get("name", "")

    newsletters = {
        'kost': 'nl_kost' in request.form,
        'mindset': 'nl_mindset' in request.form,
        'kunskap': 'nl_kunskap' in request.form,
        'veckans_pass': 'nl_veckans_pass' in request.form,
        'jaine': 'nl_jaine' in request.form,
    }

    try:
        result = subscription_service.subscribe(email, name, newsletters)
    except Exception as e:
        logger.error(f"Subscription error: {e}", exc_info=True)
        return render_template(
            "subscribe.html",
            error=f"Database error: {str(e)}",
            email=email,
            name=name,
            newsletters=newsletters,
        ), 500

    if not result.success:
        return render_template(
            "subscribe.html",
            error=result.error,
            email=email,
            name=name,
            newsletters=newsletters,
        )

    response = render_template(
        "thank_you.html",
        email=result.subscriber.email,
        name=result.subscriber.name,
        newsletters=result.subscriber.get_newsletters(),
    )
    return response, 200, {"HX-Redirect": "/subscribe/thank-you"}
