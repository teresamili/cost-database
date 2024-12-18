from flask import Blueprint, render_template, session, redirect, url_for, request
from models import Project

project_blueprint = Blueprint('projects', __name__)

@project_blueprint.route('/projects')
def project_list():
    if 'username' in session:
        page = request.args.get('page', 1, type=int)  # 获取页码参数，默认为第1页
        per_page = 10  # 每页显示10条数据
        
        # 添加分页查询
        pagination = Project.query.paginate(page=page, per_page=per_page, error_out=False)
        
        return render_template(
            'projects.html',
            projects=pagination.items,  # 当前页的数据
            pagination=pagination       # 传递pagination对象到模板
        )
    else:
        return redirect(url_for('auth.login'))

