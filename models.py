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

    def __repr__(self):
        return f'<RoadFeature {self.工程造价}>'

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

    def __repr__(self):
        return f'<DrainageFeature {self.工程造价}>'


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
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))

    # 关联到项目_单位表
    project_unit = db.relationship('ProjectUnit', backref='green_features')

    def __repr__(self):
        return f'<TelecomFeature {self.工程造价}>'