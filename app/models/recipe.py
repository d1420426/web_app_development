"""
app/models/recipe.py

Recipe Model — 食譜資料表
對應資料表：recipes
"""

from datetime import datetime
from app.models import db


class Recipe(db.Model):
    """
    食譜資料表。
    
    欄位：
        id          主鍵，自動遞增
        title       食譜名稱（必填）
        category    分類（早餐 / 午餐 / 晚餐 / 甜點 / 飲品 / 其他）
        description 食譜簡介（選填）
        cook_time   烹調時間（分鐘，選填）
        servings    份量（幾人份，選填）
        difficulty  難易度（簡單 / 普通 / 進階，選填）
        created_at  建立時間（自動填入）
        updated_at  最後更新時間（自動更新）
    
    關聯：
        ingredients  一對多 → Ingredient
        steps        一對多 → Step
    """

    __tablename__ = "recipes"

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title       = db.Column(db.Text, nullable=False)
    category    = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=True)
    cook_time   = db.Column(db.Integer, nullable=True)
    servings    = db.Column(db.Integer, nullable=True)
    difficulty  = db.Column(db.Text, nullable=True)
    created_at  = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at  = db.Column(db.DateTime, nullable=False, default=datetime.now, onupdate=datetime.now)

    # 關聯：一道食譜 → 多個食材（刪除食譜時一併刪除食材）
    ingredients = db.relationship(
        "Ingredient",
        backref="recipe",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Ingredient.id"
    )

    # 關聯：一道食譜 → 多個步驟（刪除食譜時一併刪除步驟）
    steps = db.relationship(
        "Step",
        backref="recipe",
        lazy=True,
        cascade="all, delete-orphan",
        order_by="Step.order"
    )

    # ----------------------------------------------------------
    # CRUD 方法
    # ----------------------------------------------------------

    @classmethod
    def get_all(cls):
        """
        取得所有食譜（依建立時間由新到舊排列）。
        
        Returns:
            list[Recipe]: 所有食譜物件的清單
        """
        return cls.query.order_by(cls.created_at.desc()).all()

    @classmethod
    def get_by_id(cls, recipe_id):
        """
        依 ID 取得單一食譜。
        
        Args:
            recipe_id (int): 食譜 ID
        
        Returns:
            Recipe | None: 找到的食譜物件，若不存在則回傳 None
        """
        return cls.query.get(recipe_id)

    @classmethod
    def get_by_category(cls, category):
        """
        依分類取得食譜清單。
        
        Args:
            category (str): 分類名稱
        
        Returns:
            list[Recipe]: 符合分類的食譜清單
        """
        return cls.query.filter_by(category=category).order_by(cls.created_at.desc()).all()

    @classmethod
    def search(cls, keyword=None, category=None):
        """
        依關鍵字與分類搜尋食譜。
        
        Args:
            keyword (str, optional):  搜尋關鍵字（比對 title 與 description）
            category (str, optional): 分類篩選
        
        Returns:
            list[Recipe]: 符合條件的食譜清單
        """
        query = cls.query
        if keyword:
            query = query.filter(
                db.or_(
                    cls.title.ilike(f"%{keyword}%"),
                    cls.description.ilike(f"%{keyword}%")
                )
            )
        if category:
            query = query.filter_by(category=category)
        return query.order_by(cls.created_at.desc()).all()

    @classmethod
    def create(cls, data):
        """
        新增一道食譜（不含食材與步驟）。
        
        Args:
            data (dict): 包含 title、category 等欄位的字典
        
        Returns:
            Recipe: 新建立的食譜物件
        
        Raises:
            Exception: 資料庫寫入失敗時拋出例外
        """
        try:
            recipe = cls(
                title=data["title"],
                category=data["category"],
                description=data.get("description"),
                cook_time=data.get("cook_time"),
                servings=data.get("servings"),
                difficulty=data.get("difficulty"),
            )
            db.session.add(recipe)
            db.session.commit()
            return recipe
        except Exception as e:
            db.session.rollback()
            raise e

    def update(self, data):
        """
        更新食譜基本資訊。
        
        Args:
            data (dict): 包含要更新欄位的字典
        
        Raises:
            Exception: 資料庫更新失敗時拋出例外
        """
        try:
            self.title       = data.get("title", self.title)
            self.category    = data.get("category", self.category)
            self.description = data.get("description", self.description)
            self.cook_time   = data.get("cook_time", self.cook_time)
            self.servings    = data.get("servings", self.servings)
            self.difficulty  = data.get("difficulty", self.difficulty)
            self.updated_at  = datetime.now()
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def delete(self):
        """
        刪除食譜（關聯的食材與步驟會自動一併刪除）。
        
        Raises:
            Exception: 資料庫刪除失敗時拋出例外
        """
        try:
            db.session.delete(self)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def __repr__(self):
        return f"<Recipe id={self.id} title={self.title!r}>"
