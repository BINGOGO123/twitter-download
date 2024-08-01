import logging
from configs import base_config
from tool.tool import initialLogger

module_name = __name__
logger = logging.getLogger(module_name)

initialLogger(logger, module_name, **base_config[module_name].get("logs"))