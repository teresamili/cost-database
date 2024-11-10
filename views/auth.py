from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_blueprint = Blueprint('auth', __name__)

# 假设的用户数据库（实际项目应使用数据库）
users = {
    "zjsjk": "123456"
}

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('projects.project_list'))
        else:
            flash("用户名或密码错误，请重试")
    return render_template('login.html')

@auth_blueprint.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('auth.login'))
