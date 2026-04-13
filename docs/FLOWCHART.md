# 食譜收藏夾系統 — 流程圖文件 (FLOWCHART)

**版本**：v1.0  
**撰寫日期**：2026-04-13  
**對應文件**：docs/PRD.md、docs/ARCHITECTURE.md

---

## 1. 使用者流程圖（User Flow）

描述使用者從進入網站到完成各項操作的完整路徑。

```mermaid
flowchart LR
    A([使用者開啟網站]) --> B[首頁：食譜列表]

    B --> C{要做什麼？}

    C -->|瀏覽分類| D[選擇類別篩選]
    D --> B

    C -->|搜尋食譜| E[輸入關鍵字]
    E --> F[顯示搜尋結果]
    F --> G[點選食譜]

    C -->|新增食譜| H[填寫食譜表單]
    H --> H1[輸入名稱、描述、分類]
    H1 --> H2[新增食材清單]
    H2 --> H3[新增烹調步驟]
    H3 --> H4{確認送出？}
    H4 -->|送出| I[食譜詳細頁]
    H4 -->|取消| B

    C -->|查看食譜| G
    G --> I[食譜詳細頁]
    I --> I1[查看食材清單]
    I --> I2[查看烹調步驟]

    I --> J{繼續操作？}
    J -->|編輯食譜| K[編輯表單]
    K --> K1{確認儲存？}
    K1 -->|儲存| I
    K1 -->|取消| I

    J -->|刪除食譜| L{確認刪除？}
    L -->|確認| B
    L -->|取消| I

    J -->|返回列表| B
```

---

## 2. 系統序列圖（Sequence Diagram）

### 2.1 新增食譜

描述使用者填寫表單送出後，資料儲存至資料庫的完整流程。

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model（SQLAlchemy）
    participant DB as SQLite

    User->>Browser: 填寫食譜表單並點擊送出
    Browser->>Flask: POST /recipes/new
    Flask->>Flask: 驗證表單資料
    Flask->>Model: 建立 Recipe 物件
    Model->>DB: INSERT INTO recipes
    DB-->>Model: 成功
    Flask->>Model: 建立多筆 Ingredient 物件
    Model->>DB: INSERT INTO ingredients
    DB-->>Model: 成功
    Flask->>Model: 建立多筆 Step 物件
    Model->>DB: INSERT INTO steps
    DB-->>Model: 成功
    Flask-->>Browser: 302 重導向到 /recipes/<id>
    Browser->>Flask: GET /recipes/<id>
    Flask->>Model: Recipe.query.get(id)
    Model->>DB: SELECT * FROM recipes WHERE id=?
    DB-->>Model: 回傳資料
    Model-->>Flask: Recipe 物件
    Flask-->>Browser: 渲染 recipe_detail.html
    Browser-->>User: 顯示食譜詳細頁
```

### 2.2 瀏覽與搜尋食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model（SQLAlchemy）
    participant DB as SQLite

    User->>Browser: 輸入關鍵字或選擇分類
    Browser->>Flask: GET /search?q=關鍵字&category=類別
    Flask->>Model: Recipe.query.filter(...)
    Model->>DB: SELECT * FROM recipes WHERE title LIKE ? OR category=?
    DB-->>Model: 回傳符合結果
    Model-->>Flask: Recipe 物件列表
    Flask-->>Browser: 渲染 search.html
    Browser-->>User: 顯示搜尋結果列表
```

### 2.3 刪除食譜

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Model as Model（SQLAlchemy）
    participant DB as SQLite

    User->>Browser: 點擊「刪除」按鈕並確認
    Browser->>Flask: POST /recipes/<id>/delete
    Flask->>Model: Recipe.query.get(id)
    Model->>DB: DELETE FROM steps WHERE recipe_id=?
    Model->>DB: DELETE FROM ingredients WHERE recipe_id=?
    Model->>DB: DELETE FROM recipes WHERE id=?
    DB-->>Model: 成功
    Flask-->>Browser: 302 重導向到 /
    Browser-->>User: 顯示首頁（食譜已移除）
```

---

## 3. 功能清單對照表

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
|------|-----------|----------|----------|------|
| 首頁 / 食譜列表 | GET | `/` | `index.html` | 顯示所有食譜，可依類別篩選 |
| 顯示新增表單 | GET | `/recipes/new` | `recipe_form.html` | 空白表單供使用者填寫 |
| 送出新增食譜 | POST | `/recipes/new` | 重導向 | 驗證並儲存食譜至資料庫 |
| 食譜詳細頁 | GET | `/recipes/<id>` | `recipe_detail.html` | 顯示完整食材與步驟 |
| 顯示編輯表單 | GET | `/recipes/<id>/edit` | `recipe_form.html` | 預填現有資料供修改 |
| 送出編輯食譜 | POST | `/recipes/<id>/edit` | 重導向 | 更新資料庫中的食譜資料 |
| 刪除食譜 | POST | `/recipes/<id>/delete` | 重導向 | 刪除食譜及其食材、步驟 |
| 搜尋 / 篩選 | GET | `/search` | `search.html` | 依關鍵字或類別過濾食譜 |

---

*本文件為活文件，隨開發進度持續更新。*
