import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


#导入路径
from flask import Flask, redirect, url_for, session
from models import db
from views import auth_blueprint, project_blueprint, individual_project_blueprint,individual_project2_blueprint,unit_price_blueprint

app = Flask(__name__, static_folder="static")
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:March5323@localhost/cost-database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 初始化数据库
db.init_app(app)

# 注册蓝图
app.register_blueprint(auth_blueprint)
app.register_blueprint(project_blueprint)
app.register_blueprint(individual_project_blueprint)
app.register_blueprint(individual_project2_blueprint)
app.register_blueprint(unit_price_blueprint)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('projects.project_list'))
    return redirect(url_for('auth.login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # 确保数据库和表已经创建
    app.run(debug=True)
