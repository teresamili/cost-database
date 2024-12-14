from flask import Blueprint, render_template, request
from models import UnitPrice
from sqlalchemy import and_

unit_price_blueprint = Blueprint('unit_price', __name__)

@unit_price_blueprint.route('/unit-prices', methods=['GET'])
def unit_price_list():
    """
    Displays comprehensive unit prices with filtering capabilities.
    """
    page = request.args.get('page', 1, type=int)
    per_page = 20

    # 构建筛选条件（示例）
    filters = []
    price_basis = request.args.get('price_basis')
    if price_basis and price_basis != "不限":
        filters.append(UnitPrice.价格基准期 == price_basis)

    # 查询并分页
    if filters:
        pagination = UnitPrice.query.filter(*filters).paginate(page=page, per_page=per_page)
    else:
        pagination = UnitPrice.query.paginate(page=page, per_page=per_page)

    unit_prices = pagination.items

    # 将项目名称和单位工程名称组合到一起
    data = [
        {
            "unit_price": unit_price,
            "project_name": unit_price.项目_单位.project.建设项目工程名称 if unit_price.项目_单位 else "未关联项目",
            "unit_name": unit_price.项目_单位.unit.单位工程名称 if unit_price.项目_单位 else "未关联单位工程",
            "project_id":unit_price.项目_单位.project.项目表_id
        }
        for unit_price in unit_prices
    ]

    return render_template(
        'unit_prices.html',
        unit_prices=data,
        pagination=pagination
    )
