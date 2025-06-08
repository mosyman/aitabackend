from flask import request

from cos.cosClient import cosJoin
from utils import restful
from app import db
from api import api_bp
from models import News


# 添加新闻
@api_bp.route('/news/add', methods=['POST'])
def add_news():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    author = data.get('author')
    link = data.get('link')
    image_url = data.get('image_url')
    publish_time = data.get('publish_time')

    if not title:
        return restful.params_error(message='标题不能为空')
    if not content:
        return restful.params_error(message='内容不能为空')
    if image_url:
        image_url=cosJoin(image_url)
    try:
        new_news = News(
            title=title,
            content=content,
            author=author,
            link=link,
            image_url=image_url,
            publish_time=publish_time
        )
        db.session.add(new_news)
        db.session.commit()
        result = {
            'id': new_news.id,
        }
        return restful.ok(data=result, message='新闻添加成功！')
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='提交失败！')

@api_bp.route('/news/delete', methods=['POST'])
def delete_news():
    data = request.json
    if not data or 'id' not in data:
        return restful.params_error(message='缺少必要参数: id')

    try:
        news = News.query.get(data['id'])
        if not news:
            return restful.params_error(message='新闻不存在')

        # 逻辑删除
        news.isDelete = 1
        db.session.commit()
        return restful.ok(message='新闻删除成功！')
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='删除失败！')

# 更新新闻
@api_bp.route('/news/update', methods=['POST'])
def update_news():
    data = request.json
    if not data or 'id' not in data:
        return restful.params_error(message='缺少必要参数: id')

    try:
        news = News.query.get(data['id'])
        if not news:
            return restful.params_error(message='新闻不存在')

        # 更新字段
        if 'title' in data:
            news.title = data['title']
        if 'content' in data:
            news.content = data['content']
        if 'author' in data:
            news.author = data['author']
        if 'link' in data:
            news.link = data['link']
        if 'image_url' in data:
            news.image_url = data['image_url']
            news.image_url=cosJoin(news.image_url)
        if 'publish_time' in data:
            news.publish_time = data['publish_time']

        db.session.commit()
        return restful.ok(message='新闻更新成功！', data={'result': True})
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='更新失败！')

@api_bp.route('/news/list', methods=['POST'])
def get_news_list():
    # 获取 JSON 请求体
    data = request.get_json() or {}

    # 从请求体中获取分页和排序参数，提供默认值
    pageNum = data.get('pageNum', 1)
    pageSize = data.get('pageSize', 10)
    sort_by = data.get('sort_by', 'publish_time')
    order = data.get('order', 'desc')

    # 构建基础查询
    query = News.query.filter(News.isDelete == 0)

    # 动态排序
    if hasattr(News, sort_by):
        if order.lower() == 'asc':
            query = query.order_by(getattr(News, sort_by).asc())
        else:
            query = query.order_by(getattr(News, sort_by).desc())

    # 分页处理
    try:
        pagination = query.paginate(page=pageNum, per_page=pageSize, error_out=False)
    except (TypeError, ValueError):
        return restful.params_error(message='不合理的分页参数')

    news_list = pagination.items

    # 构建返回数据
    result = [
        {
            'id': news.id,
            'title': news.title,
            'content': news.content,
            'author': news.author,
            'publish_time': news.publish_time,
            'link': news.link,
            'image_url': news.image_url,
            'createTime': news.createTime,
            'updateTime': news.updateTime
        }
        for news in news_list
    ]

    return restful.ok(data={
        'items': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'pageNum': pagination.page,
        'pageSize': pagination.per_page
    })

# 获取单个新闻
@api_bp.route('/news/detail', methods=['GET'])
def get_news():
    id = request.args.get('id')
    if not id:
        return restful.params_error(message='请求头中未提供id')
    try:
        id = int(id)
    except ValueError:
        return restful.params_error(message='参数类型错误')
    news = News.query.filter_by(id=id, isDelete=0).first()
    if not news:
        return restful.params_error(message='新闻不存在')
    return restful.ok(data={
        'id': news.id,
        'title': news.title,
        'content': news.content,
        'author': news.author,
        'publish_time': news.publish_time,
        'link': news.link,
        'image_url': news.image_url,
        'createTime': news.createTime,
        'updateTime': news.updateTime
    })