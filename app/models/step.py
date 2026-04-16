"""
app/models/step.py

Step Model — 烹調步驟資料表
對應資料表：steps
"""

from app.models import db


class Step(db.Model):
    """
    烹調步驟資料表。每道食譜可以有多個步驟，依 order 欄位排序。
    
    欄位：
        id          主鍵，自動遞增
        recipe_id   外鍵，對應 recipes.id
        order       步驟順序編號（從 1 開始，必填）
        description 步驟說明內容（必填）
    
    關聯：
        recipe ← Recipe（透過 backref）
    """

    __tablename__ = "steps"

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    recipe_id   = db.Column(db.Integer, db.ForeignKey("recipes.id", ondelete="CASCADE"), nullable=False)
    order       = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=False)

    # ----------------------------------------------------------
    # CRUD 方法
    # ----------------------------------------------------------

    @classmethod
    def get_by_recipe(cls, recipe_id):
        """
        取得某食譜的所有步驟（依 order 排序）。
        
        Args:
            recipe_id (int): 食譜 ID
        
        Returns:
            list[Step]: 步驟清單（由小到大排序）
        """
        return cls.query.filter_by(recipe_id=recipe_id).order_by(cls.order).all()

    @classmethod
    def create(cls, recipe_id, order, description):
        """
        新增一個烹調步驟。
        
        Args:
            recipe_id (int):    所屬食譜 ID
            order (int):        步驟順序編號
            description (str):  步驟說明
        
        Returns:
            Step: 新建立的步驟物件
        
        Raises:
            Exception: 資料庫寫入失敗時拋出例外
        """
        try:
            step = cls(
                recipe_id=recipe_id,
                order=order,
                description=description,
            )
            db.session.add(step)
            db.session.commit()
            return step
        except Exception as e:
            db.session.rollback()
            raise e

    @classmethod
    def delete_by_recipe(cls, recipe_id):
        """
        刪除某食譜的所有步驟（批次刪除，用於編輯時先清空再重建）。
        
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
        return f"<Step id={self.id} order={self.order} recipe_id={self.recipe_id}>"
