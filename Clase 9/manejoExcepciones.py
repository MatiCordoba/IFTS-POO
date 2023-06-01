# Realiza una función llamada agregar_una_vez(lista, elem) que reciba una lista y un elemento. La función debe añadir el elemento al final de la lista con la condición de no repetir ningún elemento. Si este elemento ya se encuentra en la lista se debe invocar un error de tipo ValueError que debes capturar y mostrar el siguiente mensaje en su lugar: 
#
# “Error: Imposible añadir elementos duplicados => [elemento]” 
#
# En una función main() inicializa la lista con: elementos = [1, 5, -2], luego intenta añadir los siguientes valores a la lista: 10, -2, "Hola". Para finalizar, muestra el contenido de la lista.

def agregar_una_vez(lista: list, elem):
    if elem in lista: 
        raise ValueError(f'Error: Imposible añadir elementos duplicados => {elem}')
    else: 
        lista.append(elem)

def main():
    elementos = [1, 5, -2]
    agregar_una_vez(elementos, 10)
    agregar_una_vez(elementos, -2)
    agregar_una_vez(elementos, "Hola")
    print(elementos)

main()