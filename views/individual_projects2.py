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
    DrainageFeatureDetail,
    CulvertFeatureDetail,
    TrafficFeatureDetail,
    BridgeFeatureDetail,
    LightingFeatureDetail,
    WaterpipeFeatureDetail,
    ElectricalFeatureDetail,
    TelecomFeatureDetail,
    GreenFeatureDetail,
    TunnelFeatureDetail
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
            "面积": round((project.道路总面积), 2),  # 示例计算
            "面积造价指标": round(feature.工程造价 / (project.道路总面积), 2) ,
            "长度": feature.道路长度,
            "长度造价指标": round(feature.工程造价 / feature.道路长度, 2) ,
            "道路面积":round((feature.道路面积), 2),
            "指标" :'车行道与人行道面积:'+str(round((feature.道路面积), 2))+'m2  '+'指标:'+str(round(feature.工程造价 / (feature.道路面积), 2) )+'元/m2' ,
            "project_unit_id": feature.项目_单位_id  # 添加 project_unit_id
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
            "中央分隔带宽度（m）": detail.中央分隔带宽度,
            "外侧分隔带宽度（m）": detail.外侧分隔带宽度,
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
            "单位工程名称": "桥梁工程" + ("/" + str(feature.备注) if feature.备注 else ""),
            "工程造价": feature.工程造价,
            "面积": feature.桥梁面积,
            "面积造价指标": round(feature.工程造价 / feature.桥梁面积, 2) ,
            "长度": feature.桥梁长度,
            "长度造价指标": round(feature.工程造价 / feature.桥梁长度, 2) ,
            "project_unit_id": feature.项目_单位_id
        })

    # 桥梁工程特征细表
    bridge_details = []
    for feature in bridge_features:
        details = BridgeFeatureDetail.query.filter_by(桥梁工程特征表_id=feature.桥梁工程特征表_id).all()
        bridge_details.extend([
        {
            "桥梁类型": detail.桥梁类型,
            "孔数孔径": detail.孔数孔径,
            "桥面宽度（m）": detail.桥面宽度,
            "桥梁结构形式": detail.桥梁结构形式,
            "上部结构形式": detail.上部结构形式,
            "桥墩结构形式": detail.桥墩结构形式,
            "基础形式 ": detail.基础形式 ,
            "是否景观桥": detail.是否景观桥,
           
        }
        for detail in details
    ])

# 涵洞工程特征
    culvert_features = CulvertFeature.query.filter(
        CulvertFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(culvert_features, start=1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "涵洞工程"+ ("/" + str(feature.备注) if feature.备注 else ""),
            "工程造价": feature.工程造价,
            "面积": feature.涵洞面积,
            "面积造价指标": round(feature.工程造价 / feature.涵洞面积, 2) ,
            "长度": feature.涵洞长度,
            "长度造价指标": round(feature.工程造价 / feature.涵洞长度, 2) ,
            "project_unit_id": feature.项目_单位_id,

        })

# 涵洞工程特征细表
    culvert_details = []
    for feature in culvert_features:
        details = CulvertFeatureDetail.query.filter_by(涵洞工程特征表_id=feature.涵洞工程特征表_id).all()
        culvert_details.extend([
        {
            "涵洞形式": detail.涵洞形式,
            "规格": detail.规格,
            "长度(m)": detail.长度,
            "备注": detail.备注,
           
        }
        for detail in details
    ])


    # 排水工程特征
    drainage_features = DrainageFeature.query.filter(
        DrainageFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(drainage_features, start=len(task_data) + 1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "排水工程",
            "工程造价": feature.工程造价,
            "面积": round((project.道路总面积), 2),  # 示例计算
            "面积造价指标": round(feature.工程造价 / (project.道路总面积), 2) ,
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) ,
            "指标" : '管线长度:'+str(feature.管线长度)+'m'+' '+'指标:'+str(round(feature.工程造价 / feature.管线长度, 2))+ '元/m',
            "project_unit_id": feature.项目_单位_id
        })

# 排水工程特征细表
    drainage_details = []
    for feature in drainage_features:
        details = DrainageFeatureDetail.query.filter_by(排水工程特征表_id=feature.排水工程特征表_id).all()
        drainage_details.extend([
        {
            "管道类型": detail.管道类型,
            "管道材质": detail.管道材质,
            "施工方法": detail.施工方法,
            "管径": detail.管径,
            "长度（m）": detail.长度,
            "备注":detail.备注,
            
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
            "单位工程名称": "交通工程"+ ("/" + str(feature.备注) if feature.备注 else ""),
            "工程造价": feature.工程造价,
            "面积": round((project.道路总面积), 2),
            "面积造价指标": round(feature.工程造价 / (project.道路总面积), 2) ,
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) ,
            "指标" : '交叉口:'+str(feature.交叉口数量)+'个'+' '+'指标:'+str(round(feature.工程造价 / feature.交叉口数量/10000, 2))+ '万元/个' if feature.交叉口数量 else 0, 
            "project_unit_id": feature.项目_单位_id,
        })

    # 交通工程特征细表
    traffic_details = []
    for feature in traffic_features:
        details = TrafficFeatureDetail.query.filter_by(交通工程特征表_id=feature.交通工程特征表_id).all()
        traffic_details.extend([
        {
            "是否含交通信号灯": detail.是否含交通信号灯,
            "是否含交通监控": detail.是否含交通监控,
            "是否含电子警察": detail.是否含电子警察,
            "十字路口个数": detail.十字路口个数,
            "T字路口个数": detail.T字路口个数,
            "备注": detail.备注,
        }    
        for detail in details
    ])

    # 照明工程特征
    lighting_features = LightingFeature.query.filter(
        LightingFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(lighting_features, start=len(task_data) + 1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "照明工程"+ ("/" + str(feature.备注) if feature.备注 else ""),
            "工程造价": feature.工程造价,
            "面积": round((project.道路总面积), 2),
            "面积造价指标": round(feature.工程造价 / (project.道路总面积), 2) ,
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) ,
            "指标" : '路灯数量:'+str(feature.灯杆数量)+'套'+' '+'指标:'+str(round(feature.工程造价 / feature.灯杆数量, 2))+'元/套', 
            "project_unit_id": feature.项目_单位_id,
            
        })
    
    # 照明工程特征细表
    lighting_details = []
    for feature in lighting_features:
        details = LightingFeatureDetail.query.filter_by(照明工程特征表_id=feature.照明工程特征表_id).all()
        lighting_details.extend([
        {
            "照明类型": detail.照明类型,
            "灯杆类型": detail.灯杆类型,
            "箱变数量（座）": detail.箱变数量,
            "备注": detail.备注,
            
        }
        for detail in details
    ])


    # 给水工程特征
    waterpipe_features = WaterpipeFeature.query.filter(
        WaterpipeFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(waterpipe_features, start=len(task_data) + 1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "给水工程",
            "工程造价": feature.工程造价,
            "面积": round((project.道路总面积), 2),
            "面积造价指标": round(feature.工程造价 / (project.道路总面积), 2) ,
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) ,
            "指标" : '管线长度:'+str(feature.管线长度)+'m'+' '+'指标:'+str(round(feature.工程造价 / feature.管线长度, 2))+ '元/m',
            "project_unit_id": feature.项目_单位_id
        })

   # 给水工程特征细表
    waterpipe_details = []
    for feature in waterpipe_features:
        details = WaterpipeFeatureDetail.query.filter_by(给水工程特征表_id=feature.给水工程特征表_id).all()
        waterpipe_details.extend([
        {
            "管径（mm）": detail.管径,
            "管道材质": detail.管道材质,
            "施工方法": detail.施工方法,
            "长度": detail.长度,
            
        }
        for detail in details
    ])
 

   # 电力工程特征
    electrical_features = ElectricalFeature.query.filter(
        ElectricalFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(electrical_features, start=len(task_data) + 1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "电力工程",
            "工程造价": feature.工程造价,
            "面积": round((project.道路总面积), 2),
            "面积造价指标": round(feature.工程造价 / (project.道路总面积), 2) ,
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) ,
            "指标" : '管线长度:'+str(feature.管线长度)+'m'+' '+'指标:'+str(round(feature.工程造价 / feature.管线长度, 2))+ '元/m',
            "project_unit_id": feature.项目_单位_id
        })

# 电力工程特征细表
    electrical_details = []
    for feature in electrical_features:
        details = ElectricalFeatureDetail.query.filter_by(电力工程特征表_id=feature.电力工程特征表_id).all()
        electrical_details.extend([
        {
            "敷设方式": detail.敷设方式,
            "管径（mm）": detail.管径,
            "管材": detail.管材,
            "孔数": detail.孔数,
            "长度（m）": detail.长度,

        }
        for detail in details
    ])



        # 通信工程特征
    telecom_features = TelecomFeature.query.filter(
        TelecomFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(telecom_features, start=len(task_data) + 1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "通信工程",
            "工程造价": feature.工程造价,
            "面积": round((project.道路总面积), 2),
            "面积造价指标": round(feature.工程造价 / (project.道路总面积), 2) ,
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) ,
            "指标" : '管线长度:'+str(feature.管线长度)+'m'+' '+'指标:'+str(round(feature.工程造价 / feature.管线长度, 2))+ '元/m',
            "project_unit_id": feature.项目_单位_id
        })

# 通信工程特征细表
    telecom_details = []
    for feature in telecom_features:
        details = TelecomFeatureDetail.query.filter_by(通信工程特征表_id=feature.通信工程特征表_id).all()
        telecom_details.extend([
        {
            "敷设方式": detail.敷设方式,
            "管径（mm）": detail.管径,
            "管材": detail.管材,
            "孔数": detail.孔数,
            "长度（m）": detail.长度,

        }
        for detail in details
    ])


         # 绿化工程特征
    green_features = GreenFeature.query.filter(
        GreenFeature.项目_单位_id.in_([unit.项目_单位_id for unit in unit_projects])
    ).all()
    for idx, feature in enumerate(green_features, start=len(task_data) + 1):
        task_data.append({
            "序号": idx,
            "单位工程名称": "绿化工程" + ("/" + str(feature.备注) if feature.备注 else ""),
            "工程造价": feature.工程造价,
            "面积": round((project.道路总面积), 2),
            "面积造价指标": round(feature.工程造价 / (project.道路总面积), 2) ,
            "长度": project.道路全长,
            "长度造价指标": round(feature.工程造价 / project.道路全长, 2) ,
            "绿化面积":round((feature.绿化面积), 2),
            "指标" :'绿化面积:'+str(round((feature.绿化面积), 2))+'m2 '+'指标:'+str(round(feature.工程造价 / (feature.绿化面积), 2) )+'元/m2',
            "project_unit_id": feature.项目_单位_id,
            
        })


        # 绿化工程特征细表
    green_details = []
    for feature in green_features:
        details = GreenFeatureDetail.query.filter_by(绿化工程特征表_id=feature.绿化工程特征表_id).all()
        green_details.extend([
        {
            "树池数量（个）": detail.树池数量,
            "乔木数量（株）": detail.乔木数量,
            "灌木数量（株）": detail.灌木数量,
            "地被数量（m2）": detail.地被数量,
            "喷灌长度（m）": detail.喷灌长度,

        }
        for detail in details
    ])


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
            "project_unit_id": feature.项目_单位_id
        })



         # 隧道工程特征细表
    tunnel_details = []
    for feature in tunnel_features:
        details = TunnelFeatureDetail.query.filter_by(隧道工程特征表_id=feature.隧道工程特征表_id).all()
        tunnel_details.extend([
        {
            "隧道工法": detail.隧道工法,
            "长度（m)": detail.长度,
            "面积（m2）": detail.面积,
    
        }
        for detail in details
    ])


    # 渲染模板
    return render_template(
        'individual_projects2.html',
        project=project,
        task_data=task_data,
        road_features=road_features,
        road_details=road_details, # 确保明细表被传递
        drainage_details=drainage_details,
        culvert_details=culvert_details,
        traffic_details=traffic_details,
        bridge_details=bridge_details,
        lighting_details=lighting_details,
        waterpipe_details=waterpipe_details,
        electrical_details=electrical_details,
        telecom_details=telecom_details,
        green_details=green_details,
        tunnel_details=tunnel_details
    )

