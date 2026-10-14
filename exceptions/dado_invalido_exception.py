from exceptions.sistema_exception import SistemaException


class DadoInvalidoException(SistemaException):
    def __init__(self, campo: str, motivo: str = "valor invalido") -> None:
        self.mensagem = "Dado invalido em '{}': {}"
        super().__init__(self.mensagem.format(campo, motivo))
