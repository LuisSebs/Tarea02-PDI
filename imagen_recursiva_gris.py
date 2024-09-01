# Autor: Arrieta Mancera Luis Sebastian

import argparse
from utils.progress_bar import progress_bar
from utils.colores import random_color, rojo, verde, azul, reset
from PIL import Image, ImageEnhance

RUTA_TONOS_DE_GRIS = './tonos_de_gris/'

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

def tonos_de_gris(imagen: Image, n: int, salida=None):
    """
        Genera n imagenes en tono de gris de una imagen

        Parameters :
        ------------

            imagen:
                imagen pillow en tono de gris ('L')

            n:
                cantidad de imagenes a generar (de 2 a 255)
            
            salida:
                ruta de la carpeta donde se desean guardar las imagenes. No se guardan por default

        Returns :
        ---------

            lista de imagenes en tonos de gris
    """
    imagenes = []
    enhancer = ImageEnhance.Brightness(imagen)
    for i in range(n):
        factor_brillo = i * (255 / (n-1))
        tono_imagen = enhancer.enhance(factor_brillo/255)
        imagenes.append((round(factor_brillo,2), tono_imagen))
        if salida:
            tono_imagen.save(f"{salida}/tono_gris_{i}.jpg")
    return imagenes

def promedio_gris(imagen: Image):
    """
        Calcula y regresa el promedio a gris de una imagen
    """
    sumatoria = 0
    cantidad_de_pixeles = 0
    for x in range(imagen.width):
        for y in range(imagen.height):
            pixel_value = imagen.getpixel((x, y))
            sumatoria += pixel_value
            cantidad_de_pixeles += 1
    return int(sumatoria / cantidad_de_pixeles)

def get_imagen_gris(promedio_gris, imagenes):    
    """
        Regresa la imagen correspondiente al promedio a gris

        Parameters :
        ------------

            promedio_gris:
                promedio a gris de 1 a 255
            
            imagenes:
                imagenes en tonos de gris
        
        Returns :
        ---------

            imagen
    """
    for tono, imagen in imagenes:
        if promedio_gris <= tono:
            return imagen

def rellena_imagen_recursiva_gris(imagen: Image, pixeles_x: int, pixeles_y:int, imagenes):
    """
        Rellena una imagen en tono de gris con subimagenes en tonos de gris

        Parameters :
        ------------

            imagen:
                imagen en tono de gris para crear la imagen recursiva

            pixeles_x:
                ancho de las subimagenes
            
            pixeles_y:
                alto de las subimagenes
            
            imagenes:
                imagenes en tonos de grises

        Returns :
        ---------

            imagen recursiva en tonos de gris
    """    

    # Dimensiones de la imagen original
    ancho_original, alto_original = imagen.size
    
    # Crear una imagen en blanco para colocar los bloques
    imagen_recursiva = Image.new('L', (ancho_original, alto_original))

    # Calcular el número total de bloques
    total_bloques_x = ancho_original // pixeles_x
    total_bloques_y = alto_original // pixeles_y
    total_bloques = total_bloques_x * total_bloques_y
    
    # Inicializar contador de bloques procesados
    bloques_procesados = 0

    # Colores randoms
    color = random_color()
    cambio_de_color = 100
    contador_color = 0

    # Mensaje informativo
    print(azul+f"Generando imagen recursiva..."+reset)

    # Recorrer la imagen en bloques
    for x in range(0, ancho_original, pixeles_x):
        for y in range(0, alto_original, pixeles_y):
            # Definir el área del bloque
            area = (x, y, x + pixeles_x, y + pixeles_y)

            # Obtenemos una parte de la imagen original
            bloque = imagen.crop(area)
            
            # Calcular el promedio de gris del bloque
            promedio = promedio_gris(bloque)
           
            # Obtener la imagen de tono de gris adecuada
            imagen_adecuada = get_imagen_gris(promedio, imagenes)
            
            # Redimensionar la imagen adecuada al tamaño del bloque
            imagen_redimensionada = imagen_adecuada.resize((pixeles_x, pixeles_y))
            
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

    print(verde+f"Imagen recursiva creada ʕ•ᴥ•ʔ"+reset)      
    
    return imagen_recursiva

def crea_imagen_recursiva_gris(imagen: Image, salida, guardar_tonos=False, factor_medida=2, n=30, f=0.02):
    """
        Crea una imagen recursiva en tonos de gris.

        Parameters :
        ------------

            imagen:
                imagen original

            salida:
                ruta donde se guardara la imagen recursiva, e.g.

                './imgs/imagen_recursiva.jpg'

            guardar_tonos:
                True si se desea guardar las imagenes en tonos de gris, False por defecto
                
            factor_medida:
                medida de la imagen recursiva
                    
                    + 1 es el tamaño original de la imagen
                    + 2 veces mas grande que la imagen original
                    + 4 veces mas grande que la imagen original            

            n:
                cantidad de tonos de gris
            
            f:
                factor de escalamiento de las subimagenes            
    """

    # Convertimos la imagen a tonos de gris
    imagen = imagen.convert('L')
    # Escalamos la imagen
    imagen_reducida = escalar(imagen, f)
    # Subimagenes en tonos de gris
    tonos = []
    if guardar_tonos:
        tonos = tonos_de_gris(imagen_reducida,n,RUTA_TONOS_DE_GRIS)
    else:
        tonos = tonos_de_gris(imagen_reducida,n)
    # Ancho de las subimagenes
    pixeles_x = int(imagen.width * f)
    # Alto de las subimagenes
    pixeles_y = int(imagen.height * f)

    # Crear la imagen recursiva
    imagen_recursiva = rellena_imagen_recursiva_gris(escalar(imagen, factor_medida), pixeles_x, pixeles_y, tonos)

    # Guardar la imagen recursiva
    imagen_recursiva.save(salida)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Programa que genera una imagen recursiva en tonos de gris")

    # Argumentos no opcionales
    parser.add_argument("imagen", help="Ruta de la imagen de entrada")
    parser.add_argument("salida", help="Ruta del archivo de salida")

    # Argumentos opcionales
    parser.add_argument("--gt", action="store_true", help="Indica si se deben guardar los tonos de gris")
    parser.add_argument("--fm", type=float, default=2, help="Factor de medida para la imagen final")
    parser.add_argument("--n", type=int, default=30, help="Número de tonos de gris a generar")
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
    crea_imagen_recursiva_gris(imagen, args.salida, args.gt, args.fm, args.n, args.f)











