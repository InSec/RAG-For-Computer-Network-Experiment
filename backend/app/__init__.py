from flask import Flask
from flask_cors import CORS
from .routes import main_routes


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'
    CORS(app)

    # 注册路由
    app.register_blueprint(main_routes)

    return app
