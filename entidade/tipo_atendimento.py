from exceptions.dado_invalido_exception import DadoInvalidoException


class TipoAtendimento:
    def __init__(self, codigo: int, nome: str, descricao: str) -> None:
        self.__codigo = codigo
        self.__nome = None
        self.__descricao = None
        self.nome = nome
        self.descricao = descricao

    @property
    def codigo(self) -> int:
        return self.__codigo

    @property
    def nome(self) -> str:
        return self.__nome

    @nome.setter
    def nome(self, nome: str) -> None:
        if not isinstance(nome, str) or not nome.strip():
            raise DadoInvalidoException("nome do tipo", "nao pode ser vazio")
        self.__nome = nome.strip()

    @property
    def descricao(self) -> str:
        return self.__descricao

    @descricao.setter
    def descricao(self, descricao: str) -> None:
        if not isinstance(descricao, str):
            raise DadoInvalidoException("descricao")
        self.__descricao = descricao.strip()
