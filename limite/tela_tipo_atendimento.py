from limite.tela_abstrata import TelaAbstrata


class TelaTipoAtendimento(TelaAbstrata):
    def tela_opcoes(self) -> int:
        print("-------- TIPOS DE ATENDIMENTO ----------")
        print("Escolha a opcao")
        print("1 - Incluir Tipo")
        print("2 - Alterar Tipo")
        print("3 - Listar Tipos")
        print("4 - Excluir Tipo")
        print("0 - Retornar")
        opcao = self.le_num_inteiro("Escolha a opcao: ", [0, 1, 2, 3, 4])
        return opcao

    def pega_dados_tipo(self) -> dict:
        print("-------- DADOS TIPO DE ATENDIMENTO ----------")
        nome = self.le_texto("Nome (ex.: Consulta, Exame, Retorno): ")
        descricao = self.le_texto("Descricao: ", obrigatorio=False)
        return {"nome": nome, "descricao": descricao}

    def mostra_tipo(self, dados_tipo: dict) -> None:
        print("CODIGO DO TIPO: ", dados_tipo["codigo"])
        print("NOME DO TIPO: ", dados_tipo["nome"])
        print("DESCRICAO: ", dados_tipo["descricao"])
        print("\n")

    def seleciona_tipo(self) -> int:
        codigo = self.le_num_inteiro(
            "Codigo do tipo que deseja selecionar: ")
        return codigo
