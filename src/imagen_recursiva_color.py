# Autor: Arrieta Mancera Luis Sebastian

import argparse
from utils.progress_bar import progress_bar
from utils.colores import random_color, rojo, verde, azul, reset
from PIL import Image, ImageStat

RUTA_TONOS_DE_COLORES = './tonos_de_colores'

def escalar(imagen: Image, factor: float, salida=None):
    """
        Escala una imagen y la regresa

        Parameters :
        ------------

            imagen:
                imagen a escalar

            factor:
                factor de escalamiento, e.g:
                    + 0.5 es la mitad
                    + 2.0 es el doble

            salida:
                la ruta de salida donde se desea guardar la imagen. No se guarda por default, e.g.

                    + ./imagenes/imagen_escalada.jpg      

        Returns :
        ---------

            imagen reescalada  
    """
    ancho_original, alto_original = imagen.size
    nuevo_ancho = int(ancho_original * factor)
    nuevo_alto = int((nuevo_ancho / ancho_original) * alto_original)
    imagen_reescalada = imagen.resize((nuevo_ancho, nuevo_alto))
    if salida:
        imagen_reescalada.save(salida)
    return imagen_reescalada

def color_promedio_sebas(imagen: Image):
    """
        Regresa el color promedio de una imagen. Implementacion propia

        Parameters :
        ------------
        
        imagen:
            imagen 
        
        Returns :
        ---------

        tupla con el color promedio
    """
    
    # Sumatoria de los canales de cada pixel
    suma_r = 0
    suma_g = 0
    suma_b = 0

    # Medidas de la imagen
    ancho = imagen.width
    alto = imagen.height

    # Cantidad total de pixeles
    total = ancho * alto

    # Calculamos la sumatoria por canal
    for x in range(0,ancho):        
        for y in range(0,alto):
            pixel = imagen.getpixel((x,y))
            # Desestructuracion del pixel
            r, g, b = pixel
            suma_r += r
            suma_g += g
            suma_b += b

    # Promedios de los canales de color
    promedio_r = int(suma_r / total)
    promedio_g = int(suma_g / total)
    promedio_b = int(suma_b / total)

    # Color promedio
    return (promedio_r, promedio_g, promedio_b)

def color_promedio(imagen: Image):
    """
        Implementacion con Pillow
    """
    stat = ImageStat.Stat(imagen)
    return tuple(map(int, stat.mean[:3]))

def crea_imagen_recursiva(imagen: Image, salida, guardar_tonos=False, factor_medida=2, f=0.02):
    """
        Crea una imagen recursiva a color y la guarda.

        Parameters :
        ------------

            imagen:
                imagen
            
            salida:
                ruta donde se guardara la imagen recursiva

            guardar_tonos:
                True si se desean guardar los tonos de colores, False por default
            
            fator_medida: 
                medida final de la imagen recursiva

                    + 1 es el tamaño original de la imagen
                    + 2 veces mas grande que la imagen original
                    + 4 veces mas grande que la imagen original     

            f:
                factor de escalamiento de las subimagenes

        Returns :
        ---------

            imagen recursiva
    """

    # Imagen reducida
    imagen_reducida = escalar(imagen, f)
    
    # Imagen aumentada
    imagen_aumentada = escalar(imagen, factor_medida)

    # Dimensiones de la subimagen
    sub_ancho, sub_alto = imagen_reducida.size

    # Dimensiones de la imagen final
    ancho, alto = imagen_aumentada.size

    # Crear una imagen en blanco para colocar los bloques
    imagen_recursiva = Image.new('RGB', (ancho, alto))

    # Calcular el número total de bloques
    total_bloques_x = ancho // sub_ancho
    total_bloques_y = alto // sub_alto
    total_bloques = total_bloques_x * total_bloques_y

    # Inicializar contador de bloques procesados
    bloques_procesados = 0

    # Colores randoms
    color = random_color()
    cambio_de_color = 100
    contador_color = 0

    # Tonos de colores
    tonos = {}

    # Mensaje informativo
    print(azul+f"Generando imagen recursiva..."+reset)
    
    # Recorrer la imagen en bloques
    for x in range(0, ancho, sub_ancho):
        for y in range(0, alto, sub_alto):

            # Definir el área del bloque
            area = (x, y, x + sub_ancho, y + sub_alto)

            # Obtenemos una parte de la imagen aumentada
            bloque = imagen_aumentada.crop(area)

            # Calcular color promedio del bloque
            tono = color_promedio(bloque)

            # Clave
            clave = str(tono)

            # Si aun no creamos la imagen con el tono de color
            if clave not in tonos:
                mica = Image.new('RGB', (sub_ancho, sub_alto), tono)
                imagen_con_mica = Image.blend(imagen_reducida, mica, alpha=0.5)
                tonos[clave] = imagen_con_mica
                if guardar_tonos:
                    imagen_con_mica.save(f"{RUTA_TONOS_DE_COLORES}/{'_'.join([str(x) for x in tono])}.jpg")

            # Imagen con el tono adecuado
            imagen_adecuada = tonos[clave]
            # Redimensionar la imagen adecuada al tamaño del bloque
            imagen_redimensionada = imagen_adecuada.resize((sub_ancho, sub_alto))
            # Pegar el bloque en la imagen recursiva
            imagen_recursiva.paste(imagen_redimensionada, (x, y))

            # Actualizar barra de progreso
            bloques_procesados += 1

            # Mostramos el progreso
            progress_bar(bloques_procesados, total_bloques, color)

            # Actualizacion de color random
            contador_color += 1
            if contador_color == cambio_de_color:
                color = random_color()
                contador_color = 0

    # Guardar la imagen recursiva
    imagen_recursiva.save(salida)

    print(verde+f"Imagen recursiva creada ʕ•ᴥ•ʔ"+reset)

    return imagen_recursiva
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Programa que genera una imagen recursiva a color")

    # Argumentos no opcionales
    parser.add_argument("imagen", help="Ruta de la imagen de entrada")
    parser.add_argument("salida", help="Ruta del archivo de salida")

    # Argumentos opcionales
    parser.add_argument("--gt", action="store_true", help="Indica si se deben guardar los tonos de colores")
    parser.add_argument("--fm", type=float, default=2, help="Factor de medida para la imagen final")
    parser.add_argument("--f", type=float, default=0.02, help="Factor de escalado de las subimagenes")

    # Obtenemos los argumentos
    args = parser.parse_args()

    # Cargamos la imagen
    imagen = None
    try:
        imagen = Image.open(args.imagen)
    except Exception as e:
        print(rojo+f"Error al cargar la imagen: {e}"+reset)
        exit()
    
    # Creamos la imagen recursiva
    crea_imagen_recursiva(imagen,args.salida, args.gt, args.fm,args.f)
