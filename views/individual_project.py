from flask import Blueprint, render_template, session, redirect, url_for, request, jsonify
from models import Project
from sqlalchemy import and_, or_

individual_project_blueprint = Blueprint('individual_project', __name__)


@individual_project_blueprint.route('/individual-projects', methods=['GET'])
def individual_project_list():
    """
    显示所有项目或根据筛选条件和关键词显示特定项目
    """
    page = request.args.get('page', 1, type=int)  # 获取页码参数，默认为第1页
    per_page = 10  # 每页显示10条数据

    # 获取关键词和筛选条件
    search_query = request.args.get('search', '', type=str)  # 输入框关键词搜索
    project_location = request.args.get('project_location')
    construction_nature = request.args.get('construction_nature')
    price_basis = request.args.get('price_basis')
    cost_type = request.args.get('cost_type')
    road_grade = request.args.get('road_grade')

    # 构建过滤条件
    filters = []
    if search_query:
        # 模糊匹配关键词（项目名称中搜索）
        filters.append(Project.建设项目工程名称.ilike(f"%{search_query}%"))
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

    # 查询数据库，结合分页
    query = Project.query.filter(and_(*filters))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    project_list = pagination.items

    # 调用计算函数
    calculated_results = perform_calculation(project_list)

    # 渲染模板，传递项目列表和分页对象
    return render_template(
        'individual_projects.html',
        projects=project_list,
        results=calculated_results,
        pagination=pagination,
        search_query=search_query,  # 传递关键词给模板
        zip=zip
    )


def perform_calculation(projects):
    results = []
    for project in projects:
        original_cost = project.单项工程费用 or 0
        road_length = project.道路全长 or 1  # 避免除0错误
        road_area = project.道路总面积 or 1  # 避免除0错误
        cost_index_length = original_cost / road_length
        cost_index_area = original_cost / road_area

        # 获取单位工程名称列表
        unit_names = [unit.单位工程名称 for unit in project.units] if project.units else []

        results.append({
            "道路长度指标": round(float(cost_index_length), 2),
            "道路面积指标": round(float(cost_index_area), 2),
            "单位工程": ', '.join(unit_names)
        })
    return results


def perform_calculation(projects):
    results = []
    for project in projects:
        original_cost = project.单项工程费用 or 0
        road_length = project.道路全长 or 1  # 避免除0错误
        road_area = project.道路总面积 or 1  # 避免除0错误
        cost_index_length = original_cost / road_length
        cost_index_area = original_cost / road_area

        # 获取单位工程名称列表
        unit_names = [unit.单位工程名称 for unit in project.units] if project.units else []

        results.append({
            "道路长度指标": round(float(cost_index_length), 2),
            "道路面积指标": round(float(cost_index_area), 2),
            "单位工程": ', '.join(unit_names)
        })
    return results

