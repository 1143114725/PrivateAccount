from flask import Flask
from api.routes import setup_routes

# 创建Flask应用实例
app = Flask(__name__)

# 设置路由
setup_routes(app)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=False)  # 监听所有地址，支持localhost访问
