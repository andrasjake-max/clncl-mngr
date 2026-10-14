from limite.tela_abstrata import TelaAbstrata


class TelaPagamento(TelaAbstrata):
    MODALIDADES = {1: "dinheiro", 2: "pix", 3: "cartao"}

    def tela_opcoes(self) -> int:
        print("-------- PAGAMENTOS ----------")
        print("Escolha a opcao")
        print("1 - Registrar Pagamento")
        print("2 - Alterar Pagamento")
        print("3 - Listar Pagamentos")
        print("4 - Excluir Pagamento")
        print("0 - Retornar")
        opcao = self.le_num_inteiro("Escolha a opcao: ", [0, 1, 2, 3, 4])
        return opcao

    def pega_dados_pagamento(self, bandeiras: tuple) -> dict:
        print("-------- DADOS PAGAMENTO ----------")
        codigo_atendimento = self.le_num_inteiro("Codigo do atendimento: ")
        data = self.le_data("Data do pagamento")
        valor = self.le_valor("Valor pago (R$): ", minimo=0.01)
        print("Modalidade de pagamento")
        print("1 - Dinheiro")
        print("2 - PIX")
        print("3 - Cartao de credito")
        opcao = self.le_num_inteiro("Escolha a modalidade: ", [1, 2, 3])
        dados_pagamento = {"codigo_atendimento": codigo_atendimento,
                           "data": data, "valor_pago": valor,
                           "modalidade": TelaPagamento.MODALIDADES[opcao]}
        if opcao == 2:
            dados_pagamento["cpf_pagador"] = self.le_cpf("CPF do pagador: ")
        elif opcao == 3:
            dados_pagamento["numero_cartao"] = self.le_digitos(
                "Numero do cartao: ", tuple(range(13, 20)))
            print("Bandeira do cartao")
            for numero, bandeira in enumerate(bandeiras, start=1):
                print("{} - {}".format(numero, bandeira))
            escolha = self.le_num_inteiro(
                "Escolha a bandeira: ", list(range(1, len(bandeiras) + 1)))
            dados_pagamento["bandeira"] = bandeiras[escolha - 1]
        return dados_pagamento

    def mostra_pagamento(self, dados_pagamento: dict) -> None:
        print("CODIGO DO PAGAMENTO: ", dados_pagamento["codigo"])
        print("DATA: ", self.formata_data(dados_pagamento["data"]))
        print("ATENDIMENTO: ", dados_pagamento["atendimento"])
        print("PACIENTE: ", dados_pagamento["paciente"])
        print("VALOR PAGO: ",
              self.formata_valor(dados_pagamento["valor_pago"]))
        print("MODALIDADE: ", dados_pagamento["modalidade"])
        print("DETALHES: ", dados_pagamento["detalhes"])
        print("RESTANTE DO ATENDIMENTO: ",
              self.formata_valor(dados_pagamento["valor_restante"]))
        print("\n")

    def seleciona_pagamento(self) -> int:
        codigo = self.le_num_inteiro(
            "Codigo do pagamento que deseja selecionar: ")
        return codigo
