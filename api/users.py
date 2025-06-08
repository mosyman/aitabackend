from flask import request, make_response

from cos.cosClient import cosJoin
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




# 注销接口
@api_bp.route('/user/logout', methods=['GET'])
def logout():
    # 清除 Cookie
    resp = restful.ok(message='退出登录成功')
    resp.delete_cookie('loginUser')
    return resp


@api_bp.route('/user/current', methods=['GET'])
def get_current_user():
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


# 添加用户
@api_bp.route('/users/add', methods=['POST'])
def add_user():
    data = request.get_json()
    account = data.get('account')
    password = data.get('password')
    name = data.get('name')
    avatar = data.get('avatar')
    profile = data.get('profile')
    role = data.get('role', 'user')
    reviewStatus = data.get('reviewStatus', 0)

    if not account:
        return restful.params_error(message='账号不能为空')
    if not password:
        return restful.params_error(message='密码不能为空')
    # 检查账户是否已存在
    existing_user = User.query.filter_by(account=account).first()
    if existing_user:
        return restful.params_error(message='该账户已存在')
    if avatar:
        avatar=cosJoin(avatar)
    try:
        new_user = User(
            account=account,
            password=password,
            name=name,
            avatar=avatar,
            profile=profile,
            role=role,
            reviewStatus=reviewStatus
        )
        db.session.add(new_user)
        db.session.commit()
        result = {
            'id': new_user.id,
        }
        return restful.ok(data=result, message='用户添加成功！')
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='提交失败！')


@api_bp.route('/users/delete', methods=['POST'])
def delete_user():
    data = request.json
    if not data or 'id' not in data:
        return restful.params_error(message='缺少必要参数: id')

    try:
        user = User.query.get(data['id'])
        if not user:
            return restful.params_error(message='用户不存在')

        # 逻辑删除
        user.isDelete = 1
        db.session.commit()
        return restful.ok(message='用户删除成功！')
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='删除失败！')



#用户审核
@api_bp.route('/users/review', methods=['POST'])
def review_user():
    data = request.json
    if not data or 'id' not in data:
        return restful.params_error(message='缺少必要参数: id')

    try:
        user = User.query.get(data['id'])
        if not user:
            return restful.params_error(message='用户不存在')
        # 更新字段
        if 'reviewStatus' in data:
            user.reviewStatus = data['reviewStatus']
        db.session.commit()
        return restful.ok(message='审核成功！', data={'result': True})
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='审核失败！')


# 更新用户
@api_bp.route('/users/update', methods=['POST'])
def update_user():
    data = request.json
    if not data or 'id' not in data:
        return restful.params_error(message='缺少必要参数: id')

    try:
        user = User.query.get(data['id'])
        if not user:
            return restful.params_error(message='用户不存在')

        # 检查新账户是否存在（排除当前用户）
        if 'account' in data and data['account'] != user.account:
            existing_user = User.query.filter(User.account == data['account'],
                User.id != user.id  # 排除当前用户
            ).first()
            if existing_user:
                return restful.params_error(message='该账户已被其他用户使用')

        # 更新字段
        if 'account' in data:
            user.account = data['account']
        if 'password' in data:
            user.password = data['password']
        if 'name' in data:
            user.name = data['name']
        if 'avatar' in data:
            user.avatar = data['avatar']
            user.avatar=cosJoin(user.avatar)
        if 'profile' in data:
            user.profile = data['profile']
        if 'role' in data:
            user.role = data['role']
        if 'reviewStatus' in data:
            user.reviewStatus = data['reviewStatus']

        db.session.commit()
        return restful.ok(message='用户更新成功！', data={'result': True})
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='更新失败！')


@api_bp.route('/users/list', methods=['POST'])
def get_users():
    # 获取 JSON 请求体
    data = request.get_json() or {}

    # 从请求体中获取分页和排序参数，提供默认值
    pageNum = data.get('pageNum', 1)
    pageSize = data.get('pageSize', 10)
    sort_by = data.get('sort_by', 'id')
    order = data.get('order', 'desc')

    # 构建基础查询
    query = User.query.filter(User.isDelete == 0)

    # 动态排序
    if hasattr(User, sort_by):
        if order.lower() == 'asc':
            query = query.order_by(getattr(User, sort_by).asc())
        else:
            query = query.order_by(getattr(User, sort_by).desc())

    # 分页处理
    try:
        pagination = query.paginate(page=pageNum, per_page=pageSize, error_out=False)
    except (TypeError, ValueError):
        return restful.params_error(message='不合理的分页参数')

    users = pagination.items

    # 构建返回数据
    result = [
        {
            'id': user.id,
            'account': user.account,
            'name': user.name,
            'avatar': user.avatar,
            'profile': user.profile,
            'role': user.role,
            'reviewStatus': user.reviewStatus,
        }
        for user in users
    ]

    return restful.ok(data={
        'items': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'pageNum': pagination.page,
        'pageSize': pagination.per_page
    })


# 获取单个用户
@api_bp.route('/users/detail', methods=['GET'])
def get_user():
    id = request.args.get('id')
    if not id:
        return restful.params_error(message='请求头中未提供id')
    try:
        id = int(id)
    except ValueError:
        return restful.params_error(message='参数类型错误')
    user = User.query.filter_by(id=id, isDelete=0).first()
    if not user:
        return restful.params_error(message='用户不存在')
    return restful.ok(data={
        'id': user.id,
        'account': user.account,
        'name': user.name,
        'avatar': user.avatar,
        'profile': user.profile,
        'role': user.role,
        'reviewStatus': user.reviewStatus,
    })


