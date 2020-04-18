import numpy as _np
import matplotlib.dates as pltdates


def relimit_axis(ax, x_or_y, lower_offset, upper_offset,
                 offset_upper_from_new_lower=False):
    '''
    Use default limits of a particular axis to relimit based on offsets.
    Can alternatively relimit upper limit based on new lower limit.
    Offsets are added to lower and upper offsets by default.

    Args:
        ax: Axes object to modify
        x_or_y: 'x', 'y'. Axis to be relimited
        lower_offset: float, addition of offset to lower limit
        upper_offset: float, behaviour depends on next arg
        offset_upper_from_new_lower: if true, offset added from offset lower
                                    limit. else, addition of offset to upper
                                    limit
    Returns:
        ax, with relimited axis
    '''

    if x_or_y.lower() == 'x':
        lower, upper = ax.get_xlim()
        new_lower = lower + lower_offset
        if offset_upper_from_new_lower:
            new_upper = new_lower + upper_offset
        else:
            new_upper = upper + upper_offset
        ax.set_xlim(new_lower, new_upper)

    if x_or_y.lower() == 'y':
        lower, upper = ax.get_ylim()
        new_lower = lower + lower_offset
        if offset_upper_from_new_lower:
            new_upper = new_lower + upper_offset
        else:
            new_upper = upper + upper_offset
        ax.set_ylim(new_lower, new_upper)

    return ax


def range_axis_ticks(ax, x_or_y, n, fmt=None):
    '''
    Create n ticks, across the limits. The limits themselves count as ticks

    Args:
        ax: Axes object to modify
        x_or_y: 'x', 'y'. Axis to apply new ticks to
        n : number of ticks to add. limits included in n
        fmt: if provided, provide a matplotlib Formatter

    Returns:
        ax, with new ticks
    '''

    if x_or_y.lower() == 'x':
        lower, upper = ax.get_xlim()
        ticks = _np.linspace(lower, upper, n)
        ax.set_xticks(ticks)
        if fmt:
            ax.xaxis.set_major_formatter(fmt)

    if x_or_y.lower() == 'y':
        lower, upper = ax.get_ylim()
        ticks = _np.linspace(lower, upper, n)
        ax.set_yticks(ticks)
        if fmt:
            ax.yaxis.set_major_formatter(fmt)

    return ax


def legend_definition(ax, bbox, loc, cols, font_size):
    '''
    Simply adds legend to axis. This function documents important options

    Args:
        ax: Axes object to modify
        bbox: Bbox creates a bounding box for the legend.
              2 element tuple - loc - (x0, y0) are lower left coords of bbox
              4 element tuple - loc & size - (x0, y0, w, h) of bbox
              Can set legend outside plot area by making x or y <0 or >1
        loc: Location of legend inside bbox. Str or int, see docs
        cols: number of columns the legend should have
        font_size: legend font size

    Returns:
        ax, with legend
    '''

    ax.legend(bbox_to_anchor=bbox,
              ncol=cols,
              loc=loc,
              fontsize=font_size,
              mode='expand')

    return ax


def x_axis_styling(axis, title_size=10, label_size=10, tick_size=8,
                   rotation=70,
                   fmt=None,
                   gridbool=True):
    '''
    Generic styling for an x axis

    Args:
        axis: Axes object to modify
        *_size (optional): size for various parameters
        rotation: degrees to rotate axis labels
        fmt (matplotlib Formatter class, optional): format for axis labels
        gridbool (optional, bool): grid on when True

    Returns:
        Axis with styled x-axis
    '''

    axis.tick_params(axis='x', rotation=rotation, bottom=True)
    axis.tick_params(axis='x', labelsize=label_size)
    axis.grid(gridbool)
    if fmt is not None:
        axis.xaxis.set_major_formatter(fmt)

    return axis


def y_axis_styling(axis, title_size=10, label_size=10, tick_size=8,
                   rotation=70,
                   fmt=None,
                   gridbool=True):
    '''
    Generic styling for a y-axis

    Args:
        axis: Axes object to modify
        *_size (optional): size for various parameters
        rotation: degrees to rotate axis labels
        fmt (matplotlib Formatter class, optional): format for axis labels
        gridbool (optional, bool): grid on when True

    Returns:
        Axis with styled y-axis
    '''

    axis.tick_params(axis='y', rotation=rotation, bottom=True)
    axis.tick_params(axis='y', labelsize=label_size)
    axis.grid(gridbool)
    if fmt is not None:
        axis.yaxis.set_major_formatter(fmt)

    return axis
