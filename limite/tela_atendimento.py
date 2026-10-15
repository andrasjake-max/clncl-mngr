from limite.tela_abstrata import TelaAbstrata


class TelaAtendimento(TelaAbstrata):
    def tela_opcoes(self) -> int:
        print("-------- ATENDIMENTOS ----------")
        print("Escolha a opcao")
        print("1 - Agendar Atendimento")
        print("2 - Alterar Atendimento")
        print("3 - Listar Atendimentos")
        print("4 - Excluir Atendimento")
        print("0 - Retornar")
        opcao = self.le_num_inteiro("Escolha a opcao: ", [0, 1, 2, 3, 4])
        return opcao

    def pega_dados_atendimento(self) -> dict:
        print("-------- DADOS ATENDIMENTO ----------")
        codigo_clinica = self.le_num_inteiro("Codigo da clinica: ")
        cpf_paciente = self.le_cpf("CPF do paciente: ")
        cpf_profissional = self.le_cpf("CPF do profissional: ")
        codigo_tipo = self.le_num_inteiro("Codigo do tipo de atendimento: ")
        data = self.le_data("Data")
        hora_inicio = self.le_hora("Horario de inicio")
        hora_fim = self.le_hora("Horario de fim")
        valor = self.le_valor("Valor (R$): ")
        return {"codigo_clinica": codigo_clinica,
                "cpf_paciente": cpf_paciente,
                "cpf_profissional": cpf_profissional,
                "codigo_tipo": codigo_tipo, "data": data,
                "hora_inicio": hora_inicio, "hora_fim": hora_fim,
                "valor": valor}

    def mostra_atendimento(self, dados_atendimento: dict) -> None:
        print("CODIGO DO ATENDIMENTO: ", dados_atendimento["codigo"])
        print("CLINICA: ", dados_atendimento["clinica"])
        print("PACIENTE: ", dados_atendimento["paciente"])
        print("PROFISSIONAL: ", dados_atendimento["profissional"])
        print("TIPO: ", dados_atendimento["tipo"])
        print("DATA: {}  {} - {}".format(
            self.formata_data(dados_atendimento["data"]),
            self.formata_hora(dados_atendimento["hora_inicio"]),
            self.formata_hora(dados_atendimento["hora_fim"])))
        print("VALOR DO ATENDIMENTO: ",
              self.formata_valor(dados_atendimento["valor"]))
        print("PROCEDIMENTOS: ", dados_atendimento["qtd_procedimentos"])
        print("VALOR TOTAL: ",
              self.formata_valor(dados_atendimento["valor_total"]))
        print("\n")

    def seleciona_atendimento(self) -> int:
        codigo = self.le_num_inteiro(
            "Codigo do atendimento que deseja selecionar: ")
        return codigo
