from flask import request

from cos.cosClient import cosJoin
from utils import restful
from app import db
from api import api_bp
from models import Dataset


# 添加数据集
@api_bp.route('/datasets/add', methods=['POST'])
def add_dataset():
    data = request.get_json()
    title = data.get('title'),
    content = data.get('content'),
    author = data.get('author'),
    link = data.get('link'),
    image_url = data.get('image_url'),
    type = data.get('type'),
    abstract = data.get('abstract')
    if not title:
        return restful.params_error(message='标题不能为空')
    if not content:
        return restful.params_error(message='内容不能为空')
    if not type:
        return restful.params_error(message='类型不能为空')
    if link:
        link=cosJoin(link)
    if image_url:
        image_url=cosJoin(image_url)
    try:
        new_dataset = Dataset(
            title=title,
            content=content,
            author=author,
            link=link,
            image_url=image_url,
            type=type,
            abstract=abstract
        )
        db.session.add(new_dataset)
        db.session.commit()
        result={
            'id': new_dataset.id,
        }
        return restful.ok(data=result, message='数据集添加成功！')
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='提交失败！')


@api_bp.route('/datasets/delete', methods=['POST'])
def delete_dataset():
    data = request.json
    if not data or 'id' not in data:
        return restful.params_error(message='缺少必要参数: id')

    try:
        dataset = Dataset.query.get(data['id'])
        if not dataset:
            return restful.params_error(message='数据集不存在')

        # 逻辑删除
        dataset.isDelete = 1
        db.session.commit()
        return restful.ok(message='数据集删除成功！')
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='删除失败！')


# 更新数据集
@api_bp.route('/datasets/update', methods=['POST'])
def update_dataset():
    data = request.json
    if not data or 'id' not in data:
        return restful.params_error(message='缺少必要参数: id')

    try:
        dataset = Dataset.query.get(data['id'])
        if not dataset:
            return restful.params_error(message='数据集不存在')

        # 更新字段
        if 'title' in data:
            dataset.title = data['title']
        if 'content' in data:
            dataset.content = data['content']
        if 'author' in data:
            dataset.author = data['author']
        if 'link' in data:
            dataset.link = data['link']
            dataset.link=cosJoin(dataset.link)
        if 'image_url' in data:
            dataset.image_url = data['image_url']
            dataset.image_url=cosJoin(dataset.image_url)
        if 'type' in data:
            dataset.type = data['type']
        if 'abstract' in data:
            dataset.abstract = data['abstract']

        db.session.commit()
        return restful.ok(message='数据集更新成功！',data={'result': True})
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='更新失败！')

@api_bp.route('/datasets/list', methods=['POST'])
def get_datasets():
    # 获取 JSON 请求体
    data = request.get_json() or {}

    # 从请求体中获取分页和排序参数，提供默认值
    pageNum = data.get('pageNum', 1)
    pageSize = data.get('pageSize', 10)
    sort_by = data.get('sort_by', 'createTime')
    order = data.get('order', 'desc')

    # 构建基础查询
    query = Dataset.query.filter(Dataset.isDelete == 0)

    # 动态排序
    if hasattr(Dataset, sort_by):
        if order.lower() == 'asc':
            query = query.order_by(getattr(Dataset, sort_by).asc())
        else:
            query = query.order_by(getattr(Dataset, sort_by).desc())

    # 分页处理
    try:
        pagination = query.paginate(page=pageNum, per_page=pageSize, error_out=False)
    except (TypeError, ValueError):
        return restful.params_error(message='不合理的分页参数')

    datasets = pagination.items

    # 构建返回数据
    result = [
        {
            'id': dataset.id,
            'title': dataset.title,
            'content': dataset.content,
            'author': dataset.author,
            'link': dataset.link,
            'image_url': dataset.image_url,
            'type': dataset.type,
            'abstract': dataset.abstract,
            'createTime': dataset.createTime,
            'updateTime': dataset.updateTime
        }
        for dataset in datasets
    ]

    return restful.ok(data={
        'items': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'pageNum': pagination.page,
        'pageSize': pagination.per_page
    })



# 获取单个数据集
@api_bp.route('/datasets/detail', methods=['GET'])
def get_dataset():
    id = request.args.get('id')
    if not id:
        return restful.params_error(message='请求头中未提供id')
    try:
        id = int(id)
    except ValueError:
        return restful.params_error(message='参数类型错误')
    dataset = Dataset.query.filter_by(id=id, isDelete=0).first();
    if not dataset:
        return restful.params_error(message='数据集不存在')
    return restful.ok(data={
        'id': dataset.id,
        'title': dataset.title,
        'content': dataset.content,
        'author': dataset.author,
        'link': dataset.link,
        'image_url': dataset.image_url,
        'type': dataset.type,
        'abstract': dataset.abstract,
        'createTime': dataset.createTime,
        'updateTime': dataset.updateTime
    })



