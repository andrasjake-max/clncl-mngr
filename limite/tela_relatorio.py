from limite.tela_abstrata import TelaAbstrata


class TelaRelatorio(TelaAbstrata):
    def tela_opcoes(self) -> int:
        print("-------- RELATORIOS ----------")
        print("Escolha a opcao")
        print("1 - Clinicas com maior numero de atendimentos")
        print("2 - Atendimentos mais caros e mais baratos")
        print("3 - Procedimentos mais realizados")
        print("4 - Procedimentos mais caros e mais baratos")
        print("0 - Retornar")
        opcao = self.le_num_inteiro("Escolha a opcao: ", [0, 1, 2, 3, 4])
        return opcao

    def mostra_titulo(self, titulo: str) -> None:
        print("\n===== {} =====".format(titulo))

    def mostra_clinica(self, posicao: int, dados_clinica: dict) -> None:
        print("{}o - {} ({}): {} atendimento(s)".format(
            posicao, dados_clinica["nome"], dados_clinica["cidade"],
            dados_clinica["quantidade"]))

    def mostra_atendimento(self, rotulo: str, dados_atendimento: dict) -> None:
        print("{}: atendimento {} - {} - {} com {} em {} - total {}".format(
            rotulo, dados_atendimento["codigo"], dados_atendimento["tipo"],
            dados_atendimento["paciente"], dados_atendimento["profissional"],
            self.formata_data(dados_atendimento["data"]),
            self.formata_valor(dados_atendimento["valor_total"])))

    def mostra_procedimento_realizado(self, posicao: int,
                                      dados_procedimento: dict) -> None:
        print("{}o - {}: realizado {} vez(es)".format(
            posicao, dados_procedimento["descricao"],
            dados_procedimento["quantidade"]))

    def mostra_procedimento(self, rotulo: str,
                            dados_procedimento: dict) -> None:
        print("{}: {} (atendimento {}) - {} - por {}".format(
            rotulo, dados_procedimento["descricao"],
            dados_procedimento["codigo_atendimento"],
            self.formata_valor(dados_procedimento["custo"]),
            dados_procedimento["profissional"]))
