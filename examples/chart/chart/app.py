import toga
from toga.style import Pack
from toga.color import BLACK,rgb
from toga import Chart
import matplotlib
from matplotlib.figure import Figure
#matplotlib.use('module://toga.widgets.chart')
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum
from toga.constants import ROW, COLUMN
from toga.sources import Source

class Examples(Enum):
    Pyplot_Simple = 1



        #self.chart.draw(self.pyplot_simple())
        #f = Figure(figsize=(5,4), dpi=100)
        #a = f.add_subplot(111)
        #t = np.arange(0.0,2.0,0.01)
        #s = 1 + np.sin(2*np.pi*t)
        #a.plot(t,s)
        #a.set_xlabel('time (s)')
        #a.set_ylabel('voltage (mV)')
        #a.set_title('About as simple as it gets, folks')
        #a.grid(True)

        #x1 = np.linspace(0.0, 5.0)
        #x2 = np.linspace(0.0, 2.0)
        #y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
        #y2 = np.cos(2 * np.pi * x2)
        #a = f.add_subplot(211)
        #a.plot(x1, y1, 'o-')
        #a.set_title('A tale of 2 subplots')
        #a.set_ylabel('Damped oscillation')
        #a = f.add_subplot(212)
        #a.plot(x2, y2, '.-')
        #a.set_xlabel('time (s)')
        #a.set_ylabel('Undamped')

        #np.random.seed(19680801)
        # example data
        #mu = 100  # mean of distribution
        #sigma = 15  # standard deviation of distribution
        #x = mu + sigma * np.random.randn(437)
        #num_bins = 50
        #ax = f.add_subplot(111)
        # the histogram of the data
        #n, bins, patches = ax.hist(x, num_bins, density=1)
        # add a 'best fit' line
        #y = ((1 / (np.sqrt(2 * np.pi) * sigma)) *
        #     np.exp(-0.5 * (1 / sigma * (bins - mu))**2))
        #ax.plot(bins, y, '--')
        #ax.set_xlabel('Smarts')
        #ax.set_ylabel('Probability density')
        #ax.set_title(r'Histogram of IQ: $\mu=100$, $\sigma=15$')

        #chart = toga.Chart(f)
        #canvas = toga.Canvas(style=Pack(flex=1))
        #box = toga.Box(children=[chart])

        # Add the content on the main window
        #self.main_window.content = box

        # Show the main window
        #self.main_window.show()

        #with canvas.stroke(color=BLACK) as stroker:
        #    stroker.write_text("Test 1 2 3",50,50)
        #with canvas.stroke() as stroker:
        #    with stroker.closed_path(50, 50) as closer:
        #        closer.line_to(100, 100)
        #        closer.line_to(100, 50)
        #with canvas.fill(color=BLACK) as filler:
        #    filler.move_to(3, 3)
        #    filler.bezier_curve_to(1, 1, 2, 2, 5, 5)

    def generateFigure(self, selection):
        print("Selection changed to {0}".format(selection.value))
        for example in Examples:
            if example.name == selection.value:
                value = example.value
                break
        f = {
                1 : self.pyplot_simple()
            }.get(value, None)
        print(f)
        self.chart.draw(f)
        self.main_window.content.refresh()

  
        
def pyplot_simple1():
    f = Figure(figsize=(5,4), dpi=100)
    a = f.add_subplot(111) 
    a.plot([1,2,3,4])
    a.set_ylabel('some numbers')
    return f
def pyplot_simple2():
    f = Figure(figsize=(5,4), dpi=100)
    a = f.add_subplot(111)
    t = np.arange(0.0,2.0,0.01)
    s = 1 + np.sin(2*np.pi*t)
    a.plot(t,s)
    a.set_xlabel('time (s)')
    a.set_ylabel('voltage (mV)')
    a.set_title('About as simple as it gets, folks')
    a.grid(True)
    return f
matplotlib_examples = [
    {'category':'PyPlot', 'title':'Simple1', 'function':pyplot_simple1 },
    {'category':'PyPlot', 'title':'Simple2', 'function':pyplot_simple2 }
]

class MatplotlibExample():
    def __init__(self,category, title, function):
        self.category = category
        self.title = title
        self.function = function

class Category:
    # A class to wrap
    def __init__(self, category):
        self._category = category
        self._data = []

    # Display values for the decade in the tree.
    @property
    def category(self):
        return "{}".format(self._category)

    # Methods required for the data source interface
    def __len__(self):
        return len(self._data)

    def __getitem__(self, index):
        return self._data[index]

    def can_have_children(self):
        return True

class MatplotlibExampleSource(Source):
    def __init__(self, source):
        super().__init__()
        self._categories = []
        for entry in source:
            self.add(entry)

    def __len__(self):
        return len(self._categories)

    def __getitem__(self, index):
        return self._categories[index]

    def add(self, entry):
        category = entry['category']
        print(category)
        try:
            category_root = {
                root.category: root
                for root in self._categories
            }[category]
        except KeyError:
            category_root = Category(category)
            self._categories.append(category_root)
            self._categories.sort(key=lambda v: v.category)
        example = MatplotlibExample(**entry)
        category_root._data.append(example)
        self._notify('insert', parent=category_root, index=len(category_root._data) - 1, item=example)

class ExampleChartApp(toga.App):

    def startup(self):
        # Set up main window
        self.main_window = toga.MainWindow(title=self.name)

        self.left_container = toga.Tree(
            headings=['category','title'], 
            data=MatplotlibExampleSource(matplotlib_examples),
            on_select=self.displayChart
        )

        self.canvas = toga.Canvas(style=Pack(flex=1))
        self.chart = toga.Chart(pyplot_simple1())
        self.chart.draw(pyplot_simple1())
        with self.canvas.stroke() as stroker:
            with stroker.closed_path(50, 50) as closer:
                closer.line_to(100, 100)
                closer.line_to(100, 50)
        self.right_content = toga.Box(
            children=[self.chart],
            #children=[
            #    self.canvas
            #],
            style=Pack(direction=COLUMN, padding_top=50)
        )

        #
        #box = toga.Box(
        #    #children=[chart],
        #    children=[self.canvas],
        #    style=Pack(direction=COLUMN, padding_top=50)
        #)

        self.right_container = toga.ScrollContainer()
        self.right_container.content = self.right_content

        self.split = toga.SplitContainer()
        self.split.content = [self.left_container, self.right_container]
        #self.split.content = [box, self.right_container]

        self.main_window.content = self.split
        self.main_window.show()

    def displayChart(self,widget, node):
        if node and hasattr(node, 'title'):
            print('You selected node: {}'.format(node.title))
            self.chart.draw(node.function())
            #self.split.refresh()
            #self.right_container.
        else:
            print('No row selected')

def main():
    return ExampleChartApp('Chart', 'org.pybee.widgets.chart')


if __name__ == '__main__':
    main().main_loop()
