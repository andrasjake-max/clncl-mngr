from limite.tela_sistema import TelaSistema
from controle.controlador_pacientes import ControladorPacientes
from controle.controlador_profissionais import ControladorProfissionais


class ControladorSistema:

    def __init__(self) -> None:
        self.__controlador_pacientes = ControladorPacientes(self)
        self.__controlador_profissionais = ControladorProfissionais(self)
        self.__tela_sistema = TelaSistema()

    @property
    def controlador_pacientes(self) -> ControladorPacientes:
        return self.__controlador_pacientes

    @property
    def controlador_profissionais(self) -> ControladorProfissionais:
        return self.__controlador_profissionais

    def inicializa_sistema(self) -> None:
        self.abre_tela()

    def cadastra_pacientes(self) -> None:
        self.__controlador_pacientes.abre_tela()

    def cadastra_profissionais(self) -> None:
        self.__controlador_profissionais.abre_tela()

    def encerra_sistema(self) -> None:
        exit(0)

    def abre_tela(self) -> None:
        lista_opcoes = {1: self.cadastra_pacientes,
                        2: self.cadastra_profissionais,
                        0: self.encerra_sistema}

        while True:
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()
