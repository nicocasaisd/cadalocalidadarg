from PIL import Image
import math
import requests
import shutil
import mercantile
import os
import random
import geopandas as gpd
from config import create_api



def get_random_loc(geojson_path):
    geojson = gpd.read_file(geojson_path)
    rand_index = random.randrange(1, len(geojson))
    random_loc = geojson.iloc[rand_index]

    return random_loc

def square_area_from_point(point, distance):
    points = gpd.GeoSeries([point])
    buffer = points.buffer(distance, cap_style=3)
    bounds = buffer.bounds;
    minx = max(buffer.bounds['minx'])
    maxx = max(buffer.bounds['maxx'])
    maxy = max(buffer.bounds['maxy'])
    miny = max(buffer.bounds['miny'])

    top_left = [maxy, minx]
    bottom_right = [miny, maxx]

    return top_left, bottom_right

def get_tile_range(top_left, bottom_right, zoom):
    # obtenemos el rango de tiles
    top_left_tiles = mercantile.tile(top_left[1],top_left[0],zoom)
    bottom_right_tiles = mercantile.tile(bottom_right[1],bottom_right[0],zoom)
    x_tile_range =[top_left_tiles.x,bottom_right_tiles.x]
    y_tile_range = [top_left_tiles.y,bottom_right_tiles.y]

    x_tile_range, y_tile_range = make_square_range(x_tile_range, y_tile_range)
    
    return x_tile_range, y_tile_range

def get_access_token():
    access_token = os.getenv("MAPBOX_ACCESS_TOKEN")
    return access_token

def get_images(x_tile_range, y_tile_range, zoom):

    access_token = get_access_token()

    #x_tile_range, y_tile_range = get_tiles_range(lat, lng, delta, zoom)

    for i,x in enumerate(range(x_tile_range[0],x_tile_range[1]+1)):
        for j,y in enumerate(range(y_tile_range[0],y_tile_range[1]+1)):   
            # Call the URL to get the image back
            r =requests.get('https://api.mapbox.com/v4/mapbox.satellite/'+str(zoom)+'/'
            +str(x)+'/'+str(y)+'@2x.pngraw?access_token='+access_token, stream=True)   
            with open('./satellite_images/' + str(i) + '.' + str(j) + '.png', 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

def clear_dirs(*dirs):
    for dir in dirs:
        # iteramos dentro del directorio
        for f in os.listdir(dir):
            #borramos cada archivo
            os.remove(os.path.join(dir, f))



def compose_image(img_name, x_tile_range, y_tile_range):
    # Make a list of the image names   
    image_files = ['./satellite_images/' + f for f in os.listdir('./satellite_images/')]
    # Open the image set using pillow
    images = [Image.open(x) for x in image_files]   
    # Calculate the number of image tiles in each direction
    edge_length_x = x_tile_range[1] - x_tile_range[0] + 1
    edge_length_y = y_tile_range[1] - y_tile_range[0] + 1
    edge_length_x = max(1,edge_length_x) # que no sea 0
    edge_length_y = max(1,edge_length_y)   
    # Find the final composed image dimensions  
    width, height = images[0].size
    total_width = width*edge_length_x
    total_height = height*edge_length_y
    # Create a new blank image we will fill in
    composite = Image.new('RGB', (total_width, total_height))   
    # Loop over the x and y ranges
    y_offset = 0
    for i in range(0,edge_length_x):
        x_offset = 0
        for j in range(0,edge_length_y):        
             # Open up the image file and paste it into the composed
             # image at the given offset position
            tmp_img = Image.open('./satellite_images/' + str(i) +  '.' + str(j) + '.png')
            composite.paste(tmp_img, (y_offset,x_offset))
            x_offset += width # Update the width
            
        y_offset += height # Update the height

    # Save the final image
    composite.save('./composite_images/'+img_name+'.png')

def make_square_range(x_tile_range, y_tile_range):
    # prueba para hacer cuadrado el marco de la imagen
    x_tile_len = (x_tile_range[1] - x_tile_range[0])
    y_tile_len = (y_tile_range[1] - y_tile_range[0])
    tile_diff = y_tile_len - x_tile_len
    if( tile_diff > 0):
        while(tile_diff != 0):
            if(tile_diff % 2 == 0):
                x_tile_range[0] -= 1
            else:
                x_tile_range[1] += 1

            x_tile_len = (x_tile_range[1] - x_tile_range[0])
            y_tile_len = (y_tile_range[1] - y_tile_range[0])
            tile_diff = y_tile_len - x_tile_len
    elif(tile_diff < 0):
        while(tile_diff != 0):
            if(tile_diff % 2 == 0):
                y_tile_range[0] -= 1
            else:
                y_tile_range[1] += 1

            x_tile_len = (x_tile_range[1] - x_tile_range[0])
            y_tile_len = (y_tile_range[1] - y_tile_range[0])
            tile_diff = y_tile_len - x_tile_len

    return x_tile_range, y_tile_range

""" if __name__ == "__main__":
    clear_dirs('satellite_images', 'composite_images')


    loc = get_random_loc('localidad.geojson')
    zoom = 15
    print(loc['nombre'])
    top_left, bottom_right = square_area_from_point(loc.geometry, 0.01)
    print(top_left)
    print(bottom_right)
    x_tile_range, y_tile_range = get_tile_range(top_left, bottom_right, zoom)
    print(f"nro de tiles en x: {x_tile_range[1]-x_tile_range[0]}")
    print(f"nro de tiles en y: {y_tile_range[1]-y_tile_range[0]}")


    get_images(x_tile_range, y_tile_range, zoom)
    compose_image('localidad', x_tile_range, y_tile_range)

    # Post tweet
    api = create_api()
    filename = "composite_images/localidad.png"
    status = "\U0001F4CD"+loc['nombre']+', '+loc['nom_depto'] +', '+loc['nom_pcia']
    api.update_status_with_media(status, filename)
 """