from abc import ABC, abstractmethod
from datetime import date, datetime, time


class TelaAbstrata(ABC):
    @abstractmethod
    def tela_opcoes(self) -> int:
        pass

    def le_num_inteiro(self, mensagem: str = " ",
                       ints_validos: list[int] | None = None) -> int:
        while True:
            valor_lido = input(mensagem)
            try:
                valor_int = int(valor_lido)
                if ints_validos and valor_int not in ints_validos:
                    raise ValueError
                return valor_int
            except ValueError:
                print("Valor incorreto!")
                if ints_validos:
                    print("Valores validos: ", ints_validos)

    def le_valor(self, mensagem: str, minimo: float = 0.0) -> float:
        while True:
            valor_lido = input(mensagem).strip().replace(",", ".")
            try:
                valor = float(valor_lido)
                if valor < minimo:
                    raise ValueError
                return round(valor, 2)
            except ValueError:
                print("Valor incorreto! Digite um numero >= {:.2f}".format(
                    minimo))

    def le_texto(self, mensagem: str, obrigatorio: bool = True) -> str:
        while True:
            texto = input(mensagem).strip()
            if texto or not obrigatorio:
                return texto
            print("Este campo e obrigatorio!")

    def le_digitos(self, mensagem: str, tamanhos: tuple) -> str:
        while True:
            texto = input(mensagem)
            digitos = "".join(c for c in texto if c.isdigit())
            if len(digitos) in tamanhos:
                return digitos
            print("Valor incorreto! Quantidade de digitos aceita: {}".format(
                ", ".join(str(t) for t in tamanhos)))

    def le_cpf(self, mensagem: str = "CPF: ") -> str:
        return self.le_digitos(mensagem, (11,))

    def le_data(self, mensagem: str) -> date:
        while True:
            texto = input(mensagem + " (dd/mm/aaaa): ").strip()
            try:
                return datetime.strptime(texto, "%d/%m/%Y").date()
            except ValueError:
                print("Data invalida! Use o formato dd/mm/aaaa.")

    def le_hora(self, mensagem: str) -> time:
        while True:
            texto = input(mensagem + " (hh:mm): ").strip()
            try:
                return datetime.strptime(texto, "%H:%M").time()
            except ValueError:
                print("Horario invalido! Use o formato hh:mm.")

    def le_sim_nao(self, mensagem: str) -> bool:
        while True:
            resposta = input(mensagem + " (s/n): ").strip().lower()
            if resposta in ("s", "n"):
                return resposta == "s"
            print("Responda com s ou n.")

    def mostra_mensagem(self, msg: str) -> None:
        print(msg)

    def formata_data(self, data: date) -> str:
        return data.strftime("%d/%m/%Y")

    def formata_hora(self, hora: time) -> str:
        return hora.strftime("%H:%M")

    def formata_valor(self, valor: float) -> str:
        return "R$ {:.2f}".format(valor)
