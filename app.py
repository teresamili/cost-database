import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


#导入路径
from flask import Flask, redirect, url_for, session
from models import db
from views import auth_blueprint
from views import project_blueprint
from views import individual_project_blueprint
from views import individual_project2_blueprint
from views import unit_price_blueprint
from views import material_price_blueprint
from views import road_blueprint
from views import bridge_blueprint
from views import culvert_blueprint
from views import drainage_blueprint
from views import traffic_blueprint
from views import lighting_blueprint
from views import waterpipe_blueprint
from views import electrical_blueprint
from views import telecom_blueprint
from views import green_blueprint
from views import tunnel_blueprint

app = Flask(__name__, static_folder="static")
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:March5323@localhost/cost-database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.jinja_env.globals.update(zip=zip)

# 初始化数据库
db.init_app(app)

# 注册蓝图
app.register_blueprint(auth_blueprint)
app.register_blueprint(project_blueprint)
app.register_blueprint(individual_project_blueprint)
app.register_blueprint(individual_project2_blueprint)
app.register_blueprint(unit_price_blueprint)
app.register_blueprint(material_price_blueprint)
app.register_blueprint(road_blueprint)
app.register_blueprint(bridge_blueprint)
app.register_blueprint(culvert_blueprint)
app.register_blueprint(drainage_blueprint)
app.register_blueprint(traffic_blueprint)
app.register_blueprint(lighting_blueprint)
app.register_blueprint(waterpipe_blueprint)
app.register_blueprint(electrical_blueprint)
app.register_blueprint(telecom_blueprint)
app.register_blueprint(green_blueprint)
app.register_blueprint(tunnel_blueprint)

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('projects.project_list'))
    return redirect(url_for('auth.login'))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # 确保数据库和表已经创建
    app.run(debug=True)
