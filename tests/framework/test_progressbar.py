import sys
import os
sys.path.append(os.path.dirname(os.path.join(os.path.dirname(__file__), "../../qtbooty")))

from qtbooty import App
from qtbooty import framework

app = App()


def update():
  pbar.update(update.value)
  update.value += 1

update.value = 0

pbar = framework.ProgressBar()
app.add_widget(pbar)
app.add_timer(100, update)
app.run()
