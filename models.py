from flask_sqlalchemy import SQLAlchemy

# 初始化 SQLAlchemy 实例
db = SQLAlchemy()

# 定义数据库模型
class Project(db.Model):
    __tablename__ = '项目表'  # 表名

    # 定义字段
    项目表_id = db.Column(db.Integer, primary_key=True)               # 主键
    建设项目工程名称 = db.Column(db.String(225))                     # 项目名称
    单项工程费用 = db.Column(db.Numeric(14, 2))                       # 工程费用
    项目阶段 = db.Column(db.Enum('项目建议书估算', '可行性研究估算', '初步设计概算', '施工图预算', '招标控制价'))  # 项目阶段
    项目地点 = db.Column(db.String(45))                               # 项目地点
    价格基准期 = db.Column(db.Date)                                   # 价格基准期
    道路等级 = db.Column(db.Enum('快速路', '主干路', '次干路', '支路'))   # 道路等级
    红线宽度 = db.Column(db.Numeric(5, 2))                             # 红线宽度
    道路全长 = db.Column(db.Numeric(7, 2))                             # 道路全长
    建设性质 = db.Column(db.Enum('新建', '改建'))                       # 建设性质

    def __repr__(self):
        return f'<Project {self.建设项目工程名称}>'
