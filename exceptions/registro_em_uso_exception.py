from exceptions.sistema_exception import SistemaException


class RegistroEmUsoException(SistemaException):
    def __init__(self, entidade: str, motivo: str) -> None:
        self.mensagem = "{} nao pode ser excluido(a): {}"
        super().__init__(self.mensagem.format(entidade, motivo))
