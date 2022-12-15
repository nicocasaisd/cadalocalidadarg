# CadaLocalidadArg


## Twitter Automated Bot

#### 🔗 [Link a la cuenta](https://mobile.twitter.com/CadaLocalidad)

Este bot utiliza el dataset del [BAHRA](http://www.bahra.gob.ar/) (Base de Asentamientos Humanos de la República Argentina) que es la primera base de datos oficial y normalizada de localidades del territorio nacional. 

Para la generación de imágenes utiliza los servicios de [MapBox](https://www.mapbox.com/) que brinda una API gratuita con uso limitado.

## Generación de imágenes

Se toma una localidad al azar del archivo `localidades.geojson`. 

```python
loc = get_random_loc('data/localidad.geojson')
```
A partir de los valores de latitud y longitud se obtienen las imágenes que corresponden al área con un valor de zoom establecido. 
```python
get_images(x_tile_range, y_tile_range, zoom)
```

Mapbox provee una serie de 'tiles' (baldosas) en alta resolución que luego deben ser compuestas para formar una única imagen.
```python
filename = str(loc['nombre'])+'-z'+str(zoom)+'-a'+str(area)
compose_image(filename, x_tile_range, y_tile_range)
```

#### Primera imagen generada
Se informa el nombre de la localidad, el departamento y la provincia.

![image](https://user-images.githubusercontent.com/76565736/207739274-55f9c3f5-6130-4481-ab8c-db8990de5d9a.png)

#### Segunda imagen generada
Se responde con una segunda imagen con un nivel mayor de zoom.
![image](https://user-images.githubusercontent.com/76565736/207739350-a149bdde-78e5-49b7-b1d2-21c107e10e06.png)


## Automatización con Github Actions

El bot realiza las publicaciones en twitter cada 2 horas utilizando los servicios de Github Actions.
