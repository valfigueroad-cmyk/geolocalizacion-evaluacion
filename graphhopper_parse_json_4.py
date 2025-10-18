import requests
import urllib.parse

# URLs base de la API
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"

# Clave API personal (reemplaza con la tuya si es distinta)
key = "c9c9a768-0f84-4744-b4a6-8dd502b121c9"

# Función para obtener coordenadas desde una ubicación
def geocoding(location, key):
    while location == "":
        location = input("Por favor, ingrese una ubicación válida: ")

    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_data = replydata.json()
    json_status = replydata.status_code

    if json_status == 200:
        lat = json_data["hits"][0]["point"]["lat"]
        lng = json_data["hits"][0]["point"]["lng"]
        name = json_data["hits"][0]["name"]
        value = json_data["hits"][0]["osm_value"]

        country = json_data["hits"][0].get("country", "")
        state = json_data["hits"][0].get("state", "")

        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif country:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name

        print(f"Coordenadas obtenidas correctamente para: {new_loc}")
        print(f"Tipo de ubicación: {value}")
        print(f"URL de geocodificación: {url}")
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        print("Error en la solicitud. Verifique la ubicación o la clave API.")
        print(f"Código de estado: {json_status}")
        print(f"Mensaje: {json_data.get('message', 'Error desconocido')}")

    return json_status, lat, lng, new_loc

# Bucle principal de interacción
while True:
    loc1 = input("Ingrese la ubicación de origen (o 's' para salir): ")
    if loc1.lower() in ["s", "salir"]:
        print("Programa finalizado por el usuario.")
        break

    orig_status, lat1, lng1, loc1_name = geocoding(loc1, key)

    loc2 = input("Ingrese la ubicación de destino (o 's' para salir): ")
    if loc2.lower() in ["s", "salir"]:
        print("Programa finalizado por el usuario.")
        break

    dest_status, lat2, lng2, loc2_name = geocoding(loc2, key)

    # Solicitud de ruta si ambas ubicaciones son válidas
    if orig_status == 200 and dest_status == 200:
        route_params = {
            "point": [f"{lat1},{lng1}", f"{lat2},{lng2}"],
            "vehicle": "car",
            "locale": "es",
            "key": key
        }
        route_url_full = route_url + urllib.parse.urlencode(route_params, doseq=True)
        route_response = requests.get(route_url_full)
        route_data = route_response.json()
        route_status = route_response.status_code

        if route_status == 200:
            distancia_km = round(route_data["paths"][0]["distance"] / 1000, 2)
            duracion_min = round(route_data["paths"][0]["time"] / 60000, 2)

            print(f"\n🛣️ Ruta desde {loc1_name} hasta {loc2_name}:")
            print(f"📏 Distancia total: {distancia_km} km")
            print(f"⏱️ Duración estimada: {duracion_min} minutos")
        else:
            print("Error al solicitar la ruta. Verifique los datos o la clave API.")
            print(f"Código de estado: {route_status}")
            print(f"Mensaje: {route_data.get('message', 'Error desconocido')}")
    else:
        print("No se pudo obtener coordenadas válidas para ambas ubicaciones.")

