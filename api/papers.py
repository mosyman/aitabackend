from flask import request

from cos.cosClient import cosJoin
from utils import restful
from app import db
from api import api_bp
from models import Papers

# 添加论文
@api_bp.route('/papers/add', methods=['POST'])
def add_paper():
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    publishTime = data.get('publishTime')
    author = data.get('author')
    abstract = data.get('abstract')
    keywords = data.get('keywords')
    source = data.get('source')
    # 引用次数
    citation_count = data.get('citation_count')
    doi = data.get('doi')
    pdf_url = data.get('pdf_url')

    if not title:
        return restful.params_error(message='论文标题不能为空')
    if not author:
        return restful.params_error(message='作者不能为空')
    if pdf_url:
        pdf_url=cosJoin(pdf_url)
    try:
        new_paper = Papers(
            title=title,
            content=content,
            publishTime=publishTime,
            author=author,
            abstract=abstract,
            keywords=keywords,
            citation_count=citation_count,
            source=source,
            doi=doi,
            pdf_url=pdf_url
        )
        db.session.add(new_paper)
        db.session.commit()
        result = {
            'id': new_paper.id,
        }
        return restful.ok(data=result, message='论文添加成功！')
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='提交失败！')


@api_bp.route('/papers/delete', methods=['POST'])
def delete_paper():
    data = request.json
    if not data or 'id' not in data:
        return restful.params_error(message='缺少必要参数: id')

    try:
        paper = Papers.query.get(data['id'])
        if not paper:
            return restful.params_error(message='论文不存在')

        # 逻辑删除
        paper.isDelete = 1
        db.session.commit()
        return restful.ok(message='论文删除成功！')
    except Exception as e:
        db.session.rollback()
        return restful.server_error(message='删除失败！')


# 更新论文
@api_bp.route('/papers/update', methods=['POST'])
def update_paper():
    data = request.json
    if not data or 'id' not in data:
        return restful.params_error(message='缺少必要参数: id')

    # try:
    paper = Papers.query.get(data['id'])
    if not paper:
        return restful.params_error(message='论文不存在')

    # 更新字段
    if 'title' in data:
        paper.title = data['title']
    if 'content' in data:
        paper.content = data['content']
    if 'publishTime' in data:
        paper.publishTime = data['publishTime']
    if 'author' in data:
        paper.author = data['author']
    if 'abstract' in data:
        paper.abstract = data['abstract']
    if 'keywords' in data:
        paper.keywords = data['keywords']
    if 'citation_count' in data:
        paper.citation_count = data['citation_count']
    if 'source' in data:
        paper.source = data['source']
    if 'doi' in data:
        paper.doi = data['doi']
    if 'pdf_url' in data:
        paper.pdf_url = data['pdf_url']
        paper.pdf_url=cosJoin(paper.pdf_url)

    db.session.commit()
    return restful.ok(message='论文更新成功！', data={'result': True})
    # except Exception as e:
    #     db.session.rollback()
    #     return restful.server_error(message='更新失败！')


@api_bp.route('/papers/list', methods=['POST'])
def get_papers():
    # 获取 JSON 请求体
    data = request.get_json() or {}

    # 从请求体中获取分页和排序参数，提供默认值
    pageNum = data.get('pageNum', 1)
    pageSize = data.get('pageSize', 10)
    sort_by = data.get('sort_by', 'createTime')
    order = data.get('order', 'desc')

    # 构建基础查询
    query = Papers.query.filter(Papers.isDelete == 0)

    # 动态排序
    if hasattr(Papers, sort_by):
        if order.lower() == 'asc':
            query = query.order_by(getattr(Papers, sort_by).asc())
        else:
            query = query.order_by(getattr(Papers, sort_by).desc())

    # 分页处理
    try:
        pagination = query.paginate(page=pageNum, per_page=pageSize, error_out=False)
    except (TypeError, ValueError):
        return restful.params_error(message='不合理的分页参数')

    papers = pagination.items

    # 构建返回数据
    result = [
        {
            'id': paper.id,
            'title': paper.title,
            'content': paper.content,
            'publishTime': paper.publishTime,
            'author': paper.author,
            'abstract': paper.abstract,
            'keywords': paper.keywords,
            'citation_count': paper.citation_count,
            'source': paper.source,
            'doi': paper.doi,
            'pdf_url': paper.pdf_url,
            'createTime': paper.createTime,
            'updateTime': paper.updateTime
        }
        for paper in papers
    ]

    return restful.ok(data={
        'items': result,
        'total': pagination.total,
        'pages': pagination.pages,
        'pageNum': pagination.page,
        'pageSize': pagination.per_page
    })


# 获取单个论文
@api_bp.route('/papers/detail', methods=['GET'])
def get_paper():
    id = request.args.get('id')
    if not id:
        return restful.params_error(message='请求头中未提供id')
    try:
        id = int(id)
    except ValueError:
        return restful.params_error(message='参数类型错误')
    paper = Papers.query.filter_by(id=id, isDelete=0).first()
    if not paper:
        return restful.params_error(message='论文不存在')
    return restful.ok(data={
        'id': paper.id,
        'title': paper.title,
        'content': paper.content,
        'publishTime': paper.publishTime,
        'author': paper.author,
        'abstract': paper.abstract,
        'keywords': paper.keywords,
        'citation_count': paper.citation_count,
        'source': paper.source,
        'doi': paper.doi,
        'pdf_url': paper.pdf_url,
        'createTime': paper.createTime,
        'updateTime': paper.updateTime
    })