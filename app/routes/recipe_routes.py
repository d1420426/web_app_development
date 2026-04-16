"""
app/routes/recipe_routes.py

食譜相關路由（Flask Blueprint）
對應文件：docs/ROUTES.md

Blueprint 名稱：recipe
URL prefix：/
"""

from flask import Blueprint, render_template, request, redirect, url_for, flash, abort

# 分類與難易度選項（與資料庫欄位對應）
CATEGORIES = ["早餐", "午餐", "晚餐", "甜點", "飲品", "其他"]
DIFFICULTIES = ["簡單", "普通", "進階"]

recipe_bp = Blueprint("recipe", __name__)


# ============================================================
# GET /
# 首頁：顯示食譜列表，支援分類篩選
# ============================================================
@recipe_bp.route("/")
def index():
    """
    首頁，顯示所有食譜列表。
    
    Query String:
        category (str, optional): 類別篩選，例如「晚餐」
    
    Context (傳入模板):
        recipes            (list[Recipe]): 食譜清單
        categories         (list[str]):   所有分類選項
        selected_category  (str|None):    目前選擇的分類
    
    Returns:
        渲染 index.html
    """
    pass  # TODO: 實作於階段六


# ============================================================
# GET /search
# 搜尋 / 篩選食譜
# ============================================================
@recipe_bp.route("/search")
def search():
    """
    依關鍵字或分類搜尋食譜。
    
    Query String:
        q        (str, optional): 搜尋關鍵字，比對 title 與 description
        category (str, optional): 分類篩選
    
    Context (傳入模板):
        recipes           (list[Recipe]): 搜尋結果
        keyword           (str):          搜尋關鍵字
        selected_category (str|None):     選擇的分類
        categories        (list[str]):    所有分類選項
    
    Returns:
        渲染 search.html
    """
    pass  # TODO: 實作於階段六


# ============================================================
# GET  /recipes/new  → 顯示新增表單
# POST /recipes/new  → 接收並儲存新食譜
# ============================================================
@recipe_bp.route("/recipes/new", methods=["GET", "POST"])
def new_recipe():
    """
    GET:  渲染空白的新增食譜表單。
    POST: 驗證表單資料並將食譜、食材、步驟存入資料庫。
    
    POST 表單欄位:
        title                (str):      食譜名稱（必填）
        category             (str):      分類（必填）
        description          (str):      簡介（選填）
        cook_time            (int):      烹調時間分鐘（選填）
        servings             (int):      份量（選填）
        difficulty           (str):      難易度（選填）
        ingredient_name[]    (list[str]):食材名稱（多筆）
        ingredient_amount[]  (list[str]):食材份量（多筆）
        ingredient_unit[]    (list[str]):食材單位（多筆）
        step_description[]   (list[str]):步驟說明（多筆）
    
    Returns:
        GET:  渲染 recipe_form.html
        POST 成功: redirect 到食譜詳細頁
        POST 失敗: 回到表單並顯示 flash 錯誤
    """
    pass  # TODO: 實作於階段六


# ============================================================
# GET /recipes/<id>
# 食譜詳細頁
# ============================================================
@recipe_bp.route("/recipes/<int:id>")
def detail(id):
    """
    顯示單一食譜的完整資訊（食材 + 步驟）。
    
    URL 參數:
        id (int): 食譜 ID
    
    Context (傳入模板):
        recipe (Recipe): 食譜物件（含 .ingredients 與 .steps）
    
    Returns:
        渲染 recipe_detail.html
        若找不到 → abort(404)
    """
    pass  # TODO: 實作於階段六


# ============================================================
# GET  /recipes/<id>/edit  → 顯示編輯表單（預填資料）
# POST /recipes/<id>/edit  → 接收並更新食譜
# ============================================================
@recipe_bp.route("/recipes/<int:id>/edit", methods=["GET", "POST"])
def edit_recipe(id):
    """
    GET:  渲染預填現有資料的編輯表單。
    POST: 驗證並更新資料庫中的食譜（先清空食材/步驟，再重新建立）。
    
    URL 參數:
        id (int): 食譜 ID
    
    POST 表單欄位:
        （同 new_recipe，欄位名稱完全相同）
    
    Returns:
        GET:  渲染 recipe_form.html（帶有現有資料）
        POST 成功: redirect 到該食譜詳細頁
        POST 失敗: 回到編輯表單並顯示 flash 錯誤
        若找不到 → abort(404)
    """
    pass  # TODO: 實作於階段六


# ============================================================
# POST /recipes/<id>/delete
# 刪除食譜
# ============================================================
@recipe_bp.route("/recipes/<int:id>/delete", methods=["POST"])
def delete_recipe(id):
    """
    刪除指定食譜及其所有食材、步驟（由資料庫 CASCADE 自動刪除）。
    
    URL 參數:
        id (int): 食譜 ID
    
    Returns:
        成功: redirect 到首頁（/）
        若找不到 → abort(404)
    """
    pass  # TODO: 實作於階段六
