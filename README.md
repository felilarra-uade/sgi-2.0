# SGI 2.0 - Sistema de Gestión de Inventario

## Descripción del Proyecto
Sistema de consola desarrollado en Python para centralizar la gestión operativa de un comercio. Permite el control de productos, categorías e inventario por depósito, con registro de movimientos e historial de stock. Los datos se guardan en archivos para que no se pierdan al cerrar el programa.

Proyecto grupal de la materia Algoritmos y Estructuras de Datos I (UADE). Se desarrolló en Python usando listas paralelas, diccionarios, tuplas, conjuntos, expresiones regulares, funciones de orden superior, archivos de texto y archivos JSON.

## Integrantes del Equipo
- **Lautaro Zanino** - Procesamiento avanzado de cadenas de caracteres y funciones con reduce; sistema de usuarios con roles y login con bloqueo por intentos fallidos; panel de administración para desbloquear usuarios; división del menú en submenús; registro de movimientos y de historial de stock en archivos de texto.
- **Felipe Larrañaga** (Referente) - Validaciones con expresiones regulares; algoritmos de ordenamiento de listas paralelas; tuplas y conjuntos; pruebas unitarias; control de ramas y merges; correcciones de bugs del sistema.
- **Agustín Poggi** - Módulo de consultas estadísticas con funciones lambda; manejo de excepciones en validaciones y menú principal; persistencia de datos en archivos JSON.
- **Felix Cabanchik** - Estructura inicial del proyecto y configuración del repositorio Git; primera versión del módulo de login. (Aclaración: no continúa cursando la materia.)

## Acceso al sistema
Al iniciar, el programa pide usuario y contraseña. Hay dos usuarios cargados de fábrica (uno con rol de administrador y otro con rol de usuario), definidos en `datos_por_defecto()`.

Si se falla la contraseña 3 veces seguidas, el usuario queda bloqueado. Un administrador puede desbloquearlo desde la opción (5) del menú principal. El administrador no se bloquea, porque es el único que puede desbloquear usuarios. El contador de intentos se reinicia cada vez que el usuario inicia sesión correctamente.

## Funcionalidades Principales
- **Control de acceso (login)** con bloqueo tras 3 intentos fallidos y administración de usuarios bloqueados (solo administrador).
- **ABM de Productos** (códigos PRD-000): alta, baja (no permite si hay stock), modificación, listado, búsqueda secuencial y binaria, búsqueda por palabras clave y generación de etiquetas.
- **ABM de Categorías** (códigos CAT-00): alta, baja (no permite si hay productos vinculados), modificación con recargo y estado activa/inactiva, y listado.
- **ABM de Inventario** (códigos INV-0000): alta, baja y modificación de stock por producto, categoría y depósito (depósitos 1 a 3). Un producto no puede estar en dos categorías distintas, y solo se pueden cargar productos existentes y categorías activas.
- **Consultas sobre el stock**:
  - Productos en stock.
  - Categorías y depósitos con stock.
  - Unidades por categoría y depósito.
  - Valor total de stock por categoría (con recargo).
  - Productos sin stock registrado.
  - Comparación de productos entre dos depósitos.
  - Historial de movimientos.
  - Historial de stock.
- **Ordenamiento** de las listas paralelas: productos por código, categorías por nombre e inventario por cantidad.
- **Validaciones** de entrada con expresiones regulares y conversiones con manejo de errores (las opciones de menú y los datos numéricos se vuelven a pedir si no son válidos). En los pedidos de códigos, nombres, cantidades y precios se puede escribir `volver` para cancelar la operación.
- **Persistencia de datos**:
  - `datos_sgi.json`: usuarios, productos, categorías e inventario. Se carga al iniciar y se guarda después de cada alta, baja o modificación, al iniciar sesión y al salir. Si el archivo no existe, está dañado o no tiene la estructura esperada, el programa arranca con los datos iniciales.
  - `movimientos.txt`: registro de cada operación (usuario, acción, entidad y código).
  - `historial_stock.txt`: un bloque con el stock de todos los productos después de cada operación de producto o inventario.

## Archivos de datos
El programa crea estos archivos en la carpeta desde donde se ejecuta. En el repositorio se incluye una versión de ejemplo de cada uno, generada con el sistema:
- `datos_sgi.json`
- `movimientos.txt`
- `historial_stock.txt`

Para arrancar con los datos iniciales, alcanza con borrar `datos_sgi.json`.

## Cómo ejecutarlo
1. Tener instalado Python 3. No se usan librerías externas.
2. Desde la carpeta del proyecto, ejecutar el sistema con `python sgi.py`.
3. Ingresar con alguno de los usuarios precargados:

| Usuario | Contraseña | Rol |
|---|---|---|
| admin | inventario2026 | administrador |
| lzanino | clave123 | usuario |

Para ejecutar las pruebas unitarias: `python pruebas_sgi.py`

## Estructura del proyecto
- `sgi.py`: programa principal. Las funciones de `main()` se ejecutan solo al correr el archivo directamente, por lo que se pueden importar sin que arranque el menú.
- `pruebas_sgi.py`: 10 pruebas unitarias (casos válidos, inválidos, límite y adicional) sobre funciones del sistema.

## Branches del Proyecto
- **main** - Rama principal (versión final).
- **felipe-larranaga** - Validaciones, ordenamiento, tuplas y conjuntos, y pruebas unitarias.
- **lautaro-zanino-parte2** - Archivos de texto, movimientos, historial de stock y modularización del menú.
- **lautaro-zanino3** - Procesamiento de cadenas y operaciones con reduce.
- **agustin-poggi** - Consultas estadísticas, manejo de excepciones y persistencia en JSON.
