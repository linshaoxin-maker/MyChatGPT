import os; os.environ['no_proxy'] = '*' # 避免代理网络产生意外污染
import gradio
from flask import Flask, g, request, render_template, flash, url_for, redirect
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, UserMixin

# create a Flask app
app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# initialize a LoginManager
login_manager = LoginManager()
login_manager.init_app(app)


# create a User model (optional)
class User(UserMixin):
    def __init__(self, username):
        self.username = username

    def get_id(self):
        return self.username

# define a user_loader function for the LoginManager
@login_manager.user_loader
def load_user(user_id):
    # return a User object or None
    return User(user_id)

# define a login view
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username, password)
        # validate username and password (here we use a simple scheme)
        if username == "admin" and password == "admin":
            user = User(username)
            login_user(user)
            return redirect(url_for('greeter'))
        else:
            flash('Invalid username/password')
            return redirect(url_for('login'))
    else:
        return render_template('login.html')

# define a logout view
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# define a page with Gradio interface which requires login
@app.route('/greeter')
@login_required
def greeter():
    def greet(name):
        return "Hello " + name + "!"

    # 接口创建函数
    # fn设置处理函数，inputs设置输入接口组件，outputs设置输出接口组件
    # fn,inputs,outputs都是必填函数
    demo = gradio.Interface(fn=greet, inputs="text", outputs="text")
    _, local_url, _ = demo.launch()
    # return iface()
    return redirect(local_url)

# the main page, which redirects to either the login or greeter view
@app.route('/')
def main():
    if current_user.is_authenticated:
        return redirect(url_for('greeter'))
    else:
        return redirect(url_for('login'))

# define the Gradio-compatible function

# run the app
if __name__ == '__main__':
    app.run(debug=True)