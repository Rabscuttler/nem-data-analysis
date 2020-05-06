import numpy as _np
import pandas as _pd
import matplotlib.pyplot as _plt

from src.plot_helpers.matplotlib_helpers\
        import range_axis_ticks as _range_axis_ticks


def plot_value_by_element(df, xaxis, element_col, value_col, ax, cmap,
                          alpha=1.0, lw=1.0,
                          x_intervals=None,  x_fmt=None):
    '''
    Plot values by each element in  the column element_col in df on ax.
    Can specify linewidth (lw), alpha of lines and colormap to use (cmap).
    The number of x-axis intervals can be specified, it it is, provide x_fmt
    Will only plot where value > 0 for given datetime

    Args:
        df: DataFrane
        xaxis: xaxis column name in df
        element_col: element column name in df
        value_col: value column name in df
        ax: matplotlib Axes object
        cmap: matplotlib.pyplot.cm colourmap object
        alpha (float, 0-1): plot alpha
        lw (float): linewidth of line plots
        x_intervals (int, optional, need x_fmt): number of x-axis intervals
        x_fmt (matplotlib Formatter, optional, need x_intervals): formatter

    Returns:
        Axis with plot of elements
    '''
    unique_elements = df[element_col].drop_duplicates()
    cmap = iter(cmap(_np.linspace(0, 1, len(unique_elements))))

    for element, colour in zip(unique_elements, cmap):
        filtered_val = df.loc[df[element_col] == element, [xaxis, value_col]]
        if abs(filtered_val[value_col].sum()) > 0:
            ax.plot(filtered_val[xaxis],
                    filtered_val[value_col],
                    label=element,
                    alpha=alpha, linewidth=lw,
                    color=colour)

    if x_intervals is not None:
        ax = _range_axis_ticks(ax, 'x', x_intervals, fmt=x_fmt)

    ax.tick_params(axis='x', labelrotation=90, labelsize=8)
    return ax


def find_nonzero_category(df, category_col, value_col):
    '''
    Returns a unique list of categories in category col.
    Each category returned has a non-zero sum in the value_col.

    Args:
        df (pandas DataFrame): DataFrame to use
        category_col (str): col within df to use to find non-zero categories
        value_col (str): col within df to assess whether category is non-zero

    Returns:
        Sorted list of categories
    '''

    cat_types = set(df[category_col])
    plot_types = []
    for cat in cat_types:
        df_cat_val = df.loc[df[category_col] == cat, value_col]
        if df_cat_val.sum() > 0:
            plot_types.append(cat)

    return sorted(plot_types)


def plot_nonzero_elements_by_category(ax, df, xaxis_col, yaxis_col,
                                      element_col, category, category_col,
                                      cmap=None, lw=1.0, alpha=1.0):
    '''
    Plot x and y axis cols on ax for each unique element
    that satisfies a given category value.

    Args:
        ax (matplotlib Axes object): axis to plot on
        df (pandas DataFrame): dataframe to use
        xaxis_col (str): x-axis col name
        yaxis_col (str): y-axis col name
        element_col (str): col name used to identify individual elements
        category (str): isolate elements that are under this category
        category_col (str): col name in df used to filter on category
        cmap (matplotlib.pyplot.cm, optional): colormap
        lw (float, optional): linewidth
        alpha (float, optional): plot alpha

    Returns:
        Axis with plotted elements tha meet category criteria
        Dataframe with categories filtered
    '''

    category_df = df.loc[df[category_col] == category, :]
    elements = set(category_df[element_col])

    if cmap is not None:
        colors = iter(cmap(_np.linspace(0, 1, len(elements))))
    else:
        colors = iter(_plt.cm.tab10(0, 1, len(elements)))

    # plot line for each element where yaxis_col > 0 for datetime range
    for element, color in zip(sorted(elements), colors):
        element_df = category_df.loc[category_df[element_col] == element, :]
        if element_df[yaxis_col].sum() > 0:
            ax.plot(element_df[xaxis_col], element_df[yaxis_col],
                    label=element, color=color, linewidth=lw)

    return ax, category_df


def nofb(df, datetime_col=None):
    '''
    Creates two series with the limits of the NEM normal operating
    frequency band.

    Args:
        df (pandas DataFrame): DataFrame length to copy for NOFB series
        datetime_col (str, optional): default is to assume DatetimeIndex,
                                      if this is not the case, supply
                                      datetime_col
    Returns:
        Tuple of Series corresponding to (upper NOFB, lower NOFB)
    '''

    if datetime_col:
        lower = _np.ones(df[datetime_col].shape) * 49.85
        upper = _np.ones(df[datetime_col].shape) * 50.15
        index = df[datetime_col]
    else:
        lower = _np.ones(df.index.shape) * 49.85
        upper = _np.ones(df.index.shape) * 50.15
        index = df.index

    return (_pd.Series(data=upper, index=index),
            _pd.Series(data=lower, index=index))


def nofb_plot(nofb_function, axis, lw=1.0, alpha=1.0, style='y--'):
    '''
    Plots NOFB. Adds label to one of the plotted series.

    Args:
        nofb_function (func): nofb function with args supplied
        axis (matplotlib Axes): Axis to plot on
        lw (float, optional): plot linewidth
        alpha(float, optional): plot alpha
        style (str): matplotlib style, refer to pyplot.plot docs
    Returns:
        Axis with NOFB plotted
    '''

    upper, lower = nofb_function
    axis.plot(upper, style, label='NOFB', linewidth=lw, alpha=alpha)
    axis.plot(lower, style, linewidth=lw, alpha=alpha)

    return axis


def stacked_bar_subplots(df, figsize, cmap,
                         xaxis_col, values_col,
                         subplots_list, subplot_col,
                         stacked_list, stacked_col,
                         label_add, ax_title_add):
    '''
    Plot stacked bar charts across a range of subplots

    Args:
        df (pd.DataFrame): DataFrame to plot, with releveant *_cols
        figsize (tuple): size in inches for figure
        cmap (plt.cmap): object to determine color palette for stacked elements
        xaxis_col (str): name of col in df to use as xticks
        values_col (str): name of col in df to plot values
        subplots_list (list): list to use as basis for separating subplots
        subplot_col (str); name of col in df to separate data for each subplot
        stacked_list (list): list of elements to stack in each subplot
        stacked_col (str): name of col in df to obtain series to stack
        label_add (str): generic str to add to the end of each stacked el label
        ax_title_add (str): generic str to add to end of ax title
    Returns:
        Fig, Ax
    '''

    fig, ax = _plt.subplots(len(subplots_list), 1,
                            figsize=figsize, sharex=True)
    x_labels = df[xaxis_col].drop_duplicates().tolist()
    x_tix = _np.arange(len(x_labels))

    colormap = _plt.get_cmap(cmap)
    colors = colormap(_np.linspace(0, 1, len(stacked_list)))
    plot_colors = {el: colors[i] for i, el in enumerate(stacked_list)}

    for i, subplot_el in enumerate(subplots_list):
        y_base = _np.zeros_like(x_tix)
        subplot_df = df.query(f'{subplot_col}==@subplot_el')
        for el in stacked_list:
            rev = subplot_df.query(f'{stacked_col}==@el')
            ax[i].bar(x_tix, rev[values_col], bottom=y_base,
                      color=plot_colors[el],
                      label=f'{el} {label_add}')
            y_base = _np.add(y_base, rev[values_col].tolist())
        ax[i].set_title(f'{subplot_el} {ax_title_add}')
    return fig, ax
