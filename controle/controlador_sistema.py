from limite.tela_sistema import TelaSistema
from controle.controlador_pacientes import ControladorPacientes


class ControladorSistema:

    def __init__(self) -> None:
        self.__controlador_pacientes = ControladorPacientes(self)
        self.__tela_sistema = TelaSistema()

    @property
    def controlador_pacientes(self) -> ControladorPacientes:
        return self.__controlador_pacientes

    def inicializa_sistema(self) -> None:
        self.abre_tela()

    def cadastra_pacientes(self) -> None:
        self.__controlador_pacientes.abre_tela()

    def encerra_sistema(self) -> None:
        exit(0)

    def abre_tela(self) -> None:
        lista_opcoes = {1: self.cadastra_pacientes,
                        0: self.encerra_sistema}

        while True:
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()
