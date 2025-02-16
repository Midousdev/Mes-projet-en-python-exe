import tkinter as tk
from tkinter import messagebox
import pyautogui
import cv2
import numpy as np
import threading
import os
from datetime import datetime

class ScreenRecorderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Application d'Enregistrement d'Écran")

        self.is_recording = False

        self.start_button = tk.Button(self.root, text="Commencer l'Enregistrement", command=self.start_recording)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Arrêter l'Enregistrement", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.quit_button = tk.Button(self.root, text="Quitter", command=self.quit_app)
        self.quit_button.pack(pady=10)

    def start_recording(self):
        self.is_recording = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        self.record_thread = threading.Thread(target=self.record_screen)
        self.record_thread.start()

    def stop_recording(self):
        self.is_recording = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def record_screen(self):
        screen_size = pyautogui.size()
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter(os.path.join(os.path.expanduser('~'), 'Desktop', f'screen_capture_{datetime.now().strftime("%Y%m%d_%H%M%S")}.avi'), fourcc, 20.0, (screen_size.width, screen_size.height))

        while self.is_recording:
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)
        
        out.release()
        cv2.destroyAllWindows()

    def quit_app(self):
        if self.is_recording:
            self.stop_recording()
        self.root.quit()

if __name__ == '__main__':
    root = tk.Tk()
    app = ScreenRecorderApp(root)
    root.mainloop()
