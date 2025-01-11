from flask import Blueprint

# 定义蓝图
routes_bp = Blueprint('routes', __name__)

# 导入并注册视图
from .views import *
