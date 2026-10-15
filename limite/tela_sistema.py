from limite.tela_abstrata import TelaAbstrata


class TelaSistema(TelaAbstrata):
    def tela_opcoes(self) -> int:
        print("-------- SISTEMA DE CLINICAS ---------")
        print("Escolha sua opcao")
        print("1 - Pacientes")
        print("2 - Profissionais de saude")
        print("3 - Clinicas")
        print("4 - Tipos de atendimento")
        print("5 - Atendimentos")
        print("0 - Finalizar sistema")
        opcao = self.le_num_inteiro("Escolha a opcao: ", list(range(0, 6)))
        return opcao
