# main.py

import tkinter as tk
from ui.dashboard import NovaProspectDashboard

if __name__ == "__main__":
    root = tk.Tk()
    app = NovaProspectDashboard(root)
    root.mainloop()