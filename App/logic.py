import time
import csv
import os

from DataStructures.List import array_list as lt
from DataStructures.List import single_linked_list as sll


base_dir = os.path.dirname(os.path.realpath('__file__'))
data_dir = os.path.join(base_dir, 'Data')

csv.field_size_limit(2147483647)



def new_logic():
    """
    Crea el catalogo para almacenar las estructuras de datos
    """
    catalog = {
        "computers": lt.new_list()
    }
    return catalog


# Funciones para la carga de datos

def load_data(catalog, filename):
    """
    Carga datos y retorna total, computador de menor precio,
    computador de mayor precio y tiempo de carga.
    """
    start_time = get_time()

    total_computers = load_computers(catalog, filename)
    min_comp, max_comp = get_min_max_price_computers(catalog["computers"])
    first_five_comp = get_first_five(catalog)
    last_five_comp = get_last_five(catalog)
    
    end_time = get_time()
    tiempo_transcurrido = delta_time(start_time, end_time)

    return total_computers, min_comp, max_comp, tiempo_transcurrido, first_five_comp, last_five_comp

# Funciones de consulta sobre el catÃ¡logo


def req_1(catalog, brand):
    """
    Retorna el resultado del requerimiento 1
    """
    #Inicializamos el tiempo
    start_time = get_time()
    tamanio = lt.size(catalog["computers"])
    #Eliminamos caracteres especiales y hacemos un lower para la marca
    brand_filter = brand.strip().lower()

    #Inicializamos la suma del total de computadores con esa marca, precio, ram, vram, num de nucleos y aÃ±o
    total_comp = 0
    sum_price = 0.0
    sum_ram = 0.0
    sum_vram = 0.0
    sum_num_nucleos = 0.0
    sum_release = 0.0

    #Inicializamos los datos solicitados en la documentaciÃ³n
    min_price = None
    max_price = None
    min_ram = None
    max_ram = None
    min_vram = None
    max_vram = None
    min_nucleos = None
    max_nucleos = None
    min_release = None
    max_release = None
    
    model_max_comp = None
    model_min_comp = None
    max_price_weight = None
    min_price_weight = None

    for i in range(tamanio):
        computer = lt.get_element(catalog["computers"], i)
        if computer["brand"].strip().lower() != brand_filter:
            continue

        price = float(computer["price"])
        ram = float(computer["ram_gb"])
        vram = float(computer["vram_gb"])
        cpu_cores = float(computer["cpu_cores"])
        release_year = int(computer["release_year"])
        weight = float(computer["weight_kg"])

        #Dado que hemos encontrado un computador con la marca ingresada, sumamos a los valores correspondientes
        total_comp += 1
        sum_price += price
        sum_ram += ram
        sum_vram += vram
        sum_num_nucleos += cpu_cores
        sum_release += release_year

        #Encontramos el menor
        if min_price is None or price < min_price:
            min_price = price
            model_min_comp = computer["model"]
            min_price_weight = weight
        #En caso de empate, nos quedamos con el de menor peso
        elif price == min_price and weight < min_price_weight:
            model_min_comp = computer["model"]
            min_price_weight = weight
        
        #Encontramos el de mayor precio
        if max_price is None or price > max_price:
            max_price = price
            model_max_comp = computer["model"]
            max_price_weight = weight
        #En caso de empate, nos quedamos con el de menor peso
        elif price == max_price and weight < max_price_weight:
            model_max_comp = computer["model"]
            max_price_weight = weight

        #Encontramos el computador de menor y mayor ram
        if min_ram is None or ram < min_ram:
            min_ram = ram
        if max_ram is None or ram > max_ram:
            max_ram = ram

        #Encontramos el computador de menor y mayor vram
        if min_vram is None or vram < min_vram:
            min_vram = vram
        if max_vram is None or vram > max_vram:
            max_vram = vram

        #Encontramos el computador de menor y mayor nÃºmero de nucleos
        if min_nucleos is None or cpu_cores < min_nucleos:
            min_nucleos = cpu_cores
        if max_nucleos is None or cpu_cores > max_nucleos:
            max_nucleos = cpu_cores

        #Encontramos el computador con el menor y mayor aÃ±o de lanzamiento
        if min_release is None or release_year < min_release:
            min_release = release_year
        if max_release is None or release_year > max_release:
            max_release = release_year

    #Verificamos que exista al menos 1 computador de dicha marca, sino retornamos 0 en cada uno de los promedios solicitados
    if total_comp > 0:
        prom_price = sum_price / total_comp
        prom_ram = sum_ram / total_comp
        prom_vram = sum_vram / total_comp
        prom_num_nucleos = sum_num_nucleos / total_comp
        prom_anio_release = sum_release / total_comp
    else:
        prom_price = 0.0
        prom_ram = 0.0
        prom_vram = 0.0
        prom_num_nucleos = 0.0
        prom_anio_release = 0.0
        
    general_info = {
        "marca": brand,
        "total_comp": total_comp,
        "prom_price": prom_price,
        "min_price": min_price,
        "max_price": max_price,
        "prom_ram": prom_ram,
        "min_ram": min_ram,
        "max_ram": max_ram,
        "prom_vram": prom_vram,
        "min_vram": min_vram,
        "max_vram": max_vram,
        "prom_nucleos": prom_num_nucleos,
        "min_nucleos": min_nucleos,
        "max_nucleos": max_nucleos,
        "prom_anio_release": prom_anio_release,
        "min_release": min_release,
        "max_release": max_release,
        "model_max": model_max_comp,
        "model_min": model_min_comp
    }
    #Finalizamos el tiempo de ejecuciÃ³n y calculamos el tiempo transcurrido
    end_time = get_time()
    tiempo_transcurrido = delta_time(start_time, end_time)

    return tiempo_transcurrido, total_comp, prom_price, min_price, max_price, prom_ram, min_ram, max_ram, prom_vram, min_vram, max_vram, prom_num_nucleos, min_nucleos, max_nucleos, prom_anio_release, min_release, max_release, model_max_comp, model_min_comp, general_info

def req_2(catalog, min_price, max_price):
    """
    Retorna el resultado del requerimiento 2
    """

    start_time = get_time()

    lista = lt.new_list()
    tamanio = lt.size(catalog["computers"])

    contador = 0
    sum_ram = 0.0
    sum_vram = 0.0
    sum_price = 0.0
    
    most_modern = None
    min_comp = None
    max_comp = None

    for i in range(tamanio):
        computer = lt.get_element(catalog["computers"], i)
        price = float(computer["price"])
        
        if min_price <= price <= max_price:
            lt.add_last(lista, computer)
            contador += 1
            sum_ram += float(computer["ram_gb"])
            sum_vram += float(computer["vram_gb"])
            sum_price += price
            
            if most_modern is None:
                most_modern = computer
            else:
                if int(computer["release_year"]) > int(most_modern["release_year"]):
                    most_modern = computer
                elif int(computer["release_year"]) == int(most_modern["release_year"]):
                    if price > float(most_modern["price"]):
                        most_modern = computer
            
            if (min_comp is None) or (price < float(min_comp["price"])):
                min_comp = computer
            
            if (max_comp is None) or (price > float(max_comp["price"])):
                max_comp = computer


    if contador > 0:

        prom_ram = sum_ram / contador
        prom_vram = sum_vram / contador
        prom_price = sum_price / contador

    else:
        prom_ram = 0.0
        prom_vram = 0.0
        prom_price = 0.0



    end_time = get_time()
    tiempo_transcurrido = delta_time(start_time, end_time)

    return lista, contador, prom_ram, prom_vram, prom_price, most_modern, min_comp, max_comp, tiempo_transcurrido


def req_3(catalog, cpu_brand, cpu_tier):
    """
    Retorna el resultado del requerimiento 3
    """
    start_time = get_time()

    filtered_computers = sll.new_list()
    sum_price = 0.0
    sum_ram = 0.0
    sum_vram = 0.0
    sum_threads = 0.0
    gpu_appearances = {}
    release_year_appearances = {}

    cpu_brand_filter = cpu_brand.lower()
    cpu_tier_filter = str(cpu_tier).lower()

    size = lt.size(catalog["computers"])
    for i in range(size):
        computer = lt.get_element(catalog["computers"], i)

        if computer["cpu_brand"].lower() == cpu_brand_filter and computer["cpu_tier"].lower() == cpu_tier_filter:
            sll.add_last(filtered_computers, computer)

            sum_price += float(computer["price"])
            sum_ram += float(computer["ram_gb"])
            sum_vram += float(computer["vram_gb"])
            sum_threads += float(computer["cpu_threads"])

            gpu_brand = computer["gpu_brand"]
            release_year = computer["release_year"]

            if gpu_brand in gpu_appearances:
                gpu_appearances[gpu_brand] += 1
            else:
                gpu_appearances[gpu_brand] = 1

            if release_year in release_year_appearances:
                release_year_appearances[release_year] += 1
            else:
                release_year_appearances[release_year] = 1

    count = sll.size(filtered_computers)

    if count > 0:
        avg_price = sum_price / count
        avg_ram = sum_ram / count
        avg_vram = sum_vram / count
        avg_threads = sum_threads / count
        most_common_gpu, most_common_gpu_appearances = get_most_common(gpu_appearances)
        most_common_release_year, most_common_release_year_appearances = get_most_common(release_year_appearances)
    else:
        avg_price = 0.0
        avg_ram = 0.0
        avg_vram = 0.0
        avg_threads = 0.0
        most_common_gpu = None
        most_common_gpu_appearances = 0
        most_common_release_year = None
        most_common_release_year_appearances = 0

    end_time = get_time()
    elapsed_time = delta_time(start_time, end_time)

    return (
        count,
        avg_price,
        avg_ram,
        avg_vram,
        avg_threads,
        most_common_gpu,
        most_common_gpu_appearances,
        most_common_release_year,
        most_common_release_year_appearances,
        elapsed_time,
    )


def get_most_common(counter_dict):
    """
    Retorna el valor de mayor frecuencia en un diccionario de conteos.
    """
    most_common = None
    max_count = -1

    for key, value in counter_dict.items():
        if value > max_count:
            max_count = value
            most_common = key
        elif value == max_count and most_common is not None and str(key) < str(most_common):
            most_common = key

    return most_common, max_count

def req_4(catalog, cpu_brand, gpu_model):
    """
    Retorna el resultado del requerimiento 4
    """
    # Inicializamos el tiempo
    start_time = get_time()
    size = lt.size(catalog["computers"])

    # Filtros normalizados
    brand_filter = cpu_brand.strip().lower()
    gpu_filter = gpu_model.strip().lower()

    # Totales y acumulados para promedios
    total_comp = 0
    sum_price = 0.0
    sum_vram = 0.0
    sum_ram = 0.0
    sum_modo_boost = 0.0

    # Dos computadores mas costosos (desempate por menor peso)
    primer_mas_costoso = None
    segundo_mas_costoso = None

    for i in range(size):
        computer = lt.get_element(catalog["computers"], i)

        if (
            computer["cpu_brand"].strip().lower() != brand_filter
            or computer["gpu_model"].strip().lower() != gpu_filter
        ):
            continue

        price = float(computer["price"])
        ram = float(computer["ram_gb"])
        vram = float(computer["vram_gb"])
        cpu_boost = float(computer["cpu_boost_ghz"])

        total_comp += 1
        sum_price += price
        sum_ram += ram
        sum_vram += vram
        sum_modo_boost += cpu_boost

        # Actualiza top 2
        if es_mejor_candidato(computer, primer_mas_costoso):
            segundo_mas_costoso = primer_mas_costoso
            primer_mas_costoso = computer
        elif es_mejor_candidato(computer, segundo_mas_costoso):
            segundo_mas_costoso = computer

    if total_comp > 0:
        prom_price = sum_price / total_comp
        prom_vram = sum_vram / total_comp
        prom_ram = sum_ram / total_comp
        prom_cpu_boost = sum_modo_boost / total_comp
    else:
        prom_price = 0.0
        prom_vram = 0.0
        prom_ram = 0.0
        prom_cpu_boost = 0.0

    mas_costosos = [primer_mas_costoso, segundo_mas_costoso]

    end_time = get_time()
    tiempo_transcurrido = delta_time(start_time, end_time)

    return tiempo_transcurrido, total_comp, prom_price, prom_vram, prom_ram, prom_cpu_boost, mas_costosos

def es_mejor_candidato(c1, c2):
        """
        Retorna True si c1 debe ir por encima de c2:
        mayor precio y, en empate, menor peso.
        """
        if c2 is None:
            return True

        c1_price = float(c1["price"])
        c2_price = float(c2["price"])

        if c1_price > c2_price:
            return True
        if c1_price < c2_price:
            return False

        c1_weight = float(c1["weight_kg"])
        c2_weight = float(c2["weight_kg"])
        return c1_weight < c2_weight
    
def req_5(catalog, filtro, resolucion, min_year, max_year):
    """
    Retorna el resultado del requerimiento 5
    """

    start_time = get_time()

    tamanio = lt.size(catalog["computers"])
    lista = lt.new_list()

    filtro = filtro.upper()
    
    total_compu = 0
    precio_suma = 0.0
    tamaño_display_suma = 0.0
    GPU_tier_suma = 0.0

    for i in range(tamanio):
            computer = lt.get_element(catalog["computers"], i)
            
            release = int(computer["release_year"])
            if min_year <= release <= max_year:
                if resolucion.strip() == computer["resolution"].strip():
                    lt.add_last(lista, computer)
                    total_compu += 1
                    precio_suma += float(computer["price"])
                    tamaño_display_suma += float(computer["display_size_in"])
                    GPU_tier_suma += float(computer["gpu_tier"])
    

    mejor_computer = None

    if filtro == "BARATO":
        for i in range(lt.size(lista)):
            computer = lt.get_element(lista, i)
            if mejor_computer is None:
                mejor_computer = computer
                
            elif float(computer["price"]) < float(mejor_computer["price"]):
                mejor_computer = computer
                
            elif float(computer["price"]) == float(mejor_computer["price"]):
                if float(computer["weight_kg"]) < float(mejor_computer["weight_kg"]):
                    mejor_computer = computer
                      

    elif filtro == "CARO":
        for i in range(lt.size(lista)):
            computer = lt.get_element(lista, i)
            if mejor_computer is None:
                mejor_computer = computer
                
            elif float(computer["price"]) > float(mejor_computer["price"]):
                mejor_computer = computer
                
            elif float(computer["price"]) == float(mejor_computer["price"]):
                if float(computer["weight_kg"]) < float(mejor_computer["weight_kg"]):
                    mejor_computer = computer

    if total_compu > 0:
        precio_promedio = precio_suma / total_compu
        tamaño_display_promedio = tamaño_display_suma / total_compu
        GPU_tier_promedio = GPU_tier_suma / total_compu
    else:
        precio_promedio = 0 
        tamaño_display_promedio = 0
        GPU_tier_promedio = 0
        
    mejor_info = None

    if mejor_computer is not None:
        mejor_info = {
            "price": mejor_computer["price"],
            "display_size": mejor_computer["display_size_in"],
            "gpu_tier": mejor_computer["gpu_tier"],
            "display_type": mejor_computer["display_type"],
            "release_year": mejor_computer["release_year"],
            "weight_kg": mejor_computer["weight_kg"]
        }

    

    end_time = get_time()
    tiempo_transcurrido = delta_time(start_time, end_time)

    return tiempo_transcurrido, filtro, total_compu, mejor_info, precio_promedio, tamaño_display_promedio, GPU_tier_promedio 

    # TODO: Modificar el requerimiento 5

def req_6(catalog):
    """
    Retorna el resultado del requerimiento 6
    """
    # TODO: Modificar el requerimiento 6
    pass


# Funciones para medir tiempos de ejecucion

def get_time():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)


def delta_time(start, end):
    """
    devuelve la diferencia entre tiempos de procesamiento muestreados
    """
    elapsed = float(end - start)
    return elapsed

# Funcion para total de computadores
def load_computers(catalog, filename):
    filepath = os.path.join(data_dir, 'computerData', filename)

    file = open(filepath, encoding="utf-8")
    reader = csv.DictReader(file)

    for computer in reader:
        lt.add_last(catalog["computers"], computer)
        
    file.close()
    return lt.size(catalog["computers"])


def get_min_max_price_computers(computers_list):
    """
    Retorna el computador de menor y mayor precio en una sola pasada.
    """
    size = lt.size(computers_list)
    if size == 0:
        return None, None

    min_comp = lt.get_element(computers_list, 0)
    max_comp = min_comp

    i = 1
    while i < size:
        comp = lt.get_element(computers_list, i)

        price = float(comp["price"])
        min_price = float(min_comp["price"])
        max_price = float(max_comp["price"])

        if price < min_price:
            min_comp = comp
        if price > max_price:
            max_comp = comp

        i += 1

    return min_comp, max_comp

def get_first_five(catalog):
    """
    FunciÃ³n para obtener los 5 primeros computadores del dataset
    """
    first_five = []
    tamanio = lt.size(catalog["computers"])
    for i in range(min(5,tamanio)):
        first_five.append(lt.get_element(catalog["computers"], i))

    return first_five

def get_last_five(catalog):
    """
    FunciÃ³n para obtener los 5 Ãºltimos computadores del dataset
    """
    last_five = []
    tamanio = lt.size(catalog["computers"])
    for i in range(max(0, tamanio - 5), tamanio):
        last_five.append(lt.get_element(catalog["computers"], i))

    return last_five

