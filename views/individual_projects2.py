from flask import Blueprint, render_template
from models import Project
from models import UnitProject
from models import RoadFeature
from models import DrainageFeature
from models import TrafficFeature

from sqlalchemy.orm import joinedload

# 定义蓝图
individual_project2_blueprint = Blueprint('individual_project2', __name__)

@individual_project2_blueprint.route('/project/<int:project_id>', methods=['GET'])
def project_details(project_id):
    """
    显示单个项目的所有单位工程特征详情页面
    """
    # 查询项目
    project = Project.query.get_or_404(project_id)

    # 查询关联的单位工程
    unit_projects = UnitProject.query.filter(UnitProject.projects.any(项目表_id=project_id)).all()
    print("关联单位工程:", unit_projects)  # 确保在此处定义后使用

    # 道路工程特征
    road_features = RoadFeature.query.filter(
        RoadFeature.项目_单位_id.in_([unit.单位工程_id for unit in unit_projects])
    ).all()
    print("道路工程特征:", road_features)  # 确保定义后使用

    # 排水工程特征
    drainage_features = DrainageFeature.query.filter(
        DrainageFeature.项目_单位_id.in_([unit.单位工程_id for unit in unit_projects])
    ).all()
    print("排水工程特征:", drainage_features)  # 确保定义后使用

    # 交通工程特征
    traffic_features = TrafficFeature.query.filter(
        TrafficFeature.项目_单位_id.in_([unit.单位工程_id for unit in unit_projects])
    ).all()
    print("交通工程特征:", traffic_features)  # 确保定义后使用

    # 准备传递到模板的数据
    task_data = []
    # 准备传递到模板的数据
    task_data = []

    # 道路工程数据处理
    for idx, feature in enumerate(road_features, start=1):
        unit_name = next(
            (unit.单位工程名称 for unit in unit_projects if unit.单位工程_id == feature.项目_单位_id),
            "未知单位工程"
        )
        task_data.append({
            "序号": idx,
            "单位工程名称": unit_name,
            "工程造价": feature.工程造价,
            "道路面积": feature.道路面积,
            "面积造价指标": round(feature.工程造价 / feature.道路面积, 2) if feature.道路面积 else "N/A",
            "道路长度": feature.道路长度,
            "长度造价指标": round(feature.工程造价 / feature.道路长度, 2) if feature.道路长度 else "N/A",
        })

    # 其他特征数据（交通工程、排水工程等）可以按类似逻辑添加到 task_data

    # 渲染模板
    return render_template(
        'individual_projects2.html',
        project=project,
        task_data=task_data
    )