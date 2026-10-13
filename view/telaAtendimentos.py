from datetime import date, time

from view.abstractTela import AbstractTela
from control.controladorAtendimentos import ControladorAtendimentos
from model.pagamento import Pagamento

class TelaAtendimento(AbstractTela):
    def __init__(self, controlador: ControladorAtendimentos) -> None:
        self.__controlador = controlador

    def mostra_menu(self) -> None:
        print("\n=== Menu de Atendimentos ===")
        print("1 - Criar Atendimento")
        print("2 - Verificar Atendimento/Pagamento")
        print("3 - Realizar Pagamento")

    def le_opcao(self) -> None:
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            self.inclui_atendimento()
        elif opcao == "2":
            self.__verifica_pagamento()
        elif opcao == "3":
            self.__realiza_pagamento()
        else:
            print("Opção inválida.")

    def criar_tipo_atendimento(self) -> None:
        nome = input("Nome do tipo de atendimento: ").strip()
        descricao = input("Descrição: ").strip()
        codigo = int(input("Código: "))
        self.__controlador.inclui_tipo(nome, descricao, codigo)

    def inclui_atendimento(self) -> None:
        clinica = self.__controlador.clinica
        pacientes = clinica.clientes
        profissionais = clinica.profissionais

        if not pacientes:
            print("Não há pacientes cadastrados na clínica.")
            return
        if not profissionais:
            print("Não há profissionais cadastrados na clínica.")
            return

        if not self.__controlador.tipos_atendimento:
            print("Cadastre o primeiro tipo de atendimento.")
            self.criar_tipo_atendimento()

        paciente = self.__seleciona_item("paciente", pacientes, lambda p: p.nome)
        profissional = self.__seleciona_item(
            "profissional",
            profissionais,
            lambda p: f"{p.nome} - {p.especialidade}",
        )
        tipos = self.__controlador.tipos_atendimento
        tipo = self.__seleciona_item(
            "tipo de atendimento",
            tipos,
            lambda t: f"{t.nome} (código {t.codigo})",
        )

        data_atendimento = date.fromisoformat(input("Data do atendimento (AAAA-MM-DD): ").strip())
        horario = time.fromisoformat(input("Horário (HH:MM): ").strip())
        valor = float(input("Valor do atendimento: "))
        parcelas = int(input("Número de parcelas: "))
        pagamento = Pagamento(date.today(), valor, parcelas)

        self.__controlador.inclui_atendimento(
            paciente,
            profissional,
            data_atendimento,
            horario,
            tipo,
            valor,
            pagamento,
        )
        print("Atendimento cadastrado.")

    def __seleciona_item(self, descricao, itens, rotulo):
        print(f"\nSelecione {descricao}:")
        for indice, item in enumerate(itens, start=1):
            print(f"{indice} - {rotulo(item)}")

        while True:
            try:
                indice = int(input("Opção: "))
            except ValueError:
                print("Digite um número válido.")
                continue

            if 1 <= indice <= len(itens):
                return itens[indice - 1]
            print("Opção fora do intervalo.")

    def __seleciona_atendimento(self):
        atendimentos = self.__controlador.lista_atendimentos()
        if not atendimentos:
            print("Não há atendimentos cadastrados.")
            return None

        atendimento = self.__seleciona_item(
            "atendimento",
            atendimentos,
            lambda a: (
                f"{a.data.isoformat()} {a.horario.strftime('%H:%M')} - "
                f"{a.paciente.nome} - {a.clinica.nome} - R$ {a.valor:.2f}"
            ),
        )
        return atendimento

    def __verifica_pagamento(self) -> None:
        atendimento = self.__seleciona_atendimento()
        if atendimento is None:
            return

        saldo = self.__controlador.verifica_pagamento(atendimento)
        print(f"Valor do atendimento: R$ {atendimento.valor:.2f}")
        print(f"Valor já pago: R$ {atendimento.pagamento.valor_pago:.2f}")
        print(f"Saldo restante: R$ {saldo:.2f}")
        print(f"Parcelas restantes: {atendimento.pagamento.parcelas_restantes}")

    def __realiza_pagamento(self) -> None:
        atendimento = self.__seleciona_atendimento()
        if atendimento is None:
            return

        self.__controlador.realiza_pagamento(atendimento)
        print(f"Saldo restante: R$ {self.__controlador.verifica_pagamento(atendimento):.2f}")
    