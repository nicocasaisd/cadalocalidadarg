import os
from config import create_api

if __name__ == "__main__":
    api = create_api()
    filename = "composite_images/localidad.png"
    status = "Prueba"
    api.update_status_with_media(status, filename)