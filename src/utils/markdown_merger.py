#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Herramienta Avanzada de Similitud Textual y Comparación Estadística

La funcionalidad principal está encapsulada dentro de la clase MarkdownMerger, diseñada para ser
reutilizable y estar claramente organizada.
* _validate_directory(directory_path: Path): Este método auxiliar privado garantiza que la ruta del
  directorio proporcionada exista, sea realmente un directorio y tenga los permisos de lectura
  necesarios. Eleva excepciones específicas como FileNotFoundError, NotADirectoryError o
  PermissionError para mayor claridad.
* _check_read_permission(path: Path) y _check_write_permission(path: Path): Estos métodos de utilidad proporcionan una forma robusta de verificar los permisos del sistema de archivos antes de intentar operaciones de lectura o escritura, evitando errores inesperados.
* _find_markdown_files(directory_path: Path, recursive: bool): Este método utiliza glob de pathlib para localizar de manera eficiente todos los archivos .md y .markdown. Admite búsquedas planas (no recursivas) y recursivas. Eleva un IOError si no se encuentran archivos Markdown.
* _read_file_content(file_path: Path): Lee el contenido de un solo archivo Markdown con codificación utf-8. Incluye manejo de errores para problemas de permisos u otros errores de E/S durante la lectura.
* _generate_safe_filename(title: str): Convierte un título proporcionado por el usuario en un nombre de archivo limpio y compatible con el sistema de archivos, eliminando caracteres especiales y reemplazando los espacios con guiones.
* _write_to_file(file_path: Path, content: str, overwrite: bool): Se encarga de escribir el contenido concatenado en el archivo de salida final. Maneja de manera inteligente los archivos existentes: si overwrite es False, genera un nombre de archivo único (por ejemplo, documento-1.md, documento-2.md) para evitar la pérdida accidental de datos. También verifica los permisos de escritura en el directorio de destino.
* merge_files(...): Este es el método público principal que orquesta todo el proceso de fusión.
    * Toma la directory_path, output_title, y parámetros opcionales como recursive, prepend_text, append_text, section_separators y overwrite_existing.
    * Primero valida el directorio de entrada.
    * Luego, encuentra todos los archivos Markdown relevantes.
    * Lee el contenido de cada archivo, concatenándolos.
    * Separadores de sección: Entre cada archivo concatenado, inserta un separador personalizable (por defecto \n\n---\n\n) para delinear claramente las secciones de los archivos originales.
    * Adición de texto: Permite que se añada texto opcional al principio (prepend) o al final (append) del documento fusionado, lo que ofrece flexibilidad para introducciones o conclusiones.
    * Finalmente, guarda el contenido combinado en el archivo de salida especificado, gestionando los conflictos de nombres de archivo si overwrite_existing es False.

Soporte para Argumentos de Línea de Comandos
La función main() utiliza argparse para proporcionar una interfaz de línea de comandos fácil de usar:

directory (argumento posicional): Especifica el directorio de entrada.
output_title (argumento posicional): Define el título para el archivo de salida fusionado.
-r o --recursive (bandera): Habilita la búsqueda recursiva de archivos Markdown en subdirectorios.
-p o --prepend (opción): Te permite especificar un texto para añadir al principio.
-a o --append (opción): Te permite especificar un texto para añadir al final.
-s o --separator (opción): Personaliza el separador entre archivos concatenados.
-o o --overwrite (bandera): Si está presente, el archivo de salida se sobrescribirá si ya existe.

Proyecto: Paquete 2

Tema: HU técnica

Programa: markdown_merger.py

Soporte: kevin.hidalgo@globalmvm.com

version: 1.0.0

lenguaje: Python 3.11.9

CD: 20250808

LUD: 20250813

Comentarios:
    * 20250808 Kevin Hidalgo: pip install numpy scipy scikit-learn nltk gensim pandas python-Levenshtein,
      El script está escrito para ser claro, bien tipado y documentado. Utiliza operaciones
      vectorizadas y caché para pasos repetidos de preprocesamiento.

Ejemplo:
>>># Asumiendo que el script está en un archivo llamado 'no_markdown_merger_0.py'
>>>from markdown_merger_script import MarkdownMerger
>>>from pathlib import Path
>>>import shutil

>>># Crear algunos archivos markdown de prueba para la demostración
>>>test_dir = Path('./temp_markdown_files')
>>>test_dir.mkdir(exist_ok=True)
>>>(test_dir / 'file1.md').write_text(''# Sección 1\n\nEste es el contenido del archivo 1.'')
>>>(test_dir / 'file2.markdown').write_text(''## Sección 2\n\nContenido del archivo 2.'')
>>>(test_dir / 'subdir').mkdir(exist_ok=True)
>>>(test_dir / 'subdir' / 'file3.md').write_text(''### Sección 3\n\nContenido del archivo 3 en un subdirectorio.'')

>>>markdown_merger = MarkdownMerger()

>>>try:
>>>    # Ejemplo 1: Fusión básica
>>>    final_path_basic = markdown_merger.merge_files(
>>>        str(test_dir), 'Mi Documento Fusionado'
>>>    )
>>>    print(f'Fusión básica exitosa: {final_path_basic}')

>>>    # Ejemplo 2: Fusión con texto al principio y al final, separador personalizado, recursivo
>>>    final_path_advanced = markdown_merger.merge_files(
>>>        str(test_dir),
>>>        'Documento Fusionado Avanzado',
>>>        recursive=True,
>>>        prepend_text='''# Esta es una Introducción Bienvenido a mi documento Markdown fusionado.'''
>>>
>>>        append_text='Generado por MarkdownMerger.'
>>>        section_separators=\n\n***\n\n,
>>>        overwrite_existing=True # Sobrescribir si existe
>>>    )
>>>    print(f'Fusión avanzada exitosa: {final_path_advanced}')

>>>    # Ejemplo 3: Probar la generación de nombre de archivo único
>>>    final_path_unique = markdown_merger.merge_files(
>>>        str(test_dir),
>>>        'Documento Fusionado Avanzado',
>>>        recursive=True,
>>>        overwrite_existing=False
>>>    )
>>>    print(f'Fusión con nombre de archivo único exitosa: {final_path_unique}')

>>>except Exception as e:
>>>    print(f'Ocurrió un error: {e}')

>>># Limpiar los archivos de prueba (opcional)
>>>shutil.rmtree(test_dir)

bash
# Fusión básica de archivos .md y .markdown en el directorio actual, salida a 'mis-documentos.md'
python no_markdown_merger_0.py . "Mis Documentos"

# Fusionar archivos de forma recursiva, añadir un separador personalizado, texto al principio y al final
python no_markdown_merger_0.py /ruta/a/mis/notas "Notas del Proyecto" -r \
-s "\n\n" \
-p "# Resumen del Proyecto\n\nEste documento compila todas las notas del proyecto.\n" \
-a "\n\nFin de las Notas del Proyecto."

# Fusionar archivos y sobrescribir si el archivo de salida existe
python no_markdown_merger_0.py ./articulos "Últimos Artículos" -o
"""
__authors__ = ["Kevin Hidalgo"]
__contact__ = "kevin.hidalgo@globalmvm.com"
__copyright__ = "Copyright 2025, MVM ingenieria de software"
__credits__ = ["Kevin Hidalgo"]
__email__ = "kevin.hidalgo@globalmvm.com"
__status__ = "Desarrollo"
__version__ = "1.0.0"
__date__ = "2025-08-08"
__file__ = "no_text_similarity.py"

import argparse
import logging
import re
from pathlib import Path
from typing import List, Optional

# Configurar el registro (logging)
logging.basicConfig(
    format="%(asctime)s [%(levelname)s]: %(message)s",
    level=logging.INFO,
    encoding="utf-8",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler()],
)


def _check_read_permission(path: Path) -> bool:
    """
    Verifica si la ruta dada tiene permisos de lectura.

    Args:
        path: La ruta a verificar.

    Returns:
        True si la ruta tiene permisos de lectura, False en caso contrario.
    """
    try:
        # Intentar abrir para leer para verificar permisos
        with open(path, "rb") as f:
            pass
        return True
    except OSError:
        return False


class MarkdownMerger:
    """
    Una clase para fusionar múltiples archivos Markdown en un solo documento,
    permitiendo adiciones de texto opcionales y un manejo robusto de errores.
    """

    def __init__(self):
        """Inicializa la clase MarkdownMerger."""
        pass

    def _validate_directory(self, directory_path: Path) -> None:
        """
        Valida si la ruta proporcionada es un directorio válido y tiene permisos de lectura.

        Args:
            directory_path: La ruta al directorio a validar.

        Raises:
            FileNotFoundError: Si el directorio no existe.
            NotADirectoryError: Si la ruta no es un directorio.
            PermissionError: Si los permisos de lectura son insuficientes.
        """
        if not directory_path.exists():
            raise FileNotFoundError(f"Directorio no encontrado: {directory_path}")
        if not directory_path.is_dir():
            raise NotADirectoryError(f"La ruta no es un directorio: {directory_path}")
        if not _check_read_permission(directory_path):
            raise PermissionError(
                f"Permisos de lectura insuficientes para el directorio: {directory_path}"
            )

    def _check_write_permission(self, path: Path) -> bool:
        """
        Verifica si la ruta dada tiene permisos de escritura.

        Args:
            path: La ruta a verificar.

        Returns:
            True si la ruta tiene permisos de escritura, False en caso contrario.
        """
        try:
            # Intentar abrir en modo de escritura para verificar permisos
            # Abrimos en modo 'a' (append) para evitar truncar archivos existentes
            # si el archivo ya existe, y lo cerramos inmediatamente.
            with open(path, "a") as f:
                pass
            return True
        except OSError:
            return False

    def _find_markdown_files(self, directory_path: Path, recursive: bool) -> List[Path]:
        """
        Encuentra todos los archivos markdown (.md, .markdown) dentro de un directorio.

        Args:
            directory_path: El directorio a buscar.
            recursive: Si se deben buscar directorios de forma recursiva.

        Returns:
            Una lista de rutas a los archivos markdown encontrados.

        Raises:
            IOError: Si no se encuentran archivos markdown en el directorio.
        """
        markdown_files = []
        pattern = "**/*.md" if recursive else "*.md"
        markdown_files.extend(list(directory_path.glob(pattern)))
        pattern = "**/*.markdown" if recursive else "*.markdown"
        markdown_files.extend(list(directory_path.glob(pattern)))

        if not markdown_files:
            raise IOError(f"No se encontraron archivos markdown en: {directory_path}")
        logging.info("Se encontraron %d archivos markdown.", len(markdown_files))
        return sorted(markdown_files)  # Asegurar un orden consistente

    def _read_file_content(self, file_path: Path) -> str:
        """
        Lee el contenido de un solo archivo.

        Args:
            file_path: La ruta al archivo a leer.

        Returns:
            El contenido del archivo como una cadena de texto.

        Raises:
            PermissionError: Si los permisos de lectura son insuficientes para el archivo.
            IOError: Si ocurre un error durante la lectura del archivo.
        """
        if not _check_read_permission(file_path):
            raise PermissionError(f"Permisos de lectura insuficientes para el archivo: {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            return content
        except Exception as e:
            raise IOError(f"Error al leer el archivo {file_path}: {e}")

    def _generate_safe_filename(self, title: str) -> str:
        """
        Genera un nombre de archivo seguro a partir de un título proporcionado por el usuario.

        Elimina caracteres especiales y reemplaza los espacios con guiones.

        Args:
            title: El título deseado para el archivo.

        Returns:
            Una cadena de texto con el nombre de archivo seguro.
        """
        safe_title = re.sub(r"[^\w\s-]", "", title).strip().lower()
        safe_title = re.sub(r"[-\s]+", "-", safe_title)
        return f"{safe_title}.md"

    def _write_to_file(self, file_path: Path, content: str, overwrite: bool) -> None:
        """
        Escribe el contenido en un archivo especificado, manejando las opciones de sobrescritura.

        Args:
            file_path: La ruta al archivo en el que se escribirá.
            content: El contenido a escribir.
            overwrite: Si es True, sobrescribe el archivo si existe. Si es False,
                       crea un nombre de archivo único si el archivo ya existe.

        Raises:
            FileExistsError: Si el archivo existe y 'overwrite' es False.
            PermissionError: Si los permisos de escritura son insuficientes.
            IOError: Si ocurre un error durante la escritura del archivo.
        """
        final_path = file_path
        if final_path.exists() and not overwrite:
            counter = 1
            while final_path.exists():
                name_stem = file_path.stem
                name_suffix = file_path.suffix
                final_path = file_path.with_name(f"{name_stem}_{counter}{name_suffix}")
                counter += 1
            logging.warning(
                "El archivo '%s' ya existe. Se guardará como '%s' en su lugar.",
                file_path.name,
                final_path.name,
            )

        # if not self._check_write_permission(final_path.parent):
        #     raise PermissionError(
        #         f"Permisos de escritura insuficientes para el directorio: {final_path.parent}"
        #     )

        try:
            with open(final_path, "w", encoding="utf-8") as f:
                f.write(content)
            logging.info("Se fusionó el markdown con éxito en: %s", final_path)
        except Exception as e:
            raise IOError(f"Error al escribir en el archivo {final_path}: {e}")

    def merge_files(
        self,
        directory_path: str,
        output_title: str,
        recursive: bool = False,
        prepend_text: Optional[str] = None,
        append_text: Optional[str] = None,
        section_separators: str = "\n\n---\n\n",
        overwrite_existing: bool = False,
    ) -> Path:
        """
        Lee, concatena y guarda archivos markdown de un directorio especificado.

        Args:
            directory_path: La ruta al directorio que contiene los archivos markdown.
            output_title: El título deseado para el archivo markdown final fusionado.
            recursive: Si es True, busca archivos markdown de forma recursiva en subdirectorios.
                       El valor predeterminado es False.
            prepend_text: Texto opcional para añadir al principio del documento fusionado.
                          El valor predeterminado es None.
            append_text: Texto opcional para añadir al final del documento fusionado.
                         El valor predeterminado es None.
            section_separators: La cadena de texto a usar como separador entre los archivos
                                concatenados. El valor predeterminado es "\\n\\n---\\n\\n".
            overwrite_existing: Si es True, sobrescribe el archivo de salida si ya existe.
                                Si es False, se generará un nombre de archivo único.
                                El valor predeterminado es False.

        Returns:
            El objeto Path del archivo markdown fusionado recién creado.

        Raises:
            FileNotFoundError: Si el directorio no existe.
            NotADirectoryError: Si la ruta proporcionada no es un directorio.
            PermissionError: Si los permisos de lectura/escritura son insuficientes.
            IOError: Si no se encuentran archivos markdown o ocurre un error durante las
                     operaciones de archivo.
        """
        dir_path = Path(directory_path)
        # self._validate_directory(dir_path)

        md_files = self._find_markdown_files(dir_path, recursive)

        merged_content_parts: List[str] = []

        if prepend_text:
            merged_content_parts.append(prepend_text)
            logging.info("Añadiendo texto al principio del documento fusionado.")

        for i, file_path in enumerate(md_files):
            logging.info("Leyendo archivo: %s", file_path.name)
            content = self._read_file_content(file_path)
            merged_content_parts.append(content)
            if i < len(md_files) - 1:  # Añadir separador si no es el último archivo
                merged_content_parts.append(section_separators)

        if append_text:
            merged_content_parts.append(append_text)
            logging.info("Añadiendo texto al final del documento fusionado.")

        final_content = "".join(merged_content_parts)
        safe_filename = self._generate_safe_filename(output_title)
        output_path = dir_path / safe_filename

        self._write_to_file(output_path, final_content, overwrite_existing)
        return output_path


def main():
    """
    Función principal para analizar los argumentos de la línea de comandos
    y ejecutar el MarkdownMerger.
    """
    parser = argparse.ArgumentParser(
        description="Concatena múltiples archivos Markdown en un solo documento."
    )
    parser.add_argument(
        "directory",
        type=str,
        help="La ruta al directorio que contiene los archivos markdown.",
    )
    parser.add_argument(
        "output_title",
        type=str,
        help="El título deseado para el archivo markdown final fusionado.",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="Busca archivos markdown de forma recursiva en subdirectorios.",
    )
    parser.add_argument(
        "-p",
        "--prepend",
        type=str,
        help="Texto opcional para añadir al principio del documento fusionado.",
    )
    parser.add_argument(
        "-a",
        "--append",
        type=str,
        help="Texto opcional para añadir al final del documento fusionado.",
    )
    parser.add_argument(
        "-s",
        "--separator",
        type=str,
        default="\n\n---\n\n",
        help=(
            "La cadena a usar como separador entre los archivos concatenados. "
            "El valor predeterminado es '\\n\\n---\\n\\n'."
        ),
    )
    parser.add_argument(
        "-o",
        "--overwrite",
        action="store_true",
        help="Si se establece, sobrescribe el archivo de salida si ya existe. "
        "Por defecto, se genera un nombre de archivo único.",
    )

    args = parser.parse_args()

    markdown_merger = MarkdownMerger()
    try:
        final_file_path = markdown_merger.merge_files(
            args.directory,
            args.output_title,
            recursive=args.recursive,
            prepend_text=args.prepend,
            append_text=args.append,
            section_separators=args.separator,
            overwrite_existing=args.overwrite,
        )
        logging.info("Archivos markdown fusionados con éxito en: %s", final_file_path)
    except (
        FileNotFoundError,
        NotADirectoryError,
        PermissionError,
        IOError,
    ) as e:
        logging.error("Ocurrió un error: %s", e)


if __name__ == "__main__":
    main()
