from flask import Blueprint, render_template, request
from models import Project, UnitPrice, ProjectUnit, Unit
from sqlalchemy import and_, or_

unit_price_blueprint = Blueprint('unit_price', __name__)

@unit_price_blueprint.route('/unit_prices', methods=['GET'])
def unit_price_list():
    """
    根据筛选条件和分页逻辑，展示综合单价指标
    """
    # 获取分页参数
    project_unit_id = request.args.get('project_unit_id', type=int)
    project_unit_id = request.args.get('project_unit_id', type=int)
    page = request.args.get('page', 1, type=int)  # 默认第 1 页
    per_page = 10  # 每页显示 10 条数据

    # 构建过滤条件
    filters = []
    if project_unit_id:
        # 如果有 project_unit_id，仅筛选该项目
        filters.append(UnitPrice.项目_单位_id == project_unit_id)


    # 获取筛选条件
    project_location = request.args.get('project_location')
    price_basis = request.args.get('price_basis')
    cost_type = request.args.get('cost_type')
    search_query = request.args.get('search', '', type=str)  # 关键词搜索
    args = request.args.to_dict(flat=True)
    args.pop('page', None)  # 移除 page 参数

    if search_query:
        filters.append(
            or_(
                UnitPrice.项目名称.ilike(f"%{search_query}%"),
                UnitPrice.项目编码.ilike(f"%{search_query}%"),
                UnitPrice.项目特征描述.ilike(f"%{search_query}%")
            )
        )
    if project_location and project_location != "不限":
        filters.append(Project.项目地点.like(f"%{project_location}%"))
    if price_basis and price_basis != "不限":
        filters.append(Project.价格基准期.like(f"%{price_basis}%"))  # **确保模糊匹配**
    if cost_type and cost_type != "不限":
        filters.append(Project.造价类型 == cost_type)

    # **修正查询**
    query = UnitPrice.query.join(ProjectUnit).join(Project).filter(and_(*filters))
    pagination = query.paginate(page=page, per_page=10, error_out=False)
    unit_prices = pagination.items

    # **处理数据**
    data = []
    for unit_price in unit_prices:
        data.append({
            "project_name": unit_price.project_unit.project.建设项目工程名称 if unit_price.project_unit else "未关联项目",
            "unit_name": unit_price.project_unit.unit.单位工程名称 if unit_price.project_unit else "未关联单位工程",
            "project_id": unit_price.project_unit.project.项目表_id if unit_price.project_unit else " ",
            "project_unit_id": unit_price.项目_单位_id,
            "project_basis": unit_price.project_unit.project.价格基准期 if unit_price.project_unit and unit_price.project_unit.project else "N/A",
            "project_location": unit_price.project_unit.project.项目地点,
            "cost_type": unit_price.project_unit.project.造价类型,
        })

    # **渲染模板**
    return render_template(
        'unit_prices.html',
        unit_prices=unit_prices,
        pagination=pagination,
        search_query=search_query,
        request=request,
        data=data,
        args=args, 
        unit_price_data=[{'unit_price': up, 'data': d} for up, d in zip(unit_prices, data)]
    )

