import sqlite3
import datetime

# Función para inicializar la base y crear tabla si ya no existe
def inicializar_db():    
    try:
        conexion = sqlite3.connect('chat.db')
        cursor = conexion.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mensajes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                contenido TEXT NOT NULL,
                fecha_envio TEXT NOT NULL,
                ip_cliente TEXT NOT NULL
            )
        ''')
        conexion.commit()
        conexion.close()
        print("[OK] Base de datos SQLite inicializada correctamente.")
    except sqlite3.Error as e:
        print(f"[ERROR] DB no accesible. Detalle: {e}")

# Función para guardar los mensajes de determinado cliente
def guardar_mensaje(contenido, ip_cliente):
    try:
        conexion = sqlite3.connect('chat.db')
        cursor = conexion.cursor()
        fecha_envio = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        cursor.execute('''
            INSERT INTO mensajes (contenido, fecha_envio, ip_cliente)
            VALUES (?, ?, ?)
        ''', (contenido, fecha_envio, ip_cliente))
        
        conexion.commit()
        conexion.close()
    except sqlite3.Error as e:
        print(f"[ERROR] Error al guardar en la base de datos: {e}")