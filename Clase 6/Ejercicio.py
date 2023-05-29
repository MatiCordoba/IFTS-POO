import random

class Password:
    _CARACTERES_VALIDOS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ<=>@#%&+"
    _LONGITUD = 8

    def __init__(self, longitud=None):
        if longitud is not None:
            if longitud < 6 or longitud > 15:
                raise ValueError(f"La longitud de la contraseña debe estar entre 6 y 15 caracteres")
            self._longitud = longitud
        else:
            self._longitud = Password._LONGITUD
        self._contraseña = self.generarPassword()

    @property
    def contraseña(self):
        return self._contraseña

    @property
    def longitud(self):
        return self._longitud

    @property
    def esFuerte(self):
        mayusculas = 0
        minusculas = 0
        numeros = 0
        especiales = 0

        for x in self._contraseña:
            if x.isupper(): 
                mayusculas += 1
            elif x.islower(): 
                minusculas += 1
            elif x.isdigit(): 
                numeros += 1
            elif x in "<=>@#%&+": 
                especiales += 1

        return mayusculas > 1 and minusculas > 1 and numeros > 1 and especiales > 1

    def generarPassword(self):
        return ''.join(random.choice(Password._CARACTERES_VALIDOS) for i in range(self._longitud))

    def _str__(self):
        return f"La contraseña generada es: {self._contraseña}. Es fuerte: {self.esFuerte()}"

def main():
    lista = []
    cantidadContraseñas = int(input("Ingrese la cantidad de contraseñas a crear: "))

    for i in range(cantidadContraseñas):
        longitud = int(input(f"Ingrese la longitud de la contraseña {i+1}: "))
        if longitud == 0:
            password = Password()
        else: 
            password = Password(longitud)
        lista.append(password)
    
    for i, password in enumerate(lista, 1):
        print(f"Contraseña{i+1}: {password.contraseña} - Es fuerte: {password.esFuerte}")

main()