from exceptions.sistema_exception import SistemaException


class PagamentoInvalidoException(SistemaException):
    def __init__(self, motivo: str) -> None:
        self.mensagem = "Pagamento invalido: {}"
        super().__init__(self.mensagem.format(motivo))
