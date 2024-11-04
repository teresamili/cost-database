from flask import Flask, render_template, request, redirect, url_for, session, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 用于会话管理

# 假设的用户数据库（实际项目应使用数据库）
users = {
    "zjsjk": "123456"  # 用户名: 密码
}

@app.route('/')
def index():
    # 如果用户已登录，跳转到项目页面，否则跳转到登录页面
    if 'username' in session:
        return redirect(url_for('projects'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # 从表单获取用户名和密码
        username = request.form['username']
        password = request.form['password']
        
        # 验证用户名和密码
        if username in users and users[username] == password:
            # 登录成功，保存会话信息
            session['username'] = username
            return redirect(url_for('projects'))  # 登录成功后跳转到项目页面
        else:
            # 登录失败，显示错误提示
            flash("用户名或密码错误，请重试")
    
    return render_template('login.html')

@app.route('/projects')
def projects():
    # 仅登录用户可以访问项目页面
    if 'username' in session:
        return render_template('projects.html')  # 渲染项目页面
    else:
        return redirect(url_for('login'))

@app.route('/logout')
def logout():
    # 退出登录，清除会话信息
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
