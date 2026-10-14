from limite.tela_abstrata import TelaAbstrata


class TelaProfissional(TelaAbstrata):
    def tela_opcoes(self) -> int:
        print("-------- PROFISSIONAIS DE SAUDE ----------")
        print("Escolha a opcao")
        print("1 - Incluir Profissional")
        print("2 - Alterar Profissional")
        print("3 - Listar Profissionais")
        print("4 - Excluir Profissional")
        print("0 - Retornar")
        opcao = self.le_num_inteiro("Escolha a opcao: ", [0, 1, 2, 3, 4])
        return opcao

    def pega_dados_profissional(self) -> dict:
        print("-------- DADOS PROFISSIONAL ----------")
        nome = self.le_texto("Nome: ")
        celular = self.le_digitos("Celular com DDD: ", (10, 11))
        cpf = self.le_cpf()
        especialidade = self.le_texto("Especialidade: ")
        registro = self.le_texto("Registro profissional (ex.: CRM 1234/SC): ")
        return {"nome": nome, "celular": celular, "cpf": cpf,
                "especialidade": especialidade,
                "registro_profissional": registro}

    def mostra_profissional(self, dados_profissional: dict) -> None:
        print("NOME DO PROFISSIONAL: ", dados_profissional["nome"])
        print("CPF DO PROFISSIONAL: ", dados_profissional["cpf"])
        print("CELULAR DO PROFISSIONAL: ", dados_profissional["celular"])
        print("ESPECIALIDADE: ", dados_profissional["especialidade"])
        print("REGISTRO: ", dados_profissional["registro_profissional"])
        print("\n")

    def seleciona_profissional(self) -> str:
        cpf = self.le_cpf("CPF do profissional que deseja selecionar: ")
        return cpf
