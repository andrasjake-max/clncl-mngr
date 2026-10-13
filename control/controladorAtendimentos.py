
from datetime import date, time

from model.atendimento import Atendimento
from model.clinica import Clinica
from model.pagamento import Pagamento
from model.paciente import Paciente
from model.profissional import Profissional
from model.tipoAtendimento import TipoAtendimento


class ControladorAtendimentos:
    def __init__(self, clinica: Clinica) -> None:
        self.__clinica = clinica
        self.__tipos_atendimento: list[TipoAtendimento] = []

    def inclui_tipo(self, nome: str, descricao: str, codigo: int) -> None:
        tipo = TipoAtendimento(nome, descricao, codigo)
        self.__tipos_atendimento.append(tipo)

    def inclui_atendimento(
        self,
        paciente: Paciente,
        profissional: Profissional,
        data: date,
        horario: time,
        tipo: TipoAtendimento,
        valor: float,
        pagamento: Pagamento,
    ) -> None:
        atendimento = Atendimento(
            self.__clinica,
            paciente,
            profissional,
            data,
            horario,
            tipo,
            valor,
            pagamento,
        )
        self.__clinica.adiciona_atendimento(atendimento)

    def verifica_pagamento(self, atendimento: Atendimento) -> float:
        pagamento = atendimento.pagamento
        return max(0.0, pagamento.valor - pagamento.valor_pago)

    def realiza_pagamento(self, atendimento: Atendimento) -> None:
        pagamento = atendimento.pagamento
        saldo = self.verifica_pagamento(atendimento)
        parcelas_restantes = pagamento.parcelas_restantes

        if saldo == 0 or parcelas_restantes == 0:
            return

        valor_parcela = saldo if parcelas_restantes == 1 else saldo / parcelas_restantes
        pagamento.efetuar_pagamento(valor_parcela)
        pagamento.reduzir_parcelas(1)