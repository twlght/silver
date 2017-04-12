from flask import Blueprint
from ..models import Permission

# 实例名 和 参数的名字 不一样可不可以
main = Blueprint('main', __name__)


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)

