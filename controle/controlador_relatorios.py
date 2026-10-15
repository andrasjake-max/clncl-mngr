from typing import TYPE_CHECKING
from limite.tela_relatorio import TelaRelatorio
from exceptions.lista_vazia_exception import ListaVaziaException

if TYPE_CHECKING:
    from controle.controlador_sistema import ControladorSistema


class ControladorRelatorios:

    def __init__(self, controlador_sistema: "ControladorSistema") -> None:
        self.__tela_relatorio = TelaRelatorio()
        self.__controlador_sistema = controlador_sistema

    def relatorio_clinicas(self) -> None:
        self.__tela_relatorio.mostra_titulo(
            "CLINICAS COM MAIOR NUMERO DE ATENDIMENTOS")
        try:
            sistema = self.__controlador_sistema
            atendimentos = sistema.controlador_atendimentos
            if not atendimentos.atendimentos:
                raise ListaVaziaException("atendimento")
            clinicas = sorted(
                sistema.controlador_clinicas.clinicas,
                key=lambda c: len(atendimentos.atendimentos_da_clinica(c)),
                reverse=True)
            for posicao, clinica in enumerate(clinicas, start=1):
                self.__tela_relatorio.mostra_clinica(posicao, {
                    "nome": clinica.nome, "cidade": clinica.cidade,
                    "quantidade":
                        len(atendimentos.atendimentos_da_clinica(clinica))})
        except ListaVaziaException as e:
            self.__tela_relatorio.mostra_mensagem(e)

    def relatorio_atendimentos(self) -> None:
        self.__tela_relatorio.mostra_titulo(
            "ATENDIMENTOS MAIS CAROS E MAIS BARATOS")
        try:
            atendimentos = self.__controlador_sistema \
                .controlador_atendimentos.atendimentos
            if not atendimentos:
                raise ListaVaziaException("atendimento")
            maior = max(a.valor_total() for a in atendimentos)
            menor = min(a.valor_total() for a in atendimentos)
            for rotulo, valor in (("Mais caro", maior),
                                  ("Mais barato", menor)):
                for atendimento in atendimentos:
                    if atendimento.valor_total() == valor:
                        self.__tela_relatorio.mostra_atendimento(rotulo, {
                            "codigo": atendimento.codigo,
                            "tipo": atendimento.tipo.nome,
                            "paciente": atendimento.paciente.nome,
                            "profissional": atendimento.profissional.nome,
                            "data": atendimento.data,
                            "valor_total": atendimento.valor_total()})
        except ListaVaziaException as e:
            self.__tela_relatorio.mostra_mensagem(e)

    def relatorio_procedimentos_realizados(self) -> None:
        self.__tela_relatorio.mostra_titulo("PROCEDIMENTOS MAIS REALIZADOS")
        try:
            todos = self.__controlador_sistema.controlador_procedimentos \
                .todos_procedimentos()
            if not todos:
                raise ListaVaziaException("procedimento")
            contagem = {}
            for atendimento, procedimento in todos:
                chave = procedimento.descricao.lower()
                if chave not in contagem:
                    contagem[chave] = {"descricao": procedimento.descricao,
                                       "quantidade": 0}
                contagem[chave]["quantidade"] += 1
            ranking = sorted(contagem.values(),
                             key=lambda linha: linha["quantidade"],
                             reverse=True)
            for posicao, linha in enumerate(ranking, start=1):
                self.__tela_relatorio.mostra_procedimento_realizado(posicao,
                                                                    linha)
        except ListaVaziaException as e:
            self.__tela_relatorio.mostra_mensagem(e)

    def relatorio_procedimentos(self) -> None:
        self.__tela_relatorio.mostra_titulo(
            "PROCEDIMENTOS MAIS CAROS E MAIS BARATOS")
        try:
            todos = self.__controlador_sistema.controlador_procedimentos \
                .todos_procedimentos()
            if not todos:
                raise ListaVaziaException("procedimento")
            maior = max(p.custo for a, p in todos)
            menor = min(p.custo for a, p in todos)
            for rotulo, custo in (("Mais caro", maior),
                                  ("Mais barato", menor)):
                for atendimento, procedimento in todos:
                    if procedimento.custo == custo:
                        self.__tela_relatorio.mostra_procedimento(rotulo, {
                            "descricao": procedimento.descricao,
                            "codigo_atendimento": atendimento.codigo,
                            "custo": procedimento.custo,
                            "profissional": procedimento.profissional.nome})
        except ListaVaziaException as e:
            self.__tela_relatorio.mostra_mensagem(e)

    def retornar(self) -> None:
        self.__controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        lista_opcoes = {1: self.relatorio_clinicas,
                        2: self.relatorio_atendimentos,
                        3: self.relatorio_procedimentos_realizados,
                        4: self.relatorio_procedimentos,
                        0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__tela_relatorio.tela_opcoes()]()
