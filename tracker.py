"""
tracker.py
==========

Script para el trackeo de precios de productos de Amazon.

Autor: David Duran <david@devduran.com>
Fecha: 11 de junio de 2023
Repositorio: https://github.com/ddevduran/py-amazon-price-track

"""
import requests
from bs4 import BeautifulSoup
import smtplib
import random
import json
from pyfiglet import Figlet
from colorama import init, Fore
from rich.console import Console
from rich.table import Table
from rich.text import Text
import time
import threading
import os
import sys

# Inicializamos una consola para rich
console = Console()

# Función para mostrar la cabecera y esperar 2 segundos
def mostrar_cabecera():
    fig = Figlet(font="standard")
    ascii_art = fig.renderText("TRACKER.PY")
    cabecera = Text(ascii_art)
    cabecera.stylize("bold yellow")
    console.print(cabecera)
    time.sleep(2)
    
# Verificamos si el archivo de configuración del correo existe, si no, lo creamos
if not os.path.isfile("email_config.json"):
    email_config = {
        'sender_email': 'sender@gmail.com',
        'receiver_email': 'receiver@gmail.com',
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'username': 'sendmail@gmail.com',
        'password': 'g.mail password'
    }
    with open("email_config.json", "w") as file:
        json.dump(email_config, file)
else:
    # Cargamos la configuración del correo del archivo json
    with open("email_config.json") as file:
        email_config = json.load(file)

# Verificamos si el archivo de la lista de productos existe, si no, lo creamos
if not os.path.isfile("product_list.json"):
    product_list = []
    with open("product_list.json", "w") as file:
        json.dump(product_list, file)
else:
    # Cargamos la lista de productos del archivo json
    with open("product_list.json") as file:
        product_list = json.load(file)

def clear_terminal():
    # 'nt' es el nombre del kernel para Windows
    if os.name == 'nt':
        _ = os.system('cls')

    # 'posix' es el nombre del kernel para Unix/Linux
    else:
        _ = os.system('clear')
        
# Obtenemos la URL de la página del producto del usuario
def get_product_page_url():
    tmp_url = input("Introduce la URL del producto: ")
    tmp_url = tmp_url.replace("//", "/").split("/")
    url = tmp_url[0] + "//" + tmp_url[1] + "/" + tmp_url[2] + "/" + tmp_url[3] + "/" + tmp_url[4]
    return url

# Enviamos una solicitud para obtener el HTML de la página
def request_product_page(url):
    # Se definen diferentes User-Agents para simular accesos desde diferentes navegadores y sistemas operativos
    user_agent = ['Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
                'Mozilla/4.0 (compatible; MSIE 5.0; SunOS 5.10 sun4u; X11)',
                'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.2pre) Gecko/2010020que Ubuntu/9.04 (Alegre) Namoroka/3.6.2pre ',
                'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Avant Browser;',
                'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT 5.0)',
                'Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.1)',
                'Mozilla/5.0 (Windows; U; Windows NT 6.en-US-Urv rv:1.9.0.6)',
                'Microsoft Internet Explorer/4.0b1 (Windows 95)',
                'Opera/8.00 (Windows queT 5.1; U; en)',
                'Amaya/9.51 libwww/5.4.0',
                'Mozilla/4.0 (compatible; MSIE 5.0; AOL Windowsndows 95; c_athome)',
                'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                'Mozilla/5.0 (compatible; Konqueror/3.5; Linux) KHTML/3.5.5 (como Gecko) (Kubuntu)',
                'Mozilla/4.0 (compatible; MSIE 5.0; Windows ME) Opera 5.11 [en]']

    headers = {
        "User-Agent": random.choice(user_agent)
    }

    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')

# Añade un nuevo producto a la lista
def add_product():
    url = get_product_page_url()
    soup = request_product_page(url)
    title = soup.find(id="productTitle").get_text().strip()
    freq = int(input("Introduce la frecuencia de comprobación (en minutos): "))
    product = {"url": url, "title": title, "frequency": freq}
    product_list.append(product)
    with open("product_list.json", "w") as file:
        json.dump(product_list, file)
    console.print(f"Producto [green]{title}[/green] guardado!", style="bold red")

# Actualiza un producto de la lista
def update_product():
    table = Table(title="Productos")
    table.add_column("Índice", style="cyan")
    table.add_column("Título", style="magenta")
    for i, product in enumerate(product_list, start=1):
        table.add_row(str(i), product["title"])
    console.print(table)

    choice = input("Ingrese el índice del producto a actualizar (0 para cancelar): ")
    if choice == "0":
        console.print("Operación cancelada.", style="bold yellow")
        return

    try:
        index = int(choice) - 1
        product = product_list[index]
        console.print(f"Producto seleccionado: {product['title']}", style="bold green")
        new_url = get_product_page_url()
        new_soup = request_product_page(new_url)
        new_title = new_soup.find(id="productTitle").get_text().strip()
        confirm = input(f"¿Está seguro de que desea actualizar el producto '{product['title']}' con la nueva URL y título '{new_title}'? (s/n): ")
        if confirm.lower() == "s":
            product["url"] = new_url
            product["title"] = new_title
            with open("product_list.json", "w") as file:
                json.dump(product_list, file)
            console.print(f"Producto '{product['title']}' actualizado.", style="bold red")
        else:
            console.print("Operación cancelada.", style="bold yellow")
    except ValueError:
        console.print("Índice inválido. Por favor, ingrese un número válido.", style="bold red")
    except IndexError:
        console.print("Índice fuera de rango. Por favor, ingrese un índice válido.", style="bold red")

# Elimina un producto de la lista
def delete_product():
    table = Table(title="Productos")
    table.add_column("Índice", style="cyan")
    table.add_column("Título", style="magenta")
    for i, product in enumerate(product_list, start=1):
        table.add_row(str(i), product["title"])
    console.print(table)

    choice = input("Ingrese el índice del producto a eliminar (0 para cancelar): ")
    if choice == "0":
        console.print("Operación cancelada.", style="bold yellow")
        return

    try:
        index = int(choice) - 1
        product = product_list[index]
        confirm = input(f"¿Está seguro de que desea eliminar el producto '{product['title']}'? (s/n): ")
        if confirm.lower() == "s":
            product_list.pop(index)
            with open("product_list.json", "w") as file:
                json.dump(product_list, file)
            console.print(f"Producto '{product['title']}' eliminado.", style="bold red")
        else:
            console.print("Operación cancelada.", style="bold yellow")
    except ValueError:
        console.print("Índice inválido. Por favor, ingrese un número válido.", style="bold red")
    except IndexError:
        console.print("Índice fuera de rango. Por favor, ingrese un índice válido.", style="bold red")

# Verifica un producto
def check_single_product(product):
    url = product["url"]
    soup = request_product_page(url)
    title = soup.find(id="productTitle").get_text().strip()
    if title != product["title"]:
        product["title"] = title
        with open("product_list.json", "w") as file:
            json.dump(product_list, file)
        console.print(f"Producto [green]{title}[/green] actualizado!", style="bold red")
        send_mail(product, "Precio reducido")

# Función que verifica un producto
def check_single_product_inscreen(product):
    url = product["url"]
    soup = request_product_page(url)
    title = soup.find(id="productTitle").get_text().strip()
    if title != product["title"]:
        price_change = soup.find(id="priceblock_ourprice")
        if price_change:
            console.print(f"¡Hay un cambio en el precio del producto '{product['title']}'!", style="bold yellow")
            console.print(f"Precio anterior: {product['price']}", style="bold cyan")
            console.print(f"Precio actual: {price_change.get_text().strip()}", style="bold cyan")
            product["price"] = price_change.get_text().strip()
            with open("product_list.json", "w") as file:
                json.dump(product_list, file)
        else:
            console.print(f"¡Hay un cambio en el título del producto '{product['title']}'!", style="bold yellow")
            console.print(f"Título anterior: {product['title']}", style="bold cyan")
            console.print(f"Título actual: {title}", style="bold cyan")
            product["title"] = title
            with open("product_list.json", "w") as file:
                json.dump(product_list, file)
    else:
        console.print(f"No hay cambios en el producto '{product['title']}'", style="bold green")
    
    time.sleep(3)

# Función que verifica un producto de forma periódica
def periodic_check_single_product(product):
    while True:
        console.print(f"Comprobando producto: {product['title']}...", style="bold blue")
        check_single_product(product)
        time.sleep(product["frequency"] * 60)

# Función que verifica todos los productos de forma periódica
def periodic_check_all_products():
    for product in product_list:
        threading.Thread(target=periodic_check_single_product, args=(product,)).start()

# Envia un correo electrónico
def send_mail(product, reason):
    server = smtplib.SMTP(email_config['smtp_server'], email_config['smtp_port'])
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(email_config['username'], email_config['password'])
    subject = 'Precio reducido'
    body = f"Revisa el link de amazon {product['url']}"
    msg = f"Subject: {subject}\n\n{body}"
    server.sendmail(
        email_config['sender_email'],
        email_config['receiver_email'],
        msg
    )
    console.print('¡Correo electrónico enviado!', style="bold green")
    server.quit()

# Verifica un producto específico
def check_product():
    clear_terminal()
    table = Table(title="Productos")
    table.add_column("Índice", style="cyan")
    table.add_column("Título", style="magenta")
    for i, product in enumerate(product_list, start=1):
        table.add_row(str(i), product["title"])
    console.print(table)

    choice = input("Ingrese el índice del producto a verificar (0 para cancelar): ")
    if choice == "0":
        console.print("Operación cancelada.", style="bold yellow")
        return

    try:
        index = int(choice) - 1
        product = product_list[index]
        console.print(f"Verificando producto: {product['title']}", style="bold blue")
        check_single_product_inscreen(product)
    except ValueError:
        console.print("Índice inválido. Por favor, ingrese un número válido.", style="bold red")
    except IndexError:
        console.print("Índice fuera de rango. Por favor, ingrese un índice válido.", style="bold red")

# Muestra el menú
def show_menu():
    time.sleep(1)
    clear_terminal()
    table = Table(title="Menú")
    table.add_column("Número", style="cyan")
    table.add_column("Opción", style="magenta")
    options = [
        "Añadir producto",
        "Actualizar producto",
        "Eliminar producto",
        "Verificar producto",
        "Salir"
    ]
    for i, option in enumerate(options, start=1):
        table.add_row(str(i), option)
    console.print(table)

if __name__ == "__main__":
    console.clear()
    mostrar_cabecera()
        
    # Verificar todos los productos periódicamente
    periodic_check_all_products()
    while True:
        try:
            show_menu()
            choice = input("Introduzca su elección: ")
            if choice == "1":
                add_product()
            elif choice == "2":
                update_product()
            elif choice == "3":
                delete_product()
            elif choice == "4":
                check_product()
            elif choice == "5":
                console.print("Ciao!", style="bold green")
                time.sleep(1)
                clear_terminal()
                time.sleep(1)
                sys.exit()
            else:
                console.print("Opción inválida. Por favor, introduzca una opción válida.", style="bold red")
        except Exception as e:
            console.print(f"Ocurrió un error: {str(e)}", style="bold red")
