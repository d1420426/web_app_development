"""
app/routes/__init__.py

初始化 routes 套件，並統一匯入所有 Blueprint。
在 app/__init__.py 中呼叫 register_blueprints(app) 完成註冊。
"""

from app.routes.recipe_routes import recipe_bp


def register_blueprints(app):
    """
    將所有 Blueprint 註冊到 Flask app。
    
    Args:
        app: Flask application instance
    """
    app.register_blueprint(recipe_bp)
