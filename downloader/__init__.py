import logging
from configs import base_config
from tool.tool import initialLogger

module_name = __name__
logger = logging.getLogger(module_name)

module_config = base_config.get(module_name)

initialLogger(logger, module_name, **module_config.get("logs"))
