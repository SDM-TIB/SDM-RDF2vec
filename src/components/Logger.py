import logging


class Logger:

    def __init__(self, name='default'):
        self.logger = logging.getLogger(name)
        self.logger.propagate = False
        self.logger.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt='%(asctime)s %(name)s %(message)s',
                                      datefmt='%d/%m/%Y %I:%M:%S %p')
        if not len(self.logger.handlers):
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            ch.setFormatter(formatter)
            self.logger.addHandler(ch)

    def log(self, msg):
        self.logger.info(msg)

    def error(self, msg):
        self.logger.error(msg)