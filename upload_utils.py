import requests

def subir_imagen_a_bucket(file_path, token):
    """
    Sube una imagen a un bucket mediante una API.
    
    Args:
        file_path: Ruta al archivo de imagen a subir
        token: Token de autenticación
        
    Returns:
        URL de la imagen subida o None si ocurre un error
    """
    url = 'https://conexiones-star.concilbot.com/fileblocks'
    
    # Configurar los encabezados con el token
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    # Preparar el archivo para enviar
    with open(file_path, 'rb') as file:
        files = {
            'file': file
        }
        
        # Realizar la solicitud POST
        try:
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()  # Lanza una excepción si hay error HTTP
            
            print(f'Imagen enviada: {file_path}')
            print(f'Respuesta de la API: {response.text}')
            
            # Procesar la respuesta JSON
            decoded_response = response.json()
            return decoded_response.get('data', {}).get('imgeUrlOpenWindows')
            
        except requests.exceptions.RequestException as e:
            print(f'Error enviando la imagen {file_path}: {str(e)}')
            return None