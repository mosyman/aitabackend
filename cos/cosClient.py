# cos_client.py
# -*- coding=utf-8 -*-
from qcloud_cos import CosConfig, CosS3Client
import os
from dotenv import load_dotenv  # 用于加载.env文件

# 加载.env文件（需确保文件位于当前工作目录或指定路径）
load_dotenv()  # 自动查找并加载当前目录下的.env文件

# 读取环境变量（从.env或系统环境中获取）
secret_id = os.getenv('COS_SECRET_ID')  # 优先从.env读取，若不存在则取系统环境变量
secret_key = os.getenv('COS_SECRET_KEY')
region = os.getenv('COS_REGION', 'ap-nanjing')  # 第二个参数为默认值
scheme = os.getenv('COS_SCHEME', 'https')
bucket=os.getenv('COS_BUCKET')

# 初始化配置（单例模式）
_config = CosConfig(
    Region=region,
    SecretId=secret_id,
    SecretKey=secret_key,
    Scheme=scheme
)

# 创建全局唯一的COS客户端实例
cos_client = CosS3Client(_config)


#  cos文件地址拼接
# https://aita-system-1327946406.cos.ap-nanjing.myqcloud.com/test/test.png
def cosJoin(path):
    return "https://{}.cos.{}.myqcloud.com/{}".format(bucket,region,path)


def upload_to_cos(file_stream,cos_path):
    """上传文件流到COS"""
    try:
        response = cos_client.put_object(
            Bucket=bucket,
            Body=file_stream,
            Key=cos_path
        )
        return {
            "success": True,
            "etag": response.get('ETag'),
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


# 文件下载函数（封装为独立函数以保证复用性）
def download_from_cos(cos_path):
    try:
        response = cos_client.get_object(
            Bucket=bucket,
            Key=cos_path
        )
        # 获取文件名（从COS路径中提取）
        file_name = os.path.basename(cos_path)
        # 获取文件流
        file_stream = response['Body'].get_raw_stream()
        return {
            "success": True,
            "file_stream": file_stream,
            "file_name": file_name
        }
    except Exception as e:
        return {
            "success": False,
            "error":str(e)
        }



if __name__ == '__main__':
    filename="patient079_frame01_slice_5.png"
    file_path = "E:\\doing_project\\AITASystem\\aitabackend\\uploads\\patient079_frame01_slice_5.png"
    with open(file_path, 'rb') as file_stream:
        result = upload_to_cos(file_stream, "test/{}".format(filename))
    print(result)



