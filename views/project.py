from flask import Blueprint, render_template, session, redirect, url_for
from models import Project

project_blueprint = Blueprint('projects', __name__)

@project_blueprint.route('/projects')
def project_list():
    if 'username' in session:
        project_list = Project.query.all()
        return render_template('projects.html', projects=project_list)
    else:
        return redirect(url_for('auth.login'))
