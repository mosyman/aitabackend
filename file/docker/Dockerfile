# 使用指定的Python镜像
FROM python:3.6.13

# 设置工作目录
WORKDIR /flaskApp


# 安装Python依赖
RUN pip install --no-cache-dir --upgrade pip==21.2.2 -i https://pypi.tuna.tsinghua.edu.cn/simple

#COPY requirements.txt .
COPY ../.. AITASystemBackend/
# 设置应用代码目录为工作目录
WORKDIR /flaskApp/AITASystemBackend
RUN pip install --no-cache-dir -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple



# 复制项目代码（保留原始目录结构）
#COPY AITASystemBackend/ AITASystemBackend/


# 暴露端口
EXPOSE 5000

# 启动命令
CMD ["python", "app.py"]

# 使用Gunicorn启动Flask应用
#CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "app:app"]
