from abc import ABC, abstractmethod


class BaseGenerator(ABC):

    @abstractmethod
    def generate(
        self,
        title: str,
        description: str,
        mitre=None
    ):
        pass