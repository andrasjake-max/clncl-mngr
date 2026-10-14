from typing import TYPE_CHECKING
from limite.tela_atendimento import TelaAtendimento
from entidade.atendimento import Atendimento
from entidade.pessoa import Pessoa
from entidade.clinica import Clinica
from exceptions.sistema_exception import SistemaException
from exceptions.registro_nao_encontrado_exception import \
    RegistroNaoEncontradoException
from exceptions.lista_vazia_exception import ListaVaziaException
from exceptions.horario_invalido_exception import HorarioInvalidoException
from exceptions.paciente_menor_idade_exception import \
    PacienteMenorIdadeException

if TYPE_CHECKING:
    from controle.controlador_sistema import ControladorSistema


class ControladorAtendimentos:

    def __init__(self, controlador_sistema: "ControladorSistema") -> None:
        self.__atendimentos = []
        self.__tela_atendimento = TelaAtendimento()
        self.__controlador_sistema = controlador_sistema
        self.__proximo_codigo = 1

    @property
    def atendimentos(self) -> list:
        return list(self.__atendimentos)

    def pega_atendimento_por_codigo(self, codigo: int) -> Atendimento | None:
        for atendimento in self.__atendimentos:
            if atendimento.codigo == codigo:
                return atendimento
        return None

    def atendimentos_da_clinica(self, clinica: Clinica) -> list:
        return [a for a in self.__atendimentos if a.clinica is clinica]

    def atendimentos_da_pessoa(self, pessoa: Pessoa) -> list:
        return [a for a in self.__atendimentos
                if a.paciente is pessoa or a.profissional is pessoa
                or any(p.profissional is pessoa for p in a.procedimentos)]

    def __seleciona_atendimento(self) -> Atendimento:
        if not self.__atendimentos:
            raise ListaVaziaException("atendimento")
        self.lista_atendimentos()
        codigo = self.__tela_atendimento.seleciona_atendimento()
        atendimento = self.pega_atendimento_por_codigo(codigo)
        if atendimento is None:
            raise RegistroNaoEncontradoException("Atendimento", codigo)
        return atendimento

    def __lista_cadastros(self) -> None:
        sistema = self.__controlador_sistema
        if not sistema.controlador_clinicas.clinicas:
            raise ListaVaziaException("clinica")
        if not sistema.controlador_pacientes.pacientes:
            raise ListaVaziaException("paciente")
        if not sistema.controlador_profissionais.profissionais:
            raise ListaVaziaException("profissional")
        if not sistema.controlador_tipos_atendimento.tipos:
            raise ListaVaziaException("tipo de atendimento")
        sistema.controlador_clinicas.lista_clinicas()
        sistema.controlador_pacientes.lista_pacientes()
        sistema.controlador_tipos_atendimento.lista_tipos()

    def __busca_cadastros(self, dados_atendimento: dict) -> dict:
        sistema = self.__controlador_sistema
        clinica = sistema.controlador_clinicas.pega_clinica_por_codigo(
            dados_atendimento["codigo_clinica"])
        if clinica is None:
            raise RegistroNaoEncontradoException(
                "Clinica", dados_atendimento["codigo_clinica"])
        paciente = sistema.controlador_pacientes.pega_paciente_por_cpf(
            dados_atendimento["cpf_paciente"])
        if paciente is None:
            raise RegistroNaoEncontradoException(
                "Paciente", dados_atendimento["cpf_paciente"])
        profissional = sistema.controlador_profissionais \
            .pega_profissional_por_cpf(dados_atendimento["cpf_profissional"])
        if profissional is None:
            raise RegistroNaoEncontradoException(
                "Profissional", dados_atendimento["cpf_profissional"])
        tipo = sistema.controlador_tipos_atendimento.pega_tipo_por_codigo(
            dados_atendimento["codigo_tipo"])
        if tipo is None:
            raise RegistroNaoEncontradoException(
                "Tipo de atendimento", dados_atendimento["codigo_tipo"])
        return {"clinica": clinica, "paciente": paciente,
                "profissional": profissional, "tipo": tipo}

    def __valida_regras(self, cadastros: dict,
                        dados_atendimento: dict) -> None:
        clinica = cadastros["clinica"]
        paciente = cadastros["paciente"]
        data = dados_atendimento["data"]
        inicio = dados_atendimento["hora_inicio"]
        fim = dados_atendimento["hora_fim"]
        if inicio >= fim:
            raise HorarioInvalidoException("inicio deve ser antes do fim")
        if not clinica.funciona_entre(inicio, fim):
            raise HorarioInvalidoException(
                "a clinica {} funciona das {} as {}".format(
                    clinica.nome, clinica.horario_abertura.strftime("%H:%M"),
                    clinica.horario_fechamento.strftime("%H:%M")))
        if not paciente.pode_ser_atendido_em(data):
            raise PacienteMenorIdadeException(paciente.nome,
                                              paciente.idade_em(data))

    def incluir_atendimento(self) -> None:
        try:
            self.__lista_cadastros()
            dados_atendimento = \
                self.__tela_atendimento.pega_dados_atendimento()
            cadastros = self.__busca_cadastros(dados_atendimento)
            self.__valida_regras(cadastros, dados_atendimento)
            atendimento = Atendimento(
                self.__proximo_codigo, cadastros["clinica"],
                cadastros["paciente"], cadastros["profissional"],
                cadastros["tipo"], dados_atendimento["data"],
                dados_atendimento["hora_inicio"],
                dados_atendimento["hora_fim"], dados_atendimento["valor"])
            self.__atendimentos.append(atendimento)
            self.__proximo_codigo += 1
            self.__tela_atendimento.mostra_mensagem(
                "Atendimento agendado com codigo {}!".format(
                    atendimento.codigo))
        except SistemaException as e:
            self.__tela_atendimento.mostra_mensagem("ATENCAO: {}".format(e))

    def alterar_atendimento(self) -> None:
        try:
            atendimento = self.__seleciona_atendimento()
            self.__lista_cadastros()
            novos_dados = self.__tela_atendimento.pega_dados_atendimento()
            cadastros = self.__busca_cadastros(novos_dados)
            self.__valida_regras(cadastros, novos_dados)
            atendimento.define_horario(novos_dados["data"],
                                       novos_dados["hora_inicio"],
                                       novos_dados["hora_fim"])
            atendimento.valor = novos_dados["valor"]
            atendimento.clinica = cadastros["clinica"]
            atendimento.paciente = cadastros["paciente"]
            atendimento.profissional = cadastros["profissional"]
            atendimento.tipo = cadastros["tipo"]
            self.__tela_atendimento.mostra_mensagem("Atendimento alterado!")
        except SistemaException as e:
            self.__tela_atendimento.mostra_mensagem("ATENCAO: {}".format(e))

    def lista_atendimentos(self) -> None:
        try:
            if not self.__atendimentos:
                raise ListaVaziaException("atendimento")
            for atendimento in self.__atendimentos:
                self.__tela_atendimento.mostra_atendimento({
                    "codigo": atendimento.codigo,
                    "clinica": atendimento.clinica.nome,
                    "paciente": "{} (CPF {})".format(
                        atendimento.paciente.nome, atendimento.paciente.cpf),
                    "profissional": "{} - {}".format(
                        atendimento.profissional.nome,
                        atendimento.profissional.especialidade),
                    "tipo": atendimento.tipo.nome,
                    "data": atendimento.data,
                    "hora_inicio": atendimento.hora_inicio,
                    "hora_fim": atendimento.hora_fim,
                    "valor": atendimento.valor,
                    "qtd_procedimentos": len(atendimento.procedimentos),
                    "valor_total": atendimento.valor_total()})
        except ListaVaziaException as e:
            self.__tela_atendimento.mostra_mensagem(e)

    def excluir_atendimento(self) -> None:
        try:
            atendimento = self.__seleciona_atendimento()
            self.__atendimentos.remove(atendimento)
            self.__tela_atendimento.mostra_mensagem(
                "Atendimento e seus procedimentos excluidos!")
        except SistemaException as e:
            self.__tela_atendimento.mostra_mensagem("ATENCAO: {}".format(e))

    def retornar(self) -> None:
        self.__controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        lista_opcoes = {1: self.incluir_atendimento,
                        2: self.alterar_atendimento,
                        3: self.lista_atendimentos,
                        4: self.excluir_atendimento,
                        0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__tela_atendimento.tela_opcoes()]()
