import socket
import datetime
import base_datos
import threading # manejo de hilos

# Configuración puerto  localhost:5000
HOST = 'localhost'
PORT = 5000

# Función para configurar el socket  TCP/IP
def inicializar_socket():
    
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Reutilizar el puerto inmediatamente si reiniciamos el servidor
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        s.bind((HOST, PORT))
        s.listen()
        print(f"[*] Servidor escuchando en {HOST}:{PORT}...")
        return s
    except OSError as e:
        # Capturo error sie s que el puerto 5000 está ocupado
        print(f"[ERROR] El puerto {PORT} está ocupado o no disponible: {e}")
        return None

# Función para guardar datos del cliente y enviarle su mensaje de respuesta "Mensaje recibido ...."
def manejar_cliente(conn, addr):
    ip_cliente = addr[0] # me guardo la ip del cliente
    with conn:
        while True:
            try:
                # Recibo el mensaje enviado por el cliente
                data = conn.recv(1024)
                
                # Si data está vacio, el cliente cerro la conexión
                if not data:
                    print(f"[-] El cliente {addr} se ha desconectado.")
                    break
                
                mensaje = data.decode('utf-8') # Si hay data decodifico.
                
                # No acepto que envien mensajes vacios
                if mensaje.strip() == "":
                    respuesta = "Error: No se puede enviar un mensaje vacío."
                    conn.sendall(respuesta.encode('utf-8'))
                    continue # Vuelve al inicio del ciclo para esperar el siguiente mensaje

                print(f"[{addr}] Mensaje recibido: {mensaje}")
                
                # Guardar el mensaje en la base 
                base_datos.guardar_mensaje(mensaje, ip_cliente)
                
                # Armar respuesta con timestamp
                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                respuesta = f"Mensaje recibido: {timestamp}"
                # Envio respuesta al cliente
                conn.sendall(respuesta.encode('utf-8'))
                
            except ConnectionResetError:
                # Cliente cerro la terminal
                print(f"[-] Cliente {addr} cerro la terminal")
                break

# Función para que el servidor este permanentemente escuchando 
def aceptar_conexiones(s):

    while True:
        try:
            conn, addr = s.accept()
            print(f"[+] Conexión establecida desde {addr}")
            #manejar_cliente(conn, addr)
            hilo_cliente = threading.Thread(target=manejar_cliente, args=(conn, addr)) #creo un hilo nuevo y le paso la funcion manejar_cleinte

            # Inicio el hilo para que corra en paralelo
            hilo_cliente.start()

        except KeyboardInterrupt:
            # Apagar el servidor con ctrl+c en la terminal
            print("\n[*] Apagando el servidor...")
            break

if __name__ == "__main__":
    # Inicializo la base de datos directamente cuando inicia el servidos
    base_datos.inicializar_db()
    
    # Levnato el  servidor
    servidor_socket = inicializar_socket()
    if servidor_socket:
        aceptar_conexiones(servidor_socket) #esperando conexiones de clientes
        servidor_socket.close()