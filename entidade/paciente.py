from datetime import date
from entidade.pessoa import Pessoa
from exceptions.dado_invalido_exception import DadoInvalidoException


class Paciente(Pessoa):
    IDADE_MINIMA_INDEPENDENTE = 18

    def __init__(self, nome: str, celular: str, cpf: str,
                 data_nascimento: date,
                 responsavel: 'Paciente | None' = None) -> None:
        super().__init__(nome, celular, cpf)
        self.__data_nascimento = None
        self.__responsavel = None
        self.data_nascimento = data_nascimento
        self.responsavel = responsavel

    @property
    def data_nascimento(self) -> date:
        return self.__data_nascimento

    @data_nascimento.setter
    def data_nascimento(self, data_nascimento: date) -> None:
        if (not isinstance(data_nascimento, date)
                or data_nascimento > date.today()):
            raise DadoInvalidoException("data de nascimento",
                                        "data futura ou invalida")
        self.__data_nascimento = data_nascimento

    @property
    def responsavel(self) -> 'Paciente | None':
        return self.__responsavel

    @responsavel.setter
    def responsavel(self, responsavel: 'Paciente | None') -> None:
        if responsavel is not None:
            if not isinstance(responsavel, Paciente):
                raise DadoInvalidoException(
                    "responsavel", "deve ser um paciente cadastrado")
            if responsavel is self:
                raise DadoInvalidoException(
                    "responsavel", "paciente nao pode ser responsavel por si")
        self.__responsavel = responsavel

    @staticmethod
    def calcula_idade(nascimento: date, data: date) -> int:
        idade = data.year - nascimento.year
        if (data.month, data.day) < (nascimento.month, nascimento.day):
            idade -= 1
        return idade

    def idade_em(self, data: date) -> int:
        return Paciente.calcula_idade(self.__data_nascimento, data)

    def eh_maior_de_idade(self, data: date) -> bool:
        return self.idade_em(data) >= Paciente.IDADE_MINIMA_INDEPENDENTE

    def pode_ser_atendido_em(self, data: date) -> bool:
        if self.eh_maior_de_idade(data):
            return True
        return (self.__responsavel is not None
                and self.__responsavel.eh_maior_de_idade(data))

    def tipo(self) -> str:
        return "Paciente"
