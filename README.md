# Simulación Avanzada (SIMULAVA) - Código: 3010192
Este repositorio contiene los materiales, fundamentos técnicos y metodologías del curso Simulación
Avanzada, impartido en el Departamento de Ciencias de la Computación y la Decisión de la Facultad de
Minas. El curso es dirigido por el F. Javier Díaz S. PhD., Profesor Titular de la Universidad
Nacional de Colombia, Sede Medellín.

## Descripción del Curso

El curso se centra en el estudio y aplicación de la Simulación de Eventos Discretos como herramienta
crítica para la toma de decisiones en entornos organizacionales. El contenido abarca desde los
fundamentos de probabilidad hasta el modelamiento de sistemas complejos sujetos a incertidumbre y
dinámica.

## Objetivos Académicos

El propósito principal es desarrollar habilidades para la estructuración de modelos de simulación
que sirvan de apoyo en el análisis y evaluación del comportamiento de organizaciones bajo
condiciones variables. Estas condiciones están caracterizadas por:

* **Incertidumbre.**
* **Dinámica.**
* **Complejidad.**

## Programa Temático

1. **Fundamentos**: Probabilidad, estadística, riesgo, aleatoriedad y ambigüedad.
2. **Modelamiento de Sistemas**: Traducción del lenguaje natural al lenguaje matemático.
3. **Metodologías de Simulación**:
   * Simulación de Eventos Discretos.
   * Simulación Continua (Dinámica de Sistemas - D.S.).
   * Simulación Basada en Agentes (SBA).
4. **Historia y Métodos Clásicos**: Desde los métodos de Montecarlo y el problema de la aguja de
   Buffon hasta el cálculo de $\pi$.


## Metodología de Modelamiento
El proceso de construcción de modelos se rige por el método científico aplicado a la toma de
decisiones, siguiendo seis etapas fundamentales:

1. **Definición del problema** y recolección de información.
2. **Formulación** del modelo de simulación.
3. **Solución** del modelo.
4. **Prueba** del modelo (Validación y Verificación).
5. **Preparación** para la aplicación.
6. **Implantación**.

## Estructura Técnica de un Modelo
Un modelo de simulación se define como una representación idealizada expresada en símbolos
matemáticos y estadísticos. Se clasifican sus componentes en:

### Clasificación de Variables

* **Variables Exógenas**: Independientes o de entrada al modelo (ej. tiempo entre llegadas, tiempo
  de servicio).
* **Variables de Estado**: Describen la condición del sistema en un tiempo $t$ (ej. número de
  clientes en el sistema o en cola).
* **Variables Endógenas**: Dependientes, generadas por la interacción del sistema (ej. tiempo total
  en el sistema).
* **Parámetros**: Valores estimados como $\lambda$ (tiempo promedio entre llegadas) y $\mu$ (tiempo
  promedio de servicio).

### Caso de Estudio: Teoría de Colas
El repositorio incluye ejemplos de **Simulación Dinámica Estocástica** aplicados a líneas de espera 
(vehículos en una estación de servicio) bajo la lógica **FIFO** (*First In, First Out*).

La relación funcional principal para evaluar el desempeño es el Tiempo Promedio de los clientes en
el Sistema ($TPS$):

$TPS = \frac{1}{n}\sum_{i=1}^{n}TSIS_{i}$

### Software y Herramientas
Para la implementación de los modelos, se consideran las siguientes herramientas tecnológicas:

* **Lenguajes y Análisis**: R, Excel.

* **Software Especializado**: Simul8, FlexSim.

## Add your files

- [ ] [Create](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#create-a-file) or [upload](https://docs.gitlab.com/ee/user/project/repository/web_editor.html#upload-a-file) files
- [ ] [Add files using the command line](https://docs.gitlab.com/ee/gitlab-basics/add-file.html#add-a-file-using-the-command-line) or push an existing Git repository with the following command:

```bash
cd existing_repo
git remote add origin https://github.com/thepadr30/SimulAva3010192
git branch -M main
git push -uf origin main
```


## Convertir jupyter a otros formatos

una buena opción es tener instalado el paquete rise

```PowerShell
jupyter nbconvert --to FORMAT notebook.ipynb
```
otra opción es:

```PowerShell
jupyter nbconvert notebook.ipynb --to slides --post serve --SlidesExporter.reveal_theme=serif --SlidesExporter.reveal_scroll=True --SlidesExporter.reveal_transition=none
jupyter nbconvert D:\SimulAva\notebooks\SimulacionMC.ipynb --to slides --post serve --SlideExporter.reveal_theme=serif --SlidesExporter.reveal_scroll=True --SlidesExporter.reveal_transition=none
jupyter nbconvert --to html D:\SimulAva\notebooks\SimulacionMC.ipynb
jupyter nbconvert --to pdf D:\SimulAva\notebooks\SimulacionMC.ipynb
```

Más info [nbconvert documentation](https://nbconvert.readthedocs.io/en/latest/usage.html)

## PowerShell

Para revisar tamaño de los archivos

```PowerShell
Get-ChildItem -path "D:\Proyectos\Diplomado_UdeM\datasets\*" | Foreach {
> $Files = Get-ChildItem $_.FullName -Recurse -File
> $Size = '{0:N2}' -f (( $Files | Measure-Object -Property Length -Sum).Sum /1MB)
> [PSCustomObject]@{Profile = $_.FullName ; TotalObjects = "$($Files.Count)" ; SizeMB = $Size}
> } | Export-CSV "D:\Proyectos\Diplomado_UdeM\folder_size_1.csv" -NoTypeInformation
```

## Git

Identifica los archivos grandes: Puedes utilizar el siguiente comando para listar los archivos grandes en tu historial de Git:

```bash
git rev-list --objects --all | grep $(git verify-pack -v .git/objects/pack/pack-*.idx | sort -k 3 -n | tail -10 | awk '{print$1}')
```

Este comando te mostrará los archivos más grandes en el historial de tu repositorio.

Reduce el tamaño de los archivos: Si puedes, intenta comprimir o reducir el tamaño de los archivos problemáticos. Por ejemplo, si se trata de imágenes, videos o archivos de datos, podrías comprimirlos o reducir su resolución.

Elimina los archivos grandes del historial de Git (si es necesario): Si necesitas eliminar los archivos grandes del historial (ya que seguirán existiendo en commits anteriores), puedes usar la herramienta BFG Repo-Cleaner o git filter-repo para limpiar el historial.

Usando BFG Repo-Cleaner:

```bash
bfg --delete-files archivo_grande
git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

Añade nuevamente los archivos (si redujiste el tamaño): Después de comprimir o reducir el tamaño de los archivos, vuelve a añadirlos con: bash Copiar código

```bash
git add archivo_comprimido
git commit -m "Archivo reducido"
git push origin rama
```

Opción 2: Usar Git LFS (Large File Storage)
Git LFS es una extensión de Git que te permite manejar archivos grandes sin afectar el rendimiento del repositorio. Con Git LFS, los archivos grandes no se almacenan directamente en Git, sino que se sustituyen por referencias, mientras los archivos reales se almacenan en un servidor separado.

Instala Git LFS: Si no lo tienes instalado, puedes instalarlo según tu sistema operativo:

Linux: bash Copiar código

```bash
sudo apt-get install git-lfs
```

Mac: bash Copiar código

```bash
brew install git-lfs
```

Windows: Descárgalo desde: git-lfs.github.com
Inicializa Git LFS en tu repositorio: Después de instalar Git LFS, debes inicializarlo en el repositorio:

```bash
git lfs install
```

Rastrear los archivos grandes con LFS: Debes especificar los tipos de archivos que deseas rastrear con Git LFS. Por ejemplo, si los archivos grandes son imágenes PNG, puedes usar el siguiente comando:

```bash
git lfs track "*.png"
```

También puedes rastrear archivos específicos de gran tamaño con:

```bash
git lfs track "archivo_grande"
```

Añade y commitea los archivos grandes: Después de configurar LFS, añade y commitea los archivos rastreados:

```bash
git add .gitattributes archivo_grande
git commit -m "Añadir archivo grande con LFS"
```

Push al repositorio: Finalmente, empuja los cambios al repositorio:

```bash
git push origin rama
```

Git LFS subirá los archivos grandes al almacenamiento de Git LFS mientras que Git seguirá manejando el resto de los archivos como de costumbre.

## The Boston Housing Dataset

[bosto](https://lib.stat.cmu.edu/datasets/boston)
[The Boston Housing Dataset](https://www.kaggle.com/code/prasadperera/the-boston-housing-dataset)


## Python Plotly Express Tutorial: Unlock Beautiful Visualizations

[Python Plotly Express Tutorial: Unlock Beautiful Visualizations](https://www.datacamp.com/tutorial/python-plotly-express-tutorial)

## UCI Machine Learning Repository

[UCI Machine Learning Repository](https://archive.ics.uci.edu/datasets?Task=Regression&skip=0&take=10&sort=desc&orderBy=NumHits&search=ridge)

## Seaborn data

[seaborn-data](https://github.com/mwaskom/seaborn-data)
[load_dataset](https://seaborn.pydata.org/generated/seaborn.load_dataset.html)

```txt
SIMULAVA-UNAL/
├── .github/                # Configuración de GitHub (acciones, plantillas)
├── data/
│   ├── raw/                # Datos originales sin procesar (CSV, XLSX)
│   └── processed/          # Datos limpios listos para la simulación
├── docs/
│   ├── teoria/             # Conceptos de probabilidad, riesgo y aleatoriedad 
│   └── reportes/           # Informes de validación y resultados finales
├── models/                 # Etapas del modelamiento 
│   ├── 01_definicion/      # Documentación del problema y recolección
│   ├── 02_formulacion/     # Modelos matemáticos y diagramas de flujo
│   ├── 03_solucion/        # Lógica de simulación (Python, R, FlexSim)
│   └── 04_validacion/      # Pruebas de bondad de ajuste y verificación
├── notebooks/              # Análisis exploratorio y pruebas con distfit/fitter
├── src/                    # Código fuente reutilizable
│   ├── core/               # Motores de simulación (Monte Carlo, Eventos Discretos)
│   └── utils/              # Funciones auxiliares (visualización, outliers)
├── requirements.txt        # Dependencias del proyecto (Python 3.12)
├── .gitignore              # Archivos a ignorar por Git
├── LICENSE                 # Licencia del software
└── README.md               # Descripción académica del repositorio
```