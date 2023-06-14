from abc import ABC, abstractmethod
from datetime import datetime

class CuentaBancaria(ABC):
    def __init__(self, nro_cuenta, cbu, alias, saldo, titular):
        self.nro_cuenta = nro_cuenta
        self.cbu = cbu
        self.alias = alias
        self.saldo = saldo
        self.titular = titular
        self.movimientos = []
    
    @property
    def nro_cuenta (self):
        return self.__nro_cuenta
    
    @nro_cuenta.setter
    def nro_cuenta (self, value):
        self.__nro_cuenta = value
    
    @property
    def cbu (self):
        return self.__cbu
    
    @cbu.setter
    def cbu (self, value):
        self.__cbu = value
    
    @property
    def alias (self):
        return self.__alias
    
    @alias.setter
    def alias (self, value):
        self.__alias = value

    @property
    def saldo (self):
        return self.__saldo
    
    @saldo.setter
    def saldo (self, value):
        self.__saldo = value
    
    @property
    def titular (self):
        return self.__titular
    
    @titular.setter
    def titular (self, value):
        self.__titular = value
    
    @property
    def movimientos (self):
        return self.__movimientos
    
    @movimientos.setter
    def movimientos (self, value):
        self.__movimientos = value

    def consultar_saldo (self):
        return self.saldo
    
    def depositar (self, monto_depositar):
        if monto_depositar > 0:
            self.saldo += monto_depositar
            fecha = datetime.now().strftime("%d/%m/%Y")
            self.movimientos.append((fecha, "depósito", monto_depositar, self.saldo))
            print(f"Se han depositado $ {monto_depositar} en la cuenta.")
            return True
        else:
            return False
    
    @abstractmethod
    def extraer (self, monto_extraer):
        fecha = datetime.now().strftime("%d/%m/%Y")
        self.movimientos.append((fecha, "extraer", monto_extraer, self.saldo))
        print(f"Se ha extraido $ {monto_extraer} de la cuenta.")
    
    @abstractmethod
    def transferir (self, monto_transferir, cuenta_destino):
        fecha = datetime.now().strftime("%d/%m/%Y")
        self.movimientos.append((fecha, "transferir", monto_transferir, self.saldo))
        print(f"Se ha transferido $ {monto_transferir} de la cuenta.")

class CajaAhorro(CuentaBancaria):
    def __init__ (self, nro_cuenta, cbu, alias, saldo, titular, monto_limite_extracciones=50000, monto_limite_transferencias=100000, cant_extracciones_disponibles=5, cant_transferencias_disponibles=5):
        super().__init__(nro_cuenta, cbu, alias, saldo, titular)
        self.monto_limite_extracciones = monto_limite_extracciones
        self.monto_limite_transferencias = monto_limite_transferencias
        self.cant_extracciones_disponibles = cant_extracciones_disponibles
        self.cant_transferencias_disponibles = cant_transferencias_disponibles
        print("Caja de ahorro creada correctamente. Titular:", titular)
    
    @property
    def monto_limite_extracciones (self):
        return self.__monto_limite_extracciones
    
    @monto_limite_extracciones.setter
    def monto_limite_extracciones (self, value):
        self.__monto_limite_extracciones = value
    
    @property
    def monto_limite_transferencias (self):
        return self.__monto_limite_transferencias
    
    @monto_limite_transferencias.setter
    def monto_limite_transferencias (self, value):
        self.__monto_limite_transferencias = value
    
    @property
    def cant_extracciones_disponibles (self):
        return self.__cant_extracciones_disponibles
    
    @cant_extracciones_disponibles.setter
    def cant_extracciones_disponibles (self, value):
        self.__cant_extracciones_disponibles = value
    
    @property
    def cant_transferencias_disponibles (self):
        return self.__cant_transferencias_disponibles
    
    @cant_transferencias_disponibles.setter
    def cant_transferencias_disponibles (self, value):
        self.__cant_transferencias_disponibles = value
    
    def extraer (self, monto_extraer):
        if (monto_extraer > 0 and monto_extraer <= self.saldo and monto_extraer <= self.monto_limite_extracciones and self.cant_extracciones_disponibles > 0 ):
            self.saldo -= monto_extraer
            super().extraer(monto_extraer)
            return True
        else:
            return False
    
    def transferir (self, monto_transferir, cuenta_destino):
        if (monto_transferir > 0 and monto_transferir <= self.saldo and monto_transferir <= self.monto_limite_transferencias and self.cant_transferencias_disponibles > 0 ):
            self.saldo -= monto_transferir
            cuenta_destino.depositar(monto_transferir)
            #cuenta_destino.saldo += monto_transferir
            super().transferir(monto_transferir, cuenta_destino)
            return True
        else:
            return False

class CuentaCorriente(CuentaBancaria):
    def __init__ (self, nro_cuenta, cbu, alias, saldo, titular, monto_maximo_descubierto=10000):
        super().__init__(nro_cuenta, cbu, alias, saldo, titular)
        self.monto_maximo_descubierto = monto_maximo_descubierto
        print("Cuenta Corriente creada correctamente. Titular:", titular)
    
    @property
    def monto_maximo_descubierto (self):
        return self.__monto_maximo_descubierto
    
    @monto_maximo_descubierto.setter
    def monto_maximo_descubierto (self, value):
        self.__monto_maximo_descubierto = value
    
    def extraer (self, monto_extraer):
        if (monto_extraer > 0 and monto_extraer <= self.saldo + self.monto_maximo_descubierto):
            self.saldo -= monto_extraer
            super().extraer(monto_extraer)
            return True
        return False
    
    def transferir (self, monto_transferir, cuenta_destino):
        if (monto_transferir > 0 and monto_transferir <= self.saldo + self.monto_maximo_descubierto):
            self.saldo -= monto_transferir
            cuenta_destino.depositar(monto_transferir)
            #cuenta_destino.saldo += monto_transferir
            super().transferir(monto_transferir, cuenta_destino)
            return True
        else:
            return False

class Cliente():
    def __init__(self, razon_social, cuit, tipo_persona, domicilio):
        self.razon_social = razon_social
        self.cuit = cuit
        self.tipo_persona = tipo_persona
        self.domicilio = domicilio
        self.cuentas_bancarias = []
        print ("Cliente creado correctamente. Razon social:", razon_social)
    
    @property
    def razon_social (self):
        return self.__razon_social
    
    @razon_social.setter
    def razon_social (self, value):
        self.__razon_social = value
    
    @property
    def cuit (self):
        return self.__cuit
    
    @cuit.setter
    def cuit (self, value):
        self.__cuit = value

    @property
    def tipo_persona (self):
        return self.__tipo_persona
    
    @tipo_persona.setter
    def tipo_persona (self, value):
        self.__tipo_persona = value
    
    @property
    def domicilio (self):
        return self.__domicilio
    
    @domicilio.setter
    def domicilio (self, value):
        self.__domicilio = value

    @property
    def cuentas_bancarias (self):
        return self.__cuentas_bancarias
    
    @cuentas_bancarias.setter
    def cuentas_bancarias (self, value):
        self.__cuentas_bancarias = value
    
    def crear_nueva_cuenta_bancaria (self, tipo_cuenta, nro_cuenta, alias, cbu, saldo):
        if tipo_cuenta == "CA":
            cuenta = CajaAhorro(nro_cuenta, alias, cbu, saldo, self.razon_social)
        else: # tipo de cuenta: "Cuenta Corriente"
            cuenta = CuentaCorriente(nro_cuenta, alias, cbu, saldo, self.razon_social)
        self.__cuentas_bancarias.append(cuenta)

class Banco:
    def __init__(self, nombre, domicilio):
        self.nombre = nombre
        self.domicilio = domicilio
        self.clientes = []
        print ("Banco creado correctamente. Nombre:", nombre)

    @property
    def nombre(self):
        return self.__nombre

    @nombre.setter
    def nombre(self, value):
        self.__nombre = value

    @property
    def domicilio(self):
        return self.__domicilio

    @domicilio.setter
    def domicilio(self, value):
        self.__domicilio = value

    @property
    def clientes(self):
        return self.__clientes
    
    @clientes.setter
    def clientes(self, value):
        self.__clientes = value

    def crear_nuevo_cliente(self, razon_social, cuit, tipo_persona, domicilio):
        nuevo_cliente = Cliente(razon_social, cuit, tipo_persona, domicilio)
        self.__clientes.append(nuevo_cliente)
        return True

def main():
    banco = Banco("Banco Narnia", "El reino 2580, Narnia")
    banco.crear_nuevo_cliente("Aslan","20652451022","Física","Narnia 500")
    banco.crear_nuevo_cliente("Caspian","20471554002","Física","Narnia 680")
    banco.crear_nuevo_cliente("Tumnus","20305355012","Física","Narnia 250")
    
    for cliente in banco.clientes:
        print("Cliente: ",cliente.razon_social)
    
    banco.clientes[0].crear_nueva_cuenta_bancaria("CA", "523203250", "1000584002800036", "ca.aslan.narnia", 200000)
    banco.clientes[0].crear_nueva_cuenta_bancaria("CC", "412052300", "1000584002800037", "cc.aslan.narnia", 200000)

    banco.clientes[1].crear_nueva_cuenta_bancaria("CA", "847785801", "1000584002800038", "ca.caspian.narnia", 0)
    banco.clientes[1].crear_nueva_cuenta_bancaria("CC", "100052555", "1000584002800039", "cc.caspian.narnia", 0)

    banco.clientes[2].crear_nueva_cuenta_bancaria("CA", "444626588", "1000584002800040", "ca.tumnus.narnia", 0)
    banco.clientes[2].crear_nueva_cuenta_bancaria("CC", "778455747", "1000584002800041", "cc.tumnus.narnia", 0)

    for cuenta in banco.clientes[0].cuentas_bancarias:
        print(f"Cuenta - Nro: {cuenta.nro_cuenta} - Alias: {cuenta.alias}")

    banco.clientes[0].cuentas_bancarias[0].depositar(50000)
    banco.clientes[0].cuentas_bancarias[0].extraer(10000)
    banco.clientes[0].cuentas_bancarias[0].transferir(20000, banco.clientes[1].cuentas_bancarias[0])

    print("\nMovimientos de la cuenta Nro",banco.clientes[0].cuentas_bancarias[0].nro_cuenta)
    for mov in banco.clientes[0].cuentas_bancarias[0].movimientos:
        print(mov)
    
    print("\nMovimientos de la cuenta Nro",banco.clientes[1].cuentas_bancarias[0].nro_cuenta)
    for mov in banco.clientes[1].cuentas_bancarias[0].movimientos:
        print(mov)

if __name__ == "__main__":
    main()