try:
  import matplotlib
  matplotlib.use("TkAgg")
  from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
  from matplotlib.figure import Figure
except:
  print('Warning: Could not find matplotlib')

try:
  import Tkinter as tk
except ImportError:
  import tkinter as tk

QUICK_UI_METADATA = {
  'font': ('Courier', 14)
}

class QuickUIState:
  def __init__(self, widgets):
    self.application_state = {}
    self.widgets = widgets
  def put_silent(self, key, value):
    self.application_state[key] = value
  def put(self, key, value):
    self.put_silent(key, value)
    for widget in self.widgets:
      widget.update(self.application_state)

class QuickUI:
  def __init__(self, parameters):
    self.parameters = parameters
    self.attached = []
  def __str__(self):
    return '<QuickUI>'
  def display_ui(self):
    root = tk.Tk()
    root.wm_title('QuickUI')
    root.minsize(800,0)
    state = QuickUIState(self.attached)
    for variable in self.parameters.keys():
      control_widget = self.parameters[variable]
      control_widget.do_your_thing(root, variable, state)
    for attached in self.attached:
      attached.init_ui(root)
  def __repr__(self):
    self.display_ui()
    return str(self)
  def show(self, *widgets):
    self.attached = self.attached + list(widgets)
    return self

class InputWidget: pass
class OutputWidget:
  def __init__(self, callback):
    self.callback = callback

class slider(InputWidget):
  def __init__(self, start, end, steps=None):
    self.start = start
    self.end = end
    if steps is None:
      self.steps = 1
    else:
      self.steps = steps
  def do_your_thing(self, root, my_name, state):
    def command(*_):
      state.put(my_name, widget.get())
    widget = tk.Scale( root
                     , from_=self.start
                     , to=self.end
                     , resolution=self.steps
                     , tickinterval=abs(self.start-self.end)
                     , orient=tk.HORIZONTAL
                     , command = command
                     )
    widget.pack(fill=tk.X, expand=1)
    widget.config(**QUICK_UI_METADATA)
    state.put_silent(my_name, self.start)

class label(OutputWidget):
  def init_ui(self, root):
    self.text = tk.StringVar()
    label = tk.Label(root, textvariable = self.text)
    label.config(**QUICK_UI_METADATA)
    label.pack(fill=tk.X, expand=1)
  def update(self, state):
    self.text.set(str(self.callback(**state)))

class plot(OutputWidget):
  def init_ui(self, root):
    self.figure = Figure(figsize=(5,5), dpi=100)
    self.subplot = self.figure.add_subplot(111)
    self.canvas = FigureCanvasTkAgg(self.figure, root)
    self.canvas.show()
    self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
    toolbar = NavigationToolbar2TkAgg(self.canvas, root)
    toolbar.update()
  def update(self, state):
    self.subplot.clear()
    self.subplot.plot(*self.callback(**state))
    self.canvas.show()

def forall(**parameters):
  return QuickUI(parameters)
