import re
from functools import reduce
# FUNCIONES DE VALIDACIÓN
# Usamos try-except para atajar el error si el usuario ingresa un string en vez de un número.
def es_entero(var_str):
    try:
        int(var_str)
        return True     
    except:
        return False

def es_float(var_str):
    try:
        float(var_str)
        return True 
    except:
        return False
    
# Usada para validar las opciones de menú, asegurando que el usuario ingrese un número dentro del rango permitido.
def solicitar_opcion_menu(mensaje, min_opcion, max_opcion):
    dato = input(mensaje)
    while not es_entero(dato) or int(dato) < min_opcion or int(dato) > max_opcion:
        print(f"Error: Ingrese una opción válida ({min_opcion} a {max_opcion}).")
        dato = input(mensaje)
    return int(dato)

# Validamos que el input no quede vacío y que no contenga solo números usando las validaciones.
def pedir_entero(mensaje):
    # Valida que el ingreso sea un número entero y mayor a cero (para códigos y cantidades).
    dato = input(mensaje)
    while not es_entero(dato) or int(dato) <= 0:
        print("Error: Debe ingresar un número entero positivo mayor a 0.")
        dato = input(mensaje)
    return int(dato)

def pedir_float(mensaje):
    # Valida que el ingreso sea un número decimal y mayor a cero (para precios y recargos).
    dato = input(mensaje)
    while not es_float(dato) or float(dato) <= 0:
        print("Error: Debe ingresar un número válido mayor a 0.")
        dato = input(mensaje)
    return float(dato)

# Validación de nombres con expresión regulares.
# Patrón: solo letras (incluye tildes y ñ) y espacios.
PATRON_NOMBRE = r"^[A-Za-zÁÉÍÓÚÜáéíóúüÑñ ]+$"

def es_nombre_valido(texto):
    texto = texto.strip()
    if not (3 <= len(texto) <= 40):
        return False
    return re.match(PATRON_NOMBRE, texto) is not None

def pedir_texto(mensaje):
    # Valida que el texto no esté vacío y no tenga números ni símbolos.
    dato = input(mensaje)
    while not es_nombre_valido(dato):
        print("Error: Debe ingresar un texto válido (solo letras y espacios, entre 3 y 40 caracteres, sin números ni símbolos).")
        dato = input(mensaje)
    return dato.strip()

# Validación de códigos con expresión regulares.
# Cada entidad del sistema tiene un código con formato alfanumérico fijo:
# Productos: PRD-NNN
# Categorías: CAT-NN
# Inventario: INV-NNNN
# El patrón se arma dinámicamente en base al prefijo y la cantidad de dígitos esperada, y luego se valida con re.match()
def es_codigo_valido(dato, prefijo, cant_digitos):
    patron = r"^" + prefijo + r"-\d{" + str(cant_digitos) + r"}$"
    return re.match(patron, dato) is not None

def pedir_codigo(mensaje, prefijo, cant_digitos):
# .strip() usado para descartar espacios de más.
    dato = input(mensaje).strip()
    while not es_codigo_valido(dato, prefijo, cant_digitos):
        ejemplo = prefijo + "-" + ("0" * (cant_digitos - 1)) + "1"
        print(f"Error: El código debe tener el formato {prefijo}-{'N' * cant_digitos} (ej: {ejemplo}).")
        dato = input(mensaje).strip()
    return dato

# ORDENAMIENTOS (Readaptación)
"""
Originalmente había tres ordenamientos distintos (burbuja, selección e inserción), uno para cada entidad.
Ahora se realiza la adaptación a una sola función que ordena cualquier conjunto de listas paralelas según
el campo que se le indique. 
"""

def ordenar_listas_paralelas(listas, indice_clave):
    """
    Ordena un conjunto de listas paralelas en base a los valores de una de ellas.
    Parámetro listas: lista que contiene las listas paralelas a ordenar.
    Parámetro indice_clave: posición, dentro de 'listas', de la lista que se usa como criterio de orden.
    """
    n = len(listas[indice_clave])
    # 1. Armamos una lista de índices (0, 1, 2, ..., n-1), uno por cada fila
    indices = list(range(n))
    # 2. Ordenamos esos índices usando sort() con una lambda que consulta, para cada índice, el valor de la columna elegida
    indices.sort(key=lambda i: listas[indice_clave][i])
    # 3. Reconstruimos cada lista paralela en el nuevo orden, usando comprensión
    #    de listas dentro de un for común por cada columna
    listas_ordenadas = []
    for columna in listas:
        nueva_columna = [columna[i] for i in indices]
        listas_ordenadas.append(nueva_columna)
    # 4. Volcamos el resultado ordenado de nuevo en cada una de las listas originales
    for j in range(len(listas)):
        for k in range(n):
            listas[j][k] = listas_ordenadas[j][k]

# Búsqueda binaria: Divide el espacio de búsqueda por la mitad en cada iteración, requiere que la lista esté ordenada previamente.
# Readaptada para trabajar con Strings en lugar de enteros.
def busqueda_binaria(lista_codigos, codigo_buscado):
    # Inicializamos los límites de búsqueda (izquierdo y derecho)
    izquierda = 0
    derecha = len(lista_codigos) - 1

    # Mientras el rango de búsqueda sea válido (izquierda no supera derecha)
    while izquierda <= derecha:
        # Calculamos el punto medio del rango actual
        centro = (izquierda + derecha) // 2

        # Si encontramos el elemento en el centro, lo retornamos
        if lista_codigos[centro] == codigo_buscado:
            return centro
        # Si el elemento del centro es menor al buscado, buscamos en la mitad derecha
        elif lista_codigos[centro] < codigo_buscado:
            izquierda = centro + 1
        # Si el elemento del centro es mayor al buscado, buscamos en la mitad izquierda
        else:
            derecha = centro - 1
    
    # Si no encontramos el elemento, retornamos -1
    return -1

# Búsqueda secuencial: recorre la lista elemento por elemento hasta encontrar el código buscado.
def buscar_indice(lista_codigos, codigo_buscado):
    # Iteramos sobre cada posición de la lista
    for i in range(len(lista_codigos)):
        # Si encontramos el código buscado, retornamos su índice
        if lista_codigos[i] == codigo_buscado:
            return i 
    # Si no encontramos el código, retornamos -1
    return -1 

def buscar_producto_secuencial(codigos, nombres, precios):
    # Solicitamos el código del producto a buscar (validado con regex, formato PRD-NNN)
    codigo = pedir_codigo("\nIngrese el código del producto (formato PRD-000): ", "PRD", 3)
    # Realizamos la búsqueda secuencial en la lista de códigos
    indice = buscar_indice(codigos, codigo)

    # Si no se encuentra (índice = -1), mostramos mensaje de error
    if indice == -1:
        print("Producto no encontrado.")
    # Si se encuentra, mostramos todos los datos del producto
    else:
        print("Código:", codigos[indice])
        print("Nombre:", nombres[indice])
        print("Precio:", precios[indice])

def buscar_producto_binaria(codigos, nombres, precios):
    # Solicitamos el código del producto a buscar (validado con regex, formato PRD-NNN)
    codigo = pedir_codigo("\nIngrese el código del producto (formato PRD-000): ", "PRD", 3)
    """
    READAPTACIÓN: la búsqueda binaria requiere que la lista esté ordenada por código.
    Para no alterar ese orden ni el de las listas originales, se arma una copia de cada lista y se ordena esa copia por código,
    reutilizando la misma función genérica de ordenamiento.
    """
    codigos_por_codigo = codigos.copy()
    nombres_por_codigo = nombres.copy()
    precios_por_codigo = precios.copy()
    ordenar_listas_paralelas([codigos_por_codigo, nombres_por_codigo, precios_por_codigo], 0)

    indice = busqueda_binaria(codigos_por_codigo, codigo)

    # Si no se encuentra (índice = -1), mostramos mensaje de error
    if indice == -1:
        print("Producto no encontrado.")
    # Si se encuentra, mostramos todos los datos del producto
    else:
        print("Código:", codigos_por_codigo[indice])
        print("Nombre:", nombres_por_codigo[indice])
        print("Precio:", precios_por_codigo[indice])


# FUNCIONES BASE Y LOGIN
def buscar_usuario(usuarios, nombre_usuario):
    # Busca un usuario por su nombre usando .get(), que devuelve el diccionario
    # con sus datos si existe, o None si no existe.
    return usuarios.get(nombre_usuario)

def iniciar_sesion(usuarios):
 
    logged_in = False
    intentos = 0
 
    # El usuario tiene 3 intentos para ingresar las credenciales correctas. Si falla los 3 intentos, se bloquea el acceso.
    while logged_in == False and intentos < 3:
        input_user = input("Ingrese su usuario: ")
        input_password = input("Ingrese su contraseña: ")
 
        user_data = buscar_usuario(usuarios, input_user)

        # A partir de acá, la cadena de elif es excluyente: si user_data es None,
        # ninguno de los elif siguientes se ejecuta. Por eso, para cuando llegamos
        # al último elif, ya está garantizado que el usuario existe.
        if user_data == None:
            print("El usuario no existe. Intente nuevamente.\n")
            intentos += 1
        elif user_data["bloqueado"]:
            print("El usuario está bloqueado. Contacte al administrador.\n")
            intentos += 1
        elif user_data["contrasena"] != input_password:
            print("Contraseña incorrecta. Intente nuevamente.\n")
            user_data["intentos_fallidos"] += 1
            intentos += 1
            if user_data["intentos_fallidos"] >= 3:
                user_data["bloqueado"] = True
                print("!!!!!!!! El usuario ha sido bloqueado por 3 intentos fallidos. !!!!!!!! \n")
        elif user_data["contrasena"] == input_password:
            # No hace falta validar el usuario de nuevo acá: si llegamos hasta este
            # punto, ya sabemos que existe (se descartó en el primer if de arriba)
            print("Inicio de sesión exitoso. Bienvenido al sistema de inventario!")
            logged_in = True

    if not logged_in:
        print("<<<<<<<<<< Fallaste 3 intentos. Volvé a intentarlo más tarde. >>>>>>>>>>\n")

    return user_data if logged_in else None


def listar_usuarios_bloqueados(usuarios):
    encontrado = False;

    print("\n --- USUARIOS BLOQUEADOS ---")
    for nombre_usuario, datos in zip(usuarios.keys(), usuarios.values()):
        if datos["bloqueado"]:
            encontrado = True
            print("Usuario:", nombre_usuario, "| Rol:", datos["rol"], "| Intentos fallidos:", datos["intentos_fallidos"])
    if not encontrado:
        print("No hay usuarios bloqueados.")

def desbloquear_usuario(usuarios, nombre_usuario):
    user_data = buscar_usuario(usuarios, nombre_usuario)

    if user_data is None:
        print("Error: El usuario no existe.")
        return
    elif user_data["bloqueado"]:
        user_data["bloqueado"] = False
        user_data["intentos_fallidos"] = 0
        print(f"Usuario '{nombre_usuario}' desbloqueado exitosamente.")

def administrar_usuarios_bloqueados(usuarios):
    # Muestra los usuarios bloqueados y permite al admin desbloquear a uno,
    # o escribir 'volver' para salir sin hacer nada.
    listar_usuarios_bloqueados(usuarios)
    nombre_usuario = pedir_texto("\nIngrese el nombre de usuario a desbloquear (o 'volver' para cancelar): ")
    if nombre_usuario.lower() == "volver":
        return
    desbloquear_usuario(usuarios, nombre_usuario)


# DATOS HARDCODEADOS DE USUARIOS (diccionario anidado: usuario -> datos del usuario)
usuarios = {
    "admin": {"contrasena": "inventario2026", "rol": "admin", "intentos_fallidos": 0, "bloqueado": False},
    "lzanino": {"contrasena": "clave123", "rol": "usuario", "intentos_fallidos": 0, "bloqueado": False},
}

#  DATOS HARDCODEADOS (LISTAS PARALELAS)
# Los códigos ahora tienen formato alfanumérico validable por RE:
# PRD-NNN (productos), CAT-NN (categorías), INV-NNNN (inventario).
prod_codigos = ["PRD-101", "PRD-102", "PRD-103", "PRD-104", "PRD-105", "PRD-106", "PRD-107", "PRD-108", "PRD-109", "PRD-110"]
prod_nombres = ["Cuaderno", "Lapicera", "Goma", "Carpeta", "Marcador", "Tijera", "Regla", "Corrector", "Mochila", "Cartuchera"]
prod_precios = [1500.0, 200.0, 150.0, 2500.0, 800.0, 1200.0, 300.0, 600.0, 15000.0, 3500.0]

cat_codigos = ["CAT-01", "CAT-02", "CAT-03", "CAT-04", "CAT-05", "CAT-06", "CAT-07", "CAT-08", "CAT-09", "CAT-10"]
cat_nombres = ["Papeleria", "Escritura", "Escolares", "Oficina", "Arte", "Mochilas", "Tecnologia", "Libros", "Regalos", "Varios"]
cat_recargos = [15.0, 10.0, 20.0, 25.0, 30.0, 35.0, 40.0, 5.0, 50.0, 10.0]
cat_estados = [1, 1, 1, 0, 1, 1, 0, 1, 1, 1]

inv_codigos = ["INV-1001", "INV-1002", "INV-1003", "INV-1004", "INV-1005", "INV-1006", "INV-1007", "INV-1008", "INV-1009", "INV-1010"]
inv_codigos_prod = ["PRD-101", "PRD-102", "PRD-103", "PRD-104", "PRD-105", "PRD-106", "PRD-107", "PRD-108", "PRD-109", "PRD-110"]
inv_codigos_cat = ["CAT-01", "CAT-02", "CAT-03", "CAT-01", "CAT-05", "CAT-03", "CAT-03", "CAT-03", "CAT-06", "CAT-03"]
inv_cantidades = [50, 200, 100, 30, 150, 80, 45, 120, 90, 15]
inv_depositos = [1, 1, 2, 1, 3, 2, 1, 2, 1, 3]

# MATRICES (cada elemento es una columna = una lista paralela ya cargada)
columnas_prod = [prod_codigos, prod_nombres, prod_precios]
columnas_cat = [cat_codigos, cat_nombres, cat_recargos, cat_estados]
columnas_inv = [inv_codigos, inv_codigos_prod, inv_codigos_cat, inv_cantidades, inv_depositos]

# FUNCIONES CRUD 
# PRODUCTOS
def alta_producto(codigos, nombres, precios):
    codigo = pedir_codigo("\nIngrese el código del nuevo producto (formato PRD-000): ", "PRD", 3)
    if buscar_indice(codigos, codigo) != -1:
        print("Error: Ya existe un producto con ese código.")
    else:
        nombre = pedir_texto("Ingrese el nombre del producto: ")
        # Validación agregada por Lautaro Zanino: evita cargar un producto con un nombre ya existente
        # (aunque difiera en mayúsculas/minúsculas o espacios) usando nombre_duplicado().
        if nombre_duplicado(nombres, nombre):
            print("Error: Ya existe un producto con un nombre igual o muy similar.")
            return
        
        precio = pedir_float("Ingrese el precio: $")
        codigos.append(codigo)
        nombres.append(nombre)
        precios.append(precio)
        print("¡Producto agregado con éxito!")

def baja_producto(codigos, nombres, precios, inv_prods):
    codigo = pedir_codigo("\nIngrese el código del producto a eliminar (formato PRD-000): ", "PRD", 3)
    
    # Verificación de integridad de datos
    # Si el producto existe en el inventario, no se puede eliminar hasta que no esté eliminado el registro de inventario que contiene ese producto
    if buscar_indice(inv_prods, codigo) != -1:
        print("Error: No se puede eliminar. Hay stock de este producto en el inventario.")
        return 

    indice = buscar_indice(codigos, codigo)
    if indice == -1:
        print("Error: El producto no existe.")
    else:
        codigos.pop(indice)
        nombre_borrado = nombres.pop(indice)
        precios.pop(indice)
        print("Producto '" + nombre_borrado + "' eliminado correctamente.")

def modificar_producto(codigos, nombres, precios):
    codigo = pedir_codigo("\nIngrese el código del producto a modificar (formato PRD-000): ", "PRD", 3)
    indice = buscar_indice(codigos, codigo)
    if indice == -1:
        print("Error: El producto no existe.")
    else:
        print("Producto actual: ", nombres[indice], "- Precio: $", precios[indice])
        nuevo_nombre = pedir_texto("Ingrese el nuevo nombre: ")
        nuevo_precio = pedir_float("Ingrese el nuevo precio: $")
        nombres[indice] = nuevo_nombre
        precios[indice] = nuevo_precio
        print("Producto actualizado.")

def listar_productos(codigos, nombres, precios):
    # Muestra el listado de productos. El armado del texto 
    # ahora lo hace generar_reporte_productos(), que usa reduce
    # para combinar todas las líneas en un único string antes de imprimirlas.
    print(generar_reporte_productos(codigos, nombres, precios))
def generar_reporte_productos(codigos, nombres, precios):
    if len(codigos) == 0:
        return "No hay productos cargados."

    lineas = []
    for i in range(len(codigos)):
        linea = "Cód: " + str(codigos[i]) + " | Nombre: " + nombres[i] + " | Precio: $" + str(precios[i])
        lineas.append(linea)

    # 'reduce' junta todas las líneas en un unico string.
    # Todo eso se guarda en la variable reporte la cual luego se usa para mostrar la informacion
    reporte = reduce(lambda acumulado, linea: acumulado + "\n" + linea, lineas)
    return "\n--- LISTA DE PRODUCTOS ---\n" + reporte

# CATEGORÍAS
def alta_categoria(codigos, nombres, recargos, estados):
    codigo = pedir_codigo("\nIngrese el código de la nueva categoría (formato CAT-00): ", "CAT", 2)
    if buscar_indice(codigos, codigo) != -1:
        print("Error: Ya existe una categoría con ese código.")
    else:
        nombre = pedir_texto("Ingrese el nombre de la categoría: ")
        # Validación agregada por Lautaro Zanino: evita cargar una categoría con un nombre ya existente
        # usando la misma función nombre_duplicado()
        if nombre_duplicado(nombres, nombre):
            print("Error: Ya existe una categoría con un nombre igual o muy similar.")
            return

        recargo = pedir_float("Ingrese el porcentaje de recargo (ej: 15.5): ")
        estado = solicitar_opcion_menu("Ingrese el estado (1 = activa / 0 = inactiva): ", 0, 1)
        codigos.append(codigo)
        nombres.append(nombre)
        recargos.append(recargo)
        estados.append(estado)
        print("¡Categoría agregada con éxito!")

def baja_categoria(codigos, nombres, recargos, estados, inv_cats):
    codigo = pedir_codigo("\nIngrese el código de la categoría a eliminar (formato CAT-00): ", "CAT", 2)
    
    # Verificación de integridad de datos - Si la categoría existe en el inventario, no se puede eliminar hasta que no esté eliminado el registro de inventario que contiene esa categoría
    if buscar_indice(inv_cats, codigo) != -1:
        print("Error: No se puede eliminar. Hay productos en el inventario vinculados a esta categoría.")
        return 

    indice = buscar_indice(codigos, codigo)
    if indice == -1:
        print("Error: La categoría no existe.")
    else:
        codigos.pop(indice)
        nombre_borrado = nombres.pop(indice)
        recargos.pop(indice)
        estados.pop(indice)
        print("Categoría '" + nombre_borrado + "' eliminada correctamente.")

def modificar_categoria(codigos, nombres, recargos, estados):
    codigo = pedir_codigo("\nIngrese el código de la categoría a modificar (formato CAT-00): ", "CAT", 2)
    indice = buscar_indice(codigos, codigo)
    if indice == -1:
        print("Error: La categoría no existe.")
    else:
        print("Categoría actual:", nombres[indice], "| Recargo:", recargos[indice], "% | Estado:", estados[indice])
        nuevo_nombre = pedir_texto("Ingrese el nuevo nombre: ")
        nuevo_recargo = pedir_float("Ingrese el nuevo recargo: ")
        nuevo_estado = solicitar_opcion_menu("Ingrese el nuevo estado (1 = activa / 0 = inactiva): ", 0, 1)
        nombres[indice] = nuevo_nombre
        recargos[indice] = nuevo_recargo
        estados[indice] = nuevo_estado
        print("Categoría actualizada.")


def listar_categorias(codigos, nombres, recargos, estados):
    # Muestra el listado de categorías. El que se encarga de armar el texto es la nueva funcion 
    # generar_reporte_categoria(), la cual usa 'reduce' para
    # combinar todas las líneas en un único string antes de imprimirlas
    print(generar_reporte_categoria(codigos, nombres, recargos, estados))

# OPERACIÓN DE AGREGACIÓN CON REDUCE (Lautaro Zanino)
def generar_reporte_categoria(codigos, nombres, recargos, estados):
    if len(codigos) == 0:
        return "No hay categorias cargadas."

    lineas = []
    for i in range(len(codigos)):
        # traduce el estado numérico (1/0) a texto legible antes de armar la línea
        estado_texto = "Activa" if estados[i] == 1 else "Inactiva"
        linea = "Código: " + str(codigos[i]) + " | Nombre: " + nombres[i] + " | Recargo: " + str(recargos[i]) + "% | Estado: " + estado_texto
        lineas.append(linea)

    # 'reduce' combina todas las líneas en un unico string 
    # para luego mostrar el contenido a traves del return 
    reporte = reduce(lambda acumulado, linea: acumulado + "\n" + linea, lineas)
    return "\n--- LISTA DE CATEGORIAS ---\n" + reporte
# INVENTARIO
def alta_inventario(inv_cods, inv_prods, inv_cats, inv_cants, inv_deps, prod_codigos, cat_codigos):
    codigo = pedir_codigo("\nIngrese el código del nuevo registro de inventario (formato INV-0000): ", "INV", 4)
    if buscar_indice(inv_cods, codigo) != -1:
        print("Error: Ya existe un registro de inventario con ese código.")
    else:
        cod_prod = pedir_codigo("Ingrese el código del producto (formato PRD-000): ", "PRD", 3)
        if buscar_indice(prod_codigos, cod_prod) == -1:
            print("Error: El producto no existe en el sistema. Alta cancelada.")
            return
        cod_cat = pedir_codigo("Ingrese el código de la categoría (formato CAT-00): ", "CAT", 2)
        if buscar_indice(cat_codigos, cod_cat) == -1:
            print("Error: La categoría no existe en el sistema. Alta cancelada.")
            return
        cantidad = pedir_entero("Ingrese la cantidad de unidades: ")
        deposito = solicitar_opcion_menu("Ingrese el número de depósito (1, 2 o 3): ", 1, 3)
        
        inv_cods.append(codigo)
        inv_prods.append(cod_prod)
        inv_cats.append(cod_cat)
        inv_cants.append(cantidad)
        inv_deps.append(deposito)
        print("¡Registro de inventario agregado con éxito!")

def baja_inventario(inv_cods, inv_prods, inv_cats, inv_cants, inv_deps):
    codigo = pedir_codigo("\nIngrese el código de inventario a eliminar (formato INV-0000): ", "INV", 4)
    indice = buscar_indice(inv_cods, codigo)
    if indice == -1:
        print("Error: El registro no existe.")
    else:
        inv_cods.pop(indice)
        inv_prods.pop(indice)
        inv_cats.pop(indice)
        inv_cants.pop(indice)
        inv_deps.pop(indice)
        print("Registro de inventario eliminado correctamente.")

def modificar_inventario(inv_cods, inv_prods, inv_cats, inv_cants, inv_deps, prod_codigos, cat_codigos):
    codigo = pedir_codigo("\nIngrese el código de inventario a modificar (formato INV-0000): ", "INV", 4)
    indice = buscar_indice(inv_cods, codigo)
    if indice == -1:
        print("Error: El registro no existe.")
    else:
        print("Registro actual -> Prod:", inv_prods[indice], "| Cat:", inv_cats[indice], "| Cant:", inv_cants[indice], "| Depósito:", inv_deps[indice])
        nuevo_cod_prod = pedir_codigo("Ingrese el nuevo código de producto (formato PRD-000): ", "PRD", 3)
        if buscar_indice(prod_codigos, nuevo_cod_prod) == -1:
            print("Error: El producto no existe. Modificación cancelada.")
            return
        nuevo_cod_cat = pedir_codigo("Ingrese el nuevo código de categoría (formato CAT-00): ", "CAT", 2)
        if buscar_indice(cat_codigos, nuevo_cod_cat) == -1:
            print("Error: La categoría no existe. Modificación cancelada.")
            return
        nueva_cant = pedir_entero("Ingrese la nueva cantidad: ")
        nuevo_dep = solicitar_opcion_menu("Ingrese el nuevo depósito (1, 2 o 3): ", 1, 3)
        
        inv_prods[indice] = nuevo_cod_prod
        inv_cats[indice] = nuevo_cod_cat
        inv_cants[indice] = nueva_cant
        inv_deps[indice] = nuevo_dep
        print("Registro de inventario actualizado.")

def listar_inventario(inv_cods, inv_prods, inv_cats, inv_cants, inv_deps):
    # Muestra el listado de inventario. El armado del texto (incluido el caso de
    # lista vacía) lo hace generar_reporte_inventario(), que usa reduce el cual
    # combina todas las líneas en un único string antes de imprimirlas.
    print(generar_reporte_inventario(inv_cods, inv_prods, inv_cats, inv_cants, inv_deps))

# OPERACIÓN DE AGREGACIÓN CON REDUCE (Lautaro Zanino)
def generar_reporte_inventario(inv_cods, inv_prods, inv_cats, inv_cants, inv_deps):
    if len(inv_cods) == 0:
        return "No hay registros en el inventario."

    lineas = []
    for i in range(len(inv_cods)):
        linea = "Codigo: " + str(inv_cods[i]) + " | Producto: " + str(inv_prods[i]) + " | Categoria: " + str(inv_cats[i]) + " | Cantidad: " + str(inv_cants[i]) + " | Deposito: " + str(inv_deps[i])
        lineas.append(linea)

    # 'reduce' junta todas las líneas en un unico string, separadas por salto de línea
    reporte = reduce(lambda acumulado, linea: acumulado + "\n" + linea, lineas)
    return "\n--- LISTA DE INVENTARIO ---\n" + reporte
# CONSULTAS
def consulta_productos_en_stock(columnas_prod, columnas_inv):
    prod_codigos = columnas_prod[0]  # Extraemos la columna 0 de la matriz de productos: los códigos
    prod_nombres = columnas_prod[1]  # Extraemos la columna 1: los nombres de los productos
    inv_prods = columnas_inv[1]      # De la matriz de inventario, columna 1: a qué producto pertenece cada fila
    inv_cants = columnas_inv[3]      # De la matriz de inventario, columna 3: cantidad de unidades de cada fila
    print("\n--- PRODUCTOS EN STOCK ---")  # Encabezado del reporte
    for p in range(len(prod_codigos)):  # Recorremos cada producto uno por uno, usando su índice p
        codigo_actual = prod_codigos[p]  # Guardamos el código del producto actual para no repetir el acceso
        indices = list(filter(lambda i: inv_prods[i] == codigo_actual, range(len(inv_prods))))
        # ↑ FILTER: recorremos todos los índices posibles del inventario y nos quedamos
        # solo con los índices i donde el producto de esa fila coincide con codigo_actual
        cantidades = list(map(lambda i: inv_cants[i], indices))
        # ↑ MAP: transformamos la lista de índices filtrados en la lista de cantidades
        # reales, yendo a buscar inv_cants[i] para cada índice que sobrevivió al filtro
        total = reduce(lambda acumulado, actual: acumulado + actual, cantidades, 0)
        # ↑ REDUCE: recorremos la lista de cantidades sumándolas de a una, empezando
        # el acumulador en 0, hasta quedarnos con un único número final
        print("Producto:", prod_nombres[p], "- Unidades en stock:", total)  # Mostramos el resultado de este producto

def consulta_por_categoria(columnas_cat, columnas_inv):
    cat_codigos = columnas_cat[0]   # Extraemos la columna 0 de la matriz de categorías: los códigos
    cat_nombres = columnas_cat[1]   # Extraemos la columna 1: los nombres de categoría
    inv_cods = columnas_inv[0]      # De la matriz de inventario, columna 0: los códigos de cada registro
    inv_prods = columnas_inv[1]     # Columna 1: a qué producto pertenece cada fila
    inv_cats = columnas_inv[2]      # Columna 2: a qué categoría pertenece cada fila
    inv_cants = columnas_inv[3]     # Columna 3: cantidad de unidades de cada fila
    inv_deps = columnas_inv[4]      # Columna 4: en qué depósito está cada fila

    cat_buscada = pedir_codigo("\nIngrese el código de categoría a consultar (formato CAT-00): ", "CAT", 2)  # Pedimos y validamos el formato del código

    indice_cat = buscar_indice(cat_codigos, cat_buscada)  # Buscamos si la categoría existe realmente en el sistema
    if indice_cat == -1:  # Si no la encontramos entre las categorías cargadas
        print("Error: la categoría no existe.")  # Avisamos que el código no corresponde a ninguna categoría real
        return  # Cortamos la función acá, no tiene sentido seguir buscando stock de algo que no existe
    nombre_cat = cat_nombres[indice_cat]  # Guardamos el nombre de la categoría para mostrarlo en los mensajes

    indices = list(filter(lambda i: inv_cats[i] == cat_buscada, range(len(inv_cods))))
    # ↑ FILTER con UNA sola condición: nos quedamos con los índices donde la categoría de esa fila coincide

    if not indices:  # Si la categoría existe, pero no tiene ningún registro de stock asociado
        print(f"No hay stock registrado para la categoría {cat_buscada} ({nombre_cat}).")  # Avisamos, ahora aclarando el nombre
    else:  # Si encontramos al menos una fila con esa categoría
        print(f"\n--- STOCK DE LA CATEGORÍA {cat_buscada} - {nombre_cat} ---")  # Encabezado con código Y nombre de la categoría
        for i in indices:  # Recorremos los índices filtrados
            print("Cód Inv:", inv_cods[i], "| Producto:", inv_prods[i], "| Cantidad:", inv_cants[i], "| Depósito:", inv_deps[i])

def consulta_por_deposito(inv_cods, inv_deps, inv_prods, inv_cants):
    dep_buscado = solicitar_opcion_menu("\nIngrese el número de depósito a consultar (1, 2 o 3): ", 1, 3)  # Pedimos y validamos el depósito (1, 2 o 3)
    
    indices = list(filter(lambda i: inv_deps[i] == dep_buscado, range(len(inv_cods))))
    # ↑ FILTER con UNA sola condición: nos quedamos con los índices donde el depósito de esa fila coincide
    
    if not indices:  # Si no encontramos ninguna fila en ese depósito
        print("No hay stock registrado en este depósito.")  # Avisamos que no hay resultados
    else:  # Si encontramos al menos una fila
        print("\n--- STOCK DEL DEPÓSITO", dep_buscado, "---")  # Encabezado con el depósito buscado
        for i in indices:  # Recorremos los índices filtrados
            print("Cód Inv:", inv_cods[i], "| Producto:", inv_prods[i], "| Cantidad:", inv_cants[i])
            # ↑ No mostramos categoría ni depósito porque no aportan info nueva:
            # el depósito ya lo eligió el usuario, y la categoría no fue criterio de búsqueda

def consulta_unidades_categoria_deposito(inv_cods, inv_cats, inv_prods, inv_cants, inv_deps):
    cat_buscada = pedir_codigo("\nIngrese el código de categoría a consultar (formato CAT-00): ", "CAT", 2)  # Pedimos y validamos el código de categoría
    dep_buscado = solicitar_opcion_menu("Ingrese el número de depósito a consultar (1, 2 o 3): ", 1, 3)  # Pedimos y validamos el depósito (solo acepta 1, 2 o 3)
    indices = list(filter(lambda i: inv_cats[i] == cat_buscada and inv_deps[i] == dep_buscado, range(len(inv_cods))))
    # ↑ FILTER con DOBLE condición: nos quedamos solo con los índices donde
    # la categoría Y el depósito de esa fila coinciden con lo buscado (deben cumplirse las dos)
    if not indices:  # Si la lista de índices quedó vacía (ninguna fila cumplió ambas condiciones)
        print("No hay stock registrado para esta categoría en ese depósito.")  # Avisamos que no hay resultados
    else:  # Si encontramos al menos un índice que cumple
        print("\n--- UNIDADES DE LA CATEGORÍA", cat_buscada, "EN EL DEPÓSITO", dep_buscado, "---")  # Encabezado con los datos buscados
        for i in indices:  # Recorremos únicamente los índices que pasaron el filtro
            print("Cód Inv:", inv_cods[i], "| Producto:", inv_prods[i], "| Cantidad:", inv_cants[i])  # Imprimimos el detalle de cada fila encontrada
        cantidades = list(map(lambda i: inv_cants[i], indices))
        # ↑ MAP: convertimos los índices filtrados en la lista real de cantidades
        total = reduce(lambda acumulado, actual: acumulado + actual, cantidades, 0)
        # ↑ REDUCE: sumamos todas las cantidades para obtener el total acumulado, arrancando en 0
        print("Cantidad total de unidades:", total)  # Mostramos el total calculado
        
# PROCESAMIENTO AVANZADO DE CADENAS DE CARACTERES (Lautaro Zanino)
def nombre_duplicado(nombres, nombre_nuevo):
    # Normaliza el nombre nuevo sin espacios y en minúsculas y lo compara contra
    # cada nombre existente en la lista, normalizado de la misma forma, de esta manera se detectan
    # duplicados aunque difieran en mayúsculas/minúsculas o espacios
    nuevo_nombre_normalizado = nombre_nuevo.strip().lower()

    for i in range(len(nombres)):
        if nombres[i].strip().lower() == nuevo_nombre_normalizado:
            return True
    return False

# PROCESAMIENTO AVANZADO DE CADENAS DE CARACTERES (Lautaro Zanino)
def buscar_por_palabras(nombres, texto_de_busqueda):
    # Separa el texto de búsqueda en palabras sueltas, si el texto viene vacío,
    # la lista queda vacía y como consecuencia ningún producto es descartado
    texto_de_busqueda_normalizado = texto_de_busqueda.lower().split()

    lista = []
    for i in range(len(nombres)):
        nombre = nombres[i].lower()
        bandera = True
        # Chequea que TODAS las palabras buscadas estén contenidas en el nombre
        # sin importar el orden en que las haya escrito el usuario
        for j in range(len(texto_de_busqueda_normalizado)):
            if texto_de_busqueda_normalizado[j] not in nombre:
                bandera = False
        if bandera == True:
            lista.append(nombres[i])

    return lista

def buscar_producto_por_palabras(nombres):
    # Pide el texto de búsqueda, llama a buscar_por_palabras() para buscar coincidencias y muestra
    # los resultados en pantalla si hubo alguna coincidencia o un mensaje si no se encontró nada
    texto = pedir_texto("\nIngrese la palabra o palabras a buscar: ")
    resultados = buscar_por_palabras(nombres, texto)

    if len(resultados) == 0:
        print("No se encontraron productos que coincidan con la búsqueda")
    else:
        print("\n--- RESULTADOS DE LA BÚSQUEDA ---")
        for i in range(len(resultados)):
            print("-", resultados[i])

# PROCESAMIENTO AVANZADO DE CADENAS DE CARACTERES (Lautaro Zanino)
def generar_etiqueta(nombre):
    palabras_sueltas = nombre.split()

    iniciales = ""
    for i in range(len(palabras_sueltas)):
        iniciales += palabras_sueltas[i][0].upper()

    longitud = len(nombre)

    codigo_final = iniciales + "-" + str(longitud)

    return codigo_final

def generar_etiquetas_productos(nombres):
    lista_etiquetas = []
    
    for i in range(len(nombres)):
        # Llama a la función generar_etiqueta() y guarda el resultado
        etiqueta = generar_etiqueta(nombres[i])
        # Junta el resultado en la lista nueva
        lista_etiquetas.append(etiqueta)
        
    return lista_etiquetas

def mostrar_etiquetas_productos(nombres):
    # Muestra cada producto junto a su etiqueta generada. La encargada de hacer las
    # etiquetas es generar_etiquetas_productos() que a su vez usa generar_etiqueta()
    # para procesar cada nombre individualmente
    if len(nombres) == 0:
        print("No hay productos cargados.")
        return

    etiquetas = generar_etiquetas_productos(nombres)

    print("\n--- ETIQUETAS DE PRODUCTOS ---")
    for i in range(len(nombres)):
        print(nombres[i], "->", etiquetas[i])
# PROGRAMA PRINCIPAL (MENÚ)
logged_in = iniciar_sesion(usuarios)
rol_actual = logged_in["rol"] if logged_in else None

opcion_menu = 1
opcion_submenu_categoria = 1
opcion_submenu_inventario = 1
opcion_submenu_consultas = 1

if logged_in:
    while opcion_menu != 999:
        print("\nElija una de las siguientes opciones:")
        print("(1) ABM de producto")
        print("(2) ABM de categoria")
        print("(3) ABM de inventario")
        print("(4) Realizar consultas sobre el stock")
        if rol_actual == "admin":
            print("(5) Administración de usuarios bloqueados")
        print("(0) Salir del sistema")

        opcion_maxima = 5 if rol_actual == "admin" else 4
        opcion_menu = solicitar_opcion_menu("\nIngrese una opción válida: ", 0, opcion_maxima)

        if opcion_menu == 0:
            print("Quiere salir de la app?")
            salir = int(input("1 para salir 2 para quedarse: "))
            if salir == 1:
                opcion_menu = 999
            # si elige quedarse (2), el while vuelve a imprimir el menú principal completo desde el inicio     
        
        if opcion_menu == 1:
            opcion_submenu_producto = -1 
            while opcion_submenu_producto != 0: 
                print("\n--- ABM PRODUCTOS ---")
                print("(1) Alta de producto")
                print("(2) Baja de producto")
                print("(3) Modificar un producto")
                print("(4) Lista de productos")
                print("(5) Buscar producto (Secuencial)")
                print("(6) Buscar producto (Binaria)")
                print("(7) Buscar productos por palabras clave")
                print("(8) Etiquetas de productos")
                print("(0) Volver atrás")

                opcion_submenu_producto = solicitar_opcion_menu("\nIngrese una opción válida: ", 0, 8)
                
                if opcion_submenu_producto == 1:
                    alta_producto(prod_codigos, prod_nombres, prod_precios)
                elif opcion_submenu_producto == 2:
                    baja_producto(prod_codigos, prod_nombres, prod_precios, inv_codigos_prod)
                elif opcion_submenu_producto == 3:
                    modificar_producto(prod_codigos, prod_nombres, prod_precios)
                elif opcion_submenu_producto == 4:
                    ordenar_listas_paralelas([prod_codigos, prod_nombres, prod_precios], 0)
                    listar_productos(prod_codigos, prod_nombres, prod_precios)
                elif opcion_submenu_producto == 5:
                    buscar_producto_secuencial(prod_codigos, prod_nombres, prod_precios)
                elif opcion_submenu_producto == 6:
                    buscar_producto_binaria(prod_codigos, prod_nombres, prod_precios)
                elif opcion_submenu_producto == 7:
                    buscar_producto_por_palabras(prod_nombres)
                elif opcion_submenu_producto == 8:
                    mostrar_etiquetas_productos(prod_nombres)

        elif opcion_menu == 2:
            opcion_submenu_categoria = -1
            while opcion_submenu_categoria != 0: 
                print("\n--- ABM CATEGORÍAS ---")
                print("(1) Alta de categoria")
                print("(2) Baja de categoria")
                print("(3) Modificar una categoria")
                print("(4) Lista de categorias")
                print("(0) Volver atrás")
                
                opcion_submenu_categoria = solicitar_opcion_menu("\nIngrese una opción válida: ", 0, 4)
                
                if opcion_submenu_categoria == 1:
                    alta_categoria(cat_codigos, cat_nombres, cat_recargos, cat_estados)
                elif opcion_submenu_categoria == 2:
                    baja_categoria(cat_codigos, cat_nombres, cat_recargos, cat_estados, inv_codigos_cat)
                elif opcion_submenu_categoria == 3:
                    modificar_categoria(cat_codigos, cat_nombres, cat_recargos, cat_estados)
                elif opcion_submenu_categoria == 4:
                    ordenar_listas_paralelas([cat_codigos, cat_nombres, cat_recargos, cat_estados], 1)
                    listar_categorias(cat_codigos, cat_nombres, cat_recargos, cat_estados)

        elif opcion_menu == 3:
            opcion_submenu_inventario = -1
            while opcion_submenu_inventario != 0: 
                print("\n--- ABM INVENTARIO ---")
                print("(1) Alta de inventario")
                print("(2) Baja de inventario")
                print("(3) Modificar inventario")
                print("(4) Lista de inventario")
                print("(0) Volver atrás")

                opcion_submenu_inventario = solicitar_opcion_menu("\nIngrese una opción válida: ", 0, 4)

                if opcion_submenu_inventario == 1:
                    alta_inventario(inv_codigos, inv_codigos_prod, inv_codigos_cat, inv_cantidades, inv_depositos, prod_codigos, cat_codigos)
                elif opcion_submenu_inventario == 2:
                    baja_inventario(inv_codigos, inv_codigos_prod, inv_codigos_cat, inv_cantidades, inv_depositos)
                elif opcion_submenu_inventario == 3:
                    modificar_inventario(inv_codigos, inv_codigos_prod, inv_codigos_cat, inv_cantidades, inv_depositos, prod_codigos, cat_codigos)
                elif opcion_submenu_inventario == 4:
                    ordenar_listas_paralelas([inv_codigos, inv_codigos_prod, inv_codigos_cat, inv_cantidades, inv_depositos], 3)
                    listar_inventario(inv_codigos, inv_codigos_prod, inv_codigos_cat, inv_cantidades, inv_depositos)

        elif opcion_menu == 4:
            opcion_submenu_consultas = -1
            while opcion_submenu_consultas != 0: 
                print("\n--- CONSULTAS ---")
                print("(1) Ver productos en stock")
                print("(2) Ver categorías con stock")
                print("(3) Ver depósitos con stock")
                print("(4) Cantidad total de unidades por categoría y depósito")
                print("(0) Volver atrás")
                
                opcion_submenu_consultas = solicitar_opcion_menu("\nIngrese una opcion válida: ", 0, 4)
                
                if opcion_submenu_consultas == 1:
                    consulta_productos_en_stock(columnas_prod, columnas_inv)
                elif opcion_submenu_consultas == 2:
                    consulta_por_categoria(columnas_cat, columnas_inv)
                elif opcion_submenu_consultas == 3:
                     consulta_por_deposito(inv_codigos, inv_depositos, inv_codigos_prod, inv_cantidades)
                elif opcion_submenu_consultas == 4:
                    consulta_unidades_categoria_deposito(inv_codigos, inv_codigos_cat, inv_codigos_prod, inv_cantidades, inv_depositos)
        elif opcion_menu == 5:
            administrar_usuarios_bloqueados(usuarios)

    print("\nSaliendo del sistema. ¡Gracias por usarlo!")
