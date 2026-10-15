from datetime import time
from entidade.profissional_saude import ProfissionalSaude
from exceptions.dado_invalido_exception import DadoInvalidoException
from exceptions.horario_invalido_exception import HorarioInvalidoException


class Clinica:
    def __init__(self, codigo: int, nome: str, cidade: str, descricao: str,
                 horario_abertura: time, horario_fechamento: time) -> None:
        self.__codigo = codigo
        self.__nome = None
        self.__cidade = None
        self.__descricao = None
        self.__horario_abertura = None
        self.__horario_fechamento = None
        self.__profissionais = []
        self.nome = nome
        self.cidade = cidade
        self.descricao = descricao
        self.define_funcionamento(horario_abertura, horario_fechamento)

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        if not isinstance(nome, str) or not nome.strip():
            raise DadoInvalidoException("nome da clinica",
                                        "nao pode ser vazio")
        self.__nome = nome.strip()

    @property
    def cidade(self) -> str:
        return self.__cidade

    @cidade.setter
    def cidade(self, cidade: str) -> None:
        if not isinstance(cidade, str) or not cidade.strip():
            raise DadoInvalidoException("cidade", "nao pode ser vazia")
        self.__cidade = cidade.strip()

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str) -> None:
        if not isinstance(descricao, str):
            raise DadoInvalidoException("descricao")
        self.__descricao = descricao.strip()

    @property
    def horario_abertura(self) -> time:
        return self.__horario_abertura

    @property
    def horario_fechamento(self) -> time:
        return self.__horario_fechamento

    @property
    def profissionais(self) -> list[ProfissionalSaude]:
        return list(self.__profissionais)

    def define_funcionamento(self, abertura: time, fechamento: time) -> None:
        if not isinstance(abertura, time) or not isinstance(fechamento, time):
            raise DadoInvalidoException("horario de funcionamento")
        if abertura >= fechamento:
            raise HorarioInvalidoException(
                "abertura deve ser antes do fechamento")
        self.__horario_abertura = abertura
        self.__horario_fechamento = fechamento

    def funciona_entre(self, inicio: time, fim: time) -> bool:
        return (self.__horario_abertura <= inicio
                and fim <= self.__horario_fechamento)

    def incluir_profissional(self, profissional: ProfissionalSaude) -> None:
        if not isinstance(profissional, ProfissionalSaude):
            raise DadoInvalidoException("profissional")
        if profissional not in self.__profissionais:
            self.__profissionais.append(profissional)

    def excluir_profissional(self, profissional: ProfissionalSaude) -> None:
        if profissional in self.__profissionais:
            self.__profissionais.remove(profissional)

    def possui_profissional(self, profissional: ProfissionalSaude) -> bool:
        return profissional in self.__profissionais
