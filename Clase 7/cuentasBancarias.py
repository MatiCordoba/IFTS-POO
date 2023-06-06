from abc import ABC, abstractmethod
from datetime import date

class CuentaBancaria(ABC):
    def __init__(self, nro_cuenta, cbu, alias, saldo):
        self.__nro_cuenta = nro_cuenta
        self.__cbu = cbu
        self.__alias = alias
        self.__saldo = saldo
        self.__movimientos = []

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

    def consultar_saldo(self):
        return self.__saldo
    
    def depositar(self, monto_a_depositar):
        nuevo_saldo = self.__saldo + monto_a_depositar
        if monto_a_depositar > 0:
            self.__movimientos.append((date.today(), "deposito", monto_a_depositar, nuevo_saldo))
            self.__saldo += monto_a_depositar 
            return True
        else:
            return False

    @abstractmethod
    def extraer(self, monto_a_extraer):
        pass

    @abstractmethod
    def transferir(self, monto_a_transferir, cuenta_destino):
        pass


class CajaDeAhorro(CuentaBancaria):
    def __init__(self, nro_cuenta, cbu, alias, saldo, monto_limite_extracciones, monto_limite_transferencias, cant_extracciones_disponibles, cant_transferencias_disponibles):
        super().__init__(nro_cuenta, cbu, alias, saldo)
        self.__monto_limite_extracciones = monto_limite_extracciones
        self.__monto_limite_transferencias = monto_limite_transferencias
        self.__cant_extracciones_disponibles = cant_extracciones_disponibles
        self.__cant_transferencias_disponibles = cant_transferencias_disponibles

    @property
    def monto_limite_extracciones(self):
        return self.__monto_limite_extracciones
    
    @monto_limite_extracciones.setter
    def monto_limite_extracciones(self, monto_limite_extracciones):
        self.__monto_limite_extracciones = monto_limite_extracciones

    @property
    def monto_limite_transferencias(self):
        return self.__monto_limite_transferencias
    
    @monto_limite_transferencias.setter
    def monto_limite_transferencias(self, monto_limite_transferencias):
        self.__monto_limite_transferencias = monto_limite_transferencias

    @property
    def cant_extracciones_disponibles(self):
        return self.__cant_extracciones_disponibles
    
    @cant_extracciones_disponibles.setter
    def cant_extracciones_disponibles(self, cant_extracciones_disponibles):
        self.__cant_extracciones_disponibles = cant_extracciones_disponibles

    @property
    def cant_transferencias_disponibles(self):
        return self.__cant_transferencias_disponibles
    
    @cant_transferencias_disponibles.setter
    def cant_transferencias_disponibles(self, cant_transferencias_disponibles):
        self.__cant_transferencias_disponibles = cant_transferencias_disponibles

    def extraer(self, monto_a_extraer):
        if monto_a_extraer > 0 and monto_a_extraer <= self.saldo and monto_a_extraer <= self.monto_limite_extracciones and self.cant_extracciones_disponibles > 0:
            nuevo_saldo = self.saldo - monto_a_extraer
            self.movimientos.append((date.today(), "extracción", monto_a_extraer, nuevo_saldo))
            self.saldo = nuevo_saldo
            self.cant_extracciones_disponibles -= 1
            return True
        else:
            return False

    def transferir(self, monto_a_transferir, cuenta_destino):
        if monto_a_transferir > 0 and monto_a_transferir <= self.saldo and monto_a_transferir <= self.monto_limite_transferencias and self.cant_transferencias_disponibles > 0:
            nuevo_saldo_origen = self.saldo - monto_a_transferir
            nuevo_saldo_destino = cuenta_destino.saldo + monto_a_transferir
            self.movimientos.append((date.today(), "transferencia", monto_a_transferir, nuevo_saldo_origen))
            self.saldo = nuevo_saldo_origen
            cuenta_destino.saldo = nuevo_saldo_destino
            self.cant_transferencias_disponibles -= 1
            return True
        else:
            return False

class CuentaCorriente(CuentaBancaria):
    def __init__(self, nro_cuenta, cbu, alias, saldo, monto_maximo_descubierto):
        super().__init__(nro_cuenta, cbu, alias, saldo)
        self.__monto_maximo_descubierto = monto_maximo_descubierto

    @property
    def monto_maximo_descubierto(self):
        return self.__monto_maximo_descubierto
    
    @monto_maximo_descubierto.setter
    def monto_maximo_descubierto(self, monto_maximo_descubierto):
        self.__monto_maximo_descubierto = monto_maximo_descubierto

    def extraer(self, monto_a_extraer):
        if monto_a_extraer > 0 and monto_a_extraer <= (self.saldo + self.monto_maximo_descubierto):
            nuevo_saldo = self.saldo - monto_a_extraer
            self.movimientos.append((date.today(), "extracción", monto_a_extraer, nuevo_saldo))
            self.saldo = nuevo_saldo
            return True
        else:
            return False

    def transferir(self, monto_a_transferir, cuenta_destino):
        if monto_a_transferir > 0 and monto_a_transferir <= (self.saldo + self.monto_maximo_descubierto):
            nuevo_saldo_origen = self.saldo - monto_a_transferir
            nuevo_saldo_destino = cuenta_destino.saldo + monto_a_transferir
            self.movimientos.append((date.today(), "transferencia", monto_a_transferir, nuevo_saldo_origen))
            self.saldo = nuevo_saldo_origen
            cuenta_destino.saldo = nuevo_saldo_destino
            return True
        else:
            return False

class Cliente:
    def __init__(self, razon_social, cuit, tipo_persona, domicilio):
        self.__razon_social = razon_social
        self.__cuit = cuit
        self.__tipo_persona = tipo_persona
        self.__domicilio = domicilio
        self.cuentas_bancarias = []

    @property
    def razon_social(self):
        return self.__razon_social
    
    @razon_social.setter
    def razon_social(self, razon_social):
        self.__razon_social = razon_social

    @property
    def cuit(self):
        return self.__cuit
    
    @cuit.setter
    def cuit(self, cuit):
        self.__cuit = cuit

    @property
    def tipo_persona(self):
        return self.__tipo_persona
    
    @tipo_persona.setter
    def tipo_persona(self, tipo_persona):
        self.__tipo_persona = tipo_persona

    @property
    def domicilio(self):
        return self.__domicilio
    
    @domicilio.setter
    def domicilio(self, domicilio):
        self.__domicilio = domicilio

    def crear_nueva_cuenta_bancaria(self, tipo_cuenta, nro_cuenta, alias, cbu, saldo, *args):
        if tipo_cuenta == "CajaDeAhorro":
            cuenta = CajaDeAhorro(nro_cuenta, cbu, alias, saldo, *args)
        elif tipo_cuenta == "CuentaCorriente":
            cuenta = CuentaCorriente(nro_cuenta, cbu, alias, saldo, *args)
        else:
            return False
        self.cuentas_bancarias.append(cuenta)
        return True

class Banco:
    def __init__(self, nombre, domicilio):
        self.__nombre = nombre
        self.__domicilio = domicilio
        self.clientes = []

    @property
    def nombre(self):
        return self.__nombre
    
    @nombre.setter
    def nombre(self, nombre):
        self.__nombre = nombre

    @property
    def domicilio(self):
        return self.__domicilio
    
    @domicilio.setter
    def domicilio(self, domicilio):
        self.__domicilio = domicilio

    def crear_nuevo_cliente(self, razon_social, cuit, tipo_persona, domicilio):
        cliente = Cliente(razon_social, cuit, tipo_persona, domicilio)
        self.clientes.append(cliente)
        return True


# Validación del modelo de gestión bancaria

def main():
    banco = Banco("Mi Banco", "Calle Principal 123")

    cliente1 = Cliente("Cliente 1", "1234567890", "Física", "Calle A 1")
    cliente2 = Cliente("Cliente 2", "0987654321", "Jurídica", "Calle B 2")
    cliente3 = Cliente("Cliente 3", "1111111111", "Física", "Calle C 3")

    cliente1.crear_nueva_cuenta_bancaria("CajaDeAhorro", "111111", "Alias1", "CBU1", 1000.0, 200, 5000, 68, 76)
    cliente1.crear_nueva_cuenta_bancaria("CuentaCorriente", "222222", "Alias2", "CBU2", 2000.0, 100)
    cliente2.crear_nueva_cuenta_bancaria("CajaDeAhorro", "333333", "Alias3", "CBU3", 500.0, 100, 6000, 68, 76)
    cliente2.crear_nueva_cuenta_bancaria("CuentaCorriente", "444444", "Alias4", "CBU4", 1500.0, 3000.0)
    cliente3.crear_nueva_cuenta_bancaria("CajaDeAhorro", "555555", "Alias5", "CBU5", 200.0, 100, 6000, 68, 76)
    cliente3.crear_nueva_cuenta_bancaria("CuentaCorriente", "666666", "Alias6", "CBU6", 1000.0, 2000.0)

    banco.clientes.append(cliente1)
    banco.clientes.append(cliente2)
    banco.clientes.append(cliente3)

    cliente1.cuentas_bancarias[0].depositar(500.0)
    cliente1.cuentas_bancarias[0].extraer(200.0)
    cliente1.cuentas_bancarias[0].transferir(300.0, cliente2.cuentas_bancarias[0])

    cliente2.cuentas_bancarias[1].depositar(1000.0)
    cliente2.cuentas_bancarias[1].extraer(500.0)
    cliente2.cuentas_bancarias[1].transferir(700.0, cliente3.cuentas_bancarias[1])

    for cliente in banco.clientes:
        print("Cliente:", cliente.razon_social)
        print("CUIT:", cliente.cuit)
        print("Tipo de persona:", cliente.tipo_persona)
        print("Domicilio:", cliente.domicilio)
        print("Cuentas bancarias:")
        for cuenta in cliente.cuentas_bancarias:
            print(" - Nro. de cuenta:", cuenta.nro_cuenta)
            print("   Alias:", cuenta.alias)
            print("   CBU:", cuenta.cbu)
            print("   Saldo:", cuenta.consultar_saldo())
            print("   Movimientos:")
            for movimiento in cuenta.movimientos:
                print("     - Fecha:", movimiento[0])
                print("       Tipo:", movimiento[1])
                print("       Monto:", movimiento[2])
                print("       Saldo:", movimiento[3])
        print()

main()