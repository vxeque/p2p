Workspace: Recopilando información del área de trabajo# Transferencia de Archivos P2P

Este proyecto implementa un servidor web simple utilizando Flask para permitir la transferencia de archivos entre dispositivos conectados a la misma red local.

## Descripción

La aplicación permite:
- Subir archivos desde cualquier dispositivo en la red local
- Listar los archivos subidos
- Descargar archivos compartidos
- Ver información de diagnóstico de red

## Requisitos previos

- Python 3.x instalado
- Conexión a red local
- Acceso a puertos (verificar firewall)

## Instalación

1. Clonar o descargar este repositorio

2. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

1. Abrir una terminal en la carpeta del proyecto

2. Ejecutar el servidor:
```bash 
python index.py
```

3. El servidor mostrará la información de conexión:
- IP local 
- Puerto (por defecto 5000)
- Nombre del equipo

4. Acceder desde cualquier dispositivo en la red usando:
```
http://<IP_LOCAL>:5000
```

## Solución de problemas

- Verificar que los dispositivos estén en la misma red WiFi
- Comprobar que el firewall permita Python
- Intentar acceder usando la IP mostrada en consola
- Como alternativa, probar usando el nombre del equipo

## Estructura del proyecto

```
.
├── index.py            # Servidor web Flask
├── requirements.txt    # Dependencias del proyecto
├── received_files/     # Carpeta donde se almacenan los archivos
└── README.md          # Este archivo
```

## Tecnologías utilizadas

- Python 3
- Flask
- Socket
- HTML/CSS básico
