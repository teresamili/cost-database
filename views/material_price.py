from flask import Blueprint, render_template, request, jsonify
from models import MaterialPrice,Project,ProjectUnit
from sqlalchemy import and_,or_

material_price_blueprint = Blueprint('material_price', __name__)

@material_price_blueprint.route('/material-prices', methods=['GET'])
def material_price_list():
    """
    Displays comprehensive material prices with filtering capabilities.
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
    query = MaterialPrice.query.join(ProjectUnit).join(Project)

    if project_location:
        filters.append(Project.项目地点 == project_location)
    if price_basis:
        filters.append(Project.价格基准期 == price_basis)
    if cost_type:
        filters.append(Project.造价类型 == cost_type)
    if search:
        filters.append(MaterialPrice.材料名称.like(f"%{search}%"))

    # 应用过滤条件
    if filters:
        query = query.filter(and_(*filters))

    # 分页查询
    pagination = query.paginate(page=page, per_page=per_page)
    material_prices = pagination.items

    # 将数据传递到模板
    price = [
        {
            "material_price": material_price,
            "project_name": material_price.project_unit.project.建设项目工程名称 if material_price.project_unit else "未关联项目",
            "unit_name": material_price.project_unit.unit.单位工程名称 if material_price.project_unit else "未关联单位工程",
            "project_id": material_price.project_unit.project.项目表_id if material_price.project_unit else None,
            "project_basis": material_price.project_unit.project.价格基准期 if material_price.project_unit  else "N/A"
        }
        for material_price in material_prices
    ]

    return render_template(
        'material_prices.html',
        material_prices=price,
        pagination=pagination
    )


@material_price_blueprint.route('/material-prices/search', methods=['GET'])
def material_price_search():
    filters = []
    project_location = request.args.get('project_location')
    price_basis = request.args.get('price_basis')  # 价格基期
    cost_type = request.args.get('cost_type')      # 造价类型
    search = request.args.get('search')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    # 构建查询条件
    query = MaterialPrice.query.join(ProjectUnit).join(Project)
    if project_location and project_location != "不限":
        filters.append(Project.项目地点 == project_location)
    if price_basis and price_basis != "不限":
        filters.append(Project.价格基准期 == price_basis)  # 确保字段正确
    if cost_type and cost_type != "不限":
        filters.append(Project.造价类型 == cost_type)  # 确保字段正确
    if search:
        filters.append(or_(MaterialPrice.材料名称.like(f"%{search}%")))

    if filters:
        query = query.filter(and_(*filters))

    # 分页查询
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    results = pagination.items

    # 格式化返回数据
    price = {
        "results": [
            {
                "material_price": {
                    "材料名称": order.材料名称,
                    "规格型号": order.规格型号,
                    "单位": order.单位,
                    "数量": order.数量,
                    "不含税单价": order.不含税单价,
                    "合计": order.合计,
                   
                 
                    
                },
                "project_basis": order.project_unit.project.价格基准期 if order.project_unit and order.project_unit.project else "N/A",
                "project_name": order.project_unit.project.建设项目工程名称 if order.project_unit else "未关联项目",
                "project_id": order.project_unit.project.项目表_id if order.project_unit else None,
                "unit_name": order.project_unit.unit.单位工程名称
            }
            for order in results
        ],
        "pagination": {
            "total_pages": pagination.pages,
            "current_page": pagination.page,
            "total_items": pagination.total
        }
    }
    return jsonify(price)
