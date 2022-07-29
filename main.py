import geopandas as gpd
from config import create_api
from collect_images import get_random_loc, square_area_from_point, get_tile_range, get_images, compose_image, clear_dirs


DEVELOPMENT = True


if __name__ == "__main__":
    clear_dirs('satellite_images', 'composite_images')

    if(DEVELOPMENT):
        geojson = gpd.read_file('data/minlocalidad.geojson')
        loc = geojson.iloc[5]

    else:
        loc = get_random_loc('data/localidad.geojson')
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
    if(DEVELOPMENT == False):
        api = create_api()
        filename = "composite_images/localidad.png"
        status = "\U0001F4CD"+loc['nombre']+', '+loc['nom_depto'] +', '+loc['nom_pcia']
        api.update_status_with_media(status, filename)
