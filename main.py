# main.py
import os
from dotenv import load_dotenv
from upload_utils import subir_imagen_a_bucket
from db_connection import get_db_connection
import mysql.connector

# Cargar las variables de entorno
load_dotenv()

# Parámetros de configuración
API_TOKEN = os.getenv("API_TOKEN")

CARPETA_IMAGENES = 'subir'
EXTENSIONES_VALIDAS = ('.jpg', '.jpeg', '.png', '.gif')

# Variables para la tabla (se pueden definir también en el .env)
NOMBRE_TABLA = os.getenv("NOMBRE_TABLA")
CAMPO_NOMBRE = os.getenv("CAMPO_NOMBRE")

def actualizar_registros(conn, nombre_imagen, url_imagen):
    """
    Actualiza en la tabla el campo de URL de la imagen para todos
    los registros donde el nombre de la imagen coincida.
    
    Args:
        conn: Conexión abierta a la base de datos.
        nombre_imagen: Nombre de la imagen (o criterio) a buscar.
        url_imagen: URL obtenida tras subir la imagen.
    """
    try:
        cursor = conn.cursor()
        update_query = f"UPDATE {NOMBRE_TABLA} SET url_imagen = %s WHERE {CAMPO_NOMBRE} = %s"
        cursor.execute(update_query, (url_imagen, nombre_imagen))
        conn.commit()
        print(f"Se actualizó {cursor.rowcount} registro(s) para la imagen: {nombre_imagen}")
    except mysql.connector.Error as e:
        print(f"Error al actualizar la base de datos para {nombre_imagen}: {e}")

def procesar_imagenes():
    """
    Recorre la carpeta de imágenes, sube cada imagen y actualiza la URL en la base de datos.
    """
    # Establecer conexión a la base de datos MySQL
    try:
        conn = get_db_connection()
        print("Conexión a la base de datos establecida correctamente.")
    except mysql.connector.Error:
        return

    if not os.path.exists(CARPETA_IMAGENES):
        print(f"La carpeta {CARPETA_IMAGENES} no existe.")
        return

    for archivo in os.listdir(CARPETA_IMAGENES):
        if archivo.lower().endswith(EXTENSIONES_VALIDAS):
            ruta_imagen = os.path.join(CARPETA_IMAGENES, archivo)
            print(f"Procesando imagen: {ruta_imagen}")
            
            # Subir imagen y obtener URL
            url_imagen = subir_imagen_a_bucket(ruta_imagen, API_TOKEN)
            
            if url_imagen:
                # Se puede definir la lógica para extraer el nombre que coincida con el campo
                nombre_imagen = archivo  # si deseas quitar la extensión: os.path.splitext(archivo)[0]
                actualizar_registros(conn, nombre_imagen, url_imagen)
            else:
                print(f"No se pudo obtener la URL para {archivo}")
    
    conn.close()
    print("Procesamiento finalizado, conexión cerrada.")

if __name__ == '__main__':
    procesar_imagenes()