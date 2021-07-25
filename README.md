# Mini Robot Caminante y Robótica Cooperativa
Robot caminante con funciones cooperativas en un ambiente estructurado y guiado por visión artificial.

## Objetivos
### General
* Desarrollar un pequeño robot caminante con funciones cooperativas en un ambiente estructurado y guiado por visión artificial.

### Específicos
1. Uso de un proyecto de código abierto.
2. Construcción e impIementación de un robot caminante.
3. Implementación de un sistema de visión artificial.
4. Comprensión y aplicación de funciones cooperativas para la ejecución de tareas.
5. Aplicar algoritmos de navegación, propioceptivos y planificados mediante entornos
estructurados.
6. Documentar técnicamente un proyecto de desarrollo.

## Tecnología utilizada

Se utilizan las siguientes herramientas

- [Python], versión: 3.7.0 - Para algoritmos de visión artificial
- [Arduino], versión 1.8.15 - Microcontrolador + IDE
- [OpenCV] - Markdown parser done right. Fast and easy to extend.
- [Twitter Bootstrap] - great UI boilerplate for modern web apps
- [Ubuntu], versión 20.04.2 LTS - Sistema Operativo (otros SO pueden requerir pasos adicionales no documentados en esta guía)
- [Express] - fast node.js network app framework [@tjholowaychuk]
- [Gulp] - the streaming build system
- [Breakdance](https://breakdance.github.io/breakdance/) - HTML
to Markdown converter
- [jQuery] - duh

And of course Dillinger itself is open source with a [public repository][dill]
 on GitHub.

## Instalación

### Python
El archivo requirements.txt contiene los requisitos necesarios para correr el código Python. Previamente se necesita tener [Python](https://www.python.org/downloads/) y pip instalado (una guía para la instalación se encuentra en [este enlace](https://pip.pypa.io/en/stable/installation/)

En la carpeta principal del repositorio, ejecutar:

```sh
pip install -r requirements.txt
```

### Arduino
1. Instalar [Arduino](arduino.cc/en/software).
2. Abrir el Arduino IDE y navegar hasta Sketch > Include Library > Add .ZIP Library.
3. En la ventana de selección de librería, navegar hasta la carpeta lib del repositorio.
4. Seleccionar OttoDIYLib.zip.
5. En la parte de abajo de la ventana principal debería aparecer un mensaje indicando que la librería ha sido instalada.
6. Para verificar que la librería fue instalada correctamente, ir a Sketch > Import Library. La nueva librería debe estar disponible. Los ejemplos pueden encontrarse en File > Examples > OttoDIYLib.
7. En Tools, seleccionar:
   * Board: "Arduino Nano"
   * Processor: "ATmega328 (Old Bootloader)"
   * Port COM# (puerto en el cual el Otto está conectado)

## Recursos utilizados
Para la implementación de este proyecto se hizo uso de herramientas de código abierto tales como:

| Recurso | Link |
| ------ | ------ |
| Otto DIY robot libraries for Arduino | [Repositorio][OttoDIY] |
| Clases de Robótica 2 | [Repositorio][Clases] |
| https://dillinger.io/ | [Sitio Web][Dillinger] |
| Otto Coding Guide | [Guía][OCG] |
| Medium | [plugins/medium/README.md][PlMe] |
| Google Analytics | [plugins/googleanalytics/README.md][PlGa] |

#### Building for source

For production release:

```sh
gulp build --prod
```

Generating pre-built zip archives for distribution:

```sh
gulp build dist --prod
```

## Docker

Dillinger is very easy to install and deploy in a Docker container.

By default, the Docker will expose port 8080, so change this within the
Dockerfile if necessary. When ready, simply use the Dockerfile to
build the image.

```sh
cd dillinger
docker build -t <youruser>/dillinger:${package.json.version} .
```

This will create the dillinger image and pull in the necessary dependencies.
Be sure to swap out `${package.json.version}` with the actual
version of Dillinger.

Once done, run the Docker image and map the port to whatever you wish on
your host. In this example, we simply map port 8000 of the host to
port 8080 of the Docker (or whatever port was exposed in the Dockerfile):

```sh
docker run -d -p 8000:8080 --restart=always --cap-add=SYS_ADMIN --name=dillinger <youruser>/dillinger:${package.json.version}
```

> Note: `--capt-add=SYS-ADMIN` is required for PDF rendering.

Verify the deployment by navigating to your server address in
your preferred browser.

```sh
127.0.0.1:8000
```

## Licencia

MIT

**Software libre**

[//]: # (Links de referencia. http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [dill]: <https://github.com/joemccann/dillinger>
   [git-repo-url]: <https://github.com/joemccann/dillinger.git>
   [john gruber]: <http://daringfireball.net>
   [df1]: <http://daringfireball.net/projects/markdown/>
   [OpenCV]: <https://opencv.org/>
   [Arduino]: <https://www.arduino.cc/>
   [Ubuntu]: <https://ubuntu.com/>
   [Twitter Bootstrap]: <http://twitter.github.com/bootstrap/>
   [jQuery]: <http://jquery.com>
   [@tjholowaychuk]: <http://twitter.com/tjholowaychuk>
   [express]: <http://expressjs.com>
   [Python]: <https://www.python.org/>
   [Gulp]: <http://gulpjs.com>

   [OttoDIY]: <https://github.com/OttoDIY/OttoDIYLib>
   [Clases]: <https://github.com/RonyBenitez/Clases-Robotica>
   [Dillinger]: <https://dillinger.io/>
   [OCG]: <https://wikifactory.com/+OttoDIY/otto-diy/v/746ad7d/file/Instruction%20manual/OttoDIY_codingguide_V9.pdf>
   [PlMe]: <https://github.com/joemccann/dillinger/tree/master/plugins/medium/README.md>
   [PlGa]: <https://github.com/RahulHP/dillinger/blob/master/plugins/googleanalytics/README.md>
