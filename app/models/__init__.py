"""
app/models/__init__.py

初始化 SQLAlchemy db 物件，供所有 Model 匯入使用。
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
