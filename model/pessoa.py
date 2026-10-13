class Pessoa:
    def __init__(self, nome: str, data_nascimento: str, cpf: str) -> None:
        self.__nome = nome
        self.__data_nascimento = data_nascimento
        self.__cpf = cpf

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        self.__nome = nome

    @property
    def data_nascimento(self) -> str:
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: str) -> None:
        self.__data_nascimento = data_nascimento

    @property
    def cpf(self) -> str:
        return self.__cpf

    @cpf.setter
    def cpf(self, cpf: str) -> None:
        self.__cpf = cpf
    