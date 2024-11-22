from flask import Blueprint, render_template
from models import LightingFeature, Project, Unit, ProjectUnit, RoadFeature, DrainageFeature, TrafficFeature

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
    unit_projects = ProjectUnit.query.filter_by(项目表_id=project_id).all()

    # 准备传递到模板的数据
    task_data = []

    # 道路工程特征
    road_features = RoadFeature.query.filter(
        RoadFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(road_features, start=1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "道路工程",
            "工程造价": feature.工程造价,
            "面积": feature.道路面积,
            "面积造价指标": round(feature.工程造价 / feature.道路面积, 2) if feature.道路面积 else "N/A",
            "长度": feature.道路长度,
            "长度造价指标": round(feature.工程造价 / feature.道路长度, 2) if feature.道路长度 else "N/A",
        })

    # 排水工程特征
    drainage_features = DrainageFeature.query.filter(
        DrainageFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(drainage_features, start=len(task_data) + 1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "排水工程",
            "工程造价": feature.工程造价,
            "面积": round((project.红线宽度 * project.道路全长), 2),  # 示例计算
            "面积造价指标": round(feature.工程造价 / (project.红线宽度 * project.道路全长), 2) if project.红线宽度 and project.道路全长 else "N/A",
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) if project.道路全长 else "N/A",
        })

    # 交通工程特征
    traffic_features = TrafficFeature.query.filter(
        TrafficFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(traffic_features, start=len(task_data) + 1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "交通工程",
            "工程造价": feature.工程造价,
            "面积": round((project.红线宽度 * project.道路全长), 2),
            "面积造价指标": round(feature.工程造价 / (project.红线宽度 * project.道路全长), 2) if project.红线宽度 and project.道路全长 else "N/A",
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) if project.道路全长 else "N/A",
        })

    
    # 照明工程特征
    lighting_features = LightingFeature.query.filter(
        LightingFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(lighting_features, start=len(task_data) + 1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "照明工程",
            "工程造价": feature.工程造价,
            "面积": round((project.红线宽度 * project.道路全长), 2),
            "面积造价指标": round(feature.工程造价 / (project.红线宽度 * project.道路全长), 2) if project.红线宽度 and project.道路全长 else "N/A",
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) if project.道路全长 else "N/A",
        })

    # 渲染模板
    return render_template(
        'individual_projects2.html',
        project=project,
        task_data=task_data
    )

