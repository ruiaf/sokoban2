import argparse


class Args:
    _instance = None

    def __init__(self):
        raise RuntimeError('Call instance() instead')

    @classmethod
    def instance(cls):
        if cls._instance is None:
            print('Creating new instance')
            cls._instance = cls.__new__(cls)
            cls._instance.parser = argparse.ArgumentParser(description="Run the game")
            cls._instance._args = None
        return cls._instance

    def args(self):
        if self._args is None:
            self._args = self.parser.parse_args()
        return self._args