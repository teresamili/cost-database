from flask import Blueprint, render_template, session, redirect, url_for, request
from models import Project
from sqlalchemy import or_

project_blueprint = Blueprint('projects', __name__)

@project_blueprint.route('/projects')
def project_list():
    if 'username' in session:
        # 获取搜索关键词和页码参数
        search_query = request.args.get('search', '', type=str)  # 获取搜索关键词，默认为空
        page = request.args.get('page', 1, type=int)
        per_page = 10  # 每页显示10条数据
        
        # 数据库查询逻辑
        query = Project.query  # 初始查询对象
        
        # 如果有搜索关键词，则过滤数据
        if search_query:
            query = query.filter(
                or_(
                    Project.建设项目工程名称.ilike(f'%{search_query}%'), 
                    
                )
            )
        
        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return render_template(
            'projects.html',
            projects=pagination.items,  # 当前页的数据
            pagination=pagination,      # 分页对象
            search_query=search_query   # 将搜索关键词传递到模板
        )
    else:
        return redirect(url_for('auth.login'))

