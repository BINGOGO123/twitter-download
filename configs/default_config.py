import pymysql
import logging

# 默认的配置
default_config = {
    "default": {
        "logs": {
            # 路径可以为相对路径或者绝对路径可以用\或者/
            "logs_dir": "logs/",
            "logger_level": logging.DEBUG,
            "file_level": logging.DEBUG,
            "stream_level": logging.INFO,
        },
    },
    "database": {
        "db_connect_params": {
            "creator": pymysql,  # 使用链接数据库的模块
            "maxconnections": 6,  # 连接池允许的最大连接数，0和None表示不限制连接数
            "mincached": 2,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
            "maxcached": 5,  # 链接池中最多闲置的链接，0和None不限制
            "maxshared": 1,  # 链接池中最多共享的链接数量，0和None表示全部共享
            "blocking": True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
            "maxusage": None,  # 一个链接最多被重复使用的次数，None表示无限制
            "setsession": [],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
            "ping": 0,
            # ping MySQL服务端，检查是否服务可用。
            # 如：0 = None = never,
            # 1 = default = whenever it is requested,
            # 2 = when a cursor is created,
            # 4 = when a query is executed,
            # 7 = always
            "charset": "utf8mb4",  # 4字节编码utf8
        },
        "sqlite_db_name": "twitter_download",
        "default_database_type": "sqlite",
    },
    "page": {
        "page_count": 40,
    },
    "persistence": {
        "target_dir": "./default_persistence_dir",
    },
    "downloader": {
        "request_max_count": 3,
        "requests_kwargs": {
            "headers": {
                "Accept": "",
                "Authorization": "",
                "Content-Type": "",
                "User-Agent": "",
                "X-Csrf-Token": "",
                "Cookie": ""
            },
            "timeout": 5,
        },
    },
    "__main__": {
        "twitter_download_dir": "./download_info/twitter/",
        "tweeted_download_dir": "./download_info/tweeted/",
        "favorite_download_dir": "./download_info/favorite/",
        "download_type": "tweeted"
    }
}
