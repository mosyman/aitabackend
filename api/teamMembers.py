from flask import request

from cos.cosClient import cosJoin
from utils import restful
from app import db
from api import api_bp
from models import TeamMembers



# 添加团队成员
@api_bp.route('/team/add', methods=['POST'])
def add_team_member():
    data = request.get_json()
    name = data.get('name')
    gender = data.get('gender')
    email = data.get('email')
    ethnicity = data.get('ethnicity')
    department = data.get('department')
    position = data.get('position')
    title = data.get('title')
    phone = data.get('phone')
    image_url = data.get('image_url')
    profile = data.get('profile')
    areas = data.get('areas')
    courses = data.get('courses')
    patents = data.get('patents')
    projects = data.get('projects')
    publications = data.get('publications')
    honors = data.get('honors')

    # 统一进行参数校验
    if not name:
        return restful.params_error(message='姓名不能为空')
    if not email:
        return restful.params_error(message='电子邮箱不能为空')
    if image_url:
        image_url=cosJoin(image_url)
    try:
        new_member = TeamMembers(
            name=name,
            gender=gender,
            ethnicity=ethnicity,
            department=department,
            position=position,
            title=title,
            phone=phone,
            email=email,
            image_url=image_url,
            profile=profile,
            areas=areas,
            courses=courses,
            patents=patents,
            projects=projects,
            publications=publications,
            honors=honors
        )
        db.session.add(new_member)
        db.session.commit()
        result = {
            'id': new_member.id,
        }
        return restful.ok(data=result, message='团队成员添加成功！')
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='提交失败！')

@api_bp.route('/team/delete', methods=['POST'])
def delete_team_member():
    data = request.json
    if not data or 'id' not in data:
        return restful.params_error(message='缺少必要参数: id')

    try:
        member = TeamMembers.query.get(data['id'])
        if not member:
            return restful.params_error(message='团队成员不存在')

        # 逻辑删除
        member.isDelete = 1
        db.session.commit()
        return restful.ok(message='团队成员删除成功！')
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='删除失败！')


# 更新团队成员
@api_bp.route('/team/update', methods=['POST'])
def update_team_member():
    data = request.json
    if not data or 'id' not in data:
        return restful.params_error(message='缺少必要参数: id')

    try:
        member = TeamMembers.query.get(data['id'])
        if not member:
            return restful.params_error(message='团队成员不存在')

        # 更新字段
        if 'name' in data:
            member.name = data['name']
        if 'gender' in data:
            member.gender = data['gender']
        if 'ethnicity' in data:
            member.ethnicity = data['ethnicity']
        if 'department' in data:
            member.department = data['department']
        if 'position' in data:
            member.position = data['position']
        if 'title' in data:
            member.title = data['title']
        if 'phone' in data:
            member.phone = data['phone']
        if 'email' in data:
            member.email = data['email']
        if 'image_url' in data:
            member.image_url = data['image_url']
            member.image_url = cosJoin(member.image_url)
        if 'profile' in data:
            member.profile = data['profile']
        if 'areas' in data:
            member.areas = data['areas']
        if 'courses' in data:
            member.courses = data['courses']
        if 'patents' in data:
            member.patents = data['patents']
        if 'projects' in data:
            member.projects = data['projects']
        if 'publications' in data:
            member.publications = data['publications']
        if 'honors' in data:
            member.honors = data['honors']

        db.session.commit()
        return restful.ok(message='团队成员更新成功！', data={'result': True})
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='更新失败！')


@api_bp.route('/team/list', methods=['POST'])
def get_team_members():
    data = request.get_json() or {}

    # 分页和排序参数（默认按创建时间倒序）
    pageNum = data.get('pageNum', 1)
    pageSize = data.get('pageSize', 10)
    sort_by = data.get('sort_by', 'id')  # 默认按ID排序
    order = data.get('order', 'desc')

    # 基础查询（过滤未删除数据）
    query = TeamMembers.query.filter(TeamMembers.isDelete == 0)

    # 动态排序
    if hasattr(TeamMembers, sort_by):
        if order.lower() == 'asc':
            query = query.order_by(getattr(TeamMembers, sort_by).asc())
        else:
            query = query.order_by(getattr(TeamMembers, sort_by).desc())

    # 分页处理
    try:
        pagination = query.paginate(page=pageNum, per_page=pageSize, error_out=False)
    except (TypeError, ValueError):
        return restful.params_error(message='不合理的分页参数')

    members = pagination.items

    # 构建返回数据
    result = [
        {
            'id': member.id,
            'name': member.name,
            'gender': member.gender,
            'ethnicity': member.ethnicity,
            'department': member.department,
            'position': member.position,
            'title': member.title,
            'phone': member.phone,
            'email': member.email,
            'image_url': member.image_url,
            'profile': member.profile,
            'areas': member.areas,
            'courses': member.courses,
            'patents': member.patents,
            'projects': member.projects,
            'publications': member.publications,
            'honors': member.honors
        }
        for member in members
    ]

    return restful.ok(data={
        'items': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'pageNum': pagination.page,
        'pageSize': pagination.per_page
    })


# 获取单个团队成员详情
@api_bp.route('/team/detail', methods=['GET'])
def get_team_member():
    id = request.args.get('id')
    if not id:
        return restful.params_error(message='请求中未提供id')

    try:
        id = int(id)
    except ValueError:
        return restful.params_error(message='参数类型错误')

    member = TeamMembers.query.filter_by(id=id, isDelete=0).first()
    if not member:
        return restful.params_error(message='团队成员不存在')

    return restful.ok(data={
        'id': member.id,
        'name': member.name,
        'gender': member.gender,
        'ethnicity': member.ethnicity,
        'department': member.department,
        'position': member.position,
        'title': member.title,
        'phone': member.phone,
        'email': member.email,
        'image_url': member.image_url,
        'profile': member.profile,
        'areas': member.areas,
        'courses': member.courses,
        'patents': member.patents,
        'projects': member.projects,
        'publications': member.publications,
        'honors': member.honors
    })


