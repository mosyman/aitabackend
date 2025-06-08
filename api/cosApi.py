from flask import request,Response
import uuid
import time
from cos.cosClient import upload_to_cos, download_from_cos
from utils import restful
from api import api_bp
from werkzeug.utils import secure_filename  # 用于安全处理上传的文件名

@api_bp.route('/file/upload', methods=['POST'])
def upload_file():
    """上传文件到COS"""
    f = request.files['file']  # 获取文件流
    # 按照目标文件目录区分不同业务类型，例如 user  dataset
    file_path = request.form.get('file_path')
    # 检查文件是否有名称
    if f.filename == '':
        return restful.params_error(message='文件名不能为空')
    # 检查file_path参数是否存在
    if not file_path:
        return restful.params_error(message='缺少文件路径参数')
    # 安全处理文件名，防止路径遍历攻击
    original_filename = secure_filename(f.filename)

    # 提取扩展名（安全处理）
    ext = ''
    if '.' in original_filename:
        ext = original_filename.rsplit('.', 1)[1].strip().lower()
    # 生成新文件名：格式为 日期_随机UUID.扩展名
    date_prefix = time.strftime('%Y%m%d')  # 当前日期，如 20250405
    # 生成新文件名：格式为 日期_随机UUID.扩展名
    if ext:
        filename = "{prefix}_{uuid}.{ext}".format(
            prefix=date_prefix,
            uuid=uuid.uuid4(),
            ext=ext
        )
    else:
        filename = "{prefix}_{uuid}".format(
            prefix=date_prefix,
            uuid=uuid.uuid4()
        )
    path="{}/{}".format(file_path,filename)
    # 调用上传函数
    result = upload_to_cos(f.stream, path)

    if result["success"]:
        return restful.ok(data={
            "etag": result["etag"],
            "path": path,
        },message='文件上传成功')
    else:
        return restful.params_error(message='文件上传失败')


@api_bp.route('/download', methods=['GET'])
def download_file():
    # 从get请求中获取文件路径
    cos_path = request.args.get('path')
    # 调用下载函数
    result = download_from_cos(cos_path)

    if result["success"]:
        # 直接返回文件流，不创建临时文件
        return Response(
            result['file_stream'],
            mimetype='application/octet-stream',
            headers={
                'Content-Disposition': f'attachment; filename="{result["file_name"]}"'
            }
        )
    else:
        return restful.params_error(message='文件下载失败')
