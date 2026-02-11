"""
Admin routes for managing subscribers with authentication.
"""

from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify

from app.data.models import User
from app.business.services.subscription_service import SubscriptionService

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


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

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["admin_logged_in"] = True
            session["admin_username"] = username
            return redirect(url_for("admin.subscribers"))
        else:
            error = "Invalid username or password"

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
    service = SubscriptionService()
    all_subscribers = service.get_all_subscribers(sort_by)
    return render_template(
        "admin/subscribers.html",
        subscribers=all_subscribers,
        count=len(all_subscribers),
        current_sort=sort_by,
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
        result = service.update_subscriber(subscriber_id, email, name)

        if result.success:
            flash("Subscriber updated successfully", "success")
            return redirect(url_for("admin.subscribers"))
        else:
            return render_template(
                "admin/edit_subscriber.html",
                subscriber=subscriber,
                error=result.error,
            )

    return render_template("admin/edit_subscriber.html", subscriber=subscriber)


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
