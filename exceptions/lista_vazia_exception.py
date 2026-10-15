from exceptions.sistema_exception import SistemaException


class ListaVaziaException(SistemaException):
    def __init__(self, entidade: str) -> None:
        self.mensagem = "Nenhum(a) {} cadastrado(a)"
        super().__init__(self.mensagem.format(entidade))
