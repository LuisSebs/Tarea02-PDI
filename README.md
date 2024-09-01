# Tarea03: Imagenes recursivas

## Author: Arrieta Mancera Luis Sebastian (318174116)

<img src="https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExNjFoend5bzNqdXk1Z200YzB0YmN4dHpkYmN2MGpjOHAzeDRidGNvbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/6aoBhilsJENZC/giphy.gif" width="400px"/>

Programa que crea imagenes recursivas a color y en tonos de grises.

# Dependencias:

+ [Colorama](https://pypi.org/project/colorama/): `pip install colorama`
+ [Pillow](https://pypi.org/project/pillow/): `pip install pillow`

# Ejecución: 

Favor de instalar las dependencias necesarias. Ejecuta con **python** o **python3** el archivo `imagen_recursiva_color.py` o `imagen_recursiva_gris.py` dependiendo de la imagen que quieras generar. Te recomiendo usar las imagenes que se encuentran en la carpeta `imgs/`. Al momento de ejecutar los programas ingresa la ruta donde quieres guardar la imagen con la extension `jpg`. Adicionalmente, puedes ingresar más argumentos como `--gt` si quieres que los tonos se guarden, `--fm` para especificar el porcentaje del tamaño de la imagen final, `--f` para indicar el porcentaje del tamaño de las subimagenes o para la creación de una imagen en tonos de gris puedes usar el argumento `--n` para indicar la cantidad de tonos de gris (de 2 a 255). Puedes saber los argumentos que recibe cada programa con la bandera `-h`.

**Ejemplos:**

Imagen recursiva en tono de grises

```bash
python3 imagen_recursiva_gris.py ./imgs/aiony.jpg ./aiony_recursiva_gris.jpg --gt --n 30 --fm 2 --f 0.02
```

Imagen recursiva a color

```bash
python3 imagen_recursiva_color.py ./imgs/aiony.jpg ./aiony_recursiva_color.jpg --fm 2 --f 0.02
```





## Para ver los argumentos que recibe cada programa

**Imagen recursiva a color**

```bash
python3 imagen_recursiva_color.py -h
```

**Imagen recursiva en tonos de gris**

```bash
python3 imagen_recursiva_gris.py -h
```

