from abc import ABCMeta, classmethod

class CuentaBancaria(ABCMeta):
    def __init__(self, nro_cuenta:str, cbu: str, alias:str, saldo:float, movimientos:list, *args):
        self.__nro_cuenta = nro_cuenta
        self.__cbu = cbu
        self.__alias = alias
        self.__saldo = saldo
        self.__movimientos = movimientos
        self.args = args

    @property
    def nro_cuenta(self):
        return self.__nro_cuenta
    
    @nro_cuenta.setter
    def nro_cuenta(self, nro_cuenta):
        self.__nro_cuenta = nro_cuenta

    @property
    def cbu(self):
        return self.__cbu
    
    @cbu.setter
    def cbu(self, cbu):
        self.__cbu = cbu

    @property
    def alias(self):
        return self.__alias
    
    @alias.setter
    def alias(self, alias):
        self.__alias = alias

    @property
    def saldo(self):
        return self.__saldo
    
    @saldo.setter
    def saldo(self, saldo):
        self.__saldo = saldo

    @property
    def movimientos(self):
        return self.__movimientos
    
    @movimientos.setter
    def movimientos(self, movimientos):
        self.__movimientos = movimientos

class CajaDeAhorro(CuentaBancaria):
    pass

class CuentaCorriente(CuentaBancaria):
    pass

class Cliente:
    pass

class Banco:
    pass