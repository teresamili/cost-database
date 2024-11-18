from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from models import Project


# 定义 individual_project2_blueprint
individual_project2_blueprint = Blueprint('individual_project2', __name__)

# 路由：项目详情页
@individual_project2_blueprint.route('/project/<int:project_id>', methods=['GET'])
def individual_project_detail(project_id):
    # 根据 project_id 查询数据库
    project = Project.query.get_or_404(project_id)  # 如果未找到项目，返回 404 错误
    # 渲染项目详情页面 individual_projects2.html
    return render_template('individual_projects2.html', project=project)