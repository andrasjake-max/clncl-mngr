from exceptions.sistema_exception import SistemaException


class RegistroNaoEncontradoException(SistemaException):
    def __init__(self, entidade: str, chave: int | str) -> None:
        self.mensagem = "{} com identificador {} nao encontrado(a)"
        super().__init__(self.mensagem.format(entidade, chave))
