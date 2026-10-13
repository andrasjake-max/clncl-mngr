from datetime import date, time
from model.clinica import Clinica
from model.paciente import Paciente
from model.profissional import Profissional
from model.tipoAtendimento import TipoAtendimento
from model.pagamento import Pagamento
from model.procedimento import Procedimento

class Atendimento:
    def __init__(
        self,
        clinica: Clinica,
        paciente: Paciente,
        profissional: Profissional,
        data: date,
        horario: time,
        tipo_atendimento: TipoAtendimento,
        valor: float,
        pagamento: Pagamento
        ) -> None:
        self.__clinica = clinica
        self.__paciente = paciente
        self.__profissional = profissional
        self.__data = data
        self.__horario = horario
        self.__tipo_atendimento = tipo_atendimento
        self.__valor = valor
        self.__pagamento = pagamento
        self.__procedimentos = list[Procedimento]

    @property
    def clinica(self) -> Clinica:
        return self.__clinica

    @clinica.setter
    def clinica(self, clinica: Clinica) -> None:
        self.__clinica = clinica

    @property
    def paciente(self) -> Paciente:
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente: Paciente) -> None:
        self.__paciente = paciente

    @property
    def profissional(self) -> Profissional:
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional: Profissional) -> None:
        self.__profissional = profissional

    @property
    def data(self) -> date:
        return self.__data

    @data.setter
    def data(self, data: date) -> None:
        self.__data = data

    @property
    def horario(self) -> time:
        return self.__horario

    @horario.setter
    def horario(self, horario: time) -> None:
        self.__horario = horario

    @property
    def tipo_atendimento(self) -> TipoAtendimento:
        return self.__tipo_atendimento

    @tipo_atendimento.setter
    def tipo_atendimento(self, tipo_atendimento: TipoAtendimento) -> None:
        self.__tipo_atendimento = tipo_atendimento

    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, valor: float) -> None:
        self.__valor = valor

    @property
    def pagamento(self) -> Pagamento:
        return self.__pagamento

    @pagamento.setter
    def pagamento(self, pagamento: Pagamento) -> None:
        self.__pagamento = pagamento