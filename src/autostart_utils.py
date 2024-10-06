import sys
from autostart import add_to_startup, remove_from_startup

def toggle_autostart(state):
    app_path = sys.executable
    app_name = "KeyboardFixer"
    if state:
        add_to_startup(app_name, app_path)
    else:
        remove_from_startup(app_name)