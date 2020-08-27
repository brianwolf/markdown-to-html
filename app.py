import os
import shutil
from typing import List

from markdown2 import markdown

DIR_IN = './in'
DIR_OUT = './out'
DIR_CSS = './css'


def hacer_relativo(ruta: str) -> str:
    ruta = ruta.replace('./', '', 1)
    
    if ruta.startswith('/'):
        ruta = ruta.replace('/', '', 1)
    
    return ruta


def rutas_relativas_archivos(directorio: str) -> List[str]:
    ruta_archivos = []

    for ruta_base, directorios, archivos in os.walk(directorio):
        ruta_archivos += [os.path.join(ruta_base, a) for a in archivos]

    return [hacer_relativo(r.replace(directorio, '')) for r in ruta_archivos]



shutil.rmtree('./out')
os.makedirs(DIR_OUT)


ruta_archivos = rutas_relativas_archivos(DIR_IN)

rutas_relativas_md = [r for r in ruta_archivos if r.endswith('.md')]
rutas_relativas_varios = [r for r in ruta_archivos if not r.endswith('.md')]


rutas_relativas_css = rutas_relativas_archivos(DIR_CSS)
shutil.copytree(DIR_CSS, os.path.join(DIR_OUT, 'css'))


for ruta in rutas_relativas_md:
    
    with open(os.path.join(DIR_IN, ruta), 'r') as archivo:
        contenido = archivo.read()
    
    for ruta_relativa_css in rutas_relativas_css:
        
        ruta_final_css = os.path.join('css', ruta_relativa_css)
        link_css = f'<link rel="stylesheet" type="text/css" href="{ruta_final_css}" media="all" />'
        contenido = f'{link_css}\n{contenido}'

    contenido = contenido.replace('.md', '.html')
    contenido = markdown(contenido)

    ruta_final = os.path.join(hacer_relativo(DIR_OUT), ruta).replace('.md', '.html')
    
    directorio_final = os.path.dirname(ruta_final)
    if not os.path.exists(directorio_final):
        os.makedirs(directorio_final)

    with open(ruta_final, 'w') as archivo:
        archivo.write(contenido)
    

print(rutas_relativas_md)
print(rutas_relativas_varios)
print(rutas_relativas_css)
