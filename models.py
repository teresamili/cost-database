from flask_sqlalchemy import SQLAlchemy

# 初始化 SQLAlchemy 实例
db = SQLAlchemy()

# 中间表，用于关联项目和单位工程
project_unit_association = db.Table('项目_单位',
    db.Column('项目表_id', db.Integer, db.ForeignKey('项目表.项目表_id'), primary_key=True),
    db.Column('单位工程_id', db.Integer, db.ForeignKey('单位工程表.单位工程_id'), primary_key=True)
)

# 定义xx项目表模型
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