from abc import ABC, abstractmethod

class AbstractTela(ABC):
    @abstractmethod
    def mostra_menu(self):
        pass
    @abstractmethod
    def le_opcao(self):
        pass