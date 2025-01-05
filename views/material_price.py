from flask import Blueprint, render_template, request
from models import MaterialPrice, Project, ProjectUnit
from sqlalchemy import and_

material_price_blueprint = Blueprint('material_price', __name__)

@material_price_blueprint.route('/material-prices', methods=['GET'])
def material_price_list():
    page = request.args.get('page', 1, type=int)
    per_page = 20

    # 获取筛选条件
    project_location = request.args.get('project_location', '')
    price_basis = request.args.get('price_basis', '')
    cost_type = request.args.get('cost_type', '')
    search_query = request.args.get('search', '')
    # 获取当前的请求参数
    args = request.args.to_dict(flat=True)
    args.pop('page', None)  # 移除分页参数

    # 构建过滤条件
    filters = []
    if search_query:
        filters.append(MaterialPrice.材料名称.like(f"%{search_query}%"))
    if project_location and project_location != "不限":
        filters.append(Project.项目地点 == project_location)
    if price_basis and price_basis != "不限":
        filters.append(Project.价格基准期 == price_basis)
    if cost_type and cost_type != "不限":
        filters.append(Project.造价类型 == cost_type)

    # 查询数据库
    query = MaterialPrice.query.join(ProjectUnit).join(Project).filter(and_(*filters))
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    material_prices = pagination.items

    # 构建模板数据
    data = []
    for material_price in material_prices:
        data.append({
            "材料名称": material_price.材料名称,
            "规格型号": material_price.规格型号,
            "单位": material_price.单位,
            "数量": material_price.数量,
            "不含税单价": material_price.不含税单价,
            "合计": material_price.合计,
            "project_name": material_price.project_unit.project.建设项目工程名称 if material_price.project_unit else "未关联项目",
            "unit_name": material_price.project_unit.unit.单位工程名称 if material_price.project_unit else "未关联单位工程",
            "project_id": material_price.project_unit.project.项目表_id if material_price.project_unit else None,
            "project_basis": material_price.project_unit.project.价格基准期 if material_price.project_unit else "N/A",
            "project_location": material_price.project_unit.project.项目地点,
            "cost_type": material_price.project_unit.project.造价类型,
        })



    # 渲染模板
    return render_template(
        'material_prices.html',
        material_prices=material_prices,
        pagination=pagination,
        search_query=search_query,
        data=data,
        args=args,
        material_price_data=[{'material_price': up, 'data': d} for up, d in zip(material_prices, data)]
    )
