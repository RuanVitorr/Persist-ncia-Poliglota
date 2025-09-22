from geopy.distance import geodesic
from db_mongo import listar_restaurantes

def calcular_distancia(coord1, coord2):
    """
    Calcula a distância em km entre duas coordenadas.
    coord1, coord2 = (lat, lon)
    """
    return geodesic(coord1, coord2).km

def restaurantes_proximos(lat, lon, raio_km=5):
    """
    Retorna uma lista de restaurantes que estão dentro do raio_km da coordenada.
    """
    resultado = []
    todos = listar_restaurantes()

    for r in todos:
        if "coordenadas" in r and r["coordenadas"].get("lat") is not None:
            r_coord = (r["coordenadas"]["lat"], r["coordenadas"]["lon"])
            distancia = calcular_distancia((lat, lon), r_coord)
            if distancia <= raio_km:
               
                r_copy = r.copy()
                r_copy["distancia_km"] = round(distancia, 2)
                resultado.append(r_copy)

    # Ordena do mais próximo para o mais distante
    resultado.sort(key=lambda x: x["distancia_km"])
    return resultado
