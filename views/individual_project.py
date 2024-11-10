# views/individual_project.py
from flask import Blueprint, render_template, session, redirect, url_for
from models import Project

individual_project_blueprint = Blueprint('individual_project', __name__)

@individual_project_blueprint.route('/individual-projects')
def individual_project_list():
    if 'username' in session:
        project_list = Project.query.all()
        return render_template('individual_projects.html', projects=project_list)
    else:
        return redirect(url_for('auth.login'))
