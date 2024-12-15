from flask import Blueprint, render_template, request, jsonify
from models import UnitPrice,Project,ProjectUnit
from sqlalchemy import and_,or_

unit_price_blueprint = Blueprint('unit_price', __name__)

@unit_price_blueprint.route('/unit-prices', methods=['GET'])
def unit_price_list():
    """
    Displays comprehensive unit prices with filtering capabilities.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 20

    # 构建筛选条件
    filters = []
    project_location = request.args.get('project_location', '')
    price_basis = request.args.get('price_basis', '')
    cost_type = request.args.get('cost_type', '')
    search = request.args.get('search', '')

    # 根据筛选条件构建查询
    query = UnitPrice.query.join(ProjectUnit).join(Project)

    if project_location:
        filters.append(Project.项目地点 == project_location)
    if price_basis:
        filters.append(Project.价格基准期 == price_basis)
    if cost_type:
        filters.append(Project.造价类型 == cost_type)
    if search:
        filters.append(UnitPrice.项目名称.like(f"%{search}%"))

    # 应用过滤条件
    if filters:
        query = query.filter(and_(*filters))

    # 分页查询
    pagination = query.paginate(page=page, per_page=per_page)
    unit_prices = pagination.items

    # 将数据传递到模板
    data = [
        {
            "unit_price": unit_price,
            "project_name": unit_price.project_unit.project.建设项目工程名称 if unit_price.project_unit else "未关联项目",
            "unit_name": unit_price.project_unit.unit.单位工程名称 if unit_price.project_unit else "未关联单位工程",
            "project_id": unit_price.project_unit.project.项目表_id if unit_price.project_unit else None
        }
        for unit_price in unit_prices
    ]

    return render_template(
        'unit_prices.html',
        unit_prices=data,
        pagination=pagination
    )

@unit_price_blueprint.route('/unit-prices/search', methods=['GET'])
def unit_price_search():
    filters = []
    project_location = request.args.get('project_location')
    price_basis = request.args.get('price_basis')  # 价格基期
    cost_type = request.args.get('cost_type')      # 造价类型
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # 构建查询条件
    query = UnitPrice.query.join(ProjectUnit).join(Project)
    if project_location and project_location != "不限":
        filters.append(Project.项目地点 == project_location)
    if price_basis and price_basis != "不限":
        filters.append(Project.价格基准期 == price_basis)  # 确保字段正确
    if cost_type and cost_type != "不限":
        filters.append(Project.造价类型 == cost_type)  # 确保字段正确
    if search:
        filters.append(or_(UnitPrice.项目名称.like(f"%{search}%"), UnitPrice.项目编码.like(f"%{search}%")))

    if filters:
        query = query.filter(and_(*filters))

    # 分页查询
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    results = pagination.items

    # 格式化返回数据
    data = {
        "results": [
            {
                "unit_price": {
                    "项目编码": item.项目编码,
                    "项目名称": item.项目名称,
                    "项目特征描述": item.项目特征描述,
                    "计量单位": item.计量单位,
                    "工程量": item.工程量,
                    "综合单价": item.综合单价,
                    "综合合价": item.综合合价
                },
                "project_name": item.project_unit.project.建设项目工程名称 if item.project_unit else "未关联项目"
            }
            for item in results
        ],
        "pagination": {
            "total_pages": pagination.pages,
            "current_page": pagination.page,
            "total_items": pagination.total
        }
    }
    return jsonify(data)
