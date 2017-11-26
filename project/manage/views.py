from flask import render_template, redirect, flash, session, url_for, Blueprint
from flask import request
from flask_login import current_user
from app import app, db
from app.models import Competition, Announcement
from project.users.views import login_required
from app.forms import AnnouncementForm

manage_blueprint = Blueprint(
    'manage', __name__,
    template_folder='templates'
)

@manage_blueprint.route('/manage')
@login_required
def manage():
    competitions = Competition.query.filter_by(organizer_id=current_user.wca_id).all()
    return render_template('manage.html', competitions=competitions)


@manage_blueprint.route('/manage/<comp_id>')
@login_required
def manage_comp(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()

    if comp == None:
        flash('Competition is not found.')
        return redirect(url_for('index'))

    return render_template('details.html', comp=comp)

@manage_blueprint.route('/manage/<comp_id>/announcements', methods=['GET', 'POST'])
@login_required
def announcements(comp_id):
    form = AnnouncementForm()

    comp = Competition.query.filter_by(comp_id=comp_id).first()
    query = Announcement.query.filter_by(comp_id=comp.comp_id).all()
    announcements = list(reversed(query))

    if request.method == 'POST':
        if form.validate_on_submit():
            newAnnounce = Announcement(comp.comp_id, current_user.wca_id, form.title.data, form.body.data)
            db.session.add(newAnnounce)
            db.session.commit()

            flash('Posted!')
            return redirect(url_for('manage.manage') + "/" + comp_id +"/announcements")
        else:
            flash('Somethings not working')
            return render_template('announcements.html', form=form, comp=comp, announcements=announcements)




    return render_template('announcements.html', form=form, comp=comp, announcements=announcements)

@app.route('/manage/<comp_id>/announcements/delete', methods=['POST'])
def delete_annc(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()
    delete_id = Announcement.query.filter_by(annc_id=request.form['post_to_delete']).first()

    db.session.delete(delete_id)
    db.session.commit()
    return redirect(url_for('manage.announcements', comp_id=comp.comp_id))

@app.route('/manage/<comp_id>/schedule')
def eventSchedule(comp_id):
    comp = Competition.query.filter_by(comp_id=comp_id).first()
    return render_template('schedule.html', comp=comp)
