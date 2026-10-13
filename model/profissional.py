from model.pessoa import Pessoa


class Profissional(Pessoa):
    def __init__(self, nome: str, data_nascimento: str, cpf: str, especialidade: str, registro: str,) -> None:
        super().__init__(nome, data_nascimento, cpf)
        self.__especialidade = especialidade
        self.__registro = registro

    @property
    def especialidade(self) -> str:
        return self.__especialidade

    @especialidade.setter
    def especialidade(self, especialidade: str) -> None:
        self.__especialidade = especialidade

    @property
    def registro(self) -> str:
        return self.__registro

    @registro.setter
    def registro(self, registro: str) -> None:
        self.__registro = registro