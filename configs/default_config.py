# 默认的配置
default_config = {
  "spider": {
    "time_out": 5,
    "request_max_count": 3,
    "logs": {
      # 路径可以为相对路径或者绝对路径可以用\或者/
      "logs_dir": "logs/",
      "logger_level": "logging.DEBUG",
      "file_level": "logging.DEBUG",
      "stream_level": "logging.INFO",
      "level_options": ["logging.DEBUG", "logging.INFO", "logging.WARNING", "logging.ERROR", "logging.CRITICAL"]
    }
  }
}