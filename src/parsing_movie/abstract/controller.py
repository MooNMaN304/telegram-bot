from abc import ABC, abstractmethod


class AbstractController(ABC):
    @abstractmethod
    def run(self, request):
        pass
