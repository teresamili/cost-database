from flask import Blueprint, render_template
from models import (
    LightingFeature, 
    Project, 
    Unit, 
    ProjectUnit, 
    RoadFeature, 
    DrainageFeature, 
    TrafficFeature,
    BridgeFeature,
    CulvertFeature,
    WaterpipeFeature,
    ElectricalFeature,
    TelecomFeature,
    GreenFeature,
    TunnelFeature,
    RoadFeatureDetail,
    DrainageFeatureDetail
)

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

    # 道路工程特征表
    road_features = RoadFeature.query.filter(
        RoadFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(road_features, start=1):

        task_data.append({
            "序号": idx,
            "单位工程名称": "道路工程",
            "工程造价": feature.工程造价,
            "面积": feature.道路面积,
            "面积造价指标": round(feature.工程造价 / feature.道路面积, 2) ,
            "长度": feature.道路长度,
            "长度造价指标": round(feature.工程造价 / feature.道路长度, 2) ,

        })

    # 道路工程特征细表
  
    road_details = []
    for feature in road_features:
        details = RoadFeatureDetail.query.filter_by(道路工程特征表_id=feature.道路工程特征表_id).all()
        road_details.extend([
        {
            "机动车道宽度（m）": detail.机动车道宽度,
            "非机动车道宽度（m）": detail.非机动车道宽度,
            "人行道宽度（m）": detail.人行道宽度,
            "机动车道面层": detail.机动车道面层,
            "非机动车道面层": detail.非机动车道面层,
            "人行道面层": detail.人行道面层,
            "是否含软基处理":detail.是否含软基处理,
            "备注": detail.备注,
        }
        for detail in details
    ])
    
    # 桥梁工程特征
    bridge_features = BridgeFeature.query.filter(
        BridgeFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(bridge_features, start=1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "桥梁工程",
            "工程造价": feature.工程造价,
            "面积": feature.桥梁面积,
            "面积造价指标": round(feature.工程造价 / feature.桥梁面积, 2) ,
            "长度": feature.桥梁长度,
            "长度造价指标": round(feature.工程造价 / feature.桥梁长度, 2) ,
        })

# 涵洞工程特征
    culvert_features = CulvertFeature.query.filter(
        CulvertFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(culvert_features, start=1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "涵洞工程",
            "工程造价": feature.工程造价,
            "面积": feature.涵洞面积,
            "面积造价指标": round(feature.工程造价 / feature.涵洞面积, 2) ,
            "长度": feature.涵洞长度,
            "长度造价指标": round(feature.工程造价 / feature.涵洞长度, 2) ,
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

# 排水工程特征细表
    drainage_details = []
    for feature in drainage_features:
        details = DrainageFeatureDetail.query.filter_by(排水工程特征表_id=feature.排水工程特征表_id).all()
        drainage_details.extend([
        {
           
            "管道材质": detail.管道材质,
            "施工方法": detail.施工方法,
            "管径": detail.管径,
            "长度（m）": detail.长度,
            
        }
        for detail in details
    ])


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

    # 给水工程特征
    waterpipe_features = WaterpipeFeature.query.filter(
        WaterpipeFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(waterpipe_features, start=len(task_data) + 1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "给水工程",
            "工程造价": feature.工程造价,
            "面积": round((project.红线宽度 * project.道路全长), 2),
            "面积造价指标": round(feature.工程造价 / (project.红线宽度 * project.道路全长), 2) if project.红线宽度 and project.道路全长 else "N/A",
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) if project.道路全长 else "N/A",
        })

   # 电力工程特征
    electrical_features = ElectricalFeature.query.filter(
        ElectricalFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(electrical_features, start=len(task_data) + 1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "电力工程",
            "工程造价": feature.工程造价,
            "面积": round((project.红线宽度 * project.道路全长), 2),
            "面积造价指标": round(feature.工程造价 / (project.红线宽度 * project.道路全长), 2) if project.红线宽度 and project.道路全长 else "N/A",
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) if project.道路全长 else "N/A",
        })

        # 通信工程特征
    telecom_features = TelecomFeature.query.filter(
        TelecomFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(telecom_features, start=len(task_data) + 1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "通信工程",
            "工程造价": feature.工程造价,
            "面积": round((project.红线宽度 * project.道路全长), 2),
            "面积造价指标": round(feature.工程造价 / (project.红线宽度 * project.道路全长), 2) if project.红线宽度 and project.道路全长 else "N/A",
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) if project.道路全长 else "N/A",
        })

         # 绿化工程特征
    green_features = GreenFeature.query.filter(
        GreenFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(green_features, start=len(task_data) + 1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "绿化工程",
            "工程造价": feature.工程造价,
            "面积": round((project.红线宽度 * project.道路全长), 2),
            "面积造价指标": round(feature.工程造价 / (project.红线宽度 * project.道路全长), 2) if project.红线宽度 and project.道路全长 else "N/A",
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) if project.道路全长 else "N/A",
        })

        # 隧道工程特征
    tunnel_features = TunnelFeature.query.filter(
        TunnelFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(tunnel_features, start=1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "隧道工程",
            "工程造价": feature.工程造价,
            "面积": feature.隧道面积,
            "面积造价指标": round(feature.工程造价 / feature.隧道面积, 2) ,
            "长度": feature.隧道长度,
            "长度造价指标": round(feature.工程造价 / feature.隧道长度, 2) ,
        })

    # 渲染模板
    return render_template(
        'individual_projects2.html',
        project=project,
        task_data=task_data,
        road_features=road_features,
        road_details=road_details, # 确保明细表被传递
        drainage_details=drainage_details
    )

