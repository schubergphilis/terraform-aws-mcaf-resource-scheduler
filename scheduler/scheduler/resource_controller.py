from abc import ABC

from aws_lambda_powertools import Logger


class ResourceController(ABC):
    def __init__(self):
        self.logger = Logger()

    def start(self):
        raise NotImplementedError('This resource type has no start command implemented.')

    def stop(self):
        raise NotImplementedError('This resource type has no stop command implemented.')
