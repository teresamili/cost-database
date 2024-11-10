from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:March5323@localhost/cost-database'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# 定义模型类
class Project(db.Model):
    __tablename__ = '项目表'
    项目表_id = db.Column(db.Integer, primary_key=True)
    建设项目工程名称 = db.Column(db.String(225))
    单项工程费用 = db.Column(db.Numeric(14, 2))
    项目阶段 = db.Column(db.Enum('项目建议书估算', '可行性研究估算', '初步设计概算', '施工图预算', '招标控制价'))
    项目地点 = db.Column(db.String(45))
    价格基准期 = db.Column(db.Date)
    道路等级 = db.Column(db.Enum('快速路', '主干路', '次干路', '支路'))
    红线宽度 = db.Column(db.Numeric(5, 2))
    道路全长 = db.Column(db.Numeric(7, 2))
    建设性质 = db.Column(db.Enum('新建', '改建'))

# 假设的用户数据库（实际项目应使用数据库）
users = {
    "zjsjk": "123456"
}

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('projects'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('projects'))
        else:
            flash("用户名或密码错误，请重试")
    return render_template('login.html')

@app.route('/projects')
def projects():
    # 检查用户是否已经登录
    if 'username' in session:
        # 用户已登录，从数据库获取项目列表
        project_list = Project.query.all()
        return render_template('projects.html', projects=project_list)
    else:
        # 用户未登录，重定向到登录页面
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)
