import logging

class LoggerWrapper:
    def __init__(self, logger: logging.Logger, print_result = False):
        self.logger = logger
        self.print_result = print_result
 
    def __call__(self, func):

        def logger_wrap(*args, **kwargs):
            if len(kwargs) == 0:
                self.logger.info("{}({})".format(func.__name__, ",".join([str(x) for x in args])))
            elif len(args) == 0:
                self.logger.info("{}({})".format(func.__name__, ",".join(["{}={}".format(x, kwargs[x]) for x in kwargs.keys()])))
            else:
                self.logger.info("{}({},{})".format(func.__name__, ",".join([str(x) for x in args]), ",".join(["{}={}".format(x, kwargs[x]) for x in kwargs.keys()])))
            result = func(*args, **kwargs)
            if self.print_result:
                self.logger.info("{}={}".format(func.__name__, result))
            return result
 
        return logger_wrap