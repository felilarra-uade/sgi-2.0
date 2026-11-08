# PRUEBAS UNITARIAS - SGI 2.0 (Segunda Parte)
# Se ejecutan aparte del programa principal con:  python pruebas_sgi.py

# Cada prueba es una función que arma sus propios datos, llama a la función del sistema, compara el resultado obtenido con el esperado y muestra todo en pantalla.
# Las pruebas no usan datos_por_defecto() ni leen/escriben archivos: así no dependen
# de los datos cargados ni de lo que haya en movimientos.txt, historial_stock.txt o los JSON.
#
# Distribución pedida por la consigna (10 pruebas sobre 10 funciones distintas):
#   Casos válidos:   pruebas 1 a 4
#   Casos inválidos: pruebas 5 a 7
#   Casos límite:    pruebas 8 y 9
#   Caso adicional:  prueba 10

import sgi

def mostrar_resultado(numero, tipo, funcion, datos, esperado, obtenido):
    # Muestra los 5 datos que pide la consigna para cada prueba y devuelve True si fue aprobada.
    aprobada = obtenido == esperado
    print("\n==================================================")
    print("PRUEBA", numero, "-", tipo)
    print("Función probada:   ", funcion)
    print("Datos utilizados:  ", datos)
    print("Resultado esperado:", esperado)
    print("Resultado obtenido:", obtenido)
    print("Prueba aprobada:   ", "SÍ" if aprobada else "NO")
    return aprobada

# CASOS VÁLIDOS

# Prueba 1: el diccionario acumulador suma bien el valor del stock por categoría.
# Hay dos registros de CAT-01, así se comprueba que el segundo se suma al primero y no lo pisa.
# Se usan recargos de 50% y 25% porque dan resultados exactos con float
# (por ejemplo, 7 unidades de $100 con 10% de recargo dan 770.0000000000001 y no 770.0).
# Si cambia una cantidad, un precio o un recargo, el valor esperado se tiene que recalcular a mano.
def prueba_01_valor_stock_por_categoria():
    productos = {"codigos": ["PRD-001", "PRD-002"], "nombres": ["Cuaderno", "Carpeta"], "precios": [100.0, 200.0]}
    categorias = {"codigos": ["CAT-01", "CAT-02"], "nombres": ["Papeleria", "Oficina"], "recargos": [50.0, 25.0], "estados": [1, 1]}
    inventario = {
        "codigos": ["INV-0001", "INV-0002", "INV-0003"],
        "codigos_prod": ["PRD-001", "PRD-002", "PRD-001"],
        "codigos_cat": ["CAT-01", "CAT-02", "CAT-01"],
        "cantidades": [10, 4, 2],
        "depositos": [1, 1, 2]
    }
    # CAT-01: 10 x 100 x 1.5 + 2 x 100 x 1.5 = 1500 + 300 = 1800 y CAT-02: 4 x 200 x 1.25 = 1000
    esperado = {"CAT-01": 1800.0, "CAT-02": 1000.0}
    obtenido = sgi.calcular_valor_stock_por_categoria(inventario, productos, categorias)
    datos = "precios " + str(productos["precios"]) + ", recargos " + str(categorias["recargos"]) + ", cantidades " + str(inventario["cantidades"])
    return mostrar_resultado(1, "Caso válido", "calcular_valor_stock_por_categoria()", datos, esperado, obtenido)


# Prueba 2: la búsqueda binaria encuentra un código que existe en una lista ordenada.
# Se busca un elemento del medio, que no es el primero que mira el algoritmo, para que tenga que achicar el rango.
# Si se busca un código que no está, el resultado tiene que ser -1.
def prueba_02_busqueda_binaria():
    codigos = ["PRD-101", "PRD-103", "PRD-105", "PRD-107", "PRD-109"]
    buscado = "PRD-107"
    esperado = 3
    obtenido = sgi.busqueda_binaria(codigos, buscado)
    datos = "lista " + str(codigos) + ", código buscado " + buscado
    return mostrar_resultado(2, "Caso válido", "busqueda_binaria()", datos, esperado, obtenido)


# Prueba 3: comparar dos depósitos con conjuntos devuelve la tupla (en ambos, solo en A, solo en B).
# PRD-101 tiene stock en los dos depósitos, PRD-102 solo en el 1 y PRD-103 solo en el 2.
# PRD-102 aparece dos veces en el depósito 1: el set lo guarda una sola vez.
# Si PRD-103 también estuviera en el depósito 1, pasaría al primer conjunto (en ambos).
def prueba_03_comparar_depositos():
    inv_prods = ["PRD-101", "PRD-102", "PRD-102", "PRD-101", "PRD-103"]
    inv_deps = [1, 1, 1, 2, 2]
    esperado = ({"PRD-101"}, {"PRD-102"}, {"PRD-103"})
    obtenido = sgi.comparar_depositos(inv_prods, inv_deps, 1, 2)
    datos = "productos " + str(inv_prods) + ", depósitos " + str(inv_deps) + ", comparar 1 y 2"
    return mostrar_resultado(3, "Caso válido", "comparar_depositos()", datos, esperado, obtenido)


# Prueba 4: una línea correcta de movimientos.txt se convierte en una tupla de 4 datos.
# Se incluye el salto de línea final porque así llegan las líneas cuando se lee el archivo.
# Si se sacara el strip() de la función, el código quedaría como "PRD-111\n" y la prueba fallaría.
def prueba_04_interpretar_linea_movimiento():
    linea = "lzanino,alta,producto,PRD-111\n"
    esperado = ("lzanino", "alta", "producto", "PRD-111")
    obtenido = sgi.interpretar_linea_movimiento(linea)
    return mostrar_resultado(4, "Caso válido", "interpretar_linea_movimiento()", repr(linea), esperado, obtenido)


# CASOS INVÁLIDOS

# Prueba 5: un precio "nan" se rechaza con ValueError (corrección que marcó Facundo).
# Se eligió porque float("nan") no da error, así que el rechazo tiene que venir del control de nan
# y no de la conversión. Si se borrara ese control, el precio se aceptaría y la prueba no se aprobaría.
def prueba_05_precio_nan():
    texto = "nan"
    esperado = "ValueError: 'nan' no es un número válido."
    try:
        valor = sgi.convertir_float_positivo(texto)
        obtenido = "Sin error, se aceptó el valor " + str(valor)
    except ValueError as error:
        obtenido = "ValueError: " + str(error)
    return mostrar_resultado(5, "Caso inválido", "convertir_float_positivo()", repr(texto), esperado, obtenido)


# Prueba 6: un código de categoría con 3 dígitos no cumple el formato CAT-NN.
# Se usa la tupla FORMATO_CATEGORIA, la misma que usa el sistema al pedir el código.
# Es el error que había en la Primera Parte: alta_categoria aceptaba códigos fuera de formato.
# Con "CAT-01" el resultado sería True.
def prueba_06_codigo_categoria_fuera_de_formato():
    prefijo, cant_digitos = sgi.FORMATO_CATEGORIA
    codigo = "CAT-001"
    esperado = False
    obtenido = sgi.es_codigo_valido(codigo, prefijo, cant_digitos)
    datos = codigo + " con formato " + str(sgi.FORMATO_CATEGORIA)
    return mostrar_resultado(6, "Caso inválido", "es_codigo_valido()", datos, esperado, obtenido)


# Prueba 7: una opción que no existe en el menú se rechaza con ValueError.
# El submenú de categorías va de 0 a 4, así que el 7 no es una opción válida.
# Con "3" la función devolvería el entero 3; con "tres" el error sería el de formato, no el de rango.
def prueba_07_opcion_inexistente():
    texto = "7"
    esperado = "ValueError: La opción 7 no existe. Ingrese una opción entre 0 y 4."
    try:
        opcion = sgi.convertir_opcion(texto, 0, 4)
        obtenido = "Sin error, se aceptó la opción " + str(opcion)
    except ValueError as error:
        obtenido = "ValueError: " + str(error)
    return mostrar_resultado(7, "Caso inválido", "convertir_opcion()", repr(texto) + ", rango 0 a 4", esperado, obtenido)


# CASOS LÍMITE

# Prueba 8: un nombre de exactamente 40 caracteres (el máximo permitido) se acepta.
# Controla que la condición use <= y no <. Si se agregara una letra más (41), el resultado sería False.
def prueba_08_nombre_largo_maximo():
    nombre = "Mochila escolar con ruedas y dos cierres"
    esperado = True
    obtenido = sgi.es_nombre_valido(nombre)
    datos = repr(nombre) + " (" + str(len(nombre)) + " caracteres)"
    return mostrar_resultado(8, "Caso límite", "es_nombre_valido()", datos, esperado, obtenido)


# Prueba 9: el reporte de productos con las listas vacías devuelve el aviso en lugar de romperse.
# reduce() sin valor inicial lanza TypeError si recibe una lista vacía; el if del principio lo evita.
# Si se sacara ese if, la prueba terminaría con error en vez de mostrar el mensaje.
def prueba_09_reporte_productos_vacio():
    esperado = "No hay productos cargados."
    obtenido = sgi.generar_reporte_productos([], [], [])
    return mostrar_resultado(9, "Caso límite", "generar_reporte_productos()", "listas de códigos, nombres y precios vacías", esperado, obtenido)


# CASO ADICIONAL (propio del sistema)

# Prueba 10: regla "un producto, una categoría".
# PRD-101 ya tiene stock en CAT-01 y se intenta dar de alta un registro nuevo en CAT-03.
# La función tiene que devolver la categoría en conflicto para que el alta se cancele.
# En un alta se pasa -1 como índice ignorado. Si el registro nuevo fuera en CAT-01, el resultado sería None.
def prueba_10_categoria_en_conflicto():
    inv_prods = ["PRD-101", "PRD-102", "PRD-101"]
    inv_cats = ["CAT-01", "CAT-02", "CAT-01"]
    esperado = "CAT-01"
    obtenido = sgi.buscar_categoria_en_conflicto(inv_prods, inv_cats, "PRD-101", "CAT-03", -1)
    datos = "productos " + str(inv_prods) + ", categorías " + str(inv_cats) + ", alta de PRD-101 en CAT-03"
    return mostrar_resultado(10, "Caso adicional", "buscar_categoria_en_conflicto()", datos, esperado, obtenido)


def ejecutar_pruebas():
    pruebas = [
        prueba_01_valor_stock_por_categoria,
        prueba_02_busqueda_binaria,
        prueba_03_comparar_depositos,
        prueba_04_interpretar_linea_movimiento,
        prueba_05_precio_nan,
        prueba_06_codigo_categoria_fuera_de_formato,
        prueba_07_opcion_inexistente,
        prueba_08_nombre_largo_maximo,
        prueba_09_reporte_productos_vacio,
        prueba_10_categoria_en_conflicto,
    ]
    aprobadas = 0
    for prueba in pruebas:
        if prueba():
            aprobadas += 1

    print("\n==================================================")
    print("RESUMEN: " + str(aprobadas) + " de " + str(len(pruebas)) + " pruebas aprobadas.")


if __name__ == "__main__":
    ejecutar_pruebas()