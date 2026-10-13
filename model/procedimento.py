from model.profissional import Profissional


class Procedimento:
    def __init__(
        self,
        descricao: str,
        custo: float,
        profissional: Profissional,
    ) -> None:
        self.__descricao = descricao
        self.__custo = custo
        self.__profissional = profissional

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str) -> None:
        self.__descricao = descricao

    @property
    def custo(self) -> float:
        return self.__custo

    @custo.setter
    def custo(self, custo: float) -> None:
        self.__custo = custo

    @property
    def profissional(self) -> Profissional:
        return self.__profissional

    @profissional.setter
    def profissional(self, profissional: Profissional) -> None:
        self.__profissional = profissional