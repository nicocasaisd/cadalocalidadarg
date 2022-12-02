import geopandas as gpd
from collect_images import get_random_loc, square_area_from_point, get_tile_range, get_images, compose_image, clear_dirs

if __name__ == "__main__":
    geojson = gpd.read_file('data/localidad.geojson')
    localidades = [0,1]
    loc = geojson.iloc[localidades]