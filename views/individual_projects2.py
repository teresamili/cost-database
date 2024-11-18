from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from models import Project
from sqlalchemy import and_

individual_project2_blueprint = Blueprint('individual_project2',__name__)

@individual_project2_blueprint.route('/project/<int:project_id>')
def individual_project2_details(project_id):
    project = Project.query.get(project_id)
    return render_template('individual_projects2.html', project=project)