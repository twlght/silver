from config import config
# 加..会报错
# ValueError: attempted relative import beyond top-level package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_mail import Mail
from flask_pagedown import PageDown
# from .main import views, errors, forms
# from .main import main as main_blueprint
# from .auth import views, errors, forms
# from .auth import auth as auth_blueprint
# 这些import 放在这里会导致循环导入db, cannot import name 'db'

# db定义在外面成为全局变量
db = SQLAlchemy()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'  # 登陆页面的端点(endpoint)
mail = Mail()
pagedown = PageDown()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])  # 这个给忘了
    config[config_name].init_app(app)  # 这是干嘛的
    db.init_app(app)
    bootstrap.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    pagedown.init_app(app)

    # 导入蓝本，附加路由和自定义错误页面
    from .main import main as main_blueprint
    from .main import views, errors, forms
    from .auth import auth as auth_blueprint
    from .auth import views, errors, forms
    app.register_blueprint(main_blueprint)  # 注册的是blueprint对象：main
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    return app
