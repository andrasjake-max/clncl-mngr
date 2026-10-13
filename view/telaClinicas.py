from view.abstractTela import AbstractTela
from control.controladorClinicas import ControladorClinicas

class TelaClinicas(AbstractTela):
    def __init__(self, controlador: ControladorClinicas):
        self.__controlador = controlador

    def mostra_menu(self) -> None:
        print("\n=== Menu de Clínicas ===")
        print("1 - Gerenciar clínicas")
        print("2 - Relatórios")
        print("3 - Atendimentos")

    def mostra_menu_clinicas(self) -> None:
        print("\n=== Gerenciar Clínicas ===")
        print("1 - Listar clínicas")
        print("2 - Cadastrar clínica")
        print("3 - Excluir clínica")
        print("4 - Gerenciar clínica")
        print("0 - Voltar")

    def mostra_menu_gerenciar(self) -> None:
        print("\n=== Gerenciar Clínica ===")
        print("1 - Cadastrar profissional")
        print("2 - Remover profissional")
        print("3 - Listar profissionais")
        print("4 - Mudar descrição")
        print("5 - Mostrar descrição")
        print("6 - Mudar localização")
        print("7 - Mostrar localização")
        print("0 - Voltar")

    def mostra_menu_relatorios(self) -> None:
        print("\n=== Relatórios ===")
        print("1 - Listar atendimentos mais caros")
        print("2 - Listar atendimentos mais baratos")
        print("3 - Listar procedimentos mais populares")
        print("4 - Listar procedimentos mais caros (com clínica)")
        print("5 - Listar procedimentos mais baratos (com clínica)")
        print("0 - Voltar")

    def le_opcao(self) -> None:
        self.__opcao = input("Escolha uma opção: ").strip()