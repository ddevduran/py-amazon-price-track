# Track precios de Productos de Amazon

Este es un script de Python diseñado para rastrear los cambios en el título de los productos de Amazon y enviar un correo electrónico si se detecta algún cambio. Se utiliza BeautifulSoup para el web scraping, `requests` para hacer solicitudes HTTP, `smtplib` para enviar correos electrónicos, y `rich` para mejorar la interfaz de usuario en la terminal.

## Características

- Agrega, actualiza y elimina productos de una lista de seguimiento basada en su URL de Amazon.
- Comprueba los productos en un intervalo definido por el usuario.
- Si se detecta un cambio en el título de un producto, se envía un correo electrónico.
- El script sigue funcionando incluso si ocurre un error.
- Se presenta un menú para elegir entre las distintas opciones disponibles.
- Mejora la apariencia de la terminal utilizando la biblioteca `rich`.

## Uso

Para utilizar el script, solo necesitas ejecutarlo y seguir las instrucciones que aparecen en el terminal. Las opciones del menú te permiten añadir, actualizar o eliminar productos.

## Requisitos

Este script requiere las siguientes bibliotecas de Python:

    

 - **requests**: Para enviar solicitudes HTTP.
 - **beautifulsoup4**: Para analizar HTML y extraer información.
 - **smtplib**: Para enviar correos electrónicos.
 - **json**: Para almacenar y cargar la configuración de correo electrónico y la lista de productos.
 - **rich**: Para imprimir con estilo en la terminal.

Puedes instalar estas bibliotecas usando pip:

    pip install requests beautifulsoup4 smtplib rich

## Advertencias

Este script se proporciona tal cual, sin ninguna garantía de su funcionalidad. Este script es sólo para uso educativo y personal. El uso indebido de este script puede infringir los términos de servicio de Amazon y/o leyes de privacidad y protección de datos. El autor no se hace responsable de cualquier uso indebido de este script.
```
La frecuencia de las solicitudes HTTP a la página del producto puede ser limitada por Amazon. Por favor, asegúrate de establecer un intervalo de seguimiento razonable.
```
## Contribuciones

Las contribuciones son bienvenidas! Por favor, abre un "pull request" con tus cambios.
Licencia

Este proyecto está licenciado bajo los términos de la licencia MIT. Consulta el archivo LICENSE para más detalles.
