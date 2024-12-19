from flask import Blueprint, render_template, request
from models import Project
from sqlalchemy import and_

individual_project_blueprint = Blueprint('individual_project', __name__)

@individual_project_blueprint.route('/individual-projects', methods=['GET'])
def individual_project_list():
    """
    根据筛选条件和分页逻辑，展示单项工程造价指标
    """
    # 获取分页参数
    page = request.args.get('page', 1, type=int)  # 默认第 1 页
    per_page = 10  # 每页显示 10 条数据


    # 获取筛选条件
    project_location = request.args.get('project_location')
    construction_nature = request.args.get('construction_nature')
    price_basis = request.args.get('price_basis')
    cost_type = request.args.get('cost_type')
    road_grade = request.args.get('road_grade')
    search_query = request.args.get('search', '', type=str)  # 工程名称关键词搜索
    
    # 构建过滤条件
    filters = []
    if search_query:
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
    projects = pagination.items

    # 计算指标
    results = perform_calculation(projects)

    # 渲染模板
    return render_template(
        'individual_projects.html',
        projects=projects,
        results=results,
        pagination=pagination,
        search_query=search_query,
        request=request  # 将 request 传递给模板
    )


def perform_calculation(projects):
    """
    根据项目列表计算长度和面积造价指标
    """
    results = []
    for project in projects:
        original_cost = project.单项工程费用 or 0
        road_length = project.道路全长 or 1  # 避免除以 0
        road_area = project.道路总面积 or 1  # 避免除以 0
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
