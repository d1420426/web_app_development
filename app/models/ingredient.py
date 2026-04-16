"""
app/models/ingredient.py

Ingredient Model — 食材資料表
對應資料表：ingredients
"""

from app.models import db


class Ingredient(db.Model):
    """
    食材資料表。每道食譜可以有多筆食材記錄。
    
    欄位：
        id         主鍵，自動遞增
        recipe_id  外鍵，對應 recipes.id
        name       食材名稱（必填，例：雞蛋）
        amount     份量數值（選填，例：2）
        unit       單位（選填，例：顆、克、毫升）
    
    關聯：
        recipe ← Recipe（透過 backref）
    """

    __tablename__ = "ingredients"

    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    name      = db.Column(db.Text, nullable=False)
    amount    = db.Column(db.Text, nullable=True)
    unit      = db.Column(db.Text, nullable=True)

    # ----------------------------------------------------------
    # CRUD 方法
    # ----------------------------------------------------------

    @classmethod
    def get_by_recipe(cls, recipe_id):
        """
        取得某食譜的所有食材。
        
        Args:
            recipe_id (int): 食譜 ID
        
        Returns:
            list[Ingredient]: 食材清單
        """
        return cls.query.filter_by(recipe_id=recipe_id).all()

    @classmethod
    def create(cls, recipe_id, name, amount=None, unit=None):
        """
        新增一筆食材記錄。
        
        Args:
            recipe_id (int): 所屬食譜 ID
            name (str):      食材名稱
            amount (str):    份量（可選）
            unit (str):      單位（可選）
        
        Returns:
            Ingredient: 新建立的食材物件
        
        Raises:
            Exception: 資料庫寫入失敗時拋出例外
        """
        try:
            ingredient = cls(
                recipe_id=recipe_id,
                name=name,
                amount=amount,
                unit=unit,
            )
            db.session.add(ingredient)
            db.session.commit()
            return ingredient
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def delete_by_recipe(cls, recipe_id):
        """
        刪除某食譜的所有食材（批次刪除，用於編輯時先清空再重建）。
        
        Args:
            recipe_id (int): 食譜 ID
        
        Raises:
            Exception: 資料庫刪除失敗時拋出例外
        """
        try:
            cls.query.filter_by(recipe_id=recipe_id).delete()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def __repr__(self):
        return f"<Ingredient id={self.id} name={self.name!r} recipe_id={self.recipe_id}>"
