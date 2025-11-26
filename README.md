# WPBruteFuerza

Script educativo para pruebas de fuerza bruta en WordPress. Herramienta diseñada para evaluaciones de seguridad y pentesting autorizado.

⚠️ **Uso exclusivo con permiso en sistemas propios o autorizados. Solo para fines educativos.**

## Descripción

WPBruteFuerza es una herramienta que implementa dos métodos de ataque de fuerza bruta contra WordPress:

1. **Ataque directo al portal de administración (wp-login.php)**
2. **Ataque vía XML-RPC (xmlrpc.php)**

Ambos métodos permiten identificar credenciales débiles en instalaciones de WordPress, facilitando auditorías de seguridad y pruebas de penetración.

## Métodos de Ataque

### 1. Ataque al Portal de Administración (wp-login.php)

**Funcionamiento:**
- Realiza solicitudes POST directas al formulario de login de WordPress
- Intenta autenticarse con cada contraseña del diccionario
- Valida el éxito mediante cookies de sesión (`wordpress_logged_in`) o redirección a `/wp-admin/`
- Utiliza múltiples hilos para acelerar el proceso

**Por qué es explotable:**
- WordPress no limita intentos de login por defecto
- Las contraseñas débiles son comunes en instalaciones mal configuradas
- Sin protección adicional (CAPTCHA, rate limiting), es vulnerable a ataques de fuerza bruta
- La ausencia de WAF o IDS permite múltiples intentos sin bloqueo

**Mitigación:**
- Implementar límite de intentos fallidos
- Usar plugins de seguridad contra fuerza bruta
- Configurar WAF/rate limiting
- Implementar autenticación de dos factores

### 2. Ataque vía XML-RPC (xmlrpc.php)

**Funcionamiento:**
- Explota el endpoint XML-RPC de WordPress (habilitado por defecto)
- Utiliza el método `wp.getUsersBlogs` para validar credenciales
- Realiza solicitudes individuales (un intento por solicitud HTTP)
- Detecta credenciales válidas por ausencia de `faultCode` en la respuesta
- Implementa multihilo para acelerar el proceso

**Por qué es explotable:**
- XML-RPC está habilitado por defecto en muchas instalaciones
- No requiere interacción con la interfaz web
- Menos logging que el ataque directo a wp-login.php
- Ideal para evadir sistemas de detección básicos
- Permite intentos más rápidos que wp-login.php

**Mitigación:**
- Deshabilitar XML-RPC si no es necesario (agregar a wp-config.php)
- Implementar autenticación de dos factores
- Usar plugins que limiten acceso a XML-RPC
- Monitorear intentos fallidos en logs

## Características

✅ **Soporte multiidioma** - Español e Inglés  
✅ **Multihilo** - Acelera el proceso de ataque  
✅ **User-Agent aleatorio** - Evita detección simple  
✅ **Validación de URL** - Verifica disponibilidad antes de atacar  
✅ **Dos métodos de ataque** - Flexibilidad en la estrategia  
✅ **Interfaz intuitiva** - Fácil de usar  

## Requisitos

```
Python 3.6+
requests
urllib3
```

## Instalación
## Uso

```bash
python WPBruteFuerza.py
```

### Pasos:

1. **Seleccionar idioma** - Elige entre Español (1) o English (2)
2. **Seleccionar tipo de ataque** - Elige entre wp-login.php (1) o XML-RPC (2)
3. **Ingresar URL** - URL del sitio WordPress o del login
4. **Ingresar usuario** - Nombre de usuario a atacar
5. **Ingresar wordlist** - Ruta al archivo de contraseñas

### Ejemplo:

```
[*] Selecciona el idioma / Select language:
  1. Español
  2. English

[?] Selecciona una opción (1/2): 1

[*] Script educativo para pruebas de fuerza bruta
[!] Uso exclusivo con permiso en sistemas propios o autorizados

[*] Selecciona el tipo de ataque de fuerza bruta:
  1. Ataque al portal de administración (wp-login.php)
  2. Ataque vía XML-RPC (xmlrpc.php)

[?] Selecciona una opción (1/2): 1

[?] Introduce la URL de login de WordPress: ejemplo.com/wp-login.php
[?] Introduce el nombre de usuario: admin
[?] Introduce la ruta al archivo de contraseñas: wordlist.txt
```

## Estructura del Código

```
WPBruteFuerza.py
├── Diccionario de traducciones (ES/EN)
├── Funciones de validación
│   ├── verificar_url()
│   ├── verificar_login_exitoso()
│   └── preparar_datos_login()
├── Métodos de ataque
│   ├── ejecutar_fuerza_bruta() - wp-login.php
│   ├── ejecutar_fuerza_bruta_xmlrpc() - XML-RPC individual
│   └── ejecutar_fuerza_bruta_xmlrpc_multicall() - XML-RPC batch
└── Interfaz
    ├── select_language()
    └── main()
```

## Parámetros de Configuración

Dentro del código puedes ajustar:

- **max_hilos** - Número de hilos simultáneos (por defecto: 5)
- **timeout** - Tiempo de espera para conexiones (por defecto: 10s)
- **User-Agent** - Lista de navegadores simulados

## Wordlist

Se recomienda usar wordlists comunes:

- `rockyou.txt` - Más de 14 millones de contraseñas
- `common.txt` - Contraseñas más frecuentes
- Wordlists personalizadas según el objetivo

## Detección y Defensa

### Indicadores de Ataque

- Múltiples intentos fallidos desde una IP
- Solicitudes POST rápidas a wp-login.php
- Acceso a xmlrpc.php con múltiples fallos
- User-Agents variados en corto tiempo

### Herramientas de Defensa

- **Wordfence** - Firewall y detección de intrusiones
- **iThemes Security** - Protección contra fuerza bruta
- **Fail2Ban** - Bloqueo de IPs por intentos fallidos
- **ModSecurity** - WAF para bloquear patrones maliciosos
- **Cloudflare** - Rate limiting y protección DDoS

## Limitaciones

- Requiere conocimiento previo del nombre de usuario
- Depende de la calidad del wordlist
- Puede ser detectado por sistemas de seguridad
- No funciona contra instalaciones con protección adicional
- Requiere acceso de red al servidor

## Consideraciones Legales

Este script es una herramienta educativa. El usuario es responsable de:

- Obtener autorización escrita antes de cualquier prueba
- Cumplir con leyes locales y regulaciones
- Usar solo en sistemas autorizados
- Documentar todas las actividades
- Reportar hallazgos de forma responsable

**No se permite:**
- Acceso no autorizado a sistemas
- Daño intencional
- Uso malicioso
- Violación de privacidad

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature
3. Commit tus cambios
4. Push a la rama
5. Abre un Pull Request

## Roadmap

- [ ] Soporte para más idiomas
- [ ] Integración con proxies
- [ ] Soporte para HTTPS con certificados auto-firmados mejorado
- [ ] Exportación de reportes
- [ ] Integración con bases de datos de credenciales

## Licencia

MIT License - Ver LICENSE para detalles

## Disclaimer

Este proyecto es solo para fines educativos y de investigación. El autor no es responsable del mal uso de esta herramienta. Úsala responsablemente y solo en sistemas autorizados.