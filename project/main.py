import tkinter as tk
from gui import InventoryGUI

def main():
    root = tk.Tk()
    app = InventoryGUI(root)
    root.geometry("800x600")
    root.mainloop()

if __name__ == "__main__":
    main()

print("Main module loaded successfully.")