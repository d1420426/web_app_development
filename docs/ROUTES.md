# 食譜收藏夾系統 — 路由設計文件 (ROUTES)

**版本**：v1.0  
**撰寫日期**：2026-04-16  
**對應文件**：docs/PRD.md、docs/ARCHITECTURE.md、docs/DB_DESIGN.md

---

## 1. 路由總覽表格

| 功能             | HTTP 方法 | URL 路徑                  | 對應模板                  | 說明                             |
|------------------|-----------|---------------------------|---------------------------|----------------------------------|
| 首頁 / 食譜列表  | GET       | `/`                       | `index.html`              | 顯示所有食譜，可依類別篩選        |
| 搜尋 / 篩選      | GET       | `/search`                 | `search.html`             | 依關鍵字或分類過濾食譜            |
| 顯示新增表單     | GET       | `/recipes/new`            | `recipe_form.html`        | 顯示空白新增表單                  |
| 送出新增食譜     | POST      | `/recipes/new`            | — (重導向)                | 驗證並儲存食譜至資料庫            |
| 食譜詳細頁       | GET       | `/recipes/<int:id>`       | `recipe_detail.html`      | 顯示完整食材與步驟                |
| 顯示編輯表單     | GET       | `/recipes/<int:id>/edit`  | `recipe_form.html`        | 預填現有資料供修改                |
| 送出編輯食譜     | POST      | `/recipes/<int:id>/edit`  | — (重導向)                | 更新資料庫中的食譜資料            |
| 刪除食譜         | POST      | `/recipes/<int:id>/delete`| — (重導向)                | 刪除食譜及其食材、步驟            |

---

## 2. 每個路由的詳細說明

---

### 2.1 GET `/` — 首頁 / 食譜列表

**輸入**
- Query String（選填）：`category=<類別名稱>`，用於篩選分類

**處理邏輯**
1. 讀取 query string 中的 `category` 參數（可為空）
2. 若有 category → 呼叫 `Recipe.get_by_category(category)`
3. 若無 category → 呼叫 `Recipe.get_all()`
4. 取得所有分類清單（供篩選按鈕使用）

**輸出**
- 渲染 `index.html`，傳入：
  - `recipes`：食譜清單
  - `categories`：所有分類
  - `selected_category`：目前選擇的分類（可為 None）

**錯誤處理**
- 無食譜時顯示「尚無食譜，點此新增」的提示

---

### 2.2 GET `/search` — 搜尋 / 篩選

**輸入**
- Query String：
  - `q=<關鍵字>`（選填）
  - `category=<分類>`（選填）

**處理邏輯**
1. 讀取 `q` 與 `category` 參數
2. 呼叫 `Recipe.search(keyword=q, category=category)`
3. 整理搜尋結果

**輸出**
- 渲染 `search.html`，傳入：
  - `recipes`：搜尋結果清單
  - `keyword`：搜尋關鍵字
  - `selected_category`：選擇的分類
  - `categories`：所有分類

**錯誤處理**
- 無結果時顯示「找不到符合的食譜」提示

---

### 2.3 GET `/recipes/new` — 顯示新增表單

**輸入**
- 無

**處理邏輯**
- 傳遞空的表單資料與分類選項

**輸出**
- 渲染 `recipe_form.html`，傳入：
  - `recipe`：None（表示新增模式）
  - `categories`：分類選項清單
  - `form_action`：`/recipes/new`

**錯誤處理**
- 無

---

### 2.4 POST `/recipes/new` — 送出新增食譜

**輸入（表單欄位）**

| 欄位名稱      | 類型   | 必填 | 說明                              |
|--------------|--------|------|-----------------------------------|
| `title`      | text   | ✅   | 食譜名稱                          |
| `category`   | select | ✅   | 分類                              |
| `description`| textarea| ❌  | 簡介                              |
| `cook_time`  | number | ❌   | 烹調時間（分鐘）                  |
| `servings`   | number | ❌   | 份量                              |
| `difficulty` | select | ❌   | 難易度                            |
| `ingredient_name[]` | text | ❌ | 食材名稱（多筆）              |
| `ingredient_amount[]`| text| ❌| 食材份量（多筆）             |
| `ingredient_unit[]` | text | ❌ | 食材單位（多筆）              |
| `step_description[]`| textarea| ❌| 步驟說明（多筆）           |

**處理邏輯**
1. 驗證必填欄位（title、category）
2. 驗證失敗 → flash 錯誤訊息，返回表單頁
3. 呼叫 `Recipe.create(data)` 新增食譜
4. 逐一處理食材清單（`ingredient_name[]` 等陣列欄位），呼叫 `Ingredient.create(...)`
5. 逐一處理步驟清單，呼叫 `Step.create(...)`

**輸出**
- 成功 → `redirect(url_for('recipe.detail', id=recipe.id))`
- 失敗 → 返回表單頁，顯示錯誤

**錯誤處理**
- title 或 category 為空 → flash 錯誤，保留原本輸入值重新渲染表單

---

### 2.5 GET `/recipes/<int:id>` — 食譜詳細頁

**輸入**
- URL 參數：`id`（食譜 ID）

**處理邏輯**
1. 呼叫 `Recipe.get_by_id(id)`
2. 若食譜不存在 → 404

**輸出**
- 渲染 `recipe_detail.html`，傳入：
  - `recipe`：食譜物件（含 `.ingredients` 與 `.steps`）

**錯誤處理**
- 找不到食譜 → `abort(404)`

---

### 2.6 GET `/recipes/<int:id>/edit` — 顯示編輯表單

**輸入**
- URL 參數：`id`（食譜 ID）

**處理邏輯**
1. 呼叫 `Recipe.get_by_id(id)`
2. 若不存在 → 404

**輸出**
- 渲染 `recipe_form.html`，傳入：
  - `recipe`：現有食譜物件（含食材與步驟，供預填）
  - `categories`：分類選項
  - `form_action`：`/recipes/<id>/edit`

**錯誤處理**
- 找不到食譜 → `abort(404)`

---

### 2.7 POST `/recipes/<int:id>/edit` — 送出編輯食譜

**輸入（表單欄位）**
- 同 2.4，欄位名稱相同

**處理邏輯**
1. 驗證必填欄位
2. 驗證失敗 → flash 錯誤，返回編輯表單
3. 呼叫 `recipe.update(data)` 更新基本資訊
4. 呼叫 `Ingredient.delete_by_recipe(id)` 清空舊食材
5. 重新逐一建立新食材清單
6. 呼叫 `Step.delete_by_recipe(id)` 清空舊步驟
7. 重新逐一建立新步驟

**輸出**
- 成功 → `redirect(url_for('recipe.detail', id=id))`
- 失敗 → 返回編輯表單

**錯誤處理**
- 找不到食譜 → `abort(404)`
- 必填欄位為空 → flash 錯誤，返回表單

---

### 2.8 POST `/recipes/<int:id>/delete` — 刪除食譜

**輸入**
- URL 參數：`id`（食譜 ID）

**處理邏輯**
1. 呼叫 `Recipe.get_by_id(id)`
2. 若不存在 → 404
3. 呼叫 `recipe.delete()`（食材與步驟由 CASCADE 自動刪除）

**輸出**
- 成功 → `redirect(url_for('recipe.index'))`

**錯誤處理**
- 找不到食譜 → `abort(404)`

---

## 3. Jinja2 模板清單

| 模板檔案              | 繼承自      | 說明                                    |
|-----------------------|-------------|----------------------------------------|
| `base.html`           | —           | 共用版型：導覽列、flash 訊息區、頁尾    |
| `index.html`          | `base.html` | 首頁：食譜列表 + 分類篩選按鈕           |
| `search.html`         | `base.html` | 搜尋結果頁：搜尋框 + 結果列表           |
| `recipe_form.html`    | `base.html` | 新增 / 編輯食譜表單（共用，依模式切換） |
| `recipe_detail.html`  | `base.html` | 食譜詳細頁：完整食材 + 步驟             |

---

## 4. 分類選項定義

```python
CATEGORIES = ["早餐", "午餐", "晚餐", "甜點", "飲品", "其他"]
DIFFICULTIES = ["簡單", "普通", "進階"]
```

---

## 5. Flask Blueprint 規劃

| Blueprint 名稱 | prefix      | 對應檔案                    |
|----------------|-------------|-----------------------------|
| `recipe`       | `/`         | `app/routes/recipe_routes.py` |

---

*本文件為活文件，隨開發進度持續更新。*
