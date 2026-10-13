from view.abstractTela import AbstractTela
from control.controladorAtendimentos import ControladorAtendimentos

class TelaAtendimento(AbstractTela):
    def __init__(self, controlador: ControladorAtendimentos):
        self.__controlador = controlador
    