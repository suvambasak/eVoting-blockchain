from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user
from .models import Candidate


main = Blueprint('main', __name__)


@main.route('/candidates')
@login_required
def candidates():
    candidates = Candidate.query.with_entities(
        Candidate.id,
        Candidate.roll_number,
        Candidate.name
    ).all()
    return render_template('candidates.html', user=current_user, candidates=candidates)
