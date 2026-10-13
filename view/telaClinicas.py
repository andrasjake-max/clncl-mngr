from view.abstractTela import AbstractTela
from control.controladorClinicas import ControladorClinicas

class TelaClinicas(AbstractTela):
    def __init__(self, controlador: ControladorClinicas):
        self.__controlador = controlador

    def mostra_menu(self) -> None:
        print("\n=== Menu de Clínicas ===")
        print("1 - Gerenciar clínicas")
        print("2 - Relatórios")

    def mostra_menu_clinicas(self) -> None:
        print("\n=== Gerenciar Clínicas ===")
        print("1 - Listar clínicas")
        print("2 - Cadastrar clínica")
        print("3 - Excluir clínica")
        print("0 - Voltar")

    def mostra_menu_relatorios(self) -> None:
        print("\n=== Relatórios ===")
        print("1 - Listar os 10 atendimentos mais caros (com clínica)")
        print("2 - Listar os 10 atendimentos mais baratos (com clínica)")
        print("3 - Listar procedimentos mais populares")
        print("4 - Listar procedimentos mais caros (com clínica)")
        print("5 - Listar procedimentos mais baratos (com clínica)")
        print("0 - Voltar")

    def le_opcao(self) -> None:
        self.__opcao = input("Escolha uma opção: ").strip()