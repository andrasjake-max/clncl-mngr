from datetime import date
from entidade.atendimento import Atendimento
from entidade.pagamento import Pagamento


class PagamentoDinheiro(Pagamento):
    def __init__(self, codigo: int, data: date, atendimento: Atendimento,
                 valor_pago: float) -> None:
        super().__init__(codigo, data, atendimento, valor_pago)

    def modalidade(self) -> str:
        return "Dinheiro"

    def detalhes(self) -> str:
        return "-"
