from flask import request, session, make_response

from utils import restful
from app import db
from api import api_bp
from models import User


@api_bp.route('/user/register', methods=['POST'])
def register():
    data = request.get_json() or {}
    # 提取参数
    user_account = data['account']
    user_password = data['password']
    check_password = data['check_password']
    if not all([user_account, user_password, check_password]):
        return restful.params_error(message='参数不能为空')
    if len(user_account) < 4:
        return restful.params_error(message='账户长度必须大于等于4')
    if len(user_password) < 6 or len(check_password) < 6:
        return restful.params_error(message='密码长度必须大于等于6')
    if user_password != check_password:
        return restful.params_error(message='两次输入的密码不一致')

    existing_user = User.query.filter_by(account=user_account).first()
    if existing_user:
        return restful.params_error(message='该账户已存在')

    new_user = User(account=user_account, password=user_password)
    db.session.add(new_user)
    db.session.commit()
    return restful.ok(data={'userId':  new_user.id})





# 登录接口
@api_bp.route('/user/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    user_account = data.get('account')
    user_password = data.get('password')

    if not user_account or not user_password:
        return restful.params_error(message='账号或密码不能为空')

    user = User.query.filter_by(account=user_account, isDelete=0).first()
    if not user:
        return restful.params_error(message='账号不存在')

    if user.reviewStatus != 1:
        return restful.params_error(message='账号未通过审核')

    if user.password != user_password:  # 明文密码比对
        return restful.params_error(message='密码错误')


    # resp=restful.ok(message='登录成功', data={
    #         'account': user.account,
    #         'name': user.name,
    #         'avatar': user.avatar,
    #         'profile': user.profile,
    #         'role': user.role
    #     })
    resp=make_response({
        "code":200,
        "message":"登录成功",
        "data":{
            "account": user.account,
            "name": user.name,
            "avatar": user.avatar,
            "profile": user.profile,
            "role": user.role
        }
    })
    resp.set_cookie(
        'loginUser',
        str(user.id),
        max_age=7 * 24 * 3600,
        path='/api',
        httponly=True,  # 允许 JS 获取（调试用）
    )
    return resp


@api_bp.route('/user/current', methods=['GET'])
def get_current_user():
    print(f"请求头: {request.headers}")  # 查看所有请求头
    print(f"所有 Cookie: {request.cookies}")  # 查看收到的所有 Cookie

    user_id=request.cookies.get('loginUser');
    # 检查用户是否已登录
    if not user_id:
        return restful.unlogin_error(message='用户未登录')
    # string to bitInt
    user_id=int(user_id)

    # 查询数据库获取用户信息
    user = User.query.filter_by(id=user_id, isDelete=0).first()

    # 检查用户是否存在且未被删除
    if not user:
        # 用户可能已被删除，清除cookie
        resp= restful.params_error(message='用户不存在或已被删除')
        resp.delete_cookie('loginUser')
        return resp

    # 返回用户信息（不包含敏感字段如密码）
    return restful.ok(data={
        'account': user.account,
        'name': user.name,
        'avatar': user.avatar,
        'profile': user.profile,
        'role': user.role,
    })


# 注销接口
@api_bp.route('/user/logout', methods=['POST'])
def logout():
    # 清除 Cookie
    resp = restful.ok(message='注销成功')
    resp.delete_cookie('loginUser')
    return resp