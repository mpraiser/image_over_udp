from abc import ABCMeta, abstractmethod


class Topic(metaclass=ABCMeta):
    def __init__(self):
        self.__runnable = True

    @abstractmethod
    def run(self):
        """run this test. only can be called once."""
        if not self.__runnable:
            raise Exception("Topic cannot run twice!")
        self.__runnable = False

    @abstractmethod
    def result(self):
        """get result of test"""
        pass
