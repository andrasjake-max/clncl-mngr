from typing import TYPE_CHECKING
from limite.tela_tipo_atendimento import TelaTipoAtendimento
from entidade.tipo_atendimento import TipoAtendimento
from exceptions.sistema_exception import SistemaException
from exceptions.registro_repetido_exception import RegistroRepetidoException
from exceptions.registro_nao_encontrado_exception import \
    RegistroNaoEncontradoException
from exceptions.lista_vazia_exception import ListaVaziaException

if TYPE_CHECKING:
    from controle.controlador_sistema import ControladorSistema


class ControladorTiposAtendimento:

    def __init__(self, controlador_sistema: "ControladorSistema") -> None:
        self.__tipos = []
        self.__tela_tipo = TelaTipoAtendimento()
        self.__controlador_sistema = controlador_sistema
        self.__proximo_codigo = 1

    @property
    def tipos(self) -> list:
        return list(self.__tipos)

    def pega_tipo_por_codigo(self, codigo: int) -> TipoAtendimento | None:
        for tipo in self.__tipos:
            if tipo.codigo == codigo:
                return tipo
        return None

    def pega_tipo_por_nome(self, nome: str) -> TipoAtendimento | None:
        for tipo in self.__tipos:
            if tipo.nome.lower() == nome.strip().lower():
                return tipo
        return None

    def __seleciona_tipo(self) -> TipoAtendimento:
        if not self.__tipos:
            raise ListaVaziaException("tipo de atendimento")
        self.lista_tipos()
        codigo_tipo = self.__tela_tipo.seleciona_tipo()
        tipo = self.pega_tipo_por_codigo(codigo_tipo)
        if tipo is None:
            raise RegistroNaoEncontradoException("Tipo de atendimento",
                                                 codigo_tipo)
        return tipo

    def incluir_tipo(self) -> None:
        dados_tipo = self.__tela_tipo.pega_dados_tipo()
        try:
            if self.pega_tipo_por_nome(dados_tipo["nome"]) is not None:
                raise RegistroRepetidoException("Tipo de atendimento",
                                                dados_tipo["nome"])
            tipo = TipoAtendimento(self.__proximo_codigo, dados_tipo["nome"],
                                   dados_tipo["descricao"])
            self.__tipos.append(tipo)
            self.__proximo_codigo += 1
            self.__tela_tipo.mostra_mensagem(
                "Tipo cadastrado com codigo {}!".format(tipo.codigo))
        except SistemaException as e:
            self.__tela_tipo.mostra_mensagem("ATENCAO: {}".format(e))

    def alterar_tipo(self) -> None:
        try:
            tipo = self.__seleciona_tipo()
            novos_dados_tipo = self.__tela_tipo.pega_dados_tipo()
            outro = self.pega_tipo_por_nome(novos_dados_tipo["nome"])
            if outro is not None and outro is not tipo:
                raise RegistroRepetidoException("Tipo de atendimento",
                                                novos_dados_tipo["nome"])
            tipo.nome = novos_dados_tipo["nome"]
            tipo.descricao = novos_dados_tipo["descricao"]
            self.__tela_tipo.mostra_mensagem("Tipo alterado!")
        except SistemaException as e:
            self.__tela_tipo.mostra_mensagem("ATENCAO: {}".format(e))

    def lista_tipos(self) -> None:
        try:
            if not self.__tipos:
                raise ListaVaziaException("tipo de atendimento")
            for tipo in self.__tipos:
                self.__tela_tipo.mostra_tipo({
                    "codigo": tipo.codigo, "nome": tipo.nome,
                    "descricao": tipo.descricao})
        except ListaVaziaException as e:
            self.__tela_tipo.mostra_mensagem(e)

    def excluir_tipo(self) -> None:
        try:
            tipo = self.__seleciona_tipo()
            self.__tipos.remove(tipo)
            self.__tela_tipo.mostra_mensagem("Tipo excluido!")
        except SistemaException as e:
            self.__tela_tipo.mostra_mensagem("ATENCAO: {}".format(e))

    def retornar(self) -> None:
        self.__controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        lista_opcoes = {1: self.incluir_tipo, 2: self.alterar_tipo,
                        3: self.lista_tipos, 4: self.excluir_tipo,
                        0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__tela_tipo.tela_opcoes()]()
