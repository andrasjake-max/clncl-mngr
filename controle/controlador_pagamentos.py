from typing import TYPE_CHECKING
from limite.tela_pagamento import TelaPagamento
from entidade.atendimento import Atendimento
from entidade.pagamento import Pagamento
from entidade.pagamento_dinheiro import PagamentoDinheiro
from entidade.pagamento_pix import PagamentoPix
from entidade.pagamento_cartao import PagamentoCartao, BANDEIRAS
from exceptions.sistema_exception import SistemaException
from exceptions.dado_invalido_exception import DadoInvalidoException
from exceptions.registro_nao_encontrado_exception import \
    RegistroNaoEncontradoException
from exceptions.lista_vazia_exception import ListaVaziaException
from exceptions.pagamento_invalido_exception import \
    PagamentoInvalidoException

if TYPE_CHECKING:
    from controle.controlador_sistema import ControladorSistema


class ControladorPagamentos:

    def __init__(self, controlador_sistema: "ControladorSistema") -> None:
        self.__pagamentos = []
        self.__tela_pagamento = TelaPagamento()
        self.__controlador_sistema = controlador_sistema
        self.__proximo_codigo = 1

    @property
    def pagamentos(self) -> list[Pagamento]:
        return list(self.__pagamentos)

    def pega_pagamento_por_codigo(self, codigo: int) -> Pagamento | None:
        for pagamento in self.__pagamentos:
            if pagamento.codigo == codigo:
                return pagamento
        return None

    def pagamentos_do_atendimento(
            self, atendimento: Atendimento) -> list[Pagamento]:
        return [p for p in self.__pagamentos if p.atendimento is atendimento]

    def total_pago(self, atendimento: Atendimento,
                   ignorar: Pagamento | None = None) -> float:
        return sum(p.valor_pago for p in self.__pagamentos
                   if p.atendimento is atendimento and p is not ignorar)

    def valor_restante(self, atendimento: Atendimento,
                       ignorar: Pagamento | None = None) -> float:
        return round(atendimento.valor_total()
                     - self.total_pago(atendimento, ignorar), 2)

    def __seleciona_pagamento(self) -> Pagamento:
        if not self.__pagamentos:
            raise ListaVaziaException("pagamento")
        self.lista_pagamentos()
        codigo = self.__tela_pagamento.seleciona_pagamento()
        pagamento = self.pega_pagamento_por_codigo(codigo)
        if pagamento is None:
            raise RegistroNaoEncontradoException("Pagamento", codigo)
        return pagamento

    def __pega_atendimento(self, codigo: int) -> Atendimento:
        atendimento = self.__controlador_sistema.controlador_atendimentos \
            .pega_atendimento_por_codigo(codigo)
        if atendimento is None:
            raise RegistroNaoEncontradoException("Atendimento", codigo)
        return atendimento

    def __cria_pagamento(self, codigo: int, atendimento: Atendimento,
                         dados_pagamento: dict) -> Pagamento:
        modalidade = dados_pagamento["modalidade"]
        if modalidade == "dinheiro":
            return PagamentoDinheiro(codigo, dados_pagamento["data"],
                                     atendimento,
                                     dados_pagamento["valor_pago"])
        if modalidade == "pix":
            return PagamentoPix(codigo, dados_pagamento["data"], atendimento,
                                dados_pagamento["valor_pago"],
                                dados_pagamento["cpf_pagador"])
        if modalidade == "cartao":
            return PagamentoCartao(codigo, dados_pagamento["data"],
                                   atendimento, dados_pagamento["valor_pago"],
                                   dados_pagamento["numero_cartao"],
                                   dados_pagamento["bandeira"])
        raise DadoInvalidoException("modalidade", "modalidade desconhecida")

    def __valida_regras(self, atendimento: Atendimento,
                        dados_pagamento: dict,
                        ignorar: Pagamento | None = None) -> None:
        if dados_pagamento["data"] > atendimento.data:
            raise PagamentoInvalidoException(
                "deve ser feito ate a data do atendimento ({})".format(
                    atendimento.data.strftime("%d/%m/%Y")))
        restante = self.valor_restante(atendimento, ignorar)
        if restante <= 0:
            raise PagamentoInvalidoException("o atendimento ja esta quitado")
        if dados_pagamento["valor_pago"] > restante:
            raise PagamentoInvalidoException(
                "o valor excede o restante de R$ {:.2f}".format(restante))

    def incluir_pagamento(self) -> None:
        try:
            atendimentos = self.__controlador_sistema.controlador_atendimentos
            if not atendimentos.atendimentos:
                raise ListaVaziaException("atendimento")
            atendimentos.lista_atendimentos()
            dados_pagamento = self.__tela_pagamento.pega_dados_pagamento(
                BANDEIRAS)
            atendimento = self.__pega_atendimento(
                dados_pagamento["codigo_atendimento"])
            self.__valida_regras(atendimento, dados_pagamento)
            pagamento = self.__cria_pagamento(self.__proximo_codigo,
                                              atendimento, dados_pagamento)
            self.__pagamentos.append(pagamento)
            self.__proximo_codigo += 1
            self.__tela_pagamento.mostra_mensagem(
                "Pagamento {} registrado! Restante: R$ {:.2f}".format(
                    pagamento.codigo, self.valor_restante(atendimento)))
        except SistemaException as e:
            self.__tela_pagamento.mostra_mensagem("ATENCAO: {}".format(e))

    def alterar_pagamento(self) -> None:
        try:
            pagamento = self.__seleciona_pagamento()
            novos_dados = self.__tela_pagamento.pega_dados_pagamento(
                BANDEIRAS)
            atendimento = self.__pega_atendimento(
                novos_dados["codigo_atendimento"])
            self.__valida_regras(atendimento, novos_dados, ignorar=pagamento)
            novo_pagamento = self.__cria_pagamento(pagamento.codigo,
                                                   atendimento, novos_dados)
            indice = self.__pagamentos.index(pagamento)
            self.__pagamentos[indice] = novo_pagamento
            self.__tela_pagamento.mostra_mensagem("Pagamento alterado!")
        except SistemaException as e:
            self.__tela_pagamento.mostra_mensagem("ATENCAO: {}".format(e))

    def lista_pagamentos(self) -> None:
        try:
            if not self.__pagamentos:
                raise ListaVaziaException("pagamento")
            for pagamento in self.__pagamentos:
                self.__tela_pagamento.mostra_pagamento({
                    "codigo": pagamento.codigo, "data": pagamento.data,
                    "atendimento": "{} ({})".format(
                        pagamento.atendimento.codigo,
                        pagamento.atendimento.tipo.nome),
                    "paciente": pagamento.paciente.nome,
                    "valor_pago": pagamento.valor_pago,
                    "modalidade": pagamento.modalidade(),
                    "detalhes": pagamento.detalhes(),
                    "valor_restante":
                        self.valor_restante(pagamento.atendimento)})
        except ListaVaziaException as e:
            self.__tela_pagamento.mostra_mensagem(e)

    def excluir_pagamento(self) -> None:
        try:
            pagamento = self.__seleciona_pagamento()
            self.__pagamentos.remove(pagamento)
            self.__tela_pagamento.mostra_mensagem("Pagamento excluido!")
        except SistemaException as e:
            self.__tela_pagamento.mostra_mensagem("ATENCAO: {}".format(e))

    def retornar(self) -> None:
        self.__controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        lista_opcoes = {1: self.incluir_pagamento, 2: self.alterar_pagamento,
                        3: self.lista_pagamentos, 4: self.excluir_pagamento,
                        0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__tela_pagamento.tela_opcoes()]()
