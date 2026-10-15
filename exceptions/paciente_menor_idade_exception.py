from exceptions.sistema_exception import SistemaException


class PacienteMenorIdadeException(SistemaException):
    def __init__(self, nome: str, idade: int) -> None:
        self.mensagem = ("Paciente {} tem {} anos e nao possui responsavel "
                         "maior de idade. Somente maiores de 18 anos podem "
                         "ser atendidos de forma independente")
        super().__init__(self.mensagem.format(nome, idade))
