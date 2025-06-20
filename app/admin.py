from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from .forms import WeightsForm, ComfortScoreForm, TypologyStatusForm
from sqlalchemy import func
from .extensions import db
from .models import User, UserType
from .statistics_utils import (
    load_typology_weights,
    update_typology_weight,
    update_comfort_score,
    load_typology_status,
    update_typology_status,
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/', methods=['GET', 'POST'])
@login_required
def statistics():
    weights_form = WeightsForm(prefix='weights')
    score_form = ComfortScoreForm(prefix='score')
    status_form = TypologyStatusForm(prefix='status')

    weights = load_typology_weights()
    status = load_typology_status()
    if request.method == 'GET':
        weights_form.temporistics.data = weights.get('Temporistics', 1.0)
        weights_form.psychosophia.data = weights.get('Psychosophia', 1.0)
        weights_form.amatoric.data = weights.get('Amatoric', 1.0)
        weights_form.socionics.data = weights.get('Socionics', 1.0)
        status_form.temporistics_enabled.data = status.get('Temporistics', True)
        status_form.psychosophia_enabled.data = status.get('Psychosophia', True)
        status_form.amatoric_enabled.data = status.get('Amatoric', True)
        status_form.socionics_enabled.data = status.get('Socionics', True)

    if weights_form.submit.data and weights_form.validate_on_submit():
        update_typology_weight('Temporistics', weights_form.temporistics.data)
        update_typology_weight('Psychosophia', weights_form.psychosophia.data)
        update_typology_weight('Amatoric', weights_form.amatoric.data)
        update_typology_weight('Socionics', weights_form.socionics.data)
        flash('Weights updated', 'success')
        return redirect(url_for('admin.statistics'))

    if status_form.submit_status.data and status_form.validate_on_submit():
        update_typology_status('Temporistics', bool(status_form.temporistics_enabled.data))
        update_typology_status('Psychosophia', bool(status_form.psychosophia_enabled.data))
        update_typology_status('Amatoric', bool(status_form.amatoric_enabled.data))
        update_typology_status('Socionics', bool(status_form.socionics_enabled.data))
        flash('Status updated', 'success')
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
        status_form=status_form,
    )


@admin_bp.route('/distribution')
@login_required
def distribution():
    city_results = (
        db.session.query(User.city, UserType.type_value, func.count(User.id))
        .join(UserType, User.type_id == UserType.id)
        .filter(User.city.isnot(None))
        .group_by(User.city, UserType.type_value)
        .all()
    )
    country_results = (
        db.session.query(User.country, UserType.type_value, func.count(User.id))
        .join(UserType, User.type_id == UserType.id)
        .filter(User.country.isnot(None))
        .group_by(User.country, UserType.type_value)
        .all()
    )

    def prepare_chart_data(results):
        labels = sorted({r[0] for r in results})
        types = sorted({r[1] for r in results})
        datasets = []
        for t in types:
            data = []
            for label in labels:
                count = next((r[2] for r in results if r[0] == label and r[1] == t), 0)
                data.append(count)
            datasets.append({'label': t, 'data': data})
        return {'labels': labels, 'datasets': datasets}

    city_data = prepare_chart_data(city_results)
    country_data = prepare_chart_data(country_results)

    return render_template('admin_distribution.html', city_data=city_data, country_data=country_data)
