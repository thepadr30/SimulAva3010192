# -*- coding: utf-8 -*-
""" Gráficas usando plotly

funciones para gráficar diferentes escenarios usando la librería plotly

Proyecto: personal

Tema: gráficas plotly

Programa: fun_graph_plotly

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

import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from scipy import stats

# =========================================================================== #
# Class plotly ============================================================== #
# =========================================================================== #

# Templates configuration
# -----------------------
#     Default template: 'plotly'
#     Available templates:
#         ['ggplot2', 'seaborn', 'simple_white', 'plotly',
#          'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
#          'ygridoff', 'gridon', 'none']
# fig.update_layout(template=template, title="Mt Bruno Elevation: '%s' theme" % template)


class FnGraphPlotly():
    """FnGraphPlotly gráficas plotly

    Available templates:
        ['ggplot2', 'seaborn', 'simple_white', 'plotly','plotly_white', 'plotly_dark',
            'presentation', 'xgridoff','ygridoff', 'gridon', 'none']
    """

    def __init__(self, var_theme: str = None) -> None:
        # pass
        self.var_format_date = "%a, %d %b %Y %H:%M:%S"
        if var_theme:
            self.var_theme = var_theme
        else:
            self.var_theme = "ggplot2"

    def graph_scatter(self, data_frame, var_x, name_x: str, var_y, name_y: str, var_add=None):
        """
        graph_scatter Gráfico de puntos
        :param data_frame: 
        :param var_x: variable indice
        :param name_x: nombre indice
        :param var_y: variable objetivo
        :param name_y: nombre variable objetivo
        :param var_add: variable adicional. Defaults to None.
        :return: graph: gráfico de puntos
        """
        if var_add is not None:
            fig = px.scatter(data_frame, x=var_x, y=var_y, color=var_add)
            fig.update_layout(
                title=dict(
                    text=f"{name_y} <br> "
                         f"Mean: {np.round(var_y.mean(), 2)} Median: {np.round(var_y.median(), 2)} <br> "
                         f"std:{np.round(var_y.std(), 2)} "
                         f"CV: {np.round(stats.variation(var_y, axis=0, nan_policy='omit') * 100, 2)} "
                         f"Skew: {np.round(stats.skew(var_y, nan_policy='omit'), 2)} <br> "
                         f"{strftime(self.var_format_date, localtime())}",
                    x=0.5,
                    y=0.95,
                    font=dict(
                        size=9
                    )
                ),
                xaxis_title=name_x, yaxis_title=name_y,
                template=self.var_theme)
        else:
            fig = px.scatter(data_frame, x=var_x, y=var_y)
            fig.update_layout(
                title=dict(
                    text=f"{name_y} <br> "
                         f"Mean: {np.round(var_y.mean(), 2)} Median: {np.round(var_y.median(), 2)} <br> "
                         f"std:{np.round(var_y.std(), 2)} "
                         f"CV: {np.round(stats.variation(var_y, axis=0, nan_policy='omit') * 100, 2)} "
                         f"Skew: {np.round(stats.skew(var_y, nan_policy='omit'), 2)} <br> "
                         f"{strftime(self.var_format_date, localtime())}",
                    x=0.5,
                    y=0.95,
                    font=dict(
                        size=9
                    )
                ),
                xaxis_title=name_x, yaxis_title=name_y,
                template=self.var_theme)
        return fig.show()

    def graph_armor(self, var_x, name_x: str, var_y, name_y: str, var_add=None, name_add=None):
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
        if var_add is not None:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=var_x, y=var_y, name=name_y))
            fig.add_trace(go.Scatter(
                x=var_x, y=var_add, name=name_add))
            fig.update_layout(
                title=dict(
                    text=f"{name_y} <br> "
                    f"Mean: {np.round(var_y.mean(), 2)} Median: {np.round(var_y.median(), 2)} <br> "
                    f"std:{np.round(var_y.std(), 2)} "
                         f"CV: {np.round(stats.variation(var_y, axis=0, nan_policy='omit') * 100, 2)} "
                         f"Skew: {np.round(stats.skew(var_y, nan_policy='omit'), 2)} <br> "
                    f"{strftime(self.var_format_date, localtime())}",
                    x=0.5,
                    y=0.95,
                    font=dict(
                        size=9
                    )
                ),
                xaxis_title=name_x, yaxis_title=name_y,
                template=self.var_theme)
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=var_x, y=var_y, name=name_y))
            fig.update_layout(
                title=dict(
                    text=f"{name_y} <br> "
                    f"Mean: {np.round(var_y.mean(), 2)} Median: {np.round(var_y.median(), 2)} <br> "
                    f"std:{np.round(var_y.std(), 2)} "
                         f"CV: {np.round(stats.variation(var_y, axis=0, nan_policy='omit') * 100, 2)} "
                         f"Skew: {np.round(stats.skew(var_y, nan_policy='omit'), 2)} <br> "
                    f"{strftime(self.var_format_date, localtime())}",
                    x=0.5,
                    y=0.95,
                    font=dict(
                        size=9
                    )
                ),
                xaxis_title=name_x, yaxis_title=name_y,
                template=self.var_theme
            )
        return fig.show()

    def graph_armor_st(self, var_x, name_x: str, var_y, name_y: str, var_add=None, name_add=None):
        """graph_armor_st Gráfico de línea para series de tiempo

        Args:
            var_x (datetime): variable fecha
            name_x (str): nombre variable fecha
            var_y (float): variable objetivo
            name_y (str): nombre variable objetivo
            var_add (float, optional): variable adicional. Defaults to None.
            name_add (str, optional): nombre variable adicional. Defaults to None.

        Returns:
            graph: gráfico de líneas
        """
        if var_add is not None:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=var_x, y=var_y, name=name_y))
            fig.add_trace(go.Scatter(
                x=var_x, y=var_add, name=name_add))
            fig.update_layout(
                title=dict(
                    text=f"{name_y} <br> "
                    f"Mean: {np.round(var_y.mean(), 2)} Median: {np.round(var_y.median(), 2)} <br> "
                    f"std:{np.round(var_y.std(), 2)} "
                         f"CV: {np.round(stats.variation(var_y, axis=0, nan_policy='omit') * 100, 2)} "
                         f"Skew: {np.round(stats.skew(var_y, nan_policy='omit'), 2)} <br> "
                    f"{strftime(self.var_format_date, localtime())}",
                    x=0.5,
                    y=0.95,
                    font=dict(
                        size=9
                    )
                ),
                xaxis_title=name_x,
                yaxis_title=name_y,
                template=self.var_theme
            )
            fig.update_layout(
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1,
                                 label="1m",
                                 step="month",
                                 stepmode="backward"),
                            dict(count=6,
                                 label="6m",
                                 step="month",
                                 stepmode="backward"),
                            dict(count=1,
                                 label="YTD",
                                 step="year",
                                 stepmode="todate"),
                            dict(count=1,
                                 label="1y",
                                 step="year",
                                 stepmode="backward"),
                            dict(step="all")
                        ])
                    ),
                    rangeslider=dict(
                        visible=True
                    ),
                    type="date"
                )
            )
        else:
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=var_x, y=var_y, name=name_y))
            fig.update_layout(
                title=dict(
                    text=f"{name_y} <br>"
                    f"Mean: {np.round(var_y.mean(), 2)} Median: {np.round(var_y.median(), 2)} <br> "
                    f"std:{np.round(var_y.std(), 2)} "
                         f"CV: {np.round(stats.variation(var_y, axis=0, nan_policy='omit') * 100, 2)} "
                         f"Skew: {np.round(stats.skew(var_y, nan_policy='omit'), 2)} <br> "
                    f"{strftime(self.var_format_date, localtime())}",
                    x=0.5,
                    y=0.95,
                    font=dict(
                        size=9
                    )
                ),
                xaxis_title=name_x,
                yaxis_title=name_y,
                template=self.var_theme
            )
            fig.update_layout(
                xaxis=dict(
                    rangeselector=dict(
                        buttons=list([
                            dict(count=1,
                                 label="1m",
                                 step="month",
                                 stepmode="backward"),
                            dict(count=6,
                                 label="6m",
                                 step="month",
                                 stepmode="backward"),
                            dict(count=1,
                                 label="YTD",
                                 step="year",
                                 stepmode="todate"),
                            dict(count=1,
                                 label="1y",
                                 step="year",
                                 stepmode="backward"),
                            dict(step="all")
                        ])
                    ),
                    rangeslider=dict(
                        visible=True
                    ),
                    type="date"
                )
            )
        return fig.show()

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
            fig = px.box(data_frame, x=var_cat, y=var_vble,
                         color=var_cat_2, points='all')
            fig.update_traces(quartilemethod="exclusive")
            fig.update_layout(
                title=f"Boxplot {var_vble} filter {var_cat} and {var_cat_2}",
                xaxis_title=var_cat,
                yaxis_title=var_vble,
                template=self.var_theme
            )
        else:
            fig = px.box(data_frame, x=var_cat, y=var_vble, points='all')
            fig.update_traces(quartilemethod="exclusive")
            fig.update_layout(
                title=f"Boxplot {var_vble} filter {var_cat}",
                xaxis_title=var_cat,
                yaxis_title=var_vble,
                template=self.var_theme
            )
        return fig.show()

    def graph_armor_box(self, data_frame, var_vble: str):
        """graph_armor_box Boxplot

        Args:
            data_frame (pd.DataFrame): dataframe contenedor de la variable objetivo
            var_vble (str): nombre variable objetivo

        Returns:
            _type_: _description_
        """
        fig = px.box(data_frame, y=var_vble, points='all')
        fig.update_traces(quartilemethod="exclusive")
        fig.update_layout(
            title=f"Boxplot {var_vble}",
            yaxis_title=var_vble,
            template=self.var_theme
        )
        return fig.show()

    def graph_armor_hist(self, data_frame, var_vble: str):
        """graph_armor_hist _summary_

        Args:
            data_frame (_type_): _description_
            var_vble (str): _description_

        Returns:
            _type_: _description_
        """
        fig = px.histogram(data_frame, var_vble, marginal='box')
        fig.add_vline(x=data_frame[var_vble].quantile(
            0.05), line_width=1, line_dash='dash', line_color='firebrick', col=1)
        fig.add_vline(x=data_frame[var_vble].quantile(
            0.25), line_width=1, line_dash='dash', line_color='firebrick', col=1)
        fig.add_vline(x=data_frame[var_vble].quantile(
            0.50), line_width=1, line_dash='dash', line_color='firebrick', col=1)
        fig.add_vline(x=data_frame[var_vble].quantile(
            0.75), line_width=1, line_dash='dash', line_color='firebrick', col=1)
        fig.add_vline(x=data_frame[var_vble].quantile(
            0.95), line_width=1, line_dash='dash', line_color='firebrick', col=1)
        fig.update_layout(
            title=f"Histogram {var_vble}",
            yaxis_title=var_vble,
            template=self.var_theme
        )
        return fig.show()

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
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data_frame[var_index],
                      y=data_frame[var_vble], name=var_vble))
        fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_inf, len(
            data_frame)), name='Mínimo IQR', line=dict(color='firebrick', dash='dash')))
        fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_sup, len(
            data_frame)), name='Máximo IQR', line=dict(color='firebrick', dash='dash')))
        fig.update_layout(
            title=f"IQR {var_vble} límite inferior = {np.round(var_inf, 2)} "
                  f"límite superior = {np.round(var_sup, 2)}",
            xaxis_title=var_index, yaxis_title=var_vble, template=self.var_theme)
        return fig.show()

    def graph_armor_percentil(self, data_frame, var_index: str, var_vble: str, var_q1: float):
        """graph_armor_percentil _summary_

        Args:
            data_frame (_type_): _description_
            var_index (str): _description_
            var_vble (str): _description_
            var_q1 (float): _description_

        Returns:
            _type_: _description_
        """
        var_q1 = data_frame[var_vble].quantile(q=var_q1)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data_frame[var_index],
                      y=data_frame[var_vble], name=var_vble))
        fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q1, len(
            data_frame)), name=f'Percentil {var_q1 * 100}', line=dict(color='firebrick', dash='dash')))
        fig.update_layout(
            title=f"Percentil {var_vble}",
            xaxis_title=var_index, yaxis_title=var_vble, template=self.var_theme)
        return fig.show()

    def graph_armor_percentiles(
        self, data_frame, var_index: str, var_vble: str, var_q1: float, var_q2: float = None,
        var_q3: float = None, var_q4: float = None, var_q5: float = None
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
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data_frame[var_index],
                          y=data_frame[var_vble], name=var_vble))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q1_tmp, len(
                data_frame)), name=f'Percentil {var_q1 * 100}', line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q2_tmp, len(
                data_frame)), name=f'Percentil {var_q2 * 100}', line=dict(dash='dot')))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q3_tmp, len(
                data_frame)), name=f'Percentil {var_q3 * 100}', line=dict(dash='dashdot')))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q4_tmp, len(
                data_frame)), name=f'Percentil {var_q4 * 100}', line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q5_tmp, len(
                data_frame)), name=f'Percentil {var_q5 * 100}', line=dict(dash='dot')))
        elif (var_q1 and var_q2 and var_q3 and var_q4):
            var_q1_tmp = data_frame[var_vble].quantile(q=var_q1)
            var_q2_tmp = data_frame[var_vble].quantile(q=var_q2)
            var_q3_tmp = data_frame[var_vble].quantile(q=var_q3)
            var_q4_tmp = data_frame[var_vble].quantile(q=var_q4)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data_frame[var_index],
                          y=data_frame[var_vble], name=var_vble))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q1_tmp, len(
                data_frame)), name=f'Percentil {var_q1 * 100}', line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q2_tmp, len(
                data_frame)), name=f'Percentil {var_q2 * 100}', line=dict(dash='dot')))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q3_tmp, len(
                data_frame)), name=f'Percentil {var_q3 * 100}', line=dict(dash='dashdot')))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q4_tmp, len(
                data_frame)), name=f'Percentil {var_q4 * 100}', line=dict(dash='dash')))
        elif (var_q1 and var_q2 and var_q3):
            var_q1_tmp = data_frame[var_vble].quantile(q=var_q1)
            var_q2_tmp = data_frame[var_vble].quantile(q=var_q2)
            var_q3_tmp = data_frame[var_vble].quantile(q=var_q3)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data_frame[var_index],
                          y=data_frame[var_vble], name=var_vble))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q1_tmp, len(
                data_frame)), name=f'Percentil {var_q1 * 100}', line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q2_tmp, len(
                data_frame)), name=f'Percentil {var_q2 * 100}', line=dict(dash='dot')))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q3_tmp, len(
                data_frame)), name=f'Percentil {var_q3 * 100}', line=dict(dash='dashdot')))
        elif (var_q1 and var_q2):
            var_q1_tmp = data_frame[var_vble].quantile(q=var_q1)
            var_q2_tmp = data_frame[var_vble].quantile(q=var_q2)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data_frame[var_index],
                          y=data_frame[var_vble], name=var_vble))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q1_tmp, len(
                data_frame)), name=f'Percentil {var_q1 * 100}', line=dict(dash='dash')))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q2_tmp, len(
                data_frame)), name=f'Percentil {var_q2 * 100}', line=dict(dash='dot')))
        else:
            var_q1_tmp = data_frame[var_vble].quantile(q=var_q1)
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=data_frame[var_index],
                          y=data_frame[var_vble], name=var_vble))
            fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q1_tmp, len(
                data_frame)), name=f'Percentil {var_q1 * 100}', line=dict(dash='dash')))
        fig.update_layout(
            title=f"Percentiles {var_vble}",
            xaxis_title=var_index, yaxis_title=var_vble, template=self.var_theme)
        return fig.show()

    def graph_armor_iqr_percentil(self, data_frame, var_index: str, var_vble: str):
        """graph_armor_iqr_percentil _summary_

        Args:
            data_frame (_type_): _description_
            var_index (str): _description_
            var_vble (str): _description_

        Returns:
            _type_: _description_
        """
        var_q1 = data_frame[var_vble].quantile(q=.25)
        var_q3 = data_frame[var_vble].quantile(q=.75)
        var_iqr = var_q3-var_q1
        var_li = var_q1 - (1.5 * var_iqr)
        var_ls = var_q3 + (1.5 * var_iqr)
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=data_frame[var_index],
                      y=data_frame[var_vble], name=var_vble))
        fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_li, len(
            data_frame)), name=f'Límite inferior', line=dict(color='firebrick', dash='dash')))
        fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_ls, len(
            data_frame)), name=f'Límite superior', line=dict(color='firebrick', dash='dash')))
        fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q1, len(
            data_frame)), name=f'Q1', line=dict(color='green', dash='dash')))
        fig.add_trace(go.Scatter(x=data_frame[var_index], y=np.repeat(var_q3, len(
            data_frame)), name=f'Q3', line=dict(color='green', dash='dash')))
        fig.update_layout(
            title=f"{var_vble}",
            xaxis_title=var_index, yaxis_title=var_vble, template=self.var_theme)
        return fig.show()
