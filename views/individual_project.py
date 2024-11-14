# views/individual_project.py
from flask import Blueprint, render_template, session, redirect, url_for
from models import Project

individual_project_blueprint = Blueprint('individual_project', __name__)

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



def perform_calculation(projects):
    results = []
    for project in projects:
        # 单项工程费用/道路全长
        original_cost = project.单项工程费用 or 0
        road_length = project.道路全长 or 1 # 避免除以0
        road_width = project.红线宽度 or 1
        cost_index_length = original_cost/road_length  
        cost_index_aquare = original_cost/( road_length * road_width )  
    
        # 获取单位工程名称列表,如果没有关联的单位工程，unit_names 将为空列表
        unit_names = [unit.单位工程名称 for unit in project.units] if project.units else []
         # 将计算结果和单位工程名称存储到字典中
        results.append({
            "道路面积指标": round(float(cost_index_aquare), 2),
            "道路长度指标": round(float(cost_index_length), 2),
            "单位工程": ', '.join(unit_names)  # 合并单位工程名称
        })



    return results


