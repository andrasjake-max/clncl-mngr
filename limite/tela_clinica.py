from limite.tela_abstrata import TelaAbstrata


class TelaClinica(TelaAbstrata):
    def tela_opcoes(self) -> int:
        print("-------- CLINICAS ----------")
        print("Escolha a opcao")
        print("1 - Incluir Clinica")
        print("2 - Alterar Clinica")
        print("3 - Listar Clinicas")
        print("4 - Excluir Clinica")
        print("5 - Vincular Profissional a Clinica")
        print("6 - Desvincular Profissional da Clinica")
        print("0 - Retornar")
        opcao = self.le_num_inteiro("Escolha a opcao: ",
                                    [0, 1, 2, 3, 4, 5, 6])
        return opcao

    def pega_dados_clinica(self) -> dict:
        print("-------- DADOS CLINICA ----------")
        nome = self.le_texto("Nome: ")
        cidade = self.le_texto("Cidade: ")
        descricao = self.le_texto("Descricao: ", obrigatorio=False)
        abertura = self.le_hora("Horario de abertura")
        fechamento = self.le_hora("Horario de fechamento")
        return {"nome": nome, "cidade": cidade, "descricao": descricao,
                "horario_abertura": abertura,
                "horario_fechamento": fechamento}

    def mostra_clinica(self, dados_clinica: dict) -> None:
        print("CODIGO DA CLINICA: ", dados_clinica["codigo"])
        print("NOME DA CLINICA: ", dados_clinica["nome"])
        print("CIDADE: ", dados_clinica["cidade"])
        print("DESCRICAO: ", dados_clinica["descricao"])
        print("FUNCIONAMENTO: {} as {}".format(
            self.formata_hora(dados_clinica["horario_abertura"]),
            self.formata_hora(dados_clinica["horario_fechamento"])))
        profissionais = dados_clinica["profissionais"]
        print("PROFISSIONAIS: ",
              ", ".join(profissionais) if profissionais else "nenhum")
        print("\n")

    def seleciona_clinica(self) -> int:
        codigo = self.le_num_inteiro(
            "Codigo da clinica que deseja selecionar: ")
        return codigo

    def seleciona_profissional(self) -> str:
        cpf = self.le_cpf("CPF do profissional: ")
        return cpf
