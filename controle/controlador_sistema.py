from limite.tela_sistema import TelaSistema
from controle.controlador_pacientes import ControladorPacientes
from controle.controlador_profissionais import ControladorProfissionais
from controle.controlador_clinicas import ControladorClinicas
from controle.controlador_tipos_atendimento import \
    ControladorTiposAtendimento
from controle.controlador_atendimentos import ControladorAtendimentos
from controle.controlador_procedimentos import ControladorProcedimentos
from controle.controlador_pagamentos import ControladorPagamentos


class ControladorSistema:

    def __init__(self) -> None:
        self.__controlador_pacientes = ControladorPacientes(self)
        self.__controlador_profissionais = ControladorProfissionais(self)
        self.__controlador_clinicas = ControladorClinicas(self)
        self.__controlador_tipos_atendimento = \
            ControladorTiposAtendimento(self)
        self.__controlador_atendimentos = ControladorAtendimentos(self)
        self.__controlador_procedimentos = ControladorProcedimentos(self)
        self.__controlador_pagamentos = ControladorPagamentos(self)
        self.__tela_sistema = TelaSistema()

    @property
    def controlador_pacientes(self) -> ControladorPacientes:
        return self.__controlador_pacientes

    @property
    def controlador_profissionais(self) -> ControladorProfissionais:
        return self.__controlador_profissionais

    @property
    def controlador_clinicas(self) -> ControladorClinicas:
        return self.__controlador_clinicas

    @property
    def controlador_tipos_atendimento(self) -> ControladorTiposAtendimento:
        return self.__controlador_tipos_atendimento

    @property
    def controlador_atendimentos(self) -> ControladorAtendimentos:
        return self.__controlador_atendimentos

    @property
    def controlador_procedimentos(self) -> ControladorProcedimentos:
        return self.__controlador_procedimentos

    @property
    def controlador_pagamentos(self) -> ControladorPagamentos:
        return self.__controlador_pagamentos

    def inicializa_sistema(self) -> None:
        self.abre_tela()

    def cadastra_pacientes(self) -> None:
        self.__controlador_pacientes.abre_tela()

    def cadastra_profissionais(self) -> None:
        self.__controlador_profissionais.abre_tela()

    def cadastra_clinicas(self) -> None:
        self.__controlador_clinicas.abre_tela()

    def cadastra_tipos_atendimento(self) -> None:
        self.__controlador_tipos_atendimento.abre_tela()

    def registra_atendimentos(self) -> None:
        self.__controlador_atendimentos.abre_tela()

    def registra_procedimentos(self) -> None:
        self.__controlador_procedimentos.abre_tela()

    def registra_pagamentos(self) -> None:
        self.__controlador_pagamentos.abre_tela()

    def encerra_sistema(self) -> None:
        exit(0)

    def abre_tela(self) -> None:
        lista_opcoes = {1: self.cadastra_pacientes,
                        2: self.cadastra_profissionais,
                        3: self.cadastra_clinicas,
                        4: self.cadastra_tipos_atendimento,
                        5: self.registra_atendimentos,
                        6: self.registra_procedimentos,
                        7: self.registra_pagamentos,
                        0: self.encerra_sistema}

        while True:
            opcao_escolhida = self.__tela_sistema.tela_opcoes()
            funcao_escolhida = lista_opcoes[opcao_escolhida]
            funcao_escolhida()
