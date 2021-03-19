#!/usr/bin/env python3
# by LuisPa
#

# Librerías necesarias
import os
import sys
import configparser
import socket
import struct
import re

# Base de datos con la configuración
dConfiguration = {}

# Despertar a un host
def despiertaHost(host):
    """ 
        Función que hace la magia, despierta un ordenador usando un paquete WOL
    """
    global dConfiguration

    # Se supone que tengo un diccionario preparado, con "los nombres de los hosts"
    # como claves y con "las direcciones mac" como "valores"
    try:
        macaddress = dConfiguration[host]['mac']
    except:
        return False

    # Compruebo la dirección mac
    found = re.fullmatch(
        '^([A-F0-9]{2}(([:][A-F0-9]{2}){5}|([-][A-F0-9]{2}){5})|([\s][A-F0-9]{2}){5})|([a-f0-9]{2}(([:][a-f0-9]{2}){5}|([-][a-f0-9]{2}){5}|([\s][a-f0-9]{2}){5}))$', macaddress)
    # O se encuentra una o está mal
    if found:
        # Si se ha encontrado entones quito los separadores [:-\s]
        macaddress = macaddress.replace(macaddress[2], '')
    else:
        raise ValueError('El formato de la dirección MAC es incorrecto')

    # Pad the synchronization stream.
    data = ''.join(['FFFFFFFFFFFF', macaddress * 20])
    send_data = b''

    # Divido los valores Hexadecimales y empaqueto
    for i in range(0, len(data), 2):
        send_data = b''.join([send_data,
                struct.pack('B', int(data[i: i + 2], 16))])

    # Envío el paquete a la red
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.sendto(send_data, (dConfiguration['General']['broadcast'], 7))
    return True


def leerFicheroConfig():
    """ 
        Leer el fichero de configuración
        
    """
    global mydir
    global dConfiguration
    Config = configparser.ConfigParser()
    Config.read(mydir+"/wol.ini")
    sections = Config.sections()
    dict1 = {}
    for section in sections:
        options = Config.options(section)

        sectkey = section
        dConfiguration[sectkey] = {}

        for option in options:
            dConfiguration[sectkey][option] = Config.get(section, option)

    return dConfiguration  # Useful for testing


# Muestra el correcto uso del programa
def uso():
    print('Uso: wol.py <nombre de host>')


if __name__ == '__main__':
    mydir = os.path.dirname(os.path.abspath(__file__))
    conf = leerFicheroConfig()
    try:
        # Use macaddresses with any seperators.
        if sys.argv[1] == 'list':
            print('Lista de hosts configurados en wol.ini:')
            for i in conf:
                if i != 'General':
                    print('\t', i)
            print('\n')
        else:
            if not despiertaHost(sys.argv[1]):
                print('No tengo ese host en wol.ini')
            else:
                print('Hecho!. Envié el paquete mágico a ' + sys.argv[1])
    except:
        uso()
