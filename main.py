import geopandas as gpd
from config import create_api, create_api_v2
from collect_images import get_random_loc, square_area_from_point, get_tile_range, get_images, compose_image, clear_dirs


DEVELOPMENT = True


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

    get_images(x_tile_range, y_tile_range, zoom)
    filename = str(loc['nombre'])+'-z'+str(zoom)+'-a'+str(area)
    compose_image(filename, x_tile_range, y_tile_range)

    # Post tweet

    api = create_api()
    client = create_api_v2()
    filename_path = 'composite_images/'+filename+'.jpeg'
    status = "\U0001F4CD"+loc['nombre']+', '+loc['nom_depto'] +', '+loc['nom_pcia']
    #first_tweet = api.update_status_with_media(status, filename_path, lat=loc['lat_gd'], long=loc['long_gd'])
    # ver algo con geo reverse: , lat=loc['lat_gd'], long=loc['long_gd']
    #Create place id
    place_id = api.reverse_geocode(lat=loc['lat_gd'], long=loc['long_gd'], max_results=1)
    print(f"place_id: {place_id}")

    if(DEVELOPMENT == False):
        media_info = api.media_upload(filename=filename_path)
        first_tweet = client.create_tweet(text=status, media_ids=[media_info.media_id])
        print(f"first tweet: {first_tweet.data['id']}")
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

    get_images(x_tile_range, y_tile_range, zoom)
    filename = str(loc['nombre'])+'-z'+str(zoom)+'-a'+str(area)
    compose_image(filename, x_tile_range, y_tile_range)

    
    #Post response tweet
    if(DEVELOPMENT == False):
        filename_path = 'composite_images/'+filename+'.jpeg'
        status = ''
        #api.update_status_with_media(status, filename_path, in_reply_to_status_id=first_tweet.id, lat=loc['lat_gd'], long=loc['long_gd'])
        media_info = api.media_upload(filename=filename_path)
        second_tweet = client.create_tweet(text=status, media_ids=[media_info.media_id], in_reply_to_tweet_id=first_tweet.data['id'])
        print(f"seconda tweet: {second_tweet.data['id']}")