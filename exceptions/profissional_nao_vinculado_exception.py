from exceptions.sistema_exception import SistemaException


class ProfissionalNaoVinculadoException(SistemaException):
    def __init__(self, nome_profissional: str, nome_clinica: str) -> None:
        self.mensagem = "Profissional {} nao atende na clinica {}"
        super().__init__(self.mensagem.format(nome_profissional,
                                              nome_clinica))
