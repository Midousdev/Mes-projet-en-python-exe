import tkinter as tk
from tkinter import filedialog, messagebox
import zipfile
import rarfile

# Fonction pour décompresser un fichier ZIP
def unzip_file():
    file_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])
    if not file_path:
        return

    destination = filedialog.askdirectory()
    if not destination:
        return

    try:
        with zipfile.ZipFile(file_path, 'r') as zip_ref:
            zip_ref.extractall(destination)
        messagebox.showinfo("Succès", f"Fichier ZIP extrait dans {destination}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'extraction du fichier ZIP : {str(e)}")

# Fonction pour décompresser un fichier RAR
def unrar_file():
    file_path = filedialog.askopenfilename(filetypes=[("RAR Files", "*.rar")])
    if not file_path:
        return

    destination = filedialog.askdirectory()
    if not destination:
        return

    try:
        with rarfile.RarFile(file_path) as rar_ref:
            rar_ref.extractall(destination)
        messagebox.showinfo("Succès", f"Fichier RAR extrait dans {destination}")
    except Exception as e:
        messagebox.showerror("Erreur", f"Erreur lors de l'extraction du fichier RAR : {str(e)}")

# Création de l'interface graphique
root = tk.Tk()
root.title("Décompresseur ZIP et RAR")
root.geometry("300x200")

# Boutons pour décompresser les fichiers ZIP et RAR
unzip_button = tk.Button(root, text="Décompresser ZIP", width=20, command=unzip_file)
unzip_button.pack(pady=20)

unrar_button = tk.Button(root, text="Décompresser RAR", width=20, command=unrar_file)
unrar_button.pack(pady=10)

# Démarrer l'interface graphique
root.mainloop()
