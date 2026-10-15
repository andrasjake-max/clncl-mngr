from typing import TYPE_CHECKING
from limite.tela_profissional import TelaProfissional
from entidade.profissional_saude import ProfissionalSaude
from exceptions.sistema_exception import SistemaException
from exceptions.registro_repetido_exception import RegistroRepetidoException
from exceptions.registro_nao_encontrado_exception import \
    RegistroNaoEncontradoException
from exceptions.lista_vazia_exception import ListaVaziaException
from exceptions.registro_em_uso_exception import RegistroEmUsoException

if TYPE_CHECKING:
    from controle.controlador_sistema import ControladorSistema


class ControladorProfissionais:

    def __init__(self, controlador_sistema: "ControladorSistema") -> None:
        self.__profissionais = []
        self.__tela_profissional = TelaProfissional()
        self.__controlador_sistema = controlador_sistema

    @property
    def profissionais(self) -> list:
        return list(self.__profissionais)

    def pega_profissional_por_cpf(self, cpf: str) -> ProfissionalSaude | None:
        for profissional in self.__profissionais:
            if profissional.cpf == cpf:
                return profissional
        return None

    def incluir_profissional(self) -> None:
        dados_profissional = self.__tela_profissional.pega_dados_profissional()
        try:
            cpf = dados_profissional["cpf"]
            if self.pega_profissional_por_cpf(cpf) is not None:
                raise RegistroRepetidoException("Profissional", cpf)
            profissional = ProfissionalSaude(
                dados_profissional["nome"], dados_profissional["celular"],
                cpf, dados_profissional["especialidade"],
                dados_profissional["registro_profissional"])
            self.__profissionais.append(profissional)
            self.__tela_profissional.mostra_mensagem(
                "Profissional cadastrado!")
        except SistemaException as e:
            self.__tela_profissional.mostra_mensagem("ATENCAO: {}".format(e))

    def alterar_profissional(self) -> None:
        try:
            if not self.__profissionais:
                raise ListaVaziaException("profissional")
            self.lista_profissionais()
            cpf_profissional = \
                self.__tela_profissional.seleciona_profissional()
            profissional = self.pega_profissional_por_cpf(cpf_profissional)
            if profissional is None:
                raise RegistroNaoEncontradoException("Profissional",
                                                     cpf_profissional)
            novos_dados = self.__tela_profissional.pega_dados_profissional()
            outro = self.pega_profissional_por_cpf(novos_dados["cpf"])
            if outro is not None and outro is not profissional:
                raise RegistroRepetidoException("Profissional",
                                                novos_dados["cpf"])
            profissional.nome = novos_dados["nome"]
            profissional.celular = novos_dados["celular"]
            profissional.cpf = novos_dados["cpf"]
            profissional.especialidade = novos_dados["especialidade"]
            profissional.registro_profissional = \
                novos_dados["registro_profissional"]
            self.__tela_profissional.mostra_mensagem("Profissional alterado!")
        except SistemaException as e:
            self.__tela_profissional.mostra_mensagem("ATENCAO: {}".format(e))

    def lista_profissionais(self) -> None:
        try:
            if not self.__profissionais:
                raise ListaVaziaException("profissional")
            for profissional in self.__profissionais:
                self.__tela_profissional.mostra_profissional({
                    "nome": profissional.nome, "cpf": profissional.cpf,
                    "celular": profissional.celular,
                    "especialidade": profissional.especialidade,
                    "registro_profissional":
                        profissional.registro_profissional})
        except ListaVaziaException as e:
            self.__tela_profissional.mostra_mensagem(e)

    def excluir_profissional(self) -> None:
        try:
            if not self.__profissionais:
                raise ListaVaziaException("profissional")
            self.lista_profissionais()
            cpf_profissional = \
                self.__tela_profissional.seleciona_profissional()
            profissional = self.pega_profissional_por_cpf(cpf_profissional)
            if profissional is None:
                raise RegistroNaoEncontradoException("Profissional",
                                                     cpf_profissional)
            atendimentos = self.__controlador_sistema.controlador_atendimentos
            if atendimentos.atendimentos_da_pessoa(profissional):
                raise RegistroEmUsoException(
                    "Profissional",
                    "possui atendimentos ou procedimentos registrados")
            clinicas = self.__controlador_sistema.controlador_clinicas
            for clinica in clinicas.clinicas:
                clinica.excluir_profissional(profissional)
            self.__profissionais.remove(profissional)
            self.__tela_profissional.mostra_mensagem("Profissional excluido!")
        except SistemaException as e:
            self.__tela_profissional.mostra_mensagem("ATENCAO: {}".format(e))

    def retornar(self) -> None:
        self.__controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        lista_opcoes = {1: self.incluir_profissional,
                        2: self.alterar_profissional,
                        3: self.lista_profissionais,
                        4: self.excluir_profissional,
                        0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__tela_profissional.tela_opcoes()]()
