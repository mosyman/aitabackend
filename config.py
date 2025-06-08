import os
from dotenv import load_dotenv

# 自动加载项目根目录的 .env 文件
load_dotenv()

class Config:
    # 需要在 项目根目录创建 .env 文件，并填写SECRET_KEY和DB_URL
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    #  session有效期7天
    # PERMANENT_SESSION_LIFETIME = timedelta(days=7)

class DevelopmentConfig(Config):
    pass
    # 开启 SQL 语句日志（方便调试）
    # SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    pass

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}  