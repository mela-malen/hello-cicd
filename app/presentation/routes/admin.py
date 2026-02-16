"""
Admin routes for managing subscribers with authentication.
"""

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify

from app.data.models import User
from app.business.services.subscription_service import SubscriptionService

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

NEWSLETTER_NAMES = {
    'kost': 'Kost & Näring',
    'mindset': 'Mindset',
    'kunskap': 'Kunskap & Forskning',
    'veckans_pass': 'Veckans Pass',
    'jaine': 'Träna med Jaine',
}


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "admin_logged_in" not in session:
            return redirect(url_for("admin.login"))
        return f(*args, **kwargs)
    return decorated_function


@admin_bp.route("/login", methods=["GET", "POST"])
def login():
    """Admin login page."""
    if "admin_logged_in" in session:
        return redirect(url_for("admin.subscribers"))

    error = None
    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        try:
            user = User.query.filter_by(username=username).first()
            if user and user.check_password(password):
                session["admin_logged_in"] = True
                session["admin_username"] = username
                return redirect(url_for("admin.subscribers"))
            else:
                error = "Invalid username or password"
        except Exception as e:
            import logging
            logging.error(f"Login error: {e}")
            error = "Login failed. Please try again."

    return render_template("admin/login.html", error=error)


@admin_bp.route("/logout")
def logout():
    """Log out admin user."""
    session.pop("admin_logged_in", None)
    session.pop("admin_username", None)
    return redirect(url_for("admin.login"))


@admin_bp.route("/subscribers")
@login_required
def subscribers():
    """Display list of all newsletter subscribers."""
    sort_by = request.args.get("sort", "date_desc")
    newsletter_filter = request.args.get("newsletter", None)

    service = SubscriptionService()
    all_subscribers = service.get_all_subscribers(sort_by, newsletter_filter)

    return render_template(
        "admin/subscribers.html",
        subscribers=all_subscribers,
        count=len(all_subscribers),
        current_sort=sort_by,
        current_filter=newsletter_filter,
        newsletter_names=NEWSLETTER_NAMES,
    )


@admin_bp.route("/subscribers/<int:subscriber_id>/edit", methods=["GET", "POST"])
@login_required
def edit_subscriber(subscriber_id: int):
    """Edit a subscriber."""
    service = SubscriptionService()
    subscriber = service.get_subscriber(subscriber_id)

    if not subscriber:
        flash("Subscriber not found", "error")
        return redirect(url_for("admin.subscribers"))

    if request.method == "POST":
        email = request.form.get("email", "")
        name = request.form.get("name", "")
        newsletters = {
            'kost': 'nl_kost' in request.form,
            'mindset': 'nl_mindset' in request.form,
            'kunskap': 'nl_kunskap' in request.form,
            'veckans_pass': 'nl_veckans_pass' in request.form,
            'jaine': 'nl_jaine' in request.form,
        }
        result = service.update_subscriber(subscriber_id, email, name, newsletters)

        if result.success:
            flash("Subscriber updated successfully", "success")
            return redirect(url_for("admin.subscribers"))
        else:
            return render_template(
                "admin/edit_subscriber.html",
                subscriber=subscriber,
                error=result.error,
                newsletter_names=NEWSLETTER_NAMES,
            )

    return render_template(
        "admin/edit_subscriber.html",
        subscriber=subscriber,
        newsletter_names=NEWSLETTER_NAMES,
    )


@admin_bp.route("/subscribers/<int:subscriber_id>/delete", methods=["POST"])
@login_required
def delete_subscriber(subscriber_id: int):
    """Delete a subscriber."""
    service = SubscriptionService()
    if service.delete_subscriber(subscriber_id):
        flash("Subscriber deleted successfully", "success")
    else:
        flash("Failed to delete subscriber", "error")
    return redirect(url_for("admin.subscribers"))


@admin_bp.route("/subscribers/delete-multiple", methods=["POST"])
@login_required
def delete_multiple_subscribers():
    """Delete multiple subscribers."""
    data = request.get_json()
    ids = data.get("ids", [])
    service = SubscriptionService()
    deleted_count = 0
    for subscriber_id in ids:
        if service.delete_subscriber(int(subscriber_id)):
            deleted_count += 1
    return jsonify({"success": True, "deleted": deleted_count})


@admin_bp.route("/subscribers/update-newsletters", methods=["POST"])
@login_required
def update_newsletters_bulk():
    """Update newsletters for multiple subscribers."""
    data = request.get_json()
    ids = data.get("ids", [])
    action = data.get("action", "")  # "add" or "remove"
    newsletter = data.get("newsletter", "")

    if not ids or not action or not newsletter:
        return jsonify({"success": False, "error": "Missing parameters"})

    if newsletter not in NEWSLETTER_NAMES:
        return jsonify({"success": False, "error": "Invalid newsletter"})

    service = SubscriptionService()
    newsletters = {newsletter: action == "add"}
    updated = service.update_newsletters_bulk([int(i) for i in ids], newsletters)

    return jsonify({"success": True, "updated": updated})
