from exceptions.sistema_exception import SistemaException


class RegistroRepetidoException(SistemaException):
    def __init__(self, entidade: str, chave: int | str) -> None:
        self.mensagem = "{} com identificador {} ja existe"
        super().__init__(self.mensagem.format(entidade, chave))
