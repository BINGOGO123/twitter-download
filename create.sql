-- 数据库格式，供参考

DROP DATABASE IF EXISTS twitter_download;

CREATE DATABASE twitter_download;

USE twitter_download;

CREATE TABLE media (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    media_url VARCHAR(1000) NOT NULL COMMENT "url链接",
    storage_path VARCHAR(500) NOT NULL COMMENT "存储路径",
    content_md5 CHAR(32) NOT NULL COMMENT "存储文件内容的md5值",
    type_suffix CHAR(32) COMMENT "文件的后缀类型",
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT "创建时间",
    lastchange_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间",
    KEY media_url_index (media_url(500)),
    UNIQUE KEY storage_path_index (storage_path)
);

-- ALTER TABLE media ADD content_md5 CHAR(32) NOT NULL;


-- 以下为SQLite的语法

CREATE TABLE media (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    media_url VARCHAR(1000) NOT NULL, -- url链接
    storage_path VARCHAR(500) NOT NULL UNIQUE, -- 存储路径，确保唯一
    content_md5 CHAR(32) NOT NULL, -- 存储文件内容的md5值
    type_suffix CHAR(32), -- 文件的后缀类型
    create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- 创建时间
    lastchange_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP -- 更新时间
);

-- 为 media_url 创建索引
CREATE INDEX idx_media_url ON media(media_url);

-- 为 storage_path 创建索引
CREATE INDEX idx_storage_path ON media(storage_path);

-- 创建触发器来自动更新 lastchange_time
CREATE TRIGGER update_lastchange_time
AFTER UPDATE ON media
FOR EACH ROW
BEGIN
    UPDATE media SET lastchange_time = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;