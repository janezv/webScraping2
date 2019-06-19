#!/usr/bin/python3

import logging

class log:
    def __init__(self):
        self.logger = logging.getLogger('myapp')
        self.hdlr = logging.FileHandler('/var/www/html/webScraping/Logs/logging.log')
        self.formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        self.hdlr.setFormatter(self.formatter)
        self.logger.addHandler(self.hdlr)
        self.logger.setLevel(logging.INFO)

    def logMessage(self, message):
        self.logger.info(message)
