from datetime import date
from entidade.atendimento import Atendimento
from entidade.pagamento import Pagamento
from exceptions.dado_invalido_exception import DadoInvalidoException


class PagamentoCartao(Pagamento):
    BANDEIRAS = ("Visa", "Mastercard", "Elo", "American Express", "Hipercard")

    def __init__(self, codigo: int, data: date, atendimento: Atendimento,
                 valor_pago: float, numero_cartao: str, bandeira: str) -> None:
        super().__init__(codigo, data, atendimento, valor_pago)
        self.__numero_cartao = None
        self.__bandeira = None
        self.numero_cartao = numero_cartao
        self.bandeira = bandeira

    @property
    def numero_cartao(self) -> str:
        return self.__numero_cartao

    @numero_cartao.setter
    def numero_cartao(self, numero_cartao: str) -> None:
        if (not isinstance(numero_cartao, str) or not numero_cartao.isdigit()
                or not 13 <= len(numero_cartao) <= 19):
            raise DadoInvalidoException("numero do cartao",
                                        "deve ter de 13 a 19 digitos")
        self.__numero_cartao = numero_cartao

    @property
    def bandeira(self) -> str:
        return self.__bandeira

    @bandeira.setter
    def bandeira(self, bandeira: str) -> None:
        if bandeira not in PagamentoCartao.BANDEIRAS:
            raise DadoInvalidoException("bandeira", "bandeira nao aceita")
        self.__bandeira = bandeira

    def modalidade(self) -> str:
        return "Cartao de credito"

    def detalhes(self) -> str:
        return "{} final {}".format(self.__bandeira, self.__numero_cartao[-4:])
