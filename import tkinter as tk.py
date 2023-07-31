import tkinter as tk
import threading

class GUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("GUI")
        self.label = tk.Label(self, text="Initial text")
        self.label.pack()

    def update_gui(self, new_text):
        # This function is called by the thread to update the GUI label
        self.label.configure(text=new_text)

    def start_thread(self):
        # This function starts the thread that updates the GUI label
        thread = threading.Thread(target=self.thread_function)
        thread.start()

    def thread_function(self):
        # This is the function that runs in a separate thread and updates the GUI label
        new_text = "New text"
        self.after(0, self.update_gui, new_text)

if __name__ == "__main__":
    gui = GUI()
    gui.start_thread()
    gui.mainloop()