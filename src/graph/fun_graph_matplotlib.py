# -*- coding: utf-8 -*-
""" Gráficas usando matplotlib
funciones para gráficar diferentes escenarios usando la librería matplotlib

Proyecto: personal

Tema: gráficas matplotlib

Programa: fun_graph_matplotlib

Soporte: kfhidalgoh@unal.edu.co

version: 1.0.0

lenguaje: Python 3.8.13

CD: 20230131

LUD: 20230131
"""

__author__ = "Kevin Hidalgo"
__contact__ = "kfhidalgoh@unal.edu.co"
__copyright__ = "Copyright 2023, Kevin Hidalgo"
__credits__ = ["Kevin Hidalgo"]
__email__ = "kfhidalgoh@unal.edu.co"
__status__ = "Production"
__version__ = "1.0.0"

# =========================================================================== #
# Librerías ================================================================= #
# =========================================================================== #

from time import localtime, strftime

import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
import seaborn as sns
import pandas as pd

# presentacion de estilos
# plt.style.use("ggplot")
# sns.set_theme(style="darkgrid")
plt.rc('figure', figsize=(16, 9))
plt.rc('font', size=14)


# https://matplotlib.org/stable/gallery/style_sheets/style_sheets_reference.html

# =========================================================================== #
# Class Matplotlib ========================================================== #
# =========================================================================== #


class FnGraphMat:
    """FnGraphMat Gráficas Matplotlib y Seaborn

    Available templates:
        ['Solarize_Light2', '_classic_test_patch', 'bmh', 'classic', 'dark_background', 'fast',
        'fivethirtyeight', 'ggplot', 'grayscale', 'seaborn', 'seaborn-bright',
        'seaborn-colorblind', 'seaborn-dark', 'seaborn-dark-palette', 'seaborn-darkgrid',
        'seaborn-deep', 'seaborn-muted', 'seaborn-notebook', 'seaborn-paper',
        'seaborn-pastel', 'seaborn-poster', 'seaborn-talk', 'seaborn-ticks',
        'seaborn-white', 'seaborn-whitegrid', 'tableau-colorblind10', 'dark_style']
    """

    def __init__(self, var_theme: str = None) -> None:
        # pass
        self.var_format_date = "%a, %d %b %Y %H:%M:%S"
        if var_theme == 'dark_style':
            plt.style.use('fivethirtyeight')
            plt.rcParams['lines.linewidth'] = 1.5
            dark_style = {
                'figure.facecolor': '#212946',
                'axes.facecolor': '#212946',
                'savefig.facecolor': '#212946',
                'axes.grid': True,
                'axes.grid.which': 'both',
                'axes.spines.left': False,
                'axes.spines.right': False,
                'axes.spines.top': False,
                'axes.spines.bottom': False,
                'grid.color': '#2A3459',
                'grid.linewidth': '1',
                'text.color': '0.9',
                'axes.labelcolor': '0.9',
                'xtick.color': '0.9',
                'ytick.color': '0.9',
                'font.size': 12
            }
            plt.rcParams.update(dark_style)
        elif var_theme:
            plt.style.use(var_theme)
        else:
            plt.style.use("ggplot")

    def graph_scatter(self, var_x: float, var_y: float, name_x: str, name_y: str,
                      var_add=None, name_add=None):
        """
        graph_scatter Gráfico de puntos
        :param var_x: variable indice
        :param var_y: variable objetivo
        :param name_x: nombre indice
        :param name_y: nombre variable objetivo
        :param var_add: variable adicional. Defaults to None.
        :param name_add: nombre variable adicional. Defaults to None.
        :return: graph: gráfico de puntos
        """
        if var_add is not None:
            _, ax = plt.subplots()
            ax.scatter(var_x, var_y, label=name_y)
            ax.scatter(var_x, var_add, label=name_add)
            ax.set_title(
                f"{name_y} \n mean: {np.round(var_y.mean(), 2)} "
                f"median: {np.round(var_y.median(), 2)} "
                f"std:{np.round(var_y.std(), 2)} "
                f"CV: {np.round(stats.variation(var_y, axis=0, nan_policy='omit') * 100, 2)} "
                f"Skew: {np.round(stats.skew(var_y, nan_policy='omit'), 2)} \n "
                f"{strftime(self.var_format_date, localtime())}")
            ax.tick_params(labelrotation=90)
            plt.xlabel(name_x)
            plt.ylabel(name_y)
            plt.legend()
        else:
            _, ax = plt.subplots()
            ax.scatter(var_x, var_y, label=name_y)
            ax.set_title(
                f"{name_y} \n mean: {np.round(var_y.mean(), 2)} "
                f"median: {np.round(var_y.median(), 2)} "
                f"std:{np.round(var_y.std(), 2)} "
                f"CV: {np.round(stats.variation(var_y, axis=0, nan_policy='omit') * 100, 2)} "
                f"Skew: {np.round(stats.skew(var_y, nan_policy='omit'), 2)} \n "
                f"{strftime(self.var_format_date, localtime())}")
            ax.tick_params(labelrotation=90)
            plt.xlabel(name_x)
            plt.ylabel(name_y)
            plt.legend()
        return plt.show()

    def graph_armor(
            self, var_x: float, name_x: str, var_y: float, name_y: str, var_add=None, name_add=None
    ):
        """graph_armor Gráfico de línea

        Args:
            var_x (float): variable indice
            name_x (str): nombre indice
            var_y (float): variable objetivo
            name_y (str): nombre variable objetivo
            var_add (float, optional): variable adicional. Defaults to None.
            name_add (str, optional): nombre variable adicional. Defaults to None.

        Returns:
            graph: gráfico de líneas
        """
        if var_add:
            _, ax = plt.subplots()
            ax.plot(var_x, var_y, label=name_y)
            ax.plot(var_x, var_add, label=name_add)
            ax.set_title(
                f"{name_y} \n mean: {np.round(var_y.mean(), 2)} "
                f"median: {np.round(var_y.median(), 2)} "
                f"std:{np.round(var_y.std(), 2)} "
                f"CV: {np.round(stats.variation(var_y, axis=0, nan_policy='omit') * 100, 2)} "
                f"Skew: {np.round(stats.skew(var_y, nan_policy='omit'), 2)} \n "
                f"{strftime(self.var_format_date, localtime())}")
            ax.tick_params(labelrotation=90)
            plt.xlabel(name_x)
            plt.ylabel(name_y)
            plt.legend()
        else:
            _, ax = plt.subplots()
            ax.plot(var_x, var_y, label=name_y)
            ax.set_title(
                f"{name_y} \n mean: {np.round(var_y.mean(), 2)} "
                f"median: {np.round(var_y.median(), 2)} "
                f"std:{np.round(var_y.std(), 2)} "
                f"CV: {np.round(stats.variation(var_y, axis=0, nan_policy='omit') * 100, 2)} "
                f"Skew: {np.round(stats.skew(var_y, nan_policy='omit'), 2)} \n "
                f"{strftime(self.var_format_date, localtime())}")
            ax.tick_params(labelrotation=90)
            plt.xlabel(name_x)
            plt.ylabel(name_y)
            plt.legend()
        return plt.show()

    def graph_armor_zoom(self, dict_prmt: dict):
        """graph_armor_zoom gráfico de líneas con zoom

        Args:
            dict_prmt (dict): Diccionario de configuración. Ejemplo::

                dict_prmt_1 = {
                        "data_frame":df_automobile,
                        "var_vble":"price",
                        "name_vble": "Price",
                        "var_index":"index",
                        "name_index": "Index",
                        "zoom": (10,25),
                    }

        Returns:
            graph: gráfico de líneas
        """
        fig = plt.figure(figsize=(16, 9))
        grid = plt.GridSpec(nrows=3, ncols=1, hspace=0.6, wspace=0)
        main_ax = fig.add_subplot(grid[1:2, :])
        zoom_ax = fig.add_subplot(grid[2:, :])
        main_ax.plot(
            dict_prmt['data_frame'][dict_prmt["var_index"]],
            dict_prmt['data_frame'][dict_prmt["var_vble"]],
            label=dict_prmt["name_vble"]
        )
        min_y = min(dict_prmt['data_frame'][dict_prmt["var_vble"]])
        max_y = max(dict_prmt['data_frame'][dict_prmt["var_vble"]])
        main_ax.fill_between(
            dict_prmt['zoom'],
            min_y,
            max_y,
            facecolor='blue',
            alpha=0.5,
            zorder=0
        )
        main_ax.set_xlabel('')
        main_ax.set_title(dict_prmt["name_vble"])
        zoom_ax.plot(
            dict_prmt['data_frame'].loc[dict_prmt['zoom'][0]: dict_prmt['zoom'][1]][dict_prmt["var_index"]],
            dict_prmt['data_frame'].loc[dict_prmt['zoom'][0]: dict_prmt['zoom'][1]][dict_prmt["var_vble"]]
        )
        zoom_ax.set_title('Zoom: ' + str(dict_prmt['zoom']))
        zoom_ax.set_xlabel(dict_prmt["name_index"])
        plt.subplots_adjust(hspace=1)
        return plt.show()

    def graph_armor_hist(self, data_frame: pd.DataFrame, var_vble: str):
        """graph_armor_hist _summary_

        Args:
            data_frame (pd.DataFrame): _description_
            var_vble (str): _description_

        Returns:
            _type_: _description_
        """
        _, axes = plt.subplots(2, 1)
        sns.boxplot(data=data_frame, x=var_vble, ax=axes[0])
        axes[1] = plt.hist(data_frame[var_vble], alpha=0.6)
        quant_5, quant_25, quant_50, quant_75, quant_95 = data_frame[var_vble].quantile(0.05), data_frame[var_vble]\
            .quantile(0.25), data_frame[var_vble].quantile(0.5), data_frame[var_vble].quantile(0.75),\
            data_frame[var_vble].quantile(0.95)
        quants = [[quant_5, 1, 0.05, "5th"], [quant_25, 1, 0.25, "25th"], [
            quant_50, 1, 0.5, "50th"],  [quant_75, 1, 0.75, "75th"], [quant_95, 1, 0.95, "95th"]]
        for i in quants:
            plt.axvline(i[0], alpha=i[1], ymax=i[2], linestyle=":")
            plt.text(i[0]-.1, i[2], i[3], size=7, alpha=0.8)
        axes[0].set(xlabel='')
        axes[0].set_xticklabels([])
        plt.title(f"Histogram {var_vble}")
        return plt.show()

    def graph_armor_box(self, var_x: float, var_name: str):
        """graph_armor_box Boxplot

        Args:
            var_x (pd.Series): Variable objetivo
            var_name (str): Nombre variable objetivo

        Returns:
            graph: Boxplot
        """
        _, ax = plt.subplots()
        ax.boxplot(var_x)
        ax.set_title(f"Boxplot {var_name}")
        return plt.show()

    def graph_armor_box_cat(self, data_frame, var_vble: str, var_cat: str, var_cat_2=None):
        """graph_armor_box_cat Boxplot con categorías

        Args:
            data_frame (pd.DataFrame): dataframe con variables objetivo
            var_vble (str): nombre variable objetivo
            var_cat (str): nombre variable categórica
            var_cat_2 (str, optional): nombre variable categórica. Defaults to None.

        Returns:
            graph: gráfica boxplot
        """
        if var_cat_2:
            ax = sns.boxplot(data=data_frame, x=var_cat,
                             y=var_vble, hue=var_cat_2)
            ax.set(
                title=f"Boxplot {var_vble} filter {var_cat} and {var_cat_2}"
            )
            ax.tick_params(labelrotation=90)
        else:
            ax = sns.boxplot(data=data_frame, x=var_cat, y=var_vble)
            ax.set(
                title=f"Boxplot {var_vble} filter {var_cat}"
            )
            ax.tick_params(labelrotation=90)
        return plt.show()

    def graph_armor_iqr(self, data_frame, var_index: str, var_vble: str):
        """graph_armor_iqr Gráfica con límites intercuantiles

        Args:
            data_frame (pd.Dataframe): DatraFrame objetivo.
            var_index (str): nombre variable indice.
            var_vble (str): nombre variable objetivo.

        Returns:
            graph: gráfica IQR
        """
        var_rq1 = data_frame[var_vble].quantile(q=.25)
        var_rq3 = data_frame[var_vble].quantile(q=.75)
        var_iqr = var_rq3-var_rq1
        var_inf = var_rq1 - (1.5 * var_iqr)
        var_sup = var_rq3 + (1.5 * var_iqr)
        _, ax = plt.subplots()
        ax.plot(data_frame[var_index],
                data_frame[var_vble], label=var_vble, color='black')
        ax.plot(data_frame[var_index], np.repeat(var_inf, len(
            data_frame)), label='Mínimo IQR', color='firebrick', linestyle='dashed')
        ax.plot(data_frame[var_index], np.repeat(var_sup, len(
            data_frame)), label='Máximo IQR', color='firebrick', linestyle='dashed')
        ax.set_title(
            f"IQR {var_vble} límite inferior = {np.round(var_inf,2)} límite superior = {np.round(var_sup,2)}")
        ax.tick_params(labelrotation=90)
        plt.xlabel(var_index)
        plt.ylabel(var_vble)
        plt.legend()
        return plt.show()

    def graph_armor_percentil(self, data_frame, var_index: str, var_vble: str, var_threshold: float):
        """graph_armor_percentil gráfica de líneas con umbral percentil

        Args:
            data_frame (pd.DataFrame): dataframe contenedor variable
            var_index (str): nombre variable eje x
            var_vble (str): nombre variable eje y
            var_threshold (float): umbral, percentil

        Returns:
            graph: gráfica
        """
        var_threshold_tmp = data_frame[var_vble].quantile(q=var_threshold)
        _, ax = plt.subplots()
        ax.plot(data_frame[var_index],
                data_frame[var_vble], label=var_vble, color='black')
        ax.plot(data_frame[var_index], np.repeat(var_threshold_tmp, len(
            data_frame)), label=f'Percentil {var_threshold * 100}', color='firebrick', linestyle='dashed')
        return plt.show()

    def graph_armor_percentiles(
        self, data_frame, var_index: str, var_vble: str,
        var_q1: float, var_q2: float = None, var_q3: float = None,
        var_q4: float = None, var_q5: float = None
    ):
        """graph_armor_percentiles _summary_

        Args:
            data_frame (_type_): _description_
            var_index (str): _description_
            var_vble (str): _description_
            var_q1 (float): _description_
            var_q2 (float, optional): _description_. Defaults to None.
            var_q3 (float, optional): _description_. Defaults to None.
            var_q4 (float, optional): _description_. Defaults to None.
            var_q5 (float, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        if (var_q1 and var_q2 and var_q3 and var_q4 and var_q5):
            var_q1_tmp = data_frame[var_vble].quantile(q=var_q1)
            var_q2_tmp = data_frame[var_vble].quantile(q=var_q2)
            var_q3_tmp = data_frame[var_vble].quantile(q=var_q3)
            var_q4_tmp = data_frame[var_vble].quantile(q=var_q4)
            var_q5_tmp = data_frame[var_vble].quantile(q=var_q5)
            _, ax = plt.subplots()
            ax.plot(data_frame[var_index],
                    data_frame[var_vble], label=var_vble, color='black')
            ax.plot(data_frame[var_index], np.repeat(var_q1_tmp, len(
                data_frame)), label=f'Percentil {var_q1 * 100}', color='firebrick', linestyle='dashed')
            ax.plot(data_frame[var_index], np.repeat(var_q2_tmp, len(
                data_frame)), label=f'Percentil {var_q2 * 100}', color='firebrick', linestyle='dashdot')
            ax.plot(data_frame[var_index], np.repeat(var_q3_tmp, len(
                data_frame)), label=f'Percentil {var_q3 * 100}', color='firebrick', linestyle=(0, (1, 10)))
            ax.plot(data_frame[var_index], np.repeat(var_q4_tmp, len(
                data_frame)), label=f'Percentil {var_q4 * 100}', color='firebrick', linestyle='dotted')
            ax.plot(data_frame[var_index], np.repeat(var_q5_tmp, len(
                data_frame)), label=f'Percentil {var_q5 * 100}', color='firebrick', linestyle=(0, (3, 10, 1, 10)))
        elif (var_q1 and var_q2 and var_q3 and var_q4):
            var_q1_tmp = data_frame[var_vble].quantile(q=var_q1)
            var_q2_tmp = data_frame[var_vble].quantile(q=var_q2)
            var_q3_tmp = data_frame[var_vble].quantile(q=var_q3)
            var_q4_tmp = data_frame[var_vble].quantile(q=var_q4)
            _, ax = plt.subplots()
            ax.plot(data_frame[var_index],
                    data_frame[var_vble], label=var_vble, color='black')
            ax.plot(data_frame[var_index], np.repeat(var_q1_tmp, len(
                data_frame)), label=f'Percentil {var_q1 * 100}', color='firebrick', linestyle='dashed')
            ax.plot(data_frame[var_index], np.repeat(var_q2_tmp, len(
                data_frame)), label=f'Percentil {var_q2 * 100}', color='firebrick', linestyle='dashdot')
            ax.plot(data_frame[var_index], np.repeat(var_q3_tmp, len(
                data_frame)), label=f'Percentil {var_q3 * 100}', color='firebrick', linestyle=(0, (1, 10)))
            ax.plot(data_frame[var_index], np.repeat(var_q4_tmp, len(
                data_frame)), label=f'Percentil {var_q4 * 100}', color='firebrick', linestyle='dotted')
        elif (var_q1 and var_q2 and var_q3):
            var_q1_tmp = data_frame[var_vble].quantile(q=var_q1)
            var_q2_tmp = data_frame[var_vble].quantile(q=var_q2)
            var_q3_tmp = data_frame[var_vble].quantile(q=var_q3)
            _, ax = plt.subplots()
            ax.plot(data_frame[var_index],
                    data_frame[var_vble], label=var_vble, color='black')
            ax.plot(data_frame[var_index], np.repeat(var_q1_tmp, len(
                data_frame)), label=f'Percentil {var_q1 * 100}', color='firebrick', linestyle='dashed')
            ax.plot(data_frame[var_index], np.repeat(var_q2_tmp, len(
                data_frame)), label=f'Percentil {var_q2 * 100}', color='firebrick', linestyle='dashdot')
            ax.plot(data_frame[var_index], np.repeat(var_q3_tmp, len(
                data_frame)), label=f'Percentil {var_q3 * 100}', color='firebrick', linestyle=(0, (1, 10)))
        elif (var_q1 and var_q2):
            var_q1_tmp = data_frame[var_vble].quantile(q=var_q1)
            var_q2_tmp = data_frame[var_vble].quantile(q=var_q2)
            _, ax = plt.subplots()
            ax.plot(data_frame[var_index],
                    data_frame[var_vble], label=var_vble, color='black')
            ax.plot(data_frame[var_index], np.repeat(var_q1_tmp, len(
                data_frame)), label=f'Percentil {var_q1 * 100}', color='firebrick', linestyle='dashed')
            ax.plot(data_frame[var_index], np.repeat(var_q2_tmp, len(
                data_frame)), label=f'Percentil {var_q2 * 100}', color='firebrick', linestyle='dashdot')
        else:
            var_q1_tmp = data_frame[var_vble].quantile(q=var_q1)
            _, ax = plt.subplots()
            ax.plot(data_frame[var_index],
                    data_frame[var_vble], label=var_vble, color='black')
            ax.plot(data_frame[var_index], np.repeat(var_q1_tmp, len(
                data_frame)), label=f'Percentil {var_q1 * 100}', color='firebrick', linestyle='dashed')
        ax.set_title(
            f"Percentiles {var_vble}")
        plt.xlabel(var_index)
        plt.ylabel(var_vble)
        plt.legend()
        return plt.show()

    def graph_armor_iqr_percentil(self, data_frame, var_index: str, var_vble: str):
        """graph_armor_iqr_percentil _summary_

        Args:
            data_frame (_type_): _description_
            var_index (str): _description_
            var_vble (str): _description_

        Returns:
            _type_: _description_
        """
        var_q1 = data_frame[var_vble].quantile(q=0.25)
        var_q3 = data_frame[var_vble].quantile(q=0.75)
        var_iqr = var_q3 - var_q1
        var_li = var_q1 - (1.5 * var_iqr)
        var_ls = var_q3 + (1.5 * var_iqr)
        _, ax = plt.subplots()
        ax.plot(data_frame[var_index],
                data_frame[var_vble], label=var_vble, color='black')
        ax.plot(data_frame[var_index], np.repeat(var_q1, len(
            data_frame)), label=f'Percentil Q1 = {np.round(var_q1,2)}', color='firebrick', linestyle='dashed')
        ax.plot(data_frame[var_index], np.repeat(var_q3, len(
            data_frame)), label=f'Percentil Q3 = {np.round(var_q3,2)}', color='firebrick', linestyle='dashed')
        ax.plot(data_frame[var_index], np.repeat(var_li, len(
            data_frame)), label=f'Límite inferior = {np.round(var_li,2)}', color='blue', linestyle='dashdot')
        ax.plot(data_frame[var_index], np.repeat(var_ls, len(
            data_frame)), label=f'Límite superior = {np.round(var_ls,2)}', color='blue', linestyle='dashdot')
        ax.set_title(f"{var_vble}")
        plt.xlabel(var_index)
        plt.ylabel(var_vble)
        plt.legend()
        return plt.show()
