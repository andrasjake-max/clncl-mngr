from entidade.profissional_saude import ProfissionalSaude
from exceptions.dado_invalido_exception import DadoInvalidoException


class Procedimento:
    def __init__(self, codigo: int, descricao: str, custo: float,
                 profissional: ProfissionalSaude) -> None:
        self.__codigo = codigo
        self.__descricao = None
        self.__custo = None
        self.__profissional = None
        self.descricao = descricao
        self.custo = custo
        self.profissional = profissional

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str) -> None:
        if not isinstance(descricao, str) or not descricao.strip():
            raise DadoInvalidoException("descricao do procedimento",
                                        "nao pode ser vazia")
        self.__descricao = descricao.strip()

    @property
    def custo(self) -> float:
        return self.__custo

    @custo.setter
    def custo(self, custo: float) -> None:
        if not isinstance(custo, (int, float)) or custo < 0:
            raise DadoInvalidoException("custo",
                                        "deve ser um numero nao negativo")
        self.__custo = float(custo)

    @property
    def profissional(self) -> ProfissionalSaude:
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional: ProfissionalSaude) -> None:
        if not isinstance(profissional, ProfissionalSaude):
            raise DadoInvalidoException("profissional responsavel")
        self.__profissional = profissional
