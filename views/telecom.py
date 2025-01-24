from flask import Blueprint, render_template, request
from models import TelecomFeature, Project, ProjectUnit,Unit
from sqlalchemy import and_

telecom_blueprint = Blueprint('telecom', __name__)

@telecom_blueprint.route('/telecoms', methods=['GET'])
def telecom_list():
    """
    根据筛选条件和分页逻辑，展示单项工程造价指标
    """
    # 获取参数
    project_id = request.args.get('project_id', type=int)
    page = request.args.get('page', 1, type=int)  # 默认第 1 页
    per_page = 10  # 每页显示 10 条数据

    # 构建过滤条件
    filters = []
    if project_id:
        # 如果有 project_id，仅筛选该项目
        filters.append(Project.项目表_id == project_id)

    # 获取筛选条件
    project_location = request.args.get('project_location')
    construction_nature = request.args.get('construction_nature')
    price_basis = request.args.get('price_basis')
    cost_type = request.args.get('cost_type')
    road_grade = request.args.get('road_grade')
    search_query = request.args.get('search', '', type=str)

    if search_query:
        filters.append(Project.建设项目工程名称.ilike(f"%{search_query}%"))
    if project_location and project_location != "不限":
        filters.append(Project.项目地点.like(f"%{project_location}%"))
    if construction_nature and construction_nature != "不限":
        filters.append(Project.建设性质 == construction_nature)
    if price_basis and price_basis != "不限":
        filters.append(Project.价格基准期.like(f"%{price_basis}%"))
    if cost_type and cost_type != "不限":
        filters.append(Project.造价类型 == cost_type)
    if road_grade and road_grade != "不限":
        filters.append(Project.道路等级 == road_grade)

    # 查询数据库，结合分页
    query = TelecomFeature.query.join(ProjectUnit).join(Project).filter(and_(*filters))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    projects = pagination.items

    # 计算指标
    results = perform_calculation(projects)

    # 渲染模板
    return render_template(
        'telecoms.html',
        projects=projects,
        results=results,
        pagination=pagination,  # 分页对象
        search_query=search_query,
        request=request,
    )

def perform_calculation(projects):
    """
    根据项目列表计算长度和面积造价指标
    """
    results = []
    for project in projects:
            original_cost = project.工程造价 or 0
            road_length = project.project_unit.project.道路全长 or 1  # 避免除以 0
            road_area = project.project_unit.project.道路总面积 or 1  # 避免除以 0
            cost_index_length = original_cost / road_length
            cost_index_area = original_cost / road_area
         

#将将一个字典添加到 results 列表中，results 是一个列表，append() 方法会将一个新元素添加到该列表中。
            results.append({
                "project_id": project.project_unit.project.项目表_id,
                "项目名称": project.project_unit.project.建设项目工程名称,
                "项目地点": project.project_unit.project.项目地点,
                "建设性质": project.project_unit.project.建设性质,
                "价格基准期": project.project_unit.project.价格基准期,
                "造价类型": project.project_unit.project.造价类型,
                "道路等级": project.project_unit.project.道路等级,
                "道路面积": project.project_unit.project.道路总面积,
                "道路长度": project.project_unit.project.道路全长,
                "长度指标": round(float(cost_index_length), 2),
                "面积指标": round(float(cost_index_area), 2),
                "单位工程": "通信工程"+("/" + str(project.备注) if project.备注 else ""),
            })

    return results

