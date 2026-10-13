from model.pessoa import Pessoa


class Paciente(Pessoa):
    def __init__(
        self,
        nome: str,
        data_nascimento: str,
        cpf: str,
        celular: str,
    ) -> None:
        super().__init__(nome, data_nascimento, cpf)
        self.__celular = celular

    @property
    def celular(self) -> str:
        return self.__celular

    @celular.setter
    def celular(self, celular: str) -> None:
        self.__celular = celular
