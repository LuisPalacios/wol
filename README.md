# wol
Programa en Python para despertar ordenadores en la wed (Wake On Lan)

Wake-On-Lan-Python
==================

Mini script (Python3) que envía un paquete mágico WOL (Wake On Lan / Despertar en la Red) a un nodo de la red para que se encienda. Necesitamos saber la direción de nivel 2 de dicho nodo, es decir, su dirección MAC. Utiliza un fichero de configuración .ini donde se define el nombre del nodo y su dirección mac.

Uso:
----
    wol.py [nombre del nodo]        # Despertar el host o nodo
    wol.py list                     # Mostrar todos los hosts que tenemos en el fichero wol.ini

wol.ini
-------

El fichero INI contiene una sección General con la dirección broadcast de tu red y el resto son HOSTs/nodos de red con sus macs. 

    [General]
    broadcast=192.168.100.255

    [jupiter]
    mac=01:78:36:23:11:af

