import socket
import os
from flask import Flask, request, send_file
# import requests
from io import BytesIO

app = Flask(__name__)

# Configuración
PORT = 5000
UPLOAD_FOLDER = 'received_files'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def get_local_ip():
    hostname = socket.gethostname()
    # Obtiene todas las IPs del sistema
    try:
        # Obtener la IP que no sea la loopback (127.0.0.1)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # No necesitamos realmente conectarnos
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception as e:
        print(f"Error obteniendo IP: {e}")
        # Fallback a obtener todas las IPs
        ips = socket.gethostbyname_ex(hostname)[2]
        for ip in ips:
            if not ip.startswith('127.'):
                return ip
        return '127.0.0.1'

def test_port():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.bind(('0.0.0.0', PORT))
        sock.close()
        return True
    except Exception as e:
        print(f"Error al intentar usar el puerto {PORT}: {e}")
        return False

@app.route('/')
def index():
    ip = get_local_ip()
    # Agregar información de diagnóstico
    client_ip = request.remote_addr
    return f'''
    <html>
        <head>
            <title>Transferencia de Archivos P2P</title>
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <style>
                .debug-info {{
                    background: #f0f0f0;
                    padding: 10px;
                    margin: 10px 0;
                    border-radius: 5px;
                }}
            </style>
        </head>
        <body style="padding: 20px;">
            <h2>Transferencia de Archivos P2P</h2>
            
            <div class="debug-info">
                <h3>Información de Diagnóstico:</h3>
                <p>IP del servidor: {ip}:{PORT}</p>
                <p>Tu IP: {client_ip}</p>
                <p>Nombre del equipo: {socket.gethostname()}</p>
            </div>

            <h3>Enviar archivo:</h3>
            <form action="/upload" method="post" enctype="multipart/form-data">
                <input type="file" name="file" required>
                <input type="submit" value="Enviar">
            </form>
            
            <h3>Archivos recibidos:</h3>
            <ul>
                {generate_file_list()}
            </ul>

            <div class="debug-info">
                <h4>Instrucciones de solución de problemas:</h4>
                <ol>
                    <li>Asegúrate de que ambos dispositivos estén en la misma red WiFi</li>
                    <li>Verifica que el Firewall de Windows permita Python</li>
                    <li>Intenta acceder usando la IP mostrada arriba</li>
                    <li>Si no funciona, prueba usando el nombre del equipo</li>
                </ol>
            </div>
        </body>
    </html>
    '''

def generate_file_list():
    try:
        files = os.listdir(UPLOAD_FOLDER)
        return ''.join([f'<li><a href="/download/{file}">{file}</a></li>' for file in files])
    except Exception as e:
        return f'<li>Error al listar archivos: {e}</li>'

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No se seleccionó ningún archivo', 400
    
    file = request.files['file']
    if file.filename == '':
        return 'No se seleccionó ningún archivo', 400
    
    try:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)
        return 'Archivo subido exitosamente'
    except Exception as e:
        return f'Error al guardar archivo: {e}', 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        return send_file(os.path.join(UPLOAD_FOLDER, filename))
    except Exception as e:
        return f'Error al descargar archivo: {e}', 404

if __name__ == '__main__':
    ip = get_local_ip()
    print("\n=== Diagnóstico de red ===")
    print(f"Nombre del equipo: {socket.gethostname()}")
    print(f"IP local: {ip}")
    print(f"Puerto: {PORT}")
    
    if test_port():
        print("\nServidor iniciando...")
        print(f"Accede desde tu móvil usando:")
        print(f"http://{ip}:{PORT}")
        print("\nSi no funciona, prueba usando el nombre del equipo:")
        print(f"http://{socket.gethostname()}:{PORT}")
        
        try:
            app.run(host='0.0.0.0', port=PORT)
        except Exception as e:
            print(f"\nError al iniciar el servidor: {e}")
    else:
        print(f"\nError: El puerto {PORT} está en uso o bloqueado.")
        print("Intenta cambiar el valor de PORT en el código o verificar el firewall.")