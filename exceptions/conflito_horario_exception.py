from datetime import date, time
from exceptions.sistema_exception import SistemaException


class ConflitoHorarioException(SistemaException):
    def __init__(self, nome: str, data: date, inicio: time,
                 fim: time) -> None:
        self.mensagem = "{} ja possui atendimento em {} das {} as {}"
        super().__init__(self.mensagem.format(
            nome, data.strftime("%d/%m/%Y"), inicio.strftime("%H:%M"),
            fim.strftime("%H:%M")))
