from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .forms import WeightsForm, ComfortScoreForm
from .statistics_utils import (
    load_typology_weights,
    update_typology_weight,
    update_comfort_score,
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/', methods=['GET', 'POST'])
@login_required
def statistics():
    weights_form = WeightsForm(prefix='weights')
    score_form = ComfortScoreForm(prefix='score')

    weights = load_typology_weights()
    if request.method == 'GET':
        weights_form.temporistics.data = weights.get('Temporistics', 1.0)
        weights_form.psychosophia.data = weights.get('Psychosophia', 1.0)
        weights_form.amatoric.data = weights.get('Amatoric', 1.0)
        weights_form.socionics.data = weights.get('Socionics', 1.0)

    if weights_form.submit.data and weights_form.validate_on_submit():
        update_typology_weight('Temporistics', weights_form.temporistics.data)
        update_typology_weight('Psychosophia', weights_form.psychosophia.data)
        update_typology_weight('Amatoric', weights_form.amatoric.data)
        update_typology_weight('Socionics', weights_form.socionics.data)
        flash('Weights updated', 'success')
        return redirect(url_for('admin.statistics'))

    if score_form.submit_score.data and score_form.validate_on_submit():
        try:
            update_comfort_score(
                score_form.typology.data,
                score_form.relationship_type.data,
                int(score_form.score.data),
            )
            flash('Comfort score updated', 'success')
            return redirect(url_for('admin.statistics'))
        except ValueError as exc:
            flash(str(exc), 'danger')

    return render_template(
        'admin_statistics.html',
        weights_form=weights_form,
        score_form=score_form,
    )
