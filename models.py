from flask_sqlalchemy import SQLAlchemy

# 初始化 SQLAlchemy 实例
db = SQLAlchemy()

# 定义中间表，用于关联项目和单位工程
class ProjectUnit(db.Model):
    __tablename__ = '项目_单位'

    项目_单位_id = db.Column(db.Integer, primary_key=True)
    项目表_id = db.Column(db.Integer, db.ForeignKey('项目表.项目表_id'), nullable=False)
    单位工程_id = db.Column(db.Integer, db.ForeignKey('单位工程表.单位工程_id'), nullable=False)

    # 双向关系
    project = db.relationship('Project', back_populates='project_units')
    unit = db.relationship('Unit', back_populates='project_units')


# 定义项目表模型
class Project(db.Model):
    __tablename__ = '项目表'

    项目表_id = db.Column(db.Integer, primary_key=True)
    建设项目工程名称 = db.Column(db.String(225))  # 项目名称
    单项工程费用 = db.Column(db.Numeric(14, 2))  # 工程费用
    造价类型 = db.Column(db.Enum('估算价', '概算价', '预算价', '招标控制价'))  # 项目阶段
    项目地点 = db.Column(db.String(45))  # 项目地点
    价格基准期 = db.Column(db.String(10))  # 价格基准期
    道路等级 = db.Column(db.Enum('快速路', '主干路', '次干路', '支路'))  # 道路等级
    红线宽度 = db.Column(db.Numeric(5, 2))  # 红线宽度
    道路全长 = db.Column(db.Numeric(7, 2))  # 道路全长
    道路总面积 = db.Column(db.Numeric(10, 2)) 
    建设性质 = db.Column(db.Enum('新建', '改建'))

    # 通过中间表关联单位工程
    project_units = db.relationship('ProjectUnit', back_populates='project')
    units = db.relationship('Unit', secondary='项目_单位', viewonly=True)

    def __repr__(self):
        return f'<Project {self.建设项目工程名称}>'


# 定义单位工程表模型
class Unit(db.Model):
    __tablename__ = '单位工程表'

    单位工程_id = db.Column(db.Integer, primary_key=True)
    单位工程名称 = db.Column(db.String(225))  # 单位工程名称

    # 通过中间表关联项目
    project_units = db.relationship('ProjectUnit', back_populates='unit')
    projects = db.relationship('Project', secondary='项目_单位', viewonly=True)

    def __repr__(self):
        return f'<Unit {self.单位工程名称}>'


# 定义道路工程模型
class RoadFeature(db.Model):
    __tablename__ = '道路工程特征表'

    道路工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))
    道路面积 = db.Column('道路面积（m2）', db.Numeric(14, 2))
    道路长度 = db.Column('道路长度（m）', db.Numeric(14, 2))
    备注 = db.Column(db.String(225))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='road_features')

    # 关联到特征明细表
    details = db.relationship('RoadFeatureDetail', back_populates='road_feature')
    
    def __repr__(self):
        return f'<RoadFeature {self.工程造价}>'

# 定义道路工程明细模型    
class RoadFeatureDetail(db.Model):
    __tablename__ = '道路工程特征细表'

    道路工程特征细表_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    道路工程特征表_id = db.Column(db.Integer, db.ForeignKey('道路工程特征表.道路工程特征表_id'), nullable=False)
    机动车道结构层厚度 = db.Column('机动车道结构层厚度（m）',db.Numeric(6, 2), nullable=True, default=None)
    机动车道宽度 = db.Column('机动车道宽度（m）',db.Numeric(6, 2), nullable=True, default=None)
    非机动车道宽度 = db.Column('非机动车道宽度（m）',db.Numeric(6, 2), nullable=True, default=None)
    人行道宽度 = db.Column('人行道宽度（m）',db.Numeric(6, 2), nullable=True, default=None)
    中央分隔带宽度 = db.Column('中央分隔带宽度（m）',db.Numeric(6, 2))
    外侧分隔带宽度 = db.Column('外侧分隔带宽度（m）',db.Numeric(6, 2))
    机动车道面层 = db.Column(db.Enum('沥青混凝土', '水泥混凝土', 'SBS改性沥青混凝土', 'SMA改性沥青玛蹄脂碎石', '其他'), nullable=True, default=None)
    非机动车道面层 = db.Column(db.Enum(
        '沥青混凝土', '水泥混凝土', '彩色沥青混凝土', '彩色水泥混凝土',
        '原色透水沥青混凝土', '原色透水水泥混凝土', '彩色透水沥青混凝土','彩色透水水泥混凝土','其他'
    ), nullable=True, default=None)
    人行道面层 = db.Column(db.Enum(
        '混凝土砖', '普通透水砖', '仿石材透水砖', 'PC砖', '花岗岩石材',
        '彩色沥青混凝土', '彩色水泥混凝土',
        '原色透水沥青混凝土', '原色透水水泥混凝土', '彩色透水沥青混凝土','彩色透水水泥混凝土','其他'
    ), nullable=True, default=None)
    
    是否含软基处理 = db.Column('是否含软基处理',db.Enum('是', '否'), nullable=True, default=None)
    备注 = db.Column(db.String(30), nullable=True, default=None)
    
    # 建立与特征表的关系
    road_feature = db.relationship('RoadFeature', back_populates='details')


# 定义桥梁工程模型
class BridgeFeature(db.Model):
    __tablename__ = '桥梁工程特征表'

    桥梁工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))
    桥梁面积 = db.Column('桥梁面积（m2）', db.Numeric(14, 2))
    桥梁长度 = db.Column('桥梁长度（m）', db.Numeric(14, 2))
    备注 = db.Column(db.String(225)) 

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='bridge_features')

    # 关联到特征明细表
    details = db.relationship('BridgeFeatureDetail', back_populates='bridge_feature')

    def __repr__(self):
        return f'<BridgeFeature {self.工程造价}>'


# 定义桥梁工程明细模型
class BridgeFeatureDetail(db.Model):
    __tablename__ = '桥梁工程特征细表'
    桥梁工程特征细表_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    桥梁工程特征表_id = db.Column(db.Integer,db.ForeignKey('桥梁工程特征表.桥梁工程特征表_id'), nullable=False)
    桥梁结构形式 = db.Column(db.Enum('梁式桥','拱式桥','钢架桥','悬索桥','斜拉桥','其他'))
    上部结构形式 = db.Column(db.Enum('预制空心板','预制小箱梁','预制T梁','预制预应力箱梁','预制装配式箱梁','预制钢混组合箱梁','现浇箱梁','现浇预应力箱梁','钢箱梁','钢管拱桥','连续钢桁梁','砼斜拉桥','钢斜拉桥'))
    桥墩结构形式 = db.Column(db.Enum('实体桥墩','空心桥墩','柱式桥墩','柔性墩','框架墩'))
    基础形式 = db.Column(db.Enum('扩大基础','混凝土灌注桩基础','混凝土预制桩基础','钢管桩基础','沉井基础'))
    是否景观桥 = db.Column(db.Enum('是','否'))

     # 建立与特征表的关系
    bridge_feature = db.relationship('BridgeFeature', back_populates='details')

# 定义涵洞工程模型
class CulvertFeature(db.Model):
    __tablename__ = '涵洞工程特征表'

    涵洞工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))
    涵洞面积 = db.Column('涵洞面积（m2）', db.Numeric(14, 2))
    涵洞长度 = db.Column('涵洞长度（m）', db.Numeric(14, 2))
    备注 = db.Column(db.String(225))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='culvert_features')
    
    # 关联到特征明细表
    details = db.relationship('CulvertFeatureDetail', back_populates='culvert_feature')

    def __repr__(self):
        return f'<CulvertFeature {self.工程造价}>'
    

# 定义涵洞工程明细模型    
class CulvertFeatureDetail(db.Model):
    __tablename__ = '涵洞工程特征细表'

    涵洞工程特征细表_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    涵洞形式 = db.Column(db.Enum('箱涵', '盖板涵', '圆管涵', name='涵洞形式_enum'), nullable=True, default=None)
    规格 = db.Column(db.String(20), nullable=True, default=None)
    长度 = db.Column('长度（m）', db.Numeric(7, 2), nullable=True, default=None)
    涵洞工程特征表_id = db.Column(db.Integer, db.ForeignKey('涵洞工程特征表.涵洞工程特征表_id'), nullable=True)

    # 外键关系声明
    culvert_feature = db.relationship('CulvertFeature', back_populates='details')


# 定义排水工程模型
class DrainageFeature(db.Model):
    __tablename__ = '排水工程特征表'

    排水工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))
    管线长度 = db.Column('管线长度（m）', db.Numeric(14, 2))
    备注 = db.Column(db.String(225))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='drainage_features')

    # 关联到细表
    details = db.relationship('DrainageFeatureDetail', back_populates='drainage_feature')


    def __repr__(self):
        return f'<DrainageFeature {self.工程造价}>'

#定义排水工程细表模型

class DrainageFeatureDetail(db.Model):
    __tablename__ = '排水工程特征细表'

    排水工程特征细表_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    管道类型 = db.Column('管道类型',db.Enum('雨水管', '污水管'),nullable=True,default=None)
    管径 = db.Column('管径（mm）', db.String(225), nullable=True, default=None)
    管道材质 = db.Column(
        db.Enum('钢筋混凝土管', '钢管', 'HDPE管', '球墨铸铁管', 'PVC-U管', 'PE管', '其他'),
        nullable=True,
        default=None
    )
    施工方法 = db.Column(
        db.Enum('开槽', '顶管', '水平定向钻'),
        nullable=True,
        default=None
    )
    长度 = db.Column('长度（m）', db.String(225), nullable=True, default=None)

    备注 = db.Column('备注', db.String(225), nullable=True, default=None)
    排水工程特征表_id = db.Column(db.Integer, db.ForeignKey('排水工程特征表.排水工程特征表_id'), nullable=True)

    # 关系设置
    drainage_feature = db.relationship('DrainageFeature', back_populates='details')

    def __repr__(self):
        return f'<DrainageFeatureDetail {self.排水工程特征细表_id}>'


# 定义交通工程模型
class TrafficFeature(db.Model):
    __tablename__ = '交通工程特征表'

    交通工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    交叉口数量 = db.Column('交叉口（个）', db.Integer, nullable=True, default=None) 
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))
    备注 = db.Column(db.String(225))  

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='traffic_features')

    details = db.relationship('TrafficFeatureDetail', back_populates='traffic_feature')

    def __repr__(self):
        return f'<TrafficFeature {self.工程造价}>'
 
 # 定义交通工程细表模型   

class TrafficFeatureDetail(db.Model):
    __tablename__ = '交通工程特征细表'

    交通工程特征细表_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    是否含交通信号灯 = db.Column(db.Enum('是', '否', name='是否含交通信号灯_enum'), nullable=True, default=None)
    是否含交通监控 = db.Column(db.Enum('是', '否', name='是否含交通监控_enum'), nullable=True, default=None)
    是否含电子警察 = db.Column(db.Enum('是', '否', name='是否含电子警察_enum'), nullable=True, default=None)
    十字路口个数 = db.Column(db.Integer, nullable=True, default=None)
    T字路口个数 = db.Column(db.Integer, nullable=True, default=None)
    交通工程特征表_id = db.Column(db.Integer, db.ForeignKey('交通工程特征表.交通工程特征表_id'), nullable=True)

    # 外键关系声明（可选）
    traffic_feature = db.relationship('TrafficFeature', back_populates='details') 



# 定义照明工程模型
class LightingFeature(db.Model):
    __tablename__ = '照明工程特征表'

    照明工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))
    灯杆数量 = db.Column('灯杆数量（套）', db.Integer) 
    备注 = db.Column(db.String(225))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='lighting_features')

    # 关联到特征明细表
    details = db.relationship('LightingFeatureDetail', back_populates='lighting_feature')

    def __repr__(self):
        return f'<LightingFeature {self.工程造价}>'
    
# 定义照明工程明细模型    
class LightingFeatureDetail(db.Model):
    __tablename__ = '照明工程特征细表'
    
    照明工程特征细表_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    照明工程特征表_id = db.Column(db.Integer, db.ForeignKey('照明工程特征表.照明工程特征表_id'), nullable=False)
    照明类型 = db.Column(db.Enum( '常规照明','景观照明'))
    灯杆类型 = db.Column(db.Enum( '常规灯杆','智慧灯杆','景观灯杆'))
    箱变数量 = db.Column('箱变数量（座）', db.Integer)   
    备注 = db.Column(db.String(225))             

     # 建立与特征表的关系
    lighting_feature = db.relationship('LightingFeature', back_populates='details')

# 定义给水工程模型
class WaterpipeFeature(db.Model):
    __tablename__ = '给水工程特征表'

    给水工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))
    管线长度 = db.Column('管线长度（m）', db.Numeric(14, 2))
    备注 = db.Column(db.String(225))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='waterpipe_features')

      # 关联到特征明细表
    details = db.relationship('WaterpipeFeatureDetail', back_populates='waterpipe_feature')

    def __repr__(self):
        return f'<WaterpipeFeature {self.工程造价}>'

# 定义给水工程明细模型    
class WaterpipeFeatureDetail(db.Model):
    __tablename__ = '给水工程特征细表'

    给水工程特征细表_id = db.Column(db.Integer, primary_key=True)
    给水工程特征表_id = db.Column(db.Integer, db.ForeignKey('给水工程特征表.给水工程特征表_id'), nullable=False)
    管径 = db.Column('管径（mm）', db.String(225), nullable=True, default=None)
    管道材质 = db.Column(db.Enum('球墨铸铁管','钢管','塑料管','复合管'), nullable=True, default=None)
    施工方法= db.Column(db.Enum('开槽','顶管','水平定向钻','沉管'), nullable=True, default=None)
    长度 = db.Column('长度（m）',db.Numeric(9, 2))

     # 建立与特征表的关系
    waterpipe_feature = db.relationship('WaterpipeFeature', back_populates='details')
  


    # 定义电力工程模型
class ElectricalFeature(db.Model):
    __tablename__ = '电力工程特征表'

    电力工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))
    管线长度 = db.Column('管线长度（m）', db.Numeric(14, 2))
    备注 = db.Column(db.String(225))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='electrical_features')
    # 关联到特征明细表
    details = db.relationship('ElectricalFeatureDetail', back_populates='electrical_feature')
    def __repr__(self):
        return f'<ElectricalFeature {self.工程造价}>'
    
# 定义电力工程明细模型    
class ElectricalFeatureDetail(db.Model):
    __tablename__ = '电力工程特征细表'
    
    电力工程特征细表_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    电力工程特征表_id = db.Column(db.Integer, db.ForeignKey('电力工程特征表.电力工程特征表_id'), nullable=False)
    敷设方式 = db.Column(db.Enum('直埋','电力排管','电缆沟','电缆隧道','水平定向钻孔'), nullable=True, default=None)
    管径 = db.Column('管径（mm）',db.String(20), nullable=True, default=None)
    管材 = db.Column(db.Enum('HDPE','PVC','MPP','玻璃钢'))
    孔数 = db.Column(db.String(20))    
    长度= db.Column('长度（m）',db.Numeric(9, 2))     

 # 建立与特征表的关系
    electrical_feature = db.relationship('ElectricalFeature', back_populates='details')

    # 定义通信工程模型
class TelecomFeature(db.Model):
    __tablename__ = '通信工程特征表'

    通信工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))
    管线长度 = db.Column('管线长度（m）', db.Numeric(14, 2))
    备注 = db.Column(db.String(225))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='telecom_features')
    # 关联到特征明细表
    details = db.relationship('TelecomFeatureDetail', back_populates='telecom_feature')
    def __repr__(self):
        return f'<TelecomFeature {self.工程造价}>'
    
# 定义通信工程明细模型    
class TelecomFeatureDetail(db.Model):
    __tablename__ = '通信工程特征细表'
    
    通信工程特征细表_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    通信工程特征表_id = db.Column(db.Integer, db.ForeignKey('通信工程特征表.通信工程特征表_id'), nullable=False)
    敷设方式 = db.Column(db.Enum('直埋','通信排管','电缆管沟','水平定向钻'), nullable=True, default=None)
    管径 = db.Column('管径（mm）',db.String(20), nullable=True, default=None)
    管材 = db.Column(db.Enum('硅芯管','PE','PVC-U','梅花管','格栅管','蜂窝管'))
    孔数 = db.Column(db.String(20))    
    长度= db.Column('长度（m）',db.Numeric(9, 2))     

 # 建立与特征表的关系
    telecom_feature = db.relationship('TelecomFeature', back_populates='details')

    # 定义绿化工程模型
class GreenFeature(db.Model):
    __tablename__ = '绿化工程特征表'

    绿化工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(12, 2))
    绿化面积 = db.Column('绿化面积（m2）', db.Numeric(10, 2))
    备注 = db.Column(db.String(225))  

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='green_features')
    # 关联到特征明细表
    details = db.relationship('GreenFeatureDetail', back_populates='green_feature')
    def __repr__(self):
        return f'<GreenFeature {self.工程造价}>'
    
    # 定义绿化工程明细模型    
class GreenFeatureDetail(db.Model):
    __tablename__ = '绿化工程特征细表'
    
    绿化工程特征细表_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    绿化工程特征表_id = db.Column(db.Integer, db.ForeignKey('绿化工程特征表.绿化工程特征表_id'), nullable=False)   
    树池数量= db.Column('树池数量（个）',db.Numeric(12, 2))     
    乔木数量= db.Column('乔木数量（株）',db.Integer)  
    灌木数量= db.Column('灌木数量（株）',db.Integer)  
    地被数量= db.Column('地被数量（m2）',db.Numeric(12, 2))    
    喷灌长度= db.Column('喷灌长度（m）',db.Numeric(12, 2))   

 # 建立与特征表的关系
    green_feature = db.relationship('GreenFeature', back_populates='details')


    # 定义隧道工程模型
class TunnelFeature(db.Model):
    __tablename__ = '隧道工程特征表'

    隧道工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))
    隧道面积 = db.Column('隧道面积（m2）', db.Numeric(14, 2))
    隧道长度 = db.Column('隧道长度（m）', db.Numeric(14, 2))
    备注 = db.Column(db.String(225))


    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='tunnel_features')
    # 关联到特征明细表
    details = db.relationship('TunnelFeatureDetail', back_populates='tunnel_feature')
    def __repr__(self):
        return f'<TunnelFeature {self.工程造价}>'
    
     # 定义隧道工程明细模型    
class TunnelFeatureDetail(db.Model):
    __tablename__ = '隧道工程特征细表'
    
    隧道工程特征细表_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    隧道工程特征表_id = db.Column(db.Integer, db.ForeignKey('隧道工程特征表.隧道工程特征表_id'), nullable=False)   
    隧道工法 = db.Column(db.Enum('明挖法','矿山法','沉管法','盾构法','顶管法'))
    长度 = db.Column('长度（m）', db.Numeric(9, 2))
    面积 = db.Column('面积（m2）', db.Numeric(9, 2))

 # 建立与特征表的关系
    tunnel_feature = db.relationship('TunnelFeature', back_populates='details')

    
    
    
    #综合单价查询页面
class UnitPrice(db.Model):
    __tablename__ = '清单库'
    清单库_id = db.Column(db.Integer, primary_key=True)
    项目编码 = db.Column(db.String(20))
    项目名称 = db.Column(db.String(45))
    项目特征描述 = db.Column(db.String(500))
    计量单位 = db.Column(db.String(10))
    工程量 = db.Column( db.Numeric(12, 2))
    综合单价 = db.Column( db.Numeric(9, 2))
    综合合价 = db.Column( db.Numeric(14, 2))
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    project_unit = db.relationship('ProjectUnit', backref='unit_prices')  # 关联到项目_单位表


    #人材机单价查询页面
class MaterialPrice(db.Model):
    __tablename__ = '材价库'
    材价库_id = db.Column(db.Integer, primary_key=True)
    材料名称 = db.Column(db.String(45))
    规格型号 = db.Column(db.String(45))
    单位 = db.Column(db.String(45))
    数量 = db.Column( db.Numeric(12, 2))
    不含税单价 = db.Column('不含税单价（元）', db.Numeric(9, 2))
    合计 = db.Column('合计（元）', db.Numeric(14, 2))
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    project_unit = db.relationship('ProjectUnit', backref='material_prices')  # 关联到项目_单位表