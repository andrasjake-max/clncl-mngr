from typing import TYPE_CHECKING
from limite.tela_procedimento import TelaProcedimento
from entidade.atendimento import Atendimento
from entidade.profissional_saude import ProfissionalSaude
from exceptions.sistema_exception import SistemaException
from exceptions.registro_nao_encontrado_exception import \
    RegistroNaoEncontradoException
from exceptions.lista_vazia_exception import ListaVaziaException
from exceptions.profissional_nao_vinculado_exception import \
    ProfissionalNaoVinculadoException

if TYPE_CHECKING:
    from controle.controlador_sistema import ControladorSistema


class ControladorProcedimentos:

    def __init__(self, controlador_sistema: "ControladorSistema") -> None:
        self.__tela_procedimento = TelaProcedimento()
        self.__controlador_sistema = controlador_sistema

    def todos_procedimentos(self) -> list:
        atendimentos = self.__controlador_sistema.controlador_atendimentos
        return [(a, p) for a in atendimentos.atendimentos
                for p in a.procedimentos]

    def __seleciona_atendimento(self) -> Atendimento:
        atendimentos = self.__controlador_sistema.controlador_atendimentos
        if not atendimentos.atendimentos:
            raise ListaVaziaException("atendimento")
        atendimentos.lista_atendimentos()
        codigo = self.__tela_procedimento.seleciona_atendimento()
        atendimento = atendimentos.pega_atendimento_por_codigo(codigo)
        if atendimento is None:
            raise RegistroNaoEncontradoException("Atendimento", codigo)
        return atendimento

    def __seleciona_procedimento(self) -> tuple:
        if not self.todos_procedimentos():
            raise ListaVaziaException("procedimento")
        self.lista_procedimentos()
        atendimentos = self.__controlador_sistema.controlador_atendimentos
        codigo_atendimento = self.__tela_procedimento.seleciona_atendimento()
        atendimento = atendimentos.pega_atendimento_por_codigo(
            codigo_atendimento)
        if atendimento is None:
            raise RegistroNaoEncontradoException("Atendimento",
                                                 codigo_atendimento)
        codigo = self.__tela_procedimento.seleciona_procedimento()
        procedimento = atendimento.pega_procedimento_por_codigo(codigo)
        if procedimento is None:
            raise RegistroNaoEncontradoException("Procedimento", codigo)
        return atendimento, procedimento

    def __pega_profissional(self, atendimento: Atendimento,
                            cpf: str) -> ProfissionalSaude:
        profissionais = self.__controlador_sistema.controlador_profissionais
        profissional = profissionais.pega_profissional_por_cpf(cpf)
        if profissional is None:
            raise RegistroNaoEncontradoException("Profissional", cpf)
        if not atendimento.clinica.possui_profissional(profissional):
            raise ProfissionalNaoVinculadoException(profissional.nome,
                                                    atendimento.clinica.nome)
        return profissional

    def incluir_procedimento(self) -> None:
        try:
            atendimento = self.__seleciona_atendimento()
            dados_procedimento = \
                self.__tela_procedimento.pega_dados_procedimento()
            profissional = self.__pega_profissional(
                atendimento, dados_procedimento["cpf_profissional"])
            procedimento = atendimento.incluir_procedimento(
                dados_procedimento["descricao"], dados_procedimento["custo"],
                profissional)
            self.__tela_procedimento.mostra_mensagem(
                "Procedimento {} registrado no atendimento {}!".format(
                    procedimento.codigo, atendimento.codigo))
        except SistemaException as e:
            self.__tela_procedimento.mostra_mensagem("ATENCAO: {}".format(e))

    def alterar_procedimento(self) -> None:
        try:
            atendimento, procedimento = self.__seleciona_procedimento()
            novos_dados = self.__tela_procedimento.pega_dados_procedimento()
            profissional = self.__pega_profissional(
                atendimento, novos_dados["cpf_profissional"])
            procedimento.descricao = novos_dados["descricao"]
            procedimento.custo = novos_dados["custo"]
            procedimento.profissional = profissional
            self.__tela_procedimento.mostra_mensagem("Procedimento alterado!")
        except SistemaException as e:
            self.__tela_procedimento.mostra_mensagem("ATENCAO: {}".format(e))

    def lista_procedimentos(self) -> None:
        try:
            todos = self.todos_procedimentos()
            if not todos:
                raise ListaVaziaException("procedimento")
            for atendimento, procedimento in todos:
                self.__tela_procedimento.mostra_procedimento({
                    "codigo_atendimento": atendimento.codigo,
                    "codigo": procedimento.codigo,
                    "descricao": procedimento.descricao,
                    "custo": procedimento.custo,
                    "profissional": procedimento.profissional.nome})
        except ListaVaziaException as e:
            self.__tela_procedimento.mostra_mensagem(e)

    def excluir_procedimento(self) -> None:
        try:
            atendimento, procedimento = self.__seleciona_procedimento()
            atendimento.excluir_procedimento(procedimento)
            self.__tela_procedimento.mostra_mensagem("Procedimento excluido!")
        except SistemaException as e:
            self.__tela_procedimento.mostra_mensagem("ATENCAO: {}".format(e))

    def retornar(self) -> None:
        self.__controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        lista_opcoes = {1: self.incluir_procedimento,
                        2: self.alterar_procedimento,
                        3: self.lista_procedimentos,
                        4: self.excluir_procedimento,
                        0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__tela_procedimento.tela_opcoes()]()
