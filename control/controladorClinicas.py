from model.atendimento import Atendimento
from model.clinica import Clinica
from model.procedimento import Procedimento


class ControladorClinicas:
    def __init__(self, clinicas: list[Clinica] | None = None) -> None:
        self.__clinicas = [] if clinicas is None else list(clinicas)

    def cadastra_clinica(self, clinica: Clinica) -> None:
        self.__clinicas.append(clinica)

    def lista_clinicas(self) -> list[Clinica]:
        return list(self.__clinicas)

    def lista_atendimento_caro(self) -> list[Atendimento]:
        atendimentos = self.__lista_atendimentos()
        return sorted(atendimentos, key=lambda atendimento: atendimento.valor, reverse=True)[:10]

    def lista_atendimento_barato(self) -> list[Atendimento]:
        atendimentos = self.__lista_atendimentos()
        return sorted(atendimentos, key=lambda atendimento: atendimento.valor)[:10]

    def procedimento_populares(self) -> list[Procedimento]:
        procedimentos = self.__lista_procedimentos()
        frequencia: dict[str, int] = {}
        representante: dict[str, Procedimento] = {}

        for procedimento in procedimentos:
            frequencia[procedimento.descricao] = frequencia.get(procedimento.descricao, 0) + 1
            representante.setdefault(procedimento.descricao, procedimento)

        descricoes_ordenadas = sorted(
            frequencia,
            key=lambda descricao: frequencia[descricao],
            reverse=True,
        )
        return [representante[descricao] for descricao in descricoes_ordenadas]

    def procedimentos_caros(self) -> list[Procedimento]:
        procedimentos = self.__lista_procedimentos()
        return sorted(procedimentos, key=lambda procedimento: procedimento.custo, reverse=True)[:10]

    def procedimentos_baratos(self) -> list[Procedimento]:
        procedimentos = self.__lista_procedimentos()
        return sorted(procedimentos, key=lambda procedimento: procedimento.custo)[:10]

    def __lista_atendimentos(self) -> list[Atendimento]:
        return [
            atendimento
            for clinica in self.__clinicas
            for atendimento in clinica.atendimentos
        ]

    def __lista_procedimentos(self) -> list[Procedimento]:
        return [
            procedimento
            for atendimento in self.__lista_atendimentos()
            for procedimento in atendimento.procedimentos
        ]
    