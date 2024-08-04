# 默认的配置
default_config = {
    "page": {
        "page_count": 40,
        "logs": {
            # 路径可以为相对路径或者绝对路径可以用\或者/
            "logs_dir": "logs/",
            "logger_level": "logging.DEBUG",
            "file_level": "logging.DEBUG",
            "stream_level": "logging.INFO",
            "level_options": [
                "logging.DEBUG",
                "logging.INFO",
                "logging.WARNING",
                "logging.ERROR",
                "logging.CRITICAL",
            ],
        },
    },
    "persistence": {
        "target_dir": "./default_persistence_dir",
        "logs": {
            # 路径可以为相对路径或者绝对路径可以用\或者/
            "logs_dir": "logs/",
            "logger_level": "logging.DEBUG",
            "file_level": "logging.DEBUG",
            "stream_level": "logging.INFO",
            "level_options": [
                "logging.DEBUG",
                "logging.INFO",
                "logging.WARNING",
                "logging.ERROR",
                "logging.CRITICAL",
            ],
        },
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
        "logs": {
            # 路径可以为相对路径或者绝对路径可以用\或者/
            "logs_dir": "logs/",
            "logger_level": "logging.DEBUG",
            "file_level": "logging.DEBUG",
            "stream_level": "logging.INFO",
            "level_options": [
                "logging.DEBUG",
                "logging.INFO",
                "logging.WARNING",
                "logging.ERROR",
                "logging.CRITICAL",
            ],
        },
    },
}
