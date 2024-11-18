from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from models import Project
from sqlalchemy import and_

individual_project_blueprint = Blueprint('individual_project', __name__) 
@individual_project_blueprint.route('/projects', methods=['GET'])
def get_projects():
    # 此处的 request.args 在请求上下文中，可以正常使用
    page = request.args.get('page', 1, type=int)  # 从请求参数中获取页码
    per_page = 10  # 每页显示10条记录

    # 示例过滤条件
    filters = []  
    project_name = request.args.get('project_name')
    if project_name:
        filters.append(Project.name.like(f"%{project_name}%"))

    # 分页查询
    pagination = Project.query.filter(and_(*filters)).paginate(page=page, per_page=per_page)
    project_list = pagination.items

    # 返回分页数据
    return {
        "projects": [{"id": p.id, "name": p.name} for p in project_list],
        "total_pages": pagination.pages,
        "current_page": pagination.page,
    }


@individual_project_blueprint.route('/individual-projects')
def individual_project_list():
    if 'username' in session:
        # 从数据库查询数据
        project_list = Project.query.all()
        # 对数据进行计算
        calculated_results = perform_calculation(project_list)
        # 将原始数据和计算结果一起传递到模板中
        return render_template('individual_projects.html', projects=project_list, results=calculated_results, zip=zip)
    else:
        return redirect(url_for('auth.login'))

from flask import jsonify
from sqlalchemy import and_

@individual_project_blueprint.route('/search', methods=['GET'])
def search():
    # 获取每行的查询条件
    project_location = request.args.get('project_location')
    construction_nature = request.args.get('construction_nature')
    price_basis = request.args.get('price_basis')
    cost_type = request.args.get('cost_type')
    road_grade = request.args.get('road_grade')

    # 构建查询条件
    filters = []
    if project_location and project_location != "不限":
        filters.append(Project.项目地点 == project_location)
    if construction_nature and construction_nature != "不限":
        filters.append(Project.建设性质 == construction_nature)
    if price_basis and price_basis != "不限":
        filters.append(Project.价格基准期 == price_basis)
    if cost_type and cost_type != "不限":
        filters.append(Project.造价类型 == cost_type)
    if road_grade and road_grade != "不限":
        filters.append(Project.道路等级 == road_grade)

    # 查询数据库
    project_list = Project.query.filter(and_(*filters)).all() if filters else Project.query.all()

    # 调用 perform_calculation 计算结果
    calculated_results = perform_calculation(project_list)

    # 将查询结果转换为字典格式
    result_list = []
    for project, result in zip(project_list, calculated_results):
        result_list.append({
            "建设项目工程名称": project.建设项目工程名称,
            "项目地点": project.项目地点,
            "建设性质": project.建设性质,
            "价格基准期": project.价格基准期,  
            "造价类型": project.造价类型,
            "道路等级": project.道路等级,
            "单项工程费用": project.单项工程费用,
            "道路长度指标": result["道路长度指标"],
            "道路面积指标": result["道路面积指标"],
            "单位工程": result["单位工程"]
        })

    return jsonify(result_list)



def perform_calculation(projects):
    results = []
    for project in projects:
        # 单项工程费用/道路全长
        original_cost = project.单项工程费用 or 0
        road_length = project.道路全长 or 1  # 避免除以0
        road_width = project.红线宽度 or 1
        cost_index_length = original_cost / road_length
        cost_index_area = original_cost / (road_length * road_width)

        # 获取单位工程名称列表
        unit_names = [unit.单位工程名称 for unit in project.units] if project.units else []
        # 将计算结果和单位工程名称存储到字典中
        results.append({
            "道路面积指标": round(float(cost_index_area), 2),
            "道路长度指标": round(float(cost_index_length), 2),
            "单位工程": ', '.join(unit_names)
        })
    return results