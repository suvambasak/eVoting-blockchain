from flask import Blueprint, render_template, url_for


main = Blueprint('main', __name__)


@main.route('/candidates')
def candidates():
    return render_template('candidates.html')
