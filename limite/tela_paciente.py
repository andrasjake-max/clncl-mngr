from limite.tela_abstrata import TelaAbstrata


class TelaPaciente(TelaAbstrata):
    def tela_opcoes(self) -> int:
        print("-------- PACIENTES ----------")
        print("Escolha a opcao")
        print("1 - Incluir Paciente")
        print("2 - Alterar Paciente")
        print("3 - Listar Pacientes")
        print("4 - Excluir Paciente")
        print("0 - Retornar")
        opcao = self.le_num_inteiro("Escolha a opcao: ", [0, 1, 2, 3, 4])
        return opcao

    def pega_dados_paciente(self) -> dict:
        print("-------- DADOS PACIENTE ----------")
        nome = self.le_texto("Nome: ")
        celular = self.le_digitos("Celular com DDD: ", (10, 11))
        cpf = self.le_cpf()
        data_nascimento = self.le_data("Data de nascimento")
        return {"nome": nome, "celular": celular, "cpf": cpf,
                "data_nascimento": data_nascimento}

    def pega_cpf_responsavel(self) -> str | None:
        print("Paciente menor de idade: informe o responsavel.")
        print("O responsavel precisa estar cadastrado como paciente.")
        if self.le_sim_nao("Deseja informar o responsavel agora?"):
            return self.le_cpf("CPF do responsavel: ")
        return None

    def mostra_paciente(self, dados_paciente: dict) -> None:
        print("NOME DO PACIENTE: ", dados_paciente["nome"])
        print("CPF DO PACIENTE: ", dados_paciente["cpf"])
        print("CELULAR DO PACIENTE: ", dados_paciente["celular"])
        print("NASCIMENTO: ",
              self.formata_data(dados_paciente["data_nascimento"]),
              "({} anos)".format(dados_paciente["idade"]))
        print("RESPONSAVEL: ", dados_paciente["responsavel"])
        print("\n")

    def seleciona_paciente(self) -> str:
        cpf = self.le_cpf("CPF do paciente que deseja selecionar: ")
        return cpf
