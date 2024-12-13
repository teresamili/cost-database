from flask import Blueprint, render_template, request, jsonify
from models import UnitPrice
from sqlalchemy import and_

unit_price_blueprint = Blueprint('unit_price', __name__)

@unit_price_blueprint.route('/unit-prices', methods=['GET'])
def unit_price_list():
    """
    Displays comprehensive unit prices with filtering capabilities.
    """
    # Retrieve filtering conditions
    project_location = request.args.get('project_location')
    price_basis = request.args.get('price_basis')
    cost_type = request.args.get('cost_type')

    # Build filtering conditions
    filters = []
    if project_location and project_location != "不限":
        filters.append(UnitPrice.项目地点 == project_location)
    if price_basis and price_basis != "不限":
        filters.append(UnitPrice.价格基准期 == price_basis)
    if cost_type and cost_type != "不限":
        filters.append(UnitPrice.造价类型 == cost_type)

    # Query database based on filters
    if filters:
        unit_price_list = UnitPrice.query.filter(and_(*filters)).all()
    else:
        unit_price_list = UnitPrice.query.all()

    # Render the template with data
    return render_template(
        'unit_prices.html',
        unit_prices=unit_price_list
    )