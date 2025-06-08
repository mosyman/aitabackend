from app import create_app

app = create_app('development')

@app.route('/')
def hello_world():  # put application's code here
    return 'AITA系统后台服务'

if __name__ == '__main__':
    app.run(host='localhost', port=5000,debug=True)