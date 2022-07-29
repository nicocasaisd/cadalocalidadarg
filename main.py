import geopandas as gpd
from config import create_api
from collect_images import get_random_loc, square_area_from_point, get_tile_range, get_images, compose_image, clear_dirs


DEVELOPMENT = False


if __name__ == "__main__":

    clear_dirs('satellite_images', 'composite_images')

    #geojson = gpd.read_file('data/localidad.geojson')
    #loc = geojson.iloc[1445]

    loc = get_random_loc('data/localidad.geojson')
    
    print(loc['nombre'])

    # Obtengo imagenes con zoom=15 y area=0.01
    zoom=15
    area=0.01
    top_left, bottom_right = square_area_from_point(loc.geometry, area)
    x_tile_range, y_tile_range = get_tile_range(top_left, bottom_right, zoom)
    # Log
    print(top_left)
    print(bottom_right)
    print(f"nro de tiles en x: {x_tile_range[1]-x_tile_range[0]} \t range: {x_tile_range}")
    print(f"nro de tiles en y: {y_tile_range[1]-y_tile_range[0]} \t range: {y_tile_range}")

    if(DEVELOPMENT == False):
        get_images(x_tile_range, y_tile_range, zoom)
        filename = str(loc['nombre'])+'-z'+str(zoom)+'-a'+str(area)
        compose_image(filename, x_tile_range, y_tile_range)

    # Post tweet
    if(DEVELOPMENT == False):
        api = create_api()
        filename_path = 'composite_images/'+filename+'.jpeg'
        status = "\U0001F4CD"+loc['nombre']+', '+loc['nom_depto'] +', '+loc['nom_pcia']
        first_tweet = api.update_status_with_media(status, filename_path, lat=loc['lat_gd'], long=loc['long_gd'])
        print(f"first tweet: {first_tweet.id}")
    # Obtengo imagenes con zoom=16 y area=0.005
    zoom=16
    area=0.005
    top_left, bottom_right = square_area_from_point(loc.geometry, area)
    x_tile_range, y_tile_range = get_tile_range(top_left, bottom_right, zoom)
    # Log
    print(top_left)
    print(bottom_right)
    print(f"nro de tiles en x: {x_tile_range[1]-x_tile_range[0]} \t range: {x_tile_range}")
    print(f"nro de tiles en y: {y_tile_range[1]-y_tile_range[0]} \t range: {y_tile_range}")

    if(DEVELOPMENT == False):
        get_images(x_tile_range, y_tile_range, zoom)
        filename = str(loc['nombre'])+'-z'+str(zoom)+'-a'+str(area)
        compose_image(filename, x_tile_range, y_tile_range)

    
    #Post response tweet
    if(DEVELOPMENT == False):
        filename_path = 'composite_images/'+filename+'.jpeg'
        api.update_status_with_media(status, filename_path, in_reply_to_status_id=first_tweet.id, lat=loc['lat_gd'], long=loc['long_gd'])
