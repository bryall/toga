from contextlib import contextmanager
from math import pi

from .base import Widget
from .canvas import Canvas
from ..color import BLACK
from ..color import color as parse_color, rgba
from ..font import Font, SYSTEM, SERIF, SANS_SERIF

from matplotlib.backend_bases import (
    FigureCanvasBase,FigureManagerBase,RendererBase,GraphicsContextBase
)
from matplotlib.figure import Figure
from matplotlib.path import Path
from matplotlib.transforms import Affine2D

class ChartRenderer(RendererBase):
    """
    The renderer handles drawing/rendering operations.
    This is a minimal do-nothing class that can be used to get started when
    writing a new backend. Refer to backend_bases.RendererBase for
    documentation of the classes methods.
    """
    def __init__(self,renderer,width,height,dpi):
        self.dpi = dpi
        self.width=width
        self.height=height
        self._renderer = renderer
        RendererBase.__init__(self)

    def draw_path(self, gc, path, transform, rgbFace=None):
        #print("ChartRenderer - draw_path")
        #print(path)
        if rgbFace is not None:
            r,g,b,a = rgbFace
        else:
            r,g,b,a = gc.get_rgb()

        transform = transform + \
            Affine2D().scale(1.0, -1.0).translate(0.0, self.height)
        color = parse_color(rgba(r*255,g*255,b*255,a*255))
        #with self._renderer.fill(color=color,preserve=True) as filler:
        with self._renderer.stroke(color=color, line_width=gc.get_linewidth()) as stroker:
            for points, code in path.iter_segments(transform):
                if code == Path.MOVETO:
                    stroker.move_to(points[0],points[1])
                    #filler.move_to(points[0],points[1])
                elif code == Path.LINETO:
                    stroker.line_to(points[0],points[1])
                elif code == Path.CURVE3:
                    stroker.quadratic_curve_to(points[0],points[1],points[2],points[3])
                elif code == Path.CURVE4:
                    stroker.bezier_curve_to(points[0],points[1],points[2],points[3],points[4],points[5])
                elif code == Path.CLOSEPOLY:
                    #print(points)
                    stroker.closed_path(points[0],points[1])
        #print("ChartRenderer - draw_path")

    def draw_image(self, gc, x, y, im):
        pass
        #print("ChartRenderer - draw_image")
        #print(gc)
        #print(x)
        #print(y)
        #print(im)
        #print("ChartRenderer - end draw_image")

    def draw_text(self, gc, x, y, s, prop, angle, ismath=False, mtext=None):
        #print("ChartRenderer - draw_text")
        self._draw_text_as_path(gc, x, y, s, prop, angle, ismath)
        #print("ChartRenderer - draw_text end")


    def _draw_text_as_path(self, gc, x, y, s, prop, angle, ismath):
        """
        draw the text by converting them to paths using textpath module.
        Parameters
        ----------
        prop : `matplotlib.font_manager.FontProperties`
          font property
        s : str
          text to be converted
        usetex : bool
          If True, use matplotlib usetex mode.
        ismath : bool
          If True, use mathtext parser. If "TeX", use *usetex* mode.
        """
        path, transform = self._get_text_path_transform(
            x, y, s, prop, angle, ismath)
        color = gc.get_rgb()

        gc.set_linewidth(.75)
        self.draw_path(gc, path, transform, rgbFace=color)

    def flipy(self):
        return True

    def get_canvas_width_height(self):
        return self.width, self.height

    def get_text_width_height_descent(self, s, prop, ismath):
        """
        get the width and height in display coords of the string s
        with FontPropertry prop
        """

        if(prop.get_family()[0] == SANS_SERIF):
            font_family = SANS_SERIF
        elif(prop.get_family()[0] == CURSIVE):
            font_family = CURSIVE
        elif(prop.get_family()[0] == FANTASY):
            font_family = FANTASY
        elif(prop.get_family()[0] == MONOSPACE):
            font_family = MONOSPACE
        else:
            font_family = SERIF
        font = Font(family=font_family, size=int(prop.get_size()))

        w,h = font.measure(s)
        return w, h, 1

    def points_to_pixels(self, points):
        # if backend doesn't have dpi, e.g., postscript or svg
        return points
        # elif backend assumes a value for pixels_per_inch
        #return points/72.0 * self.dpi.get() * pixels_per_inch/72.0
        # else
        #return points/72.0 * self.dpi.get()

class Chart(Canvas, FigureCanvasBase):
    """Create new chart.

    Args:
        id (str):  An identifier for this widget.
        style (:obj:`Style`): An optional style object. If no
            style is provided then a new one will be created for the widget.
        factory (:obj:`module`): A python module that is capable to return a
            implementation of this class with the same name. (optional &
            normally not needed)
    """

    def __init__(self, figure, id=None, style=None, factory=None):
        self.figure = figure
        Canvas.__init__(self,id=id, style=style, factory=factory)

    def draw(self, figure):
        self.figure = figure
        FigureCanvasBase.__init__(self, self.figure)
        l,b,w,h = self.figure.bbox.bounds
        renderer = ChartRenderer(self,w,h,self.figure.dpi)
        self.figure.draw(renderer)
