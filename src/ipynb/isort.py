import logging
import os
import random
import sys
import warnings
from time import localtime, strftime
from typing import Callable, Tuple

import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import HTML, Image, display
from scipy import stats

from src.graph.fun_graph_matplotlib import FnGraphMat
from src.ipynb.estiloDashboard import (estilo_dashboard, estilo_dashboard_v0,
                                       estilo_dashboard_v2)
from src.ipynb.simulacionMonedaMonteCarlo import (graficar_matplotlib,
                                                  graficar_plotly,
                                                  graficar_seaborn)
from src.logs.logger import setup_logging
from src.utils import statisticsBase as sB
