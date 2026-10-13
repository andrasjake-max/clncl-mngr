from model.atendimento import Atendimento
from model.paciente import Paciente
from model.profissional import Profissional


class Clinica:
    def __init__(
        self,
        nome: str,
        localizacao: str,
        descricao: str,
        profissionais: list[Profissional],
    ) -> None:
        self.__nome = nome
        self.__localizacao = localizacao
        self.__descricao = descricao
        self.__profissionais = list(profissionais)
        self.__clientes: list[Paciente] = []
        self.__atendimentos: list[Atendimento] = []

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        self.__nome = nome

    @property
    def localizacao(self) -> str:
        return self.__localizacao

    @localizacao.setter
    def localizacao(self, localizacao: str) -> None:
        self.__localizacao = localizacao

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str) -> None:
        self.__descricao = descricao

    @property
    def profissionais(self) -> list[Profissional]:
        return self.__profissionais

    @property
    def clientes(self) -> list[Paciente]:
        return self.__clientes

    @property
    def atendimentos(self) -> list[Atendimento]:
        return self.__atendimentos

    def adiciona_profissional(self, profissional: Profissional) -> None:
        self.__profissionais.append(profissional)

    def remove_profissional(self, profissional: Profissional) -> None:
        self.__profissionais.remove(profissional)

    def adiciona_atendimento(self, atendimento: Atendimento) -> None:
        self.__atendimentos.append(atendimento)

    def remove_atendimento(self, atendimento: Atendimento) -> None:
        self.__atendimentos.remove(atendimento)

    def adiciona_cliente(self, cliente: Paciente) -> None:
        self.__clientes.append(cliente)

    def remove_cliente(self, cliente: Paciente) -> None:
        self.__clientes.remove(cliente)