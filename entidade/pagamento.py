from abc import ABC, abstractmethod
from datetime import date
from entidade.atendimento import Atendimento
from entidade.paciente import Paciente
from exceptions.dado_invalido_exception import DadoInvalidoException


class Pagamento(ABC):
    @abstractmethod
    def __init__(self, codigo: int, data: date, atendimento: Atendimento,
                 valor_pago: float) -> None:
        self.__codigo = codigo
        self.__data = None
        self.__atendimento = None
        self.__valor_pago = None
        self.data = data
        self.atendimento = atendimento
        self.valor_pago = valor_pago

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def data(self) -> date:
        return self.__data

    @data.setter
    def data(self, data: date) -> None:
        if not isinstance(data, date):
            raise DadoInvalidoException("data do pagamento")
        self.__data = data

    @property
    def atendimento(self) -> Atendimento:
        return self.__atendimento

    @atendimento.setter
    def atendimento(self, atendimento: Atendimento) -> None:
        if not isinstance(atendimento, Atendimento):
            raise DadoInvalidoException("atendimento")
        self.__atendimento = atendimento

    @property
    def paciente(self) -> Paciente:
        return self.__atendimento.paciente

    @property
    def valor_pago(self) -> float:
        return self.__valor_pago

    @valor_pago.setter
    def valor_pago(self, valor_pago: float) -> None:
        if not isinstance(valor_pago, (int, float)) or valor_pago <= 0:
            raise DadoInvalidoException("valor pago",
                                        "deve ser maior que zero")
        self.__valor_pago = float(valor_pago)

    @abstractmethod
    def modalidade(self) -> str:
        pass

    @abstractmethod
    def detalhes(self) -> str:
        pass
