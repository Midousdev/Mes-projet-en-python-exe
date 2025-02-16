import tkinter as tk
from tkinter import messagebox
import psutil
import subprocess

class TaskManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestionnaire de tâches")
        self.root.geometry("1000x700")  # Fenêtre encore plus grande
        self.root.config(bg="#1F2A44")  # Fond de l'application

        # Titre de l'application avec un texte personnalisé
        self.title_label = tk.Label(self.root, text="Gestionnaire de tâches by Ahmed", font=("Arial", 20, "bold"), fg="#FFFFFF", bg="#1F2A44")
        self.title_label.pack(pady=20)

        # Champ de recherche
        self.search_label = tk.Label(self.root, text="Rechercher un processus :", font=("Arial", 14), fg="#ECF0F1", bg="#1F2A44")
        self.search_label.pack(pady=10)

        self.search_var = tk.StringVar()  # Variable pour la recherche
        self.search_entry = tk.Entry(self.root, textvariable=self.search_var, font=("Arial", 14), bg="#34495E", fg="#ECF0F1", relief="flat")
        self.search_entry.pack(pady=5, padx=30, fill='x')

        # Liste des tâches
        self.task_listbox = tk.Listbox(self.root, width=100, height=20, font=("Arial", 12), bg="#34495E", fg="#ECF0F1", selectmode=tk.SINGLE, relief="flat")
        self.task_listbox.pack(pady=20)

        # Cadre pour les boutons (ajustement dans un même espace)
        button_frame = tk.Frame(self.root, bg="#1F2A44")
        button_frame.pack(pady=20)

        # Bouton pour rafraîchir la liste des processus
        self.refresh_button = tk.Button(button_frame, text="Rafraîchir", width=20, font=("Arial", 12), bg="#27AE60", fg="white", relief="flat", command=self.refresh_tasks)
        self.refresh_button.pack(side=tk.LEFT, padx=20)

        # Bouton pour tuer un processus
        self.kill_button = tk.Button(button_frame, text="Tuer le processus", width=20, font=("Arial", 12), bg="#E74C3C", fg="white", relief="flat", command=self.kill_process)
        self.kill_button.pack(side=tk.LEFT, padx=20)

        # Bouton pour afficher la fenêtre du processus
        self.show_window_button = tk.Button(button_frame, text="Afficher la fenêtre", width=20, font=("Arial", 12), bg="#F39C12", fg="white", relief="flat", command=self.show_process_window)
        self.show_window_button.pack(side=tk.LEFT, padx=20)

        # Mettre à jour les processus au lancement
        self.refresh_tasks()

        # Lier l'événement de la recherche pour filtrer en temps réel
        self.search_var.trace("w", lambda name, index, mode: self.filter_tasks())

    def refresh_tasks(self):
        """ Rafraîchit la liste des processus en cours """
        self.task_listbox.delete(0, tk.END)  # Effacer la liste actuelle

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                # Ajouter chaque processus à la liste
                self.task_listbox.insert(tk.END, f"{proc.info['pid']} - {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass  # Ignorer les erreurs liées aux processus qui ne sont plus valides

    def filter_tasks(self):
        """ Filtrer les processus en fonction de la recherche """
        search_term = self.search_var.get().lower()  # Termes de recherche en minuscules
        self.task_listbox.delete(0, tk.END)  # Effacer la liste actuelle

        for proc in psutil.process_iter(['pid', 'name']):
            try:
                process_name = proc.info['name'].lower()  # Nom du processus en minuscules
                if search_term in process_name:
                    self.task_listbox.insert(tk.END, f"{proc.info['pid']} - {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass  # Ignorer les erreurs liées aux processus qui ne sont plus valides

    def kill_process(self):
        """ Tuer le processus sélectionné """
        try:
            selected = self.task_listbox.curselection()  # Récupérer la tâche sélectionnée
            if selected:
                process_info = self.task_listbox.get(selected[0])
                pid = int(process_info.split(' - ')[0])  # Extraire le PID
                process = psutil.Process(pid)
                process.terminate()  # Terminer le processus

                messagebox.showinfo("Succès", f"Processus {pid} tué avec succès.")
                self.refresh_tasks()  # Rafraîchir la liste après suppression
            else:
                messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un processus.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la tentative de tuer le processus : {e}")

    def show_process_window(self):
        """ Afficher la fenêtre d'un processus """
        try:
            selected = self.task_listbox.curselection()  # Récupérer la tâche sélectionnée
            if selected:
                process_info = self.task_listbox.get(selected[0])
                pid = int(process_info.split(' - ')[0])  # Extraire le PID
                process = psutil.Process(pid)

                # Vérifier si le processus existe encore avant d'essayer d'ouvrir sa fenêtre
                if process.is_running():
                    try:
                        # Utiliser open_files pour récupérer le chemin du fichier exécutable
                        exe_path = process.exe()  # Tentative pour récupérer le fichier exécutable du processus
                        if exe_path:
                            subprocess.Popen([exe_path])  # Essayer d'ouvrir le fichier exécutable
                            messagebox.showinfo("Fenêtre", f"Ouverture de la fenêtre du processus.")
                        else:
                            messagebox.showwarning("Erreur", "Impossible de trouver l'exécutable du processus.")
                    except psutil.AccessDenied:
                        messagebox.showwarning("Accès refusé", "Accès refusé pour ouvrir ce processus.")
                    except psutil.NoSuchProcess:
                        messagebox.showwarning("Erreur", "Le processus a été terminé avant d'essayer de l'ouvrir.")
                    except Exception as e:
                        messagebox.showerror("Erreur", f"Erreur lors de l'ouverture de la fenêtre : {e}")
                else:
                    messagebox.showwarning("Erreur", "Le processus n'est plus en cours d'exécution.")
            else:
                messagebox.showwarning("Aucune sélection", "Veuillez sélectionner un processus.")
        except psutil.NoSuchProcess:
            messagebox.showwarning("Erreur", "Le processus a été terminé avant d'essayer de l'ouvrir.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'affichage de la fenêtre du processus : {e}")

def main():
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
