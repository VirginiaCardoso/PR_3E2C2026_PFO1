import socket

# Configuración puerto  localhost:5000
HOST = 'localhost'
PORT = 5000

def iniciar_cliente():
    # Configuración del socket TCP/IP. Con with para asegurarme el socket se cierre al terminr o si ocurre un error
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Intentar conexión con el servidor
            s.connect((HOST, PORT))
            print(f"[*] Conectado al servidor en {HOST}:{PORT}")
            print("Escribí tus mensajes. Ingresá 'éxito' para salir de la conexión.")

            # Bucle para poder mandar mensajes hasta que se escriba éxito o exito
            while True:
                mensaje = input(">> ")
                mensaje_limpio = mensaje.strip().lower() #elimino espacio y paso a minuscula

                # si escriben éxito sale del cliclo y cierra chat
                if mensaje_limpio == 'éxito':
                    print("Saliendo del chat...")
                    break
                # Porque me paso varias veces permito escriban sin tilde para salir ;)
                elif mensaje_limpio == 'exito':
                    print("Aviso: Escribiste 'exito' sin tilde, pero cerraremos la conexión de todos modos. Saliendo del chat...")
                    break
                
                # Enviar mensaje
                s.sendall(mensaje.encode('utf-8'))
                
                # Espero confirmación del servidor
                data = s.recv(1024)
                print(f"Servidor: {data.decode('utf-8')}")

        # Muestro error si falla la conexión. Puede ser que no se inicio el servidor    
        except ConnectionRefusedError:
            print(f"[ERROR] No se pudo conectar. ¿Iniciaste el servidor?")

if __name__ == "__main__":
    iniciar_cliente()