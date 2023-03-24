from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user


main = Blueprint('main', __name__)


@main.route('/candidates')
@login_required
def candidates():
    return render_template('candidates.html', user=current_user)
