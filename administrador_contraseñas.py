import requests

# Ruta completa al archivo
ruta = r"C:\Users\marti\OneDrive\Desktop\ESCUELA\CUATRIMESTRE 2\PROGRAMACION ESTRUCTURADA\contraseñas.txt"

url_login = "https://httpbin.org/post"

try:
    with open(ruta, 'r', encoding='utf-8') as f:
        contraseñas = f.readlines()
        contraseñas = [c.strip() for c in contraseñas]
except FileNotFoundError:
    print("El archivo contraseñas.txt no se encontró.")
    exit(1)

for contraseña in contraseñas:
    try:
        response = requests.post(url_login, data={'username': 'tu_usuario', 'password': contraseña})
        if response.status_code == 200:
            print(f"Login exitoso con la contraseña: {contraseña}")
            break
        else:
            print(f"Login fallido con la contraseña: {contraseña}")
    except requests.exceptions.RequestException as e:
        print(f"Ocurrió un error al intentar hacer el login: {e}")