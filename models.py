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
    机动车道宽度 = db.Column('机动车道宽度（m）',db.Numeric(6, 2), nullable=True, default=None)
    非机动车道宽度 = db.Column('非机动车道宽度（m）',db.Numeric(6, 2), nullable=True, default=None)
    人行道宽度 = db.Column('人行道宽度（m）',db.Numeric(6, 2), nullable=True, default=None)
    中央分隔带宽度 = db.Column('中央分隔带宽度（m）',db.Numeric(6, 2))
    外侧分隔带宽度 = db.Column('外侧分隔带宽度（m）',db.Numeric(6, 2))
    机动车道面层 = db.Column(db.Enum('沥青混凝土', '水泥混凝土'), nullable=True, default=None)
    非机动车道面层 = db.Column(db.Enum(
        '沥青混凝土', '水泥混凝土', '彩色沥青混凝土', '彩色水泥混凝土',
        '透水沥青混凝土', '透水水泥混凝土', '其他'
    ), nullable=True, default=None)
    人行道面层 = db.Column(db.Enum(
        '混凝土砖', '透水砖', '透水混凝土砖', 'PC砖', '花岗岩石材',
        '透水水泥混凝土', '其他'
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

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='bridge_features')

    def __repr__(self):
        return f'<BridgeFeature {self.工程造价}>'
    
# 定义涵洞工程模型
class CulvertFeature(db.Model):
    __tablename__ = '涵洞工程特征表'

    涵洞工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))
    涵洞面积 = db.Column('涵洞面积（m2）', db.Numeric(14, 2))
    涵洞长度 = db.Column('涵洞长度（m）', db.Numeric(14, 2))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='culvert_features')

    def __repr__(self):
        return f'<CulvertFeature {self.工程造价}>'

# 定义排水工程模型
class DrainageFeature(db.Model):
    __tablename__ = '排水工程特征表'

    排水工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))

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
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='traffic_features')

    def __repr__(self):
        return f'<TrafficFeature {self.工程造价}>'


# 定义照明工程模型
class LightingFeature(db.Model):
    __tablename__ = '照明工程特征表'

    照明工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='lighting_features')

    def __repr__(self):
        return f'<LightingFeature {self.工程造价}>'

# 定义给水工程模型
class WaterpipeFeature(db.Model):
    __tablename__ = '给水工程特征表'

    给水工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='waterpipe_features')

    def __repr__(self):
        return f'<WaterpipeFeature {self.工程造价}>'
    
    # 定义电力工程模型
class ElectricalFeature(db.Model):
    __tablename__ = '电力工程特征表'

    电力工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='electrical_features')

    def __repr__(self):
        return f'<ElectricalFeature {self.工程造价}>'
    
    # 定义通信工程模型
class TelecomFeature(db.Model):
    __tablename__ = '通信工程特征表'

    通信工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='telecom_features')

    def __repr__(self):
        return f'<TelecomFeature {self.工程造价}>'
    
    # 定义绿化工程模型
class GreenFeature(db.Model):
    __tablename__ = '绿化工程特征表'

    绿化工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(12, 2))
    绿化面积 = db.Column('绿化面积（m2）', db.Numeric(10, 2))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='green_features')

    def __repr__(self):
        return f'<GreenFeature {self.工程造价}>'
    
    # 定义隧道工程模型
class TunnelFeature(db.Model):
    __tablename__ = '隧道工程特征表'

    隧道工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))
    隧道面积 = db.Column('隧道面积（m2）', db.Numeric(14, 2))
    隧道长度 = db.Column('隧道长度（m）', db.Numeric(14, 2))


    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='tunnel_features')

    def __repr__(self):
        return f'<TunnelFeature {self.工程造价}>'