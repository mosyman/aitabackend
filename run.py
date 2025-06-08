from app import create_app,login_manager
from models import User

app = create_app('development')

@login_manager.user_loader
def load_user(user_id):
    """Flask-Login 必须的用户加载函数"""
    return User.query.filter_by(id=int(user_id), isDelete=0).first()


@app.route('/')
def hello_world():  # put application's code here
    return 'AITA系统后台服务'

if __name__ == '__main__':
    app.run(host='localhost', port=5000,debug=True)