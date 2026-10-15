from datetime import date, time
from entidade.clinica import Clinica
from entidade.paciente import Paciente
from entidade.profissional_saude import ProfissionalSaude
from entidade.tipo_atendimento import TipoAtendimento
from entidade.procedimento import Procedimento
from exceptions.dado_invalido_exception import DadoInvalidoException
from exceptions.horario_invalido_exception import HorarioInvalidoException


class Atendimento:
    def __init__(self, codigo: int, clinica: Clinica, paciente: Paciente,
                 profissional: ProfissionalSaude, tipo: TipoAtendimento,
                 data: date, hora_inicio: time, hora_fim: time,
                 valor: float) -> None:
        self.__codigo = codigo
        self.__clinica = None
        self.__paciente = None
        self.__profissional = None
        self.__tipo = None
        self.__data = None
        self.__hora_inicio = None
        self.__hora_fim = None
        self.__valor = None
        self.__procedimentos = []
        self.__proximo_codigo_procedimento = 1
        self.clinica = clinica
        self.paciente = paciente
        self.profissional = profissional
        self.tipo = tipo
        self.define_horario(data, hora_inicio, hora_fim)
        self.valor = valor

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def clinica(self) -> Clinica:
        return self.__clinica

    @clinica.setter
    def clinica(self, clinica: Clinica) -> None:
        if not isinstance(clinica, Clinica):
            raise DadoInvalidoException("clinica")
        self.__clinica = clinica

    @property
    def paciente(self) -> Paciente:
        return self.__paciente

    @paciente.setter
    def paciente(self, paciente: Paciente) -> None:
        if not isinstance(paciente, Paciente):
            raise DadoInvalidoException("paciente")
        self.__paciente = paciente

    @property
    def profissional(self) -> ProfissionalSaude:
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional: ProfissionalSaude) -> None:
        if not isinstance(profissional, ProfissionalSaude):
            raise DadoInvalidoException("profissional")
        self.__profissional = profissional

    @property
    def tipo(self) -> TipoAtendimento:
        return self.__tipo

    @tipo.setter
    def tipo(self, tipo: TipoAtendimento) -> None:
        if not isinstance(tipo, TipoAtendimento):
            raise DadoInvalidoException("tipo de atendimento")
        self.__tipo = tipo

    @property
    def data(self) -> date:
        return self.__data

    @property
    def hora_inicio(self) -> time:
        return self.__hora_inicio

    @property
    def hora_fim(self) -> time:
        return self.__hora_fim

    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, valor: float) -> None:
        if not isinstance(valor, (int, float)) or valor < 0:
            raise DadoInvalidoException("valor",
                                        "deve ser um numero nao negativo")
        self.__valor = float(valor)

    @property
    def procedimentos(self) -> list[Procedimento]:
        return list(self.__procedimentos)

    def define_horario(self, data: date, inicio: time, fim: time) -> None:
        if not isinstance(data, date):
            raise DadoInvalidoException("data")
        if not isinstance(inicio, time) or not isinstance(fim, time):
            raise DadoInvalidoException("horario")
        if inicio >= fim:
            raise HorarioInvalidoException("inicio deve ser antes do fim")
        self.__data = data
        self.__hora_inicio = inicio
        self.__hora_fim = fim

    def conflita_com(self, data: date, inicio: time, fim: time) -> bool:
        return (self.__data == data
                and inicio < self.__hora_fim and self.__hora_inicio < fim)

    def valor_total(self) -> float:
        return self.__valor + sum(p.custo for p in self.__procedimentos)

    def incluir_procedimento(self, descricao: str, custo: float,
                             profissional: ProfissionalSaude) -> Procedimento:
        procedimento = Procedimento(self.__proximo_codigo_procedimento,
                                    descricao, custo, profissional)
        self.__procedimentos.append(procedimento)
        self.__proximo_codigo_procedimento += 1
        return procedimento

    def pega_procedimento_por_codigo(self, codigo: int) -> Procedimento | None:
        for procedimento in self.__procedimentos:
            if procedimento.codigo == codigo:
                return procedimento
        return None

    def excluir_procedimento(self, procedimento: Procedimento) -> None:
        if procedimento in self.__procedimentos:
            self.__procedimentos.remove(procedimento)
