from entidade.pessoa import Pessoa
from exceptions.dado_invalido_exception import DadoInvalidoException


class ProfissionalSaude(Pessoa):
    def __init__(self, nome: str, celular: str, cpf: str,
                 especialidade: str, registro_profissional: str) -> None:
        super().__init__(nome, celular, cpf)
        self.__especialidade = None
        self.__registro_profissional = None
        self.especialidade = especialidade
        self.registro_profissional = registro_profissional

    @property
    def especialidade(self) -> str:
        return self.__especialidade

    @especialidade.setter
    def especialidade(self, especialidade: str) -> None:
        if not isinstance(especialidade, str) or not especialidade.strip():
            raise DadoInvalidoException("especialidade", "nao pode ser vazia")
        self.__especialidade = especialidade.strip()

    @property
    def registro_profissional(self) -> str:
        return self.__registro_profissional

    @registro_profissional.setter
    def registro_profissional(self, registro_profissional: str) -> None:
        if (not isinstance(registro_profissional, str)
                or not registro_profissional.strip()):
            raise DadoInvalidoException("registro profissional",
                                        "nao pode ser vazio")
        self.__registro_profissional = registro_profissional.strip()

    def tipo(self) -> str:
        return "Profissional de saude"
