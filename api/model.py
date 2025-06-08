from flask import request
from cos.cosClient import upload_to_cos, cosJoin
from model.inference import run_inference_on_h5
from utils import restful
from api import api_bp
import os
from werkzeug.utils import secure_filename  # 用于安全处理上传的文件名

@api_bp.route('/model/upload', methods=['POST'])
def model_upload():
    """上传文件到COS"""
    f = request.files['file']  # 获取文件流
    # 按照目标文件目录区分不同业务类型，这里是modelResult
    file_dir = request.form.get('file_path')
    if f and f.filename.endswith(".h5"):  # 验证文件类型
        # 安全处理文件名，防止路径遍历攻击
        filename = secure_filename(f.filename)
        # 构建存储路径
        UPLOAD_FOLDER="tempUpload"
        RESULT_FOLDER="tempResult"
        # 确保上传和结果目录存在（不存在则创建）
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(RESULT_FOLDER, exist_ok=True)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        output_filename = os.path.basename(filename).replace(".h5", ".png")  # 生成输出文件名
        result_path= os.path.join(RESULT_FOLDER, output_filename)
        try:
            # 保存上传的文件
            f.save(file_path)

            # 调用推理函数处理H5文件并获取结果路径
            isTrue = run_inference_on_h5(file_path, result_path)
            if isTrue != "true":
                return restful.params_error("模型处理失败")
            # 上传文件到COS
            cos_path="{}/{}".format(file_dir,output_filename)
            with open(result_path, 'rb') as file_stream:
                result = upload_to_cos(file_stream, cos_path)

            if result["success"]:
                return restful.ok(message='模型处理成功', data={
                    "cosPath": cosJoin(cos_path),
                    "path": cos_path
                })
            else:
                return restful.params_error(message='模型结果保存失败')

        finally:
            # 无论是否成功，都尝试删除临时文件
            if os.path.exists(file_path):
                os.remove(file_path)
            if os.path.exists(result_path):
                os.remove(result_path)



