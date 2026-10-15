import unittest
from contextlib import ExitStack
from datetime import date, time
from typing import Callable
from unittest.mock import patch

from controle.controlador_sistema import ControladorSistema
from entidade.atendimento import Atendimento
from limite.tela_atendimento import TelaAtendimento
from limite.tela_clinica import TelaClinica
from limite.tela_paciente import TelaPaciente
from limite.tela_pagamento import TelaPagamento
from limite.tela_procedimento import TelaProcedimento
from limite.tela_profissional import TelaProfissional
from limite.tela_tipo_atendimento import TelaTipoAtendimento

DIA = date(2026, 11, 10)
CPF_ADULTO = "11111111111"
CPF_MENOR = "22222222222"
CPF_MENOR_ACOMPANHADO = "33333333333"
CPF_PROFISSIONAL = "55555555555"


class TestRegras(unittest.TestCase):
    def setUp(self) -> None:
        silencia_tela = patch("builtins.print")
        silencia_tela.start()
        self.addCleanup(silencia_tela.stop)
        self.sistema = ControladorSistema()
        self.executa(TelaClinica, self.sistema.controlador_clinicas
                     .incluir_clinica, pega_dados_clinica={
                         "nome": "Clinica Centro", "cidade": "Florianopolis",
                         "descricao": "", "horario_abertura": time(8, 0),
                         "horario_fechamento": time(18, 0)})
        self.executa(TelaProfissional, self.sistema.controlador_profissionais
                     .incluir_profissional, pega_dados_profissional={
                         "nome": "Dra. Ana", "celular": "48999990000",
                         "cpf": CPF_PROFISSIONAL,
                         "especialidade": "Clinica geral",
                         "registro_profissional": "CRM 123"})
        self.executa(TelaClinica, self.sistema.controlador_clinicas
                     .vincular_profissional, seleciona_clinica=1,
                     seleciona_profissional=CPF_PROFISSIONAL)
        self.cadastra_paciente("Adulto", CPF_ADULTO, date(1990, 5, 20))
        self.cadastra_paciente("Menor", CPF_MENOR, date(2015, 3, 1))
        self.cadastra_paciente("Menor Acompanhado", CPF_MENOR_ACOMPANHADO,
                               date(2015, 3, 1), CPF_ADULTO)
        self.executa(TelaTipoAtendimento, self.sistema
                     .controlador_tipos_atendimento.incluir_tipo,
                     pega_dados_tipo={"nome": "Consulta", "descricao": ""})

    def executa(self, tela: type, acao: Callable[[], None],
                **respostas: object) -> list:
        with ExitStack() as pilha:
            for metodo, resposta in respostas.items():
                pilha.enter_context(
                    patch.object(tela, metodo, return_value=resposta))
            mensagens = pilha.enter_context(
                patch.object(tela, "mostra_mensagem"))
            acao()
        return [str(c.args[0]) for c in mensagens.call_args_list]

    def cadastra_paciente(self, nome: str, cpf: str, nascimento: date,
                          cpf_responsavel: str | None = None) -> None:
        self.executa(TelaPaciente, self.sistema.controlador_pacientes
                     .incluir_paciente, pega_dados_paciente={
                         "nome": nome, "celular": "48911110000", "cpf": cpf,
                         "data_nascimento": nascimento},
                     pega_cpf_responsavel=cpf_responsavel)

    def agenda(self, cpf_paciente: str = CPF_ADULTO,
               inicio: time = time(10, 0), fim: time = time(10, 30),
               valor: float = 100.0) -> list:
        return self.executa(TelaAtendimento, self.sistema
                            .controlador_atendimentos.incluir_atendimento,
                            pega_dados_atendimento={
                                "codigo_clinica": 1,
                                "cpf_paciente": cpf_paciente,
                                "cpf_profissional": CPF_PROFISSIONAL,
                                "codigo_tipo": 1, "data": DIA,
                                "hora_inicio": inicio, "hora_fim": fim,
                                "valor": valor})

    def paga(self, valor: float, data: date = DIA,
             **modalidade: str) -> list:
        dados_pagamento = {"codigo_atendimento": 1, "data": data,
                           "valor_pago": valor, "modalidade": "dinheiro"}
        dados_pagamento.update(modalidade)
        return self.executa(TelaPagamento, self.sistema
                            .controlador_pagamentos.incluir_pagamento,
                            pega_dados_pagamento=dados_pagamento)

    def atendimentos(self) -> list:
        return self.sistema.controlador_atendimentos.atendimentos

    def atendimento(self) -> Atendimento:
        return self.atendimentos()[0]

    def restante(self) -> float:
        return self.sistema.controlador_pagamentos.valor_restante(
            self.atendimento())

    def test_menor_sem_responsavel_nao_e_atendido(self) -> None:
        mensagens = self.agenda(cpf_paciente=CPF_MENOR)
        self.assertIn("nao possui responsavel", mensagens[-1])
        self.assertEqual(len(self.atendimentos()), 0)

    def test_menor_com_responsavel_maior_e_atendido(self) -> None:
        self.agenda(cpf_paciente=CPF_MENOR_ACOMPANHADO)
        self.assertEqual(len(self.atendimentos()), 1)

    def test_atendimento_dentro_do_horario(self) -> None:
        self.agenda(inicio=time(8, 0), fim=time(8, 30))
        self.assertEqual(len(self.atendimentos()), 1)

    def test_atendimento_comeca_antes_da_abertura(self) -> None:
        mensagens = self.agenda(inicio=time(7, 30), fim=time(8, 30))
        self.assertIn("Horario invalido", mensagens[-1])
        self.assertEqual(len(self.atendimentos()), 0)

    def test_atendimento_termina_depois_do_fechamento(self) -> None:
        mensagens = self.agenda(inicio=time(17, 45), fim=time(18, 15))
        self.assertIn("Horario invalido", mensagens[-1])
        self.assertEqual(len(self.atendimentos()), 0)

    def test_pagamento_no_dia_do_atendimento(self) -> None:
        self.agenda()
        self.paga(100.0)
        self.assertEqual(self.restante(), 0.0)

    def test_pagamento_depois_do_atendimento(self) -> None:
        self.agenda()
        mensagens = self.paga(100.0, data=date(2026, 11, 11))
        self.assertIn("ate a data do atendimento", mensagens[-1])
        self.assertEqual(self.restante(), 100.0)

    def test_pagamentos_parciais_calculam_restante(self) -> None:
        self.agenda(valor=100.0)
        self.paga(30.0)
        self.assertEqual(self.restante(), 70.0)
        self.paga(50.0, modalidade="pix", cpf_pagador=CPF_ADULTO)
        self.assertEqual(self.restante(), 20.0)
        self.paga(20.0, modalidade="cartao",
                  numero_cartao="4111111111111111", bandeira="Visa")
        self.assertEqual(self.restante(), 0.0)

    def test_pagamento_maior_que_o_restante(self) -> None:
        self.agenda(valor=100.0)
        self.paga(80.0)
        mensagens = self.paga(30.0)
        self.assertIn("excede o restante", mensagens[-1])
        self.assertEqual(self.restante(), 20.0)

    def test_restante_inclui_procedimentos(self) -> None:
        self.agenda(valor=100.0)
        self.executa(TelaProcedimento, self.sistema.controlador_procedimentos
                     .incluir_procedimento, seleciona_atendimento=1,
                     pega_dados_procedimento={
                         "descricao": "Raio-X", "custo": 50.0,
                         "cpf_profissional": CPF_PROFISSIONAL})
        self.assertEqual(self.restante(), 150.0)


if __name__ == "__main__":
    unittest.main()
