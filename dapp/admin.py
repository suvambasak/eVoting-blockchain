from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, logout_user

from .role import is_admin

admin = Blueprint('admin', __name__)


@admin.route('/admin_panel')
@login_required
def admin_panel():
    if not is_admin(current_user):
        return redirect(url_for('auth.index'))
    return render_template('admin_panel.html')
