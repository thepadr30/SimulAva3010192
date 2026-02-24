import os
import re
import logging
from pathlib import Path
from typing import Union, Dict

import pandas as pd

NAME_USER = 'KEV'

if NAME_USER == 'hola':
    print('hello word')

if NAME_USER == 'KEV' and os.name == "nt":
    ROOT = Path(os.getcwd())

def get_data_path_0(folder: str = None) -> Path:
    """Determines the path to the data directory.

    Args:
        folder (str, optional): Subfolder inside the data directory.

    Returns:
        Path: Absolute path to the data directory.
    """
    base_path = Path(os.getcwd()) if os.name == "nt" else Path(".").resolve()

    # is_windows = os.name == "nt"  # NOSONAR
    # if is_windows:
    #     return Path(os.getcwd()) / f"{folder}"
    # return Path(f"./{folder}").resolve()
    if folder:
        return base_path / folder
    return base_path


def _validate_folder(folder: str) -> None:
    """Valida el nombre del folder (si se proporciona)."""
    if not isinstance(folder, str):
        raise ValueError("El parámetro 'folder' debe ser una cadena de texto.")

    # if Path(folder).is_absolute():
    #     raise ValueError("No se permite una ruta absoluta en 'folder'. Solo rutas relativas.")

    invalid_chars = r'[<>:"/\\|?*]' if os.name == 'nt' else r'[\0]'
    if re.search(invalid_chars, folder):
        raise ValueError("El nombre del folder contiene caracteres no permitidos.")

    if '..' in Path(folder).parts:
        raise ValueError("El nombre del folder no debe contener '..' (escape de directorio).")

def _get_base_path() -> Path:
    """Retorna el path base dependiendo del sistema operativo."""
    return Path(os.getcwd()) if os.name == "nt" else Path(".").resolve()

def _create_directory(path: Path, use_logging: bool) -> None:
    """Crea el directorio si no existe, usando logging o print."""
    if not path.exists():
        path.mkdir(parents=True, exist_ok=True)
        message = f"📁 Carpeta creada: {path}"
    else:
        message = f"✅ Carpeta existente: {path}"

    if use_logging:
        logging.info(message)
    else:
        print(message)

def get_data_path(folder: str = None, use_logging: bool = False) -> Path:
    """Determina y crea (si es necesario) el path al directorio de datos.

    Args:
        folder (str, optional): Subcarpeta dentro del directorio de datos.
        use_logging (bool): Si es True, usa logging en vez de print.

    Returns:
        Path: Ruta absoluta al directorio de datos.

    Raises:
        ValueError: Si el nombre del folder no es válido.
    """
    # if folder:
    #     _validate_folder(folder)

    base_path = _get_base_path()
    full_path = base_path / folder if folder else base_path

    _create_directory(full_path, use_logging)

    return full_path

# os.chdir(ROOT)
def listar_archivos_en_ruta(ruta):
    """
    Retorna una lista de nombres de archivos en la ruta especificada.

    Parámetros:
        ruta (str): Ruta del directorio a inspeccionar.

    Retorna:
        List[str]: Lista de nombres de archivos (no incluye carpetas).
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"La ruta especificada no existe: {ruta}")

    if not os.path.isdir(ruta):
        raise NotADirectoryError(f"La ruta especificada no es un directorio: {ruta}")

    archivos = [
        archivo for archivo in os.listdir(ruta) if os.path.isfile(os.path.join(ruta, archivo))
    ]

    return archivos

def listar_nombres_sin_extension(ruta):
    """
    Retorna una lista con los nombres de archivos sin extensión desde la ruta dada.

    Parámetros:
        ruta (str): Ruta del directorio a inspeccionar.

    Retorna:
        List[str]: Lista de nombres de archivos sin extensión.
    """
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"La ruta especificada no existe: {ruta}")

    if not os.path.isdir(ruta):
        raise NotADirectoryError(f"La ruta especificada no es un directorio: {ruta}")

    nombres_sin_extension = [
        os.path.splitext(archivo)[0]
        for archivo in os.listdir(ruta)
        if os.path.isfile(os.path.join(ruta, archivo))
    ]

    return nombres_sin_extension


def leer_archivos_excel(ruta_directorio: Union[str, Path]) -> Dict[str, pd.DataFrame]:
    """
    Lee todos los archivos Excel (.xlsx y .xls) en la ruta de directorio especificada
    y devuelve su contenido como DataFrames de pandas.

    Args:
        ruta_directorio: La ruta al directorio que contiene los archivos Excel.

    Returns:
        Un diccionario donde las claves son los nombres de los archivos Excel (sin extensión)
        y los valores son los DataFrames correspondientes.
        Devuelve un diccionario vacío si no se encuentran archivos Excel.

    # --- EJEMPLO DE USO ---

    # Crea un directorio temporal y archivos ficticios para la demostración
    ruta_prueba = Path("./datos_excel_temp")
    ruta_prueba.mkdir(exist_ok=True)

    # Crear datos de ejemplo
    datos_1 = {'ColA': [1, 2], 'ColB': ['X', 'Y']}
    df_ejemplo_1 = pd.DataFrame(datos_1)
    df_ejemplo_1.to_excel(ruta_prueba / "informe_ventas.xlsx", index=False)

    datos_2 = {'Nombre': ['Ana', 'Luis'], 'Edad': [25, 30]}
    df_ejemplo_2 = pd.DataFrame(datos_2)
    # Podrías crear un archivo .xls si lo necesitaras, pero .xlsx es el estándar moderno
    df_ejemplo_2.to_excel(ruta_prueba / "lista_empleados.xlsx", index=False)

    # Ejecutar la función
    directorio_a_leer = ruta_prueba # O usa una ruta real, e.g., "C:/Users/MiUsuario/Documentos/Informes"
    archivos_cargados = leer_archivos_excel(directorio_a_leer)

    # Mostrar los DataFrames cargados
    if archivos_cargados:
    print("\n--- DataFrames Cargados ---")
    for nombre, df in archivos_cargados.items():
        print(f"\nDataFrame '{nombre}':")
        print(df.head())

    # Limpiar el directorio temporal (opcional)
    for archivo in ruta_prueba.glob("*"):
    os.remove(archivo)
    os.rmdir(ruta_prueba)
    """
    ruta_directorio = Path(ruta_directorio)
    dataframes_excel = {}

    # 1. Verificar si la ruta existe y es un directorio
    if not ruta_directorio.is_dir():
        print(f"❌ Error: La ruta '{ruta_directorio}' no es un directorio válido o no existe.")
        return dataframes_excel  # Devuelve diccionario vacío

    print(f"🔎 Buscando archivos Excel en: {ruta_directorio}")

    # 2. Iterar sobre todos los archivos que coincidan con las extensiones de Excel
    # Usamos .rglob() para buscar recursivamente si es necesario, o .glob() para el nivel superior.
    # Aquí usaremos .glob() para el nivel superior.
    for archivo in ruta_directorio.glob("*.xlsx"):
        try:
            # Leer el archivo. La clave será el nombre del archivo sin la extensión.
            df = pd.read_excel(archivo)
            nombre_clave = archivo.stem
            dataframes_excel[nombre_clave] = df
            print(f"✅ Leído: {archivo.name} (Clave: '{nombre_clave}')")
        except Exception as e:
            print(f"⚠️ Advertencia: No se pudo leer el archivo XLSX '{archivo.name}'. Error: {e}")

    # También buscamos la extensión antigua .xls
    for archivo in ruta_directorio.glob("*.xls"):
        try:
            df = pd.read_excel(archivo)
            nombre_clave = archivo.stem
            dataframes_excel[nombre_clave] = df
            print(f"✅ Leído: {archivo.name} (Clave: '{nombre_clave}')")
        except Exception as e:
            print(f"⚠️ Advertencia: No se pudo leer el archivo XLS '{archivo.name}'. Error: {e}")

    print(f"\n✨ Lectura completada. Total de archivos cargados: {len(dataframes_excel)}")
    return dataframes_excel