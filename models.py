from datetime import datetime
from app import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='id')
    account = db.Column(db.String(256), nullable=False, comment='账号')
    password = db.Column(db.String(512), nullable=False, comment='密码')
    name = db.Column(db.String(256), nullable=True, comment='用户昵称')
    avatar = db.Column(db.String(1024), nullable=True, comment='用户头像')
    profile = db.Column(db.String(512), nullable=True, comment='用户简介')
    role = db.Column(db.String(256), default='user', nullable=False, comment='用户角色：user/admin/ban')
    reviewStatus = db.Column(db.SmallInteger, default=0, nullable=False, comment='审核状态：0-待审核，1-通过，2-拒绝')
    isDelete = db.Column(db.SmallInteger, default=0, nullable=False, comment='0不删除，1删除')

class Dataset(db.Model):
    __tablename__ = 'dataset'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='ID')
    title = db.Column(db.String(256), nullable=True, comment='标题')
    content = db.Column(db.Text, nullable=True, comment='内容')
    author = db.Column(db.String(128), nullable=True, comment='作者')
    link = db.Column(db.String(1024), nullable=True, comment='链接')
    image_url = db.Column(db.String(1024), nullable=True, comment='图片URL')
    type = db.Column(db.String(128), nullable=True, comment='类型')
    abstract = db.Column(db.Text, nullable=True, comment='摘要')
    createTime = db.Column(db.DateTime, default=datetime.utcnow, nullable=True, comment='创建时间')
    updateTime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True, comment='修改时间')
    isDelete = db.Column(db.SmallInteger, default=0, nullable=False, comment='是否删除')

class Papers(db.Model):
    __tablename__ = 'papers'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='论文ID')
    title = db.Column(db.String(255), nullable=False, comment='论文标题')
    content = db.Column(db.Text, comment='论文正文')
    publishTime = db.Column(db.DateTime, nullable=True, comment='发布时间')
    author = db.Column(db.String(100), nullable=False, comment='作者')
    abstract = db.Column(db.Text, comment='摘要')
    keywords = db.Column(db.String(500), comment='关键词，逗号分隔')
    citation_count = db.Column(db.Integer, default=0, comment='被引用次数')
    source = db.Column(db.String(100), comment='论文来源')
    doi = db.Column(db.String(100), comment='DOI编号')
    pdf_url = db.Column(db.String(2083), comment='PDF文件URL')
    createTime = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, comment='创建时间')
    updateTime = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False, comment='更新时间')
    isDelete = db.Column(db.SmallInteger, default=0, nullable=False, comment='是否删除')

class TeamMembers(db.Model):
    __tablename__ = 'team_members'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, comment='姓名')
    gender = db.Column(db.SmallInteger, default=0, comment='性别0-男 1-女')
    ethnicity = db.Column(db.String(30), comment='民族')
    department = db.Column(db.String(100), comment='系所')
    position = db.Column(db.String(50), comment='职务')
    title = db.Column(db.String(50), comment='职称')
    phone = db.Column(db.String(20), comment='办公电话')
    email = db.Column(db.String(100), unique=True, comment='电子邮箱')
    image_url = db.Column(db.String(255), comment='照片')
    profile = db.Column(db.Text, comment='个人简介')
    areas = db.Column(db.Text, comment='研究领域')
    courses = db.Column(db.Text, comment='主讲课程')
    patents = db.Column(db.Text, comment='专利')
    projects = db.Column(db.Text, comment='科研项目')
    publications = db.Column(db.Text, comment='论文')
    honors = db.Column(db.Text, comment='荣誉')
    isDelete = db.Column(db.SmallInteger, default=0, nullable=False, comment='是否删除')


class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True, comment='新闻ID')
    title = db.Column(db.String(128), nullable=False, comment='新闻标题')
    content = db.Column(db.Text, nullable=False, comment='新闻内容')
    author = db.Column(db.String(128), default='佚名', comment='作者名称')
    publish_time = db.Column(db.DateTime, default=datetime.now, comment='发布时间')
    link = db.Column(db.String(256), comment='原文链接')
    image_url = db.Column(db.Text, comment='封面图URL')
    isDelete = db.Column(db.SmallInteger, default=0, nullable=False, comment='删除标志：0-正常，1-已删除')
    createTime = db.Column(db.DateTime, default=datetime.now, nullable=False, comment='创建时间')
    updateTime = db.Column(db.DateTime, default=datetime.now, nullable=False, onupdate=datetime.now, comment='更新时间')
