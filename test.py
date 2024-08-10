from database.mysql import Db
from data_manager.resource_data_manager import ResourceDataManager
import datetime
from data_manager.media import Media
# db = Db()

# result = db.execute("""
# CREATE TABLE media (
#     `id` INT PRIMARY KEY AUTO_INCREMENT,
#     media_url VARCHAR(1000) NOT NULL COMMENT "url链接",
#     storage_path VARCHAR(500) NOT NULL COMMENT "存储路径",
#     content_md5 CHAR(32) NOT NULL COMMENT "存储文件内容的md5值",
#     type_suffix CHAR(32) COMMENT "文件的后缀类型",
#     create_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT "创建时间",
#     lastchange_time DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT "更新时间",
#     KEY media_url_index (media_url(500)),
#     UNIQUE KEY storage_path_index (storage_path)
# );
# """)

# print(result)

# result = db.execute("""
# CREATE INDEX idx_media_url ON media(media_url);
# """)

# print(result)

# result = db.execute("""
# CREATE TRIGGER update_lastchange_time
# AFTER UPDATE ON media
# FOR EACH ROW
# BEGIN
#     UPDATE media SET lastchange_time = CURRENT_TIMESTAMP WHERE id = OLD.id;
# END;
# """)

# print(result)


# result = db.execute("insert into media (media_url, storage_path, content_md5) values  ('1', '4', '3')")

# print(result)

# result = db.execute("select * from media")

# '2024-08-09 18:00:45'

# string_date = "2022-01-01"
# string_time = "12:00:00"
# format = "%Y-%m-%d %H:%M:%S"
# datetime_object = datetime.strptime(string_date + " " + string_time, format)

# print(result)
# for one in result:
#     for a in one:
#         print(type(a))


obj = ResourceDataManager(Db())

print(obj.get_all_data())


print(obj.get_data_info_by_url("1"))

print(type(obj.get_data_info_by_url("1")[0].get_create_time()))

obj.insert_data(Media(media_url = "b", storage_path = "e", content_md5 = "c"))

print(obj.get_all_data())


