from abc import ABC, abstractmethod
from exceptions.dado_invalido_exception import DadoInvalidoException


class Pessoa(ABC):
    @abstractmethod
    def __init__(self, nome: str, celular: str, cpf: str) -> None:
        self.__nome = None
        self.__celular = None
        self.__cpf = None
        self.nome = nome
        self.celular = celular
        self.cpf = cpf

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        if not isinstance(nome, str) or not nome.strip():
            raise DadoInvalidoException("nome", "nao pode ser vazio")
        self.__nome = nome.strip()

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, celular: str) -> None:
        if (not isinstance(celular, str) or not celular.isdigit()
                or len(celular) not in (10, 11)):
            raise DadoInvalidoException(
                "celular", "informe DDD + numero (10 ou 11 digitos)")
        self.__celular = celular

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str) -> None:
        if not isinstance(cpf, str) or not cpf.isdigit() or len(cpf) != 11:
            raise DadoInvalidoException("CPF", "deve ter 11 digitos")
        self.__cpf = cpf

    @abstractmethod
    def tipo(self) -> str:
        pass
