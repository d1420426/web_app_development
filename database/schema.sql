-- 食譜收藏夾系統 — 資料庫建表語法
-- 對應：docs/DB_DESIGN.md
-- 資料庫：SQLite

-- 啟用外鍵支援（SQLite 預設關閉）
PRAGMA foreign_keys = ON;

-- ============================================================
-- 資料表：recipes（食譜）
-- ============================================================
CREATE TABLE IF NOT EXISTS recipes (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    title       TEXT     NOT NULL,
    category    TEXT     NOT NULL,
    description TEXT,
    cook_time   INTEGER,
    servings    INTEGER,
    difficulty  TEXT,
    created_at  DATETIME NOT NULL DEFAULT (datetime('now', 'localtime')),
    updated_at  DATETIME NOT NULL DEFAULT (datetime('now', 'localtime'))
);

-- ============================================================
-- 資料表：ingredients（食材）
-- ============================================================
CREATE TABLE IF NOT EXISTS ingredients (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    recipe_id   INTEGER  NOT NULL,
    name        TEXT     NOT NULL,
    amount      TEXT,
    unit        TEXT,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);

-- ============================================================
-- 資料表：steps（烹調步驟）
-- ============================================================
CREATE TABLE IF NOT EXISTS steps (
    id          INTEGER  PRIMARY KEY AUTOINCREMENT,
    recipe_id   INTEGER  NOT NULL,
    "order"     INTEGER  NOT NULL,
    description TEXT     NOT NULL,
    FOREIGN KEY (recipe_id) REFERENCES recipes(id) ON DELETE CASCADE
);
