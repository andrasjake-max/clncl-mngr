from datetime import date
from model.paciente import Paciente


class Pagamento:
    def __init__(self, data: date, valor: float, parcelas: int):
        self.__data = data
        self.__valor = valor
        self.__parcelas = parcelas
        self.__tipo = f"Parcelado em {parcelas}x" if parcelas > 1 else "À vista"
        self.__valor_pago = valor

    @property
    def data(self) -> date:
        return self.__data

    @data.setter
    def data(self, data: date) -> None:
        self.__data = data

    @property
    def valor(self) -> float:
        return self.__valor

    @valor.setter
    def valor(self, valor: float) -> None:
        self.__valor = valor

    @property
    def parcelas(self) -> int:
        return self.__parcelas

    @parcelas.setter
    def parcelas(self, parcelas: int) -> None:
        self.__parcelas = parcelas

    @property
    def tipo(self):
        return self.__tipo

    def efetuar_pagamento(self, valor):
        self.__valor_pago += valor