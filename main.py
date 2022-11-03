# This is a sample Python script.

# Press Mayús+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import re
import string
from sys import stdin

from unicodedata import normalize

tipoViaUrbana = ['CARRERA', 'CUENTAS CORRIDAS', 'AVENIDA CARRERA', 'AVENIDA CALLE', 'CIRCUNVALAR', 'AVENIDA CLL',
            'AVENIDA CRA', 'AVENIDA KRA', 'TRANSVERSAL', 'AVENIDA CL', 'AVENIDA KR', 'AVENIDA CR', 'CARRETERA',
            'AUTOPISTA', 'AVENIDA C', 'AVENIDA K', 'CIRCULAR', 'DIAGONAL', 'GLORIETA', 'CALLEJON', 'PEATONAL',
            'VARIANTE', 'AVENIDA', 'BULEVAR', 'TRONCAL', 'PASAJE', 'CELULA',
            'CALLE', 'PASEO', 'TRANS', 'DIAG', 'CRA', 'KRA', 'CLL', 'CIR', 'CRV', 'AUT', 'VIA', 'CLJ', 'CEL',
            'KR', 'CR', 'CL', 'CT', 'CQ', 'CV', 'CC', 'AU', 'AV', 'AC', 'AK', 'BL', 'DG', 'PJ', 'PS', 'PT', 'TV', 'TR',
            'TC', 'VT', 'VI', 'DK', 'DC', 'GT']

tipoViaRural = ['CORREGIMIENTO', 'ANILLO VIAL', 'CARRETERA', 'KILOMETRO', 'PROPIEDAD',
                   'MUNICIPIO', 'HACIENDA', 'VARIANTE', 'ENTRADA', 'CASERIO'
                                                                   'CAMINO', 'BARRIO', 'PREDIO', 'SECTOR', 'HANGAR',
                   'VEREDA', 'MUELLE',
                   'FINCA', 'AVIAL', 'CARR', 'CASA', 'CORR', 'LOTE', 'BRR', 'FCA',
                   'MCP', 'SEC', 'VTE', 'VDA', 'VRD', 'VIA', 'MLL', 'CN', 'CT',
                   'CA', 'CS', 'BR', 'EN', 'FI', 'HC', 'HG', 'KM',
                   'PD', 'LT', 'SC', 'VT', 'VI', 'VR']

salida = ''
validacion = True
auxS = False

exprNumerica = re.compile("[0-9]")


def existeSimboloMas(direccion, pos):
    print('simbolo +')
    global validacion
    global mensaje

    if len(direccion) < pos + 1:
        validacion = False
        mensaje += '1'
        estadoFinal(direccion, pos)
    elif direccion[pos] == ' ':
        existeSimboloMas(direccion, pos + 1)
    elif exprNumerica.match(direccion[pos]) or direccion[pos] == 'm':
        estadoRural2(direccion, pos + 1)
    elif direccion[pos] == ' ' and exprNumerica.match(direccion[pos]):
        mensaje += '0'
        validacion = False
        estadoRural2(direccion, pos + 1)
    elif direccion[pos] in string.ascii_lowercase:
        mensaje += '1'
        validacion = False
        estadoFinal(direccion, pos)


def existeNomKM(direccion, pos):
    print('val km')
    global validacion
    global mensaje

    if len(direccion) < pos + 1:
        validacion = False
        mensaje += '1'
        estadoFinal(direccion, pos)
    elif direccion[pos] == ' ':
        existeNomKM(direccion, pos + 1)
    elif exprNumerica.match(direccion[pos]):
        # Existe un numero despues de Km
        existeNomKM(direccion, pos + 1)
    # Validar numeros adicionales en la direccion despues del simbolo +
    elif (direccion[pos - 1] == '+' or direccion[pos] == '+' or direccion[pos:pos + 3] == 'mas') and (
            exprNumerica.match(direccion[pos - 1]) or exprNumerica.match(direccion[pos - 2])):
        if direccion[pos:pos + 3] == 'MAS':
            validacion = False
            # Existe palabra mas
            existeSimboloMas(direccion, pos + 3)
        else:
            validacion = False
            # Existe simbolo +
            existeSimboloMas(direccion, pos + 1)
    # Existencia de otra nomenclatura
    elif direccion[pos] in string.ascii_lowercase:
        for i in tipoViaRural:
            if direccion[pos:pos + len(i)] in tipoViaRural:
                validacion = False
                estadoRural3(direccion, pos + len(i))
                return True
    else:
        mensaje += '2'
        estadoFinal(direccion, pos)

def estadoRural4(direccion, pos):
    print('rul 4')
    # Validar complementos
    global validacion
    global mensaje
    if len(direccion) < pos + 1:
        # Estado Final minimo rural
        print('u')
        mensaje += '1'
        validacion = True
        print(validacion)
        estadoFinal(direccion, pos + 1)

    elif direccion[pos] in string.ascii_lowercase or exprNumerica.match(direccion[pos]) or direccion[pos] == ' ':
        mensaje += '0'
        validacion = True
        estadoRural4(direccion, pos + 1)


def estadoRural3(direccion, pos):
    print('rul 3')
    global mensaje
    global validacion

    if direccion[pos] == ' ':
        validacion = False
        mensaje += '0'
        estadoRural3(direccion, pos + 1)
    else:
        validacion = False
        mensaje += '0'
        estadoRural4(direccion, pos)


def estadoRural2(direccion, pos):
    global validacion
    global mensaje
    if len(direccion) < pos + 1:
        mensaje += '1'
        validacion = False
        estadoFinal(direccion, pos)
    elif direccion[pos] == ' ':
        estadoRural2(direccion, pos + 1)
    elif direccion[pos] in string.ascii_lowercase or exprNumerica.match(direccion[pos]):
        for i in tipoViaRural:
            if direccion[pos:pos + len(i)] in tipoViaRural:
                validacion = False
                # Segunda nomenclatura
                estadoRural3(direccion, pos + len(i))
                return True
        validacion = False
        estadoRural2(direccion, pos + 1)


def estadoInicioRural(direccion, pos):
    if direccion.startswith('kilometro') or direccion.startswith('kilom') or direccion.startswith('km'):
        existeNomKM(direccion, pos)
    else:
        estadoRural2(direccion, pos + 1)


#------------------------------------------------

def estadoInicioUrbano(direccion, pos):
    global salida
    global validacion

    if len(direccion) == pos:
        salida += '1'
        validacion = False
        #Tamaño minimo no valido
        estadoFinal(direccion, pos)
    elif direccion[pos] == ' ':
        estadoUrbano2(direccion, pos)
    elif direccion[pos + 1] in string.ascii_uppercase:
        salida += '0'
        estadoUrbano2(direccion, pos)
    elif direccion[pos] in string.ascii_uppercase or exprNumerica.match(direccion[pos]):
        salida += '0'
        estadoUrbano2(direccion, pos)
    else:
        return 'La direccion '+direccion+" es invalida para la nomenclatura Colombiana"

def estadoUrbano2(direccion, pos):
    global salida
    global validacion

    if len(direccion) < pos + 1:
        salida += '1'
        validacion = False
        # Tamaño minimo no valido
        estadoFinal(direccion, pos)
    elif direccion[pos] == ' ':
        estadoUrbano2(direccion, pos + 1)
    elif exprNumerica.match(direccion[pos]):
        salida += '0'
        #Via principal numerica
        estadoUrbano2(direccion, pos + 1)
    elif direccion[pos] in string.ascii_uppercase:
        #Via principal alfabetica
        estadoUrbano3(direccion, pos)

    #Validacion del simbolo de la via generadora
    elif direccion[pos:pos + 6] == 'NUMERO':
        salida += '0'
        validacion = False
        estadoUrbanoCard(direccion, pos + 6)
    elif direccion[pos:pos + 3] == 'NO.' or direccion[pos:pos + 3] == 'NRO' or direccion[pos:pos + 3] == 'NUM':
        salida += '0'
        validacion = False
        estadoUrbanoCard(direccion, pos + 2)
    elif direccion[pos:pos + 2] == 'NO' or direccion[pos:pos + 2] == 'N°' or direccion[pos:pos + 2] == 'N.' or \
            direccion[pos:pos + 2] == 'N.º':
        salida += '0'
        validacion = False
        estadoUrbanoCard(direccion, pos + 2)
    elif direccion[pos] == 'N' or direccion[pos] == '#' or direccion[pos] == '-':
        salida += '0'
        validacion = False
        estadoUrbanoNumPlaca(direccion, pos + 1)

def estadoUrbano3(direccion, pos):
    global salida
    global validacion

    if len(direccion) < pos + 1:
        validacion = False
        salida += '1'
        # Tamaño minimo no valido
        estadoFinal(direccion, pos)
    elif direccion[pos:pos + 3] == 'BIS':
        validacion = False
        salida += '0'
        estadoUrbanoBis(direccion, pos + 3)
    elif direccion[pos:pos + 4] == 'ESTE':
        salida += '0'
        estadoUrbanoCard(direccion, pos + 4)
    elif direccion[pos:pos + 5] == 'NORTE' or direccion[pos:pos + 5] == 'OESTE':
        salida += '0'
        validacion = False
        estadoUrbanoCard(direccion, pos + 5)
    elif direccion[pos:pos + 3] == 'SUR':
        salida += '0'
        validacion = False
        estadoUrbanoCard(direccion, pos + 3)
    elif direccion[pos] in string.ascii_uppercase or direccion[pos] == ' ':
        salida += '0'
        validacion = False
        estadoUrbano3(direccion, pos + 1)
    else:
        estadoUrbanoSinComp(direccion, pos)


def estadoUrbanoSinComp(direccion, pos):
    global salida
    if len(direccion) < pos + 1:
        salida += '1'
        # Tamaño minimo no valido
        estadoFinal(direccion, pos)
    elif direccion[pos] == ' ':
        estadoUrbanoSinComp(direccion, pos + 1)
    elif direccion[pos:pos + 2] == 'BIS':
        salida += '0'
        estadoUrbanoBis(direccion, pos + 2)
    else:
        estadoUrbanoCard(direccion, pos)

def estadoUrbanoBis(direccion, pos):
    global salida
    global validacion
    if len(direccion) < pos + 1:
        validacion = validacion
        salida += '1'
        # Tamaño minimo no valido
        estadoFinal(direccion, pos)
    elif direccion[pos] == ' ' or direccion[pos] == '#':
        estadoUrbanoBis(direccion, pos + 1)
    elif direccion[pos] == ' ' or exprNumerica.match(direccion[pos]):
        #Bis sin letras
        estadoUrbanoCard(direccion, pos)
    elif direccion[pos] in string.ascii_uppercase:
        #Bis con letra, letra-letra, letra-numero-letra, cardinalidad
        estadoUrbanoBisCompl(direccion, pos)


def estadoUrbanoBisCompl(direccion, pos):
    global salida
    global validacion
    if len(direccion) < pos + 1:
        validacion = validacion
        salida += '1'
        # Tamaño minimo no valido
        estadoFinal(direccion, pos)
    elif direccion[pos] == ' ':
        estadoUrbanoBisCompl(direccion, pos + 1)
    elif direccion[pos:pos + 5] == 'NORTE' or direccion[pos:pos + 4] == 'ESTE' or direccion[pos:pos + 5] == 'OESTE' \
            or direccion[ pos:pos + 3] == 'SUR':
        if direccion[pos:pos + 5] == 'NORTE':
            salida += '0'
            estadoUrbanoCard(direccion, pos + 5)
        elif direccion[pos:pos + 4] == 'ESTE':
            salida += '0'
            estadoUrbanoCard(direccion, pos + 4)
        elif direccion[pos:pos + 5] == 'OESTE':
            salida += '0'
            estadoUrbanoCard(direccion, pos + 5)
        elif direccion[pos:pos + 3] == 'SUR':
            salida += '0'
            estadoUrbanoCard(direccion, pos + 3)
    elif (direccion[pos:pos + 3] in string.ascii_uppercase) and \
            (direccion[pos:pos + 5] != 'NORTE' or direccion[pos:pos + 4] != 'ESTE' or
             direccion[pos:pos + 5] != 'OESTE' or direccion[pos:pos + 3] != 'SUR') \
            and len(direccion[pos:pos + 3]) == 3:
        salida += '1'
        validacion = False
        #Bis con 3 letras
        estadoUrbanoCard(direccion, pos + 3)
    elif len(direccion[pos:pos + 3]) == 3 and direccion[pos] in string.ascii_uppercase and direccion[
        pos + 1] in string.ascii_uppercase and exprNumerica.match(direccion[pos + 2]):
        #Bis letra-letra-numero
        salida += '1'
        estadoUrbanoCard(direccion, pos + 1)
    elif len(direccion[pos:pos + 2]) == 2 and direccion[pos] in string.ascii_uppercase and \
            direccion[pos + 1] in string.ascii_uppercase:
        for i in tipoViaUrbana:
            if direccion[pos:pos + len(i)] in tipoViaUrbana:
                #Con via nomenclatura via generadora
                estadoUrbanoCard(direccion, pos + len(i))
                break
        salida += '0'
        #Bis letra-letra
        estadoUrbanoCard(direccion, pos + 2)
    elif exprNumerica.match(direccion[pos]) and exprNumerica.match(direccion[pos + 1]):
        salida += '0'
        #Bis letra-numero
        estadoUrbanoBisCompl(direccion, pos + 1)
    elif len(direccion[pos:pos]) >= 3 and (
            direccion[pos] in string.ascii_uppercase and exprNumerica.match(
            direccion[pos + 1]) or exprNumerica.match(direccion[pos + 1]) and exprNumerica.match(direccion[pos])):
        #Bis alfanumerico
        estadoUrbanoBisCompl(direccion, pos + 1)
    elif len(direccion[pos:pos + 3]) == 3 and (exprNumerica.match(direccion[pos - 1]) and direccion[
        pos + 1] in string.ascii_uppercase or exprNumerica.match(direccion[pos]) and direccion[
                                                             pos + 1] in string.ascii_uppercase):
        #Bis letra-numero-letra
        salida += '0'
        estadoUrbanoCard(direccion, pos + 1)
    elif direccion[pos] in string.ascii_uppercase or direccion[pos + 1] == ' ':
        #Bis letra
        estadoUrbanoCard(direccion, pos + 1)
    else:
        #Solo bis
        estadoUrbanoCard(direccion, pos + 1)


def estadoUrbanoCard(direccion, pos):
    global auxS
    global salida
    global validacion

    if len(direccion) < pos + 1:
        if (direccion[pos - 1] == '-' or direccion[pos - 1] == ' ' or exprNumerica.match(direccion[pos - 1])) \
                and (direccion[pos - 2] in string.ascii_uppercase or exprNumerica.match(direccion[pos - 2])):
            validacion = False
            validacion = validacion
            salida += '1'
            # Tamaño minimo no valido
            estadoFinal(direccion, pos)
        else:
            validacion = validacion
            salida += '1'
            # Tamaño minimo no valido
            estadoFinal(direccion, pos)

    elif direccion[pos] == ' ':
        estadoUrbanoCard(direccion, pos + 1)
    elif direccion[pos:pos + 5] == 'NORTE' or direccion[pos:pos + 4] == 'ESTE' or direccion[pos:pos + 5] == 'OESTE' \
            or direccion[pos:pos + 3] == 'SUR':
        if direccion[pos:pos + 5] == 'NORTE':
            salida += '0'
            estadoUrbanoCard(direccion, pos + 5)
        elif direccion[pos:pos + 4] == 'ESTE':
            salida += '0'
            estadoUrbanoCard(direccion, pos + 4)
        elif direccion[pos:pos + 5] == 'OESTE':
            salida += '0'
            estadoUrbanoCard(direccion, pos + 5)
        elif direccion[pos:pos + 3] == 'SUR':
            salida += '0'
            estadoUrbanoCard(direccion, pos + 3)
    elif direccion[pos:pos + 6] == 'NUMERO':
        validacion = False
        salida += '0'
        estadoUrbanoNumPlaca(direccion, pos + 6)
    elif direccion[pos:pos + 3] == 'NO.' or direccion[pos:pos + 3] == 'NRO' or direccion[pos:pos + 3] == 'NUM':
        salida += '0'
        validacion = False
    elif direccion[pos:pos + 2] == 'NO' or direccion[pos:pos + 2] == 'N°' or direccion[pos:pos + 2] == 'N.':
        salida += '0'
        validacion = False
        estadoUrbanoNumPlaca(direccion, pos + 2)
    elif direccion[pos] == 'N' or direccion[pos] == '#' or direccion[pos] == '-':
        salida += '0'
        validacion = False
        auxS = True
        estadoUrbanoNumPlaca(direccion, pos + 1)
    elif exprNumerica.match(direccion[pos]) and direccion[pos - 1] in string.ascii_uppercase:
        salida += '1'
        validacion = False
        #Numeros despues de las letras numero de placa - Invalido
        estadoUrbanoNumPlaca(direccion, pos + 1)
    elif exprNumerica.match(direccion[pos]) or direccion[pos:pos + 3] == 'BIS' \
            or (direccion[pos] in string.ascii_uppercase and exprNumerica.match(
        direccion[pos - 1]) or exprNumerica.match(direccion[pos - 2])):
        if direccion[pos:pos + 3] == 'BIS':
            validacion = False
            estadoUrbanoNumPlaca(direccion, pos)
        elif exprNumerica.match(direccion[pos]) and len(direccion) == pos:
            salida += '1'
            validacion = False
            estadoUrbanoNumPlaca(direccion, pos)
        else:
            validacion = True
            estadoUrbanoCard(direccion, pos + 1)
    elif direccion[pos] in string.ascii_uppercase:
        salida += '0'
        estadoUrbanoCompl(direccion, pos)
    else:
        salida += '1'
        estadoUrbanoNumPlaca(direccion, pos + 1)

def estadoUrbanoNumPlaca(direccion, pos):
    global salida
    global validacion
    if len(direccion) < pos + 1:
        if (direccion[pos - 1] == '-' or direccion[pos - 1] == ' ' or exprNumerica.match(
                direccion[pos - 1])) and (
                direccion[pos - 2] in string.ascii_uppercase or exprNumerica.match(direccion[pos - 2])):
            validacion = True
            validacion = validacion
            salida += '1'
            # Tamaño minimo no valido por terminar en simbolos
            estadoFinal(direccion, pos)
        else:
            validacion = validacion
            salida += '1'
            # Tamaño minimo no valido
            estadoFinal(direccion, pos)
    elif direccion[pos] == ' ':
        estadoUrbanoNumPlaca(direccion, pos + 1)
    elif direccion[pos:pos + 3] == 'BIS' and direccion[pos + 3] != '-':
        validacion = False
        #Num Placa - Bis - complemento
        estadoUrbanoValBis(direccion, pos + 3)
    elif direccion[pos:pos + 3] == 'BIS' and direccion[pos + 3] == '-':
        #Num Placa - Bis
        estadoUrbanoFin(direccion, pos + 3)
    elif direccion[pos:pos + 5] == 'NORTE' or direccion[pos:pos + 4] == 'ESTE' or direccion[pos:pos + 5] == 'OESTE' \
            or direccion[pos:pos + 3] == 'SUR':
        salida += '0'
        if direccion[pos:pos + 5] == 'NORTE':
            salida += '0'
            estadoUrbanoFin(direccion, pos + 5)
        elif direccion[pos:pos + 4] == 'ESTE':
            salida += '0'
            estadoUrbanoCard(direccion, pos + 4)
        elif direccion[pos:pos + 5] == 'OESTE':
            salida += '0'
            estadoUrbanoFin(direccion, pos + 5)
        elif direccion[pos:pos + 3] == 'SUR':
            salida += '0'
            estadoUrbanoFin(direccion, pos + 3)
    elif (direccion[pos] in string.ascii_uppercase or direccion[pos] == ' ') and auxS == True:
        estadoUrbanoCompl(direccion, pos + 1)
    elif direccion[pos] in string.ascii_uppercase and (
            exprNumerica.match(direccion[pos - 1]) or exprNumerica.match(direccion[pos - 2])):
        if direccion[pos - 1] in string.ascii_uppercase or exprNumerica.match(direccion[pos - 1]) or \
                direccion[pos - 1] == ' ':
            #Numero - letra via generadora
            salida += '0'
            estadoUrbanoNumPlaca(direccion, pos + 1)
    elif direccion[pos] in string.ascii_uppercase and direccion[pos - 1] == ' ' or direccion[
        pos - 1] == '#' and direccion[pos] in string.ascii_uppercase:
        salida += '1'
        estadoUrbanoCompPlaca(direccion, pos)
    elif direccion[pos] == ' ':
        estadoUrbanoNumPlaca(direccion, pos + 1)
    elif exprNumerica.match(direccion[pos]) or direccion[pos] in string.ascii_uppercase:
        if len(direccion) == pos:
            salida += '1'
            validacion = False
        else:
            validacion = True
            salida += '0'
            #Solo numero
            estadoUrbanoNumPlaca(direccion, pos + 1)
    elif exprNumerica.match(direccion[pos - 1]) and direccion[pos] in string.ascii_uppercase:
        salida += '0'
        validacion = True
        #Numero - letra
        estadoUrbanoCompPlaca(direccion, pos + 1)
        # SALTO DE 28-33
    elif direccion[pos] == '-' and direccion[pos - 3:pos] != 'BIS':
        validacion = False
        #Sin complemento bis
        estadoUrbanoFin(direccion, pos)
    else:
        return False

def estadoUrbanoCompPlaca(direccion, pos):
    global salida
    global validacion
    if len(direccion) < pos + 1:
        validacion = validacion
        salida += '1'
        # Tamaño minimo no valido
        estadoFinal(direccion, pos)
    elif direccion[pos] == ' ' or direccion[pos] == '-':
        #Simbolo del numero placa
        estadoUrbanoCompPlaca(direccion, pos + 1)
    elif direccion[pos:pos + 3] == 'BIS' and direccion[pos:pos + 4] != '-':
        validacion = False
        #Num placa - bis - complemento
        estadoUrbanoValBis(direccion, pos + 3)
    elif direccion[pos:pos + 3] == 'BIS' and direccion[pos:pos + 4] == '-':
        #Num placa - bis
        estadoUrbanoFin(direccion, pos + 3)
    elif direccion[pos] in string.ascii_uppercase and exprNumerica.match(direccion[pos - 1]) and \
            direccion[pos + 1] in string.ascii_uppercase == False:
        salida += '0'
        #Num placa - letra
        estadoUrbanoAuxBis(direccion, pos + 1)
    elif exprNumerica.match(direccion[pos - 1]) and direccion[pos] in string.ascii_uppercase and \
            exprNumerica.match(direccion[pos + 2]):
        salida += '1'
        #2 numeros placa
        estadoUrbanoAuxBis(direccion, pos + 1)
    elif exprNumerica.match(direccion[pos - 1]) and direccion[pos] in string.ascii_uppercase:
        salida += '1'
        #num via generadora - letra
        estadoUrbanoAuxBis(direccion, pos + 1)
    elif exprNumerica.match(direccion[pos]):
        salida += '0'
        estadoUrbanoCompPlaca(direccion, pos + 1)
    elif direccion[pos] in string.ascii_uppercase and exprNumerica.match(direccion[pos - 1]) and \
            direccion[pos + 1] in string.ascii_uppercase:
        salida += '1'
        #Sin complementos num placa
        estadoUrbanoAuxBis(direccion, pos + 1)
    else:
        estadoUrbanoAuxBis(direccion, pos)


def estadoUrbanoAuxBis(direccion, pos):
    if direccion[pos] == ' ':
        estadoUrbanoAuxBis(direccion, pos + 1)
    else:
        estadoUrbanoValBis(direccion, pos + 1)


def estadoUrbanoValBis(direccion, pos):
    global salida

    if len(direccion) <= pos + 1:
        salida += '1'
        # Tamaño minimo no valido
        estadoFinal(direccion, pos)
    elif direccion[pos] == ' ' or direccion[pos] == '-':
        estadoUrbanoValBis(direccion, pos + 1)
    elif direccion[pos] in string.ascii_uppercase and exprNumerica.match(
            direccion[pos + 1]) and exprNumerica.match(direccion[pos + 2]) and exprNumerica.match(
        direccion[pos + 3]) and direccion[pos + 4] in string.ascii_uppercase:
        salida += '0'
        #Bis con 3 letras - numero - letra
        estadoUrbanoFin(direccion, pos + 5)
    elif direccion[pos] in string.ascii_uppercase and exprNumerica.match(
            direccion[pos + 1]) and exprNumerica.match(direccion[pos + 2]) and exprNumerica.match(
        direccion[pos + 3]):
        # Bis con 3 letras - numero
        salida += '0'
        estadoUrbanoFin(direccion, pos + 4)
    elif direccion[pos] in string.ascii_uppercase and exprNumerica.match(
            direccion[pos + 1]) and exprNumerica.match(direccion[pos + 2]):
        #Bis con 2 letras - numero
        salida += '0'
        estadoUrbanoFin(direccion, pos + 3)
    elif direccion[pos] in string.ascii_uppercase and direccion[pos + 1] in string.ascii_uppercase:
        #Bis con 3 letras
        salida += '0'
        estadoUrbanoFin(direccion, pos + 2)
    elif direccion[pos] in string.ascii_uppercase:
        #Bis - letra
        salida += '0'
        estadoUrbanoFin(direccion, pos + 1)

    elif direccion[pos] in string.ascii_uppercase and direccion[pos + 1] in string.ascii_uppercase and \
            direccion[pos + 2] in string.ascii_uppercase:
        #3 letras - 2 bis
        salida += '1'
        estadoUrbanoFin(direccion, pos + 3)
    elif direccion[pos] in string.ascii_uppercase and direccion[
        pos + 1] in string.ascii_uppercase and exprNumerica.match(direccion[pos + 2]):
        #3 letras - 2 bis - numeros
        salida += '1'
        estadoUrbanoFin(direccion, pos + 2)
    elif exprNumerica.match(direccion[pos]):
        salida += '0'
        estadoUrbanoFin(direccion, pos + 1)
    else:
        #Sin restricciones
        salida += '1'
        estadoUrbanoFin(direccion, pos + 1)


def estadoUrbanoFin(direccion, pos):
    global salida
    global validacion
    if len(direccion) < pos + 1:
        validacion = validacion
        salida += '0'
        #Si se recorrio toda puede finalizar
        estadoFinal(direccion, pos)
    elif direccion[pos] == ' ':
        estadoUrbanoFin(direccion, pos + 1)
    elif direccion[pos:pos + 5] == 'NORTE' or direccion[pos:pos + 4] == 'ESTE' or direccion[pos:pos + 5] == 'OESTE' or \
            direccion[ pos:pos + 3] == 'SUR':
        if direccion[pos:pos + 5] == 'NORTE':
            salida += '0'
            estadoUrbanoValFinal(direccion, pos + 5)
        elif direccion[pos:pos + 4] == 'ESTE':
            salida += '0'
            estadoUrbanoValFinal(direccion, pos + 4)
        elif direccion[pos:pos + 5] == 'OESTE':
            salida += '0'
            estadoUrbanoValFinal(direccion, pos + 5)
        elif direccion[pos:pos + 3] == 'SUR':
            salida += '0'
            estadoUrbanoValFinal(direccion, pos + 3)
    elif direccion[pos:pos + 6] == 'NUMERO':
        salida += '0'
        estadoUrbanoValFinal(direccion, pos + 6)
    elif direccion[pos:pos + 3] == 'NO.' or direccion[pos:pos + 3] == 'NRO' or direccion[pos:pos + 3] == 'NUM':
        salida += '0'
        estadoUrbanoValFinal(direccion, pos + 3)
    elif direccion[pos:pos + 2] == 'NO' or direccion[pos:pos + 2] == 'N°' or direccion[pos:pos + 2] == 'N.':
        salida += '0'
        estadoUrbanoValFinal(direccion, pos + 2)
    elif direccion[pos] == 'N' or direccion[pos] == '#' or direccion[pos] == '-':
        salida += '0'
        validacion = False
        estadoUrbanoFin(direccion, pos + 1)
    elif exprNumerica.match(direccion[pos]) or (exprNumerica.match(direccion[pos - 1]) and
                                                direccion[pos] in string.ascii_uppercase):
        salida += '0'
        validacion = True
        estadoUrbanoFin(direccion, pos + 1)
        if direccion[pos] == ' ':
            estadoUrbanoFin(direccion, pos + 1)
    elif direccion[pos] == ' ' and exprNumerica.match(direccion[pos + 1]):
        salida += '0'
        estadoUrbanoFin(direccion, pos + 1)
    elif direccion[pos] == ' ' and direccion[pos + 1] in string.ascii_uppercase or direccion[
        pos] in string.ascii_uppercase:
        #Validacion complementos
        estadoUrbanoCompl(direccion, pos + 1)
    else:
        salida += '1'
        #Paso a validacion final
        estadoUrbanoValFinal(direccion, pos + 1)


def estadoUrbanoValFinal(direccion, pos):
    global salida
    if len(direccion) == pos:
        salida += '0'
        estadoFinal(direccion, pos)
    elif direccion[pos] == ' ':
        salida += '0'
        estadoUrbanoValFinal(direccion, pos + 1)
    elif direccion[pos] == '-':
        salida += '0'
        estadoUrbanoValFinal(direccion, pos + 1)
    elif exprNumerica.match(direccion[pos]):
        salida += '0'
        estadoUrbanoCompl(direccion, pos)
    elif direccion[pos] in string.ascii_uppercase:
        salida += '0'
        estadoUrbanoCompl(direccion, pos)
    else:
        salida += '1'
        #Sin restricciones para finalizar
        estadoUrbanoCompl(direccion, pos)

def estadoUrbanoCompl(direccion, pos):
    global salida
    global validacion

    if len(direccion) <= pos + 1:
        salida += '1'
        validacion = validacion
        #Recorrido completo para finalizar
        estadoFinal(direccion, pos)
    elif direccion[pos] == '-' or direccion[pos] == ' ':
        salida += '0'
        validacion = True
        estadoUrbanoCompl(direccion, pos + 1)
    elif direccion[pos] in string.ascii_uppercase or exprNumerica.match(direccion[pos]):
        salida += '0'
        validacion = True
        estadoUrbanoCompl(direccion, pos + 1)


def estadoFinal(direccion, pos):
    global validacion
    if (salida[len(salida) - 1] == '1' and validacion != False and salida.count('1') == 1 and salida.count(
            '2') == 0) or (validacion != False and salida[len(salida) - 1] == '0' and salida.count('1') == 0):
        validacion = True
    elif salida.count('1') > 1 or validacion == False or salida[len(salida) - 1] != '1' or salida.count('2') >= 1:
        validacion = False


def tipoDireccion(direccion):
    global salida
    global validacion
    global auxS
    salida = ''

    direccionAux = direccion
    reemplazo2 = direccionAux.replace('N.°', '#')
    reemplazo1 = re.sub('[.,]', '', reemplazo2).upper()
    trans_tab = dict.fromkeys(map(ord, u'\u0301\u0308'), None)
    reemplazo = normalize('NFKC', normalize('NFKD', reemplazo1).translate(trans_tab))

    for i in tipoViaUrbana:
        if reemplazo.count(i) > 1:
            salida += '2'
            estadoFinal(reemplazo, 0)
        elif reemplazo.startswith(i, 0, len(i)):
            estadoInicioUrbano(reemplazo, len(i))
            break
    else:
        for j in tipoViaRural:
            if reemplazo.count(j) > 1:
                salida += '2'
                estadoFinal(direccion, 0)
            elif reemplazo.startswith(j, 0, len(j)):
                estadoInicioRural(reemplazo, len(j))
                break
        else:
            return False
    return validacion


if __name__ == '__main__':
    archivo = open("PruebasDir.txt")
    for i in archivo:
        print(i)
        print(tipoDireccion(i))

    print(tipoDireccion('Carrera 12 No. 19-00 Local 18 Centro Comercial Altavista , Locales comerciales Santo Domingo, Bogotá D.C - Cundinamarca'))
    print(tipoDireccion('Corregimiento el recuerdo salon comunal principal '))
    #corregimiento salon comunal lote