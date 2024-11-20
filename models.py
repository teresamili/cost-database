from flask_sqlalchemy import SQLAlchemy

# 初始化 SQLAlchemy 实例
db = SQLAlchemy()

# 中间表，用于关联项目和单位工程
project_unit_association = db.Table('项目_单位',
    db.Column('项目表_id', db.Integer, db.ForeignKey('项目表.项目表_id'), primary_key=True),
    db.Column('单位工程_id', db.Integer, db.ForeignKey('单位工程表.单位工程_id'), primary_key=True)
)

# 定义项目表模型
class Project(db.Model):
    __tablename__ = '项目表'  # 表名

    # 定义字段 .Column是一个特殊类。它来描述模型类中的每一个字段与数据库表中的一列之间的对应关系。
    项目表_id = db.Column(db.Integer, primary_key=True)               # 主键
    建设项目工程名称 = db.Column(db.String(225))                     # 项目名称
    单项工程费用 = db.Column(db.Numeric(14, 2))                       # 工程费用
    造价类型 = db.Column(db.Enum('估算价','概算价','预算价','招标控制价'))  # 项目阶段
    项目地点 = db.Column(db.String(45))                               # 项目地点
    价格基准期 = db.Column(db.Date)                                   # 价格基准期
    道路等级 = db.Column(db.Enum('快速路', '主干路', '次干路', '支路'))   # 道路等级
    红线宽度 = db.Column(db.Numeric(5, 2))                             # 红线宽度
    道路全长 = db.Column(db.Numeric(7, 2))                             # 道路全长
    建设性质 = db.Column(db.Enum('新建', '改建'))                       # 建设性质

  # 多对多关系，使用中间表 project_unit_association
    units = db.relationship('UnitProject', secondary=project_unit_association, back_populates='projects')

    def __repr__(self):
        return f'<Project {self.建设项目工程名称}>'

# 定义单位工程模型
class UnitProject(db.Model):
    __tablename__ = '单位工程表'  # 表名

    # 定义字段
    单位工程_id = db.Column(db.Integer, primary_key=True)  # 主键
    单位工程名称 = db.Column(db.String(225))              # 单位工程名称

    # 多对多关系，使用中间表 project_unit_association
    projects = db.relationship('Project', secondary=project_unit_association, back_populates='units')

    def __repr__(self):
        return f'<UnitProject {self.单位工程名称}>'
    
# 定义道路工程模型
class RoadFeature(db.Model):
    __tablename__ = '道路工程特征表'  # 数据库表名

    道路工程特征表_id = db.Column(db.Integer, primary_key=True)  # 主键
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('项目_单位.项目_单位_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))
    道路面积 = db.Column('道路面积（m2）', db.Numeric(14, 2))
    道路长度 = db.Column('道路长度（m）', db.Numeric(14, 2))
    机动车道宽度 = db.Column('机动车道宽度（m）', db.Numeric(5, 2))
    非机动车道宽度 = db.Column('非机动车道宽度（m）', db.Numeric(5, 2))
    人行道宽度 = db.Column('人行道宽度（m）', db.Numeric(5, 2))
    机动车道面层 = db.Column(db.String(225))
    非机动车道面层 = db.Column(db.String(225))
    人行道面层 = db.Column(db.String(225))
    是否含软基处理 = db.Column(db.Enum('是', '否'))

    def __repr__(self):
        return f'<RoadFeature {self.工程造价}>'
     
# 定义排水工程模型   
class DrainageFeature(db.Model):
    __tablename__ = '排水工程特征表'

    排水工程特征表_id = db.Column(db.Integer, primary_key=True)
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('单位工程表.单位工程_id'), nullable=False)
    工程造价 = db.Column('工程造价（元）', db.Numeric(14, 2))  # 注意映射数据库的实际字段名


    # 关联到单位工程表
    unit_project = db.relationship('UnitProject', backref='drainage_features')
    def __repr__(self):
        return f'<DrainageFeature {self.工程造价}>'

# 定义交通工程模型 
class TrafficFeature(db.Model):
    __tablename__ = '交通工程特征表'

    交通工程特征表_id = db.Column(db.Integer, primary_key=True)  # 主键
    工程造价 = db.Column('工程造价（元）', db.Numeric(12, 2))  # 工程造价
    是否含交通监控 = db.Column(db.Enum('是', '否'))  # 是否含交通监控
    是否含电子警察 = db.Column(db.Enum('是', '否'))  # 是否含电子警察
    十字路口个数 = db.Column(db.Integer)  # 十字路口个数
    T字路口个数 = db.Column(db.Integer)  # T字路口个数
    项目_单位_id = db.Column(db.Integer, db.ForeignKey('单位工程表.单位工程_id'), nullable=False)  # 外键

    # 关联到单位工程表
    unit_project = db.relationship('UnitProject', backref='traffic_features')

    def __repr__(self):
        return f'<TrafficFeature 工程造价={self.工程造价}>'
