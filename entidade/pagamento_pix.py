from datetime import date
from entidade.atendimento import Atendimento
from entidade.pagamento import Pagamento
from exceptions.dado_invalido_exception import DadoInvalidoException


class PagamentoPix(Pagamento):
    def __init__(self, codigo: int, data: date, atendimento: Atendimento,
                 valor_pago: float, cpf_pagador: str) -> None:
        super().__init__(codigo, data, atendimento, valor_pago)
        self.__cpf_pagador = None
        self.cpf_pagador = cpf_pagador

    @property
    def cpf_pagador(self) -> str:
        return self.__cpf_pagador

    @cpf_pagador.setter
    def cpf_pagador(self, cpf_pagador: str) -> None:
        if (not isinstance(cpf_pagador, str) or not cpf_pagador.isdigit()
                or len(cpf_pagador) != 11):
            raise DadoInvalidoException("CPF do pagador",
                                        "deve ter 11 digitos")
        self.__cpf_pagador = cpf_pagador

    def modalidade(self) -> str:
        return "PIX"

    def detalhes(self) -> str:
        return "CPF do pagador: {}".format(self.__cpf_pagador)
