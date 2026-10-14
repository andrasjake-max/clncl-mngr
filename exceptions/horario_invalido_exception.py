from exceptions.sistema_exception import SistemaException


class HorarioInvalidoException(SistemaException):
    def __init__(self, motivo: str) -> None:
        self.mensagem = "Horario invalido: {}"
        super().__init__(self.mensagem.format(motivo))
