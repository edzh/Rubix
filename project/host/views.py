from flask import render_template, redirect, flash, session, url_for, request, Blueprint
from flask_login import current_user
from app import app, db
from app.models import Competition, Event
from app.forms import CompetitionForm

from project.users.views import login_required

host_blueprint = Blueprint(
    'host', __name__,
    template_folder='templates'
)

@host_blueprint.route('/host', methods=['GET', 'POST'])
@login_required
def host():
    form = CompetitionForm()

    # form.event.choices =

    if request.method == 'POST':
        if form.validate_on_submit():
            # datetime_object = datetime.strftime(form.date.data, '%Y/%m/%d')
            print(current_user.wca_id)

            newComp = Competition(current_user.id, form.name.data, form.location.data, form.date.data)

            db.session.add(newComp)
            db.session.commit()

            flash(form.name.data + " has been created!")
            return redirect(url_for('manage.manage'))
        else:
            return render_template('host.html', form=form)
    return render_template('host.html', form=form)

