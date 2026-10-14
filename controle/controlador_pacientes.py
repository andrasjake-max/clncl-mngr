from datetime import date
from typing import TYPE_CHECKING
from limite.tela_paciente import TelaPaciente
from entidade.paciente import Paciente
from exceptions.sistema_exception import SistemaException
from exceptions.dado_invalido_exception import DadoInvalidoException
from exceptions.registro_repetido_exception import RegistroRepetidoException
from exceptions.registro_nao_encontrado_exception import \
    RegistroNaoEncontradoException
from exceptions.lista_vazia_exception import ListaVaziaException
from exceptions.registro_em_uso_exception import RegistroEmUsoException

if TYPE_CHECKING:
    from controle.controlador_sistema import ControladorSistema


class ControladorPacientes:

    def __init__(self, controlador_sistema: "ControladorSistema") -> None:
        self.__pacientes = []
        self.__tela_paciente = TelaPaciente()
        self.__controlador_sistema = controlador_sistema

    @property
    def pacientes(self) -> list:
        return list(self.__pacientes)

    def pega_paciente_por_cpf(self, cpf: str) -> Paciente | None:
        for paciente in self.__pacientes:
            if paciente.cpf == cpf:
                return paciente
        return None

    def __pega_responsavel(self, dados_paciente: dict) -> Paciente | None:
        idade = Paciente.calcula_idade(dados_paciente["data_nascimento"],
                                       date.today())
        if idade >= Paciente.IDADE_MINIMA_INDEPENDENTE:
            return None
        cpf_responsavel = self.__tela_paciente.pega_cpf_responsavel()
        if cpf_responsavel is None:
            return None
        if cpf_responsavel == dados_paciente["cpf"]:
            raise DadoInvalidoException(
                "responsavel", "paciente nao pode ser responsavel por si")
        responsavel = self.pega_paciente_por_cpf(cpf_responsavel)
        if responsavel is None:
            raise RegistroNaoEncontradoException("Responsavel",
                                                 cpf_responsavel)
        if not responsavel.eh_maior_de_idade(date.today()):
            raise DadoInvalidoException(
                "responsavel", "o responsavel deve ser maior de idade")
        return responsavel

    def incluir_paciente(self) -> None:
        dados_paciente = self.__tela_paciente.pega_dados_paciente()
        try:
            if self.pega_paciente_por_cpf(dados_paciente["cpf"]) is not None:
                raise RegistroRepetidoException("Paciente",
                                                dados_paciente["cpf"])
            responsavel = self.__pega_responsavel(dados_paciente)
            paciente = Paciente(dados_paciente["nome"],
                                dados_paciente["celular"],
                                dados_paciente["cpf"],
                                dados_paciente["data_nascimento"],
                                responsavel)
            self.__pacientes.append(paciente)
            self.__tela_paciente.mostra_mensagem("Paciente cadastrado!")
        except SistemaException as e:
            self.__tela_paciente.mostra_mensagem("ATENCAO: {}".format(e))

    def alterar_paciente(self) -> None:
        try:
            if not self.__pacientes:
                raise ListaVaziaException("paciente")
            self.lista_pacientes()
            cpf_paciente = self.__tela_paciente.seleciona_paciente()
            paciente = self.pega_paciente_por_cpf(cpf_paciente)
            if paciente is None:
                raise RegistroNaoEncontradoException("Paciente", cpf_paciente)
            novos_dados_paciente = self.__tela_paciente.pega_dados_paciente()
            outro = self.pega_paciente_por_cpf(novos_dados_paciente["cpf"])
            if outro is not None and outro is not paciente:
                raise RegistroRepetidoException("Paciente",
                                                novos_dados_paciente["cpf"])
            responsavel = self.__pega_responsavel(novos_dados_paciente)
            if responsavel is paciente:
                raise DadoInvalidoException(
                    "responsavel", "paciente nao pode ser responsavel por si")
            paciente.data_nascimento = novos_dados_paciente["data_nascimento"]
            paciente.responsavel = responsavel
            paciente.nome = novos_dados_paciente["nome"]
            paciente.celular = novos_dados_paciente["celular"]
            paciente.cpf = novos_dados_paciente["cpf"]
            self.__tela_paciente.mostra_mensagem("Paciente alterado!")
        except SistemaException as e:
            self.__tela_paciente.mostra_mensagem("ATENCAO: {}".format(e))

    def lista_pacientes(self) -> None:
        try:
            if not self.__pacientes:
                raise ListaVaziaException("paciente")
            for paciente in self.__pacientes:
                responsavel = "-"
                if paciente.responsavel is not None:
                    responsavel = "{} (CPF {})".format(
                        paciente.responsavel.nome, paciente.responsavel.cpf)
                self.__tela_paciente.mostra_paciente({
                    "nome": paciente.nome, "cpf": paciente.cpf,
                    "celular": paciente.celular,
                    "data_nascimento": paciente.data_nascimento,
                    "idade": paciente.idade_em(date.today()),
                    "responsavel": responsavel})
        except ListaVaziaException as e:
            self.__tela_paciente.mostra_mensagem(e)

    def excluir_paciente(self) -> None:
        try:
            if not self.__pacientes:
                raise ListaVaziaException("paciente")
            self.lista_pacientes()
            cpf_paciente = self.__tela_paciente.seleciona_paciente()
            paciente = self.pega_paciente_por_cpf(cpf_paciente)
            if paciente is None:
                raise RegistroNaoEncontradoException("Paciente", cpf_paciente)
            atendimentos = self.__controlador_sistema.controlador_atendimentos
            if atendimentos.atendimentos_da_pessoa(paciente):
                raise RegistroEmUsoException(
                    "Paciente", "possui atendimentos registrados")
            if any(p.responsavel is paciente for p in self.__pacientes):
                raise RegistroEmUsoException(
                    "Paciente", "e responsavel por outro paciente")
            self.__pacientes.remove(paciente)
            self.__tela_paciente.mostra_mensagem("Paciente excluido!")
        except SistemaException as e:
            self.__tela_paciente.mostra_mensagem("ATENCAO: {}".format(e))

    def retornar(self) -> None:
        self.__controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        lista_opcoes = {1: self.incluir_paciente, 2: self.alterar_paciente,
                        3: self.lista_pacientes, 4: self.excluir_paciente,
                        0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__tela_paciente.tela_opcoes()]()
