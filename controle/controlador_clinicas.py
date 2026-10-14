from typing import TYPE_CHECKING
from limite.tela_clinica import TelaClinica
from entidade.clinica import Clinica
from entidade.profissional_saude import ProfissionalSaude
from exceptions.sistema_exception import SistemaException
from exceptions.registro_nao_encontrado_exception import \
    RegistroNaoEncontradoException
from exceptions.lista_vazia_exception import ListaVaziaException
from exceptions.registro_em_uso_exception import RegistroEmUsoException
from exceptions.horario_invalido_exception import HorarioInvalidoException

if TYPE_CHECKING:
    from controle.controlador_sistema import ControladorSistema


class ControladorClinicas:

    def __init__(self, controlador_sistema: "ControladorSistema") -> None:
        self.__clinicas = []
        self.__tela_clinica = TelaClinica()
        self.__controlador_sistema = controlador_sistema
        self.__proximo_codigo = 1

    @property
    def clinicas(self) -> list:
        return list(self.__clinicas)

    def pega_clinica_por_codigo(self, codigo: int) -> Clinica | None:
        for clinica in self.__clinicas:
            if clinica.codigo == codigo:
                return clinica
        return None

    def __seleciona_clinica(self) -> Clinica:
        if not self.__clinicas:
            raise ListaVaziaException("clinica")
        self.lista_clinicas()
        codigo_clinica = self.__tela_clinica.seleciona_clinica()
        clinica = self.pega_clinica_por_codigo(codigo_clinica)
        if clinica is None:
            raise RegistroNaoEncontradoException("Clinica", codigo_clinica)
        return clinica

    def __seleciona_profissional(self) -> ProfissionalSaude:
        profissionais = self.__controlador_sistema.controlador_profissionais
        if not profissionais.profissionais:
            raise ListaVaziaException("profissional")
        profissionais.lista_profissionais()
        cpf_profissional = self.__tela_clinica.seleciona_profissional()
        profissional = profissionais.pega_profissional_por_cpf(
            cpf_profissional)
        if profissional is None:
            raise RegistroNaoEncontradoException("Profissional",
                                                 cpf_profissional)
        return profissional

    def incluir_clinica(self) -> None:
        dados_clinica = self.__tela_clinica.pega_dados_clinica()
        try:
            clinica = Clinica(self.__proximo_codigo, dados_clinica["nome"],
                              dados_clinica["cidade"],
                              dados_clinica["descricao"],
                              dados_clinica["horario_abertura"],
                              dados_clinica["horario_fechamento"])
            self.__clinicas.append(clinica)
            self.__proximo_codigo += 1
            self.__tela_clinica.mostra_mensagem(
                "Clinica cadastrada com codigo {}!".format(clinica.codigo))
        except SistemaException as e:
            self.__tela_clinica.mostra_mensagem("ATENCAO: {}".format(e))

    def alterar_clinica(self) -> None:
        try:
            clinica = self.__seleciona_clinica()
            novos_dados_clinica = self.__tela_clinica.pega_dados_clinica()
            abertura = novos_dados_clinica["horario_abertura"]
            fechamento = novos_dados_clinica["horario_fechamento"]
            atendimentos = self.__controlador_sistema.controlador_atendimentos
            for atendimento in atendimentos.atendimentos_da_clinica(clinica):
                if not (abertura <= atendimento.hora_inicio
                        and atendimento.hora_fim <= fechamento):
                    raise HorarioInvalidoException(
                        "o atendimento {} ficaria fora do novo horario de "
                        "funcionamento".format(atendimento.codigo))
            clinica.define_funcionamento(abertura, fechamento)
            clinica.nome = novos_dados_clinica["nome"]
            clinica.cidade = novos_dados_clinica["cidade"]
            clinica.descricao = novos_dados_clinica["descricao"]
            self.__tela_clinica.mostra_mensagem("Clinica alterada!")
        except SistemaException as e:
            self.__tela_clinica.mostra_mensagem("ATENCAO: {}".format(e))

    def lista_clinicas(self) -> None:
        try:
            if not self.__clinicas:
                raise ListaVaziaException("clinica")
            for clinica in self.__clinicas:
                self.__tela_clinica.mostra_clinica({
                    "codigo": clinica.codigo, "nome": clinica.nome,
                    "cidade": clinica.cidade,
                    "descricao": clinica.descricao,
                    "horario_abertura": clinica.horario_abertura,
                    "horario_fechamento": clinica.horario_fechamento,
                    "profissionais": [p.nome for p in clinica.profissionais]})
        except ListaVaziaException as e:
            self.__tela_clinica.mostra_mensagem(e)

    def excluir_clinica(self) -> None:
        try:
            clinica = self.__seleciona_clinica()
            atendimentos = self.__controlador_sistema.controlador_atendimentos
            if atendimentos.atendimentos_da_clinica(clinica):
                raise RegistroEmUsoException(
                    "Clinica", "possui atendimentos registrados")
            self.__clinicas.remove(clinica)
            self.__tela_clinica.mostra_mensagem("Clinica excluida!")
        except SistemaException as e:
            self.__tela_clinica.mostra_mensagem("ATENCAO: {}".format(e))

    def vincular_profissional(self) -> None:
        try:
            clinica = self.__seleciona_clinica()
            profissional = self.__seleciona_profissional()
            clinica.incluir_profissional(profissional)
            self.__tela_clinica.mostra_mensagem(
                "{} agora atende na clinica {}".format(profissional.nome,
                                                       clinica.nome))
        except SistemaException as e:
            self.__tela_clinica.mostra_mensagem("ATENCAO: {}".format(e))

    def desvincular_profissional(self) -> None:
        try:
            clinica = self.__seleciona_clinica()
            profissional = self.__seleciona_profissional()
            if not clinica.possui_profissional(profissional):
                raise RegistroNaoEncontradoException(
                    "Vinculo do profissional", profissional.cpf)
            clinica.excluir_profissional(profissional)
            self.__tela_clinica.mostra_mensagem("Profissional desvinculado!")
        except SistemaException as e:
            self.__tela_clinica.mostra_mensagem("ATENCAO: {}".format(e))

    def retornar(self) -> None:
        self.__controlador_sistema.abre_tela()

    def abre_tela(self) -> None:
        lista_opcoes = {1: self.incluir_clinica, 2: self.alterar_clinica,
                        3: self.lista_clinicas, 4: self.excluir_clinica,
                        5: self.vincular_profissional,
                        6: self.desvincular_profissional,
                        0: self.retornar}

        continua = True
        while continua:
            lista_opcoes[self.__tela_clinica.tela_opcoes()]()
