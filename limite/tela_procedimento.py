from limite.tela_abstrata import TelaAbstrata


class TelaProcedimento(TelaAbstrata):
    def tela_opcoes(self) -> int:
        print("-------- PROCEDIMENTOS REALIZADOS ----------")
        print("Escolha a opcao")
        print("1 - Registrar Procedimento")
        print("2 - Alterar Procedimento")
        print("3 - Listar Procedimentos")
        print("4 - Excluir Procedimento")
        print("0 - Retornar")
        opcao = self.le_num_inteiro("Escolha a opcao: ", [0, 1, 2, 3, 4])
        return opcao

    def pega_dados_procedimento(self) -> dict:
        print("-------- DADOS PROCEDIMENTO ----------")
        descricao = self.le_texto("Descricao: ")
        custo = self.le_valor("Custo (R$): ")
        cpf_profissional = self.le_cpf("CPF do profissional responsavel: ")
        return {"descricao": descricao, "custo": custo,
                "cpf_profissional": cpf_profissional}

    def mostra_procedimento(self, dados_procedimento: dict) -> None:
        print("ATENDIMENTO {} / PROCEDIMENTO {}".format(
            dados_procedimento["codigo_atendimento"],
            dados_procedimento["codigo"]))
        print("DESCRICAO: ", dados_procedimento["descricao"])
        print("CUSTO: ", self.formata_valor(dados_procedimento["custo"]))
        print("PROFISSIONAL: ", dados_procedimento["profissional"])
        print("\n")

    def seleciona_atendimento(self) -> int:
        codigo = self.le_num_inteiro("Codigo do atendimento: ")
        return codigo

    def seleciona_procedimento(self) -> int:
        codigo = self.le_num_inteiro("Codigo do procedimento: ")
        return codigo
