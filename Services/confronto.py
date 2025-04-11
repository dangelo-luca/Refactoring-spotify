import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

def __init__(self, root):
        self.root = root
        self.root.title("Seleziona Playlist")
        
        # Variabili per salvare gli ID delle playlist
        self.playlist1_id = None
        self.playlist2_id = None

        # Etichetta e pulsanti per la prima playlist
        self.label1 = tk.Label(root, text="Playlist 1:")
        self.label1.pack(pady=5)
        self.button1 = tk.Button(root, text="Seleziona Playlist 1", command=self.seleziona_playlist1)
        self.button1.pack(pady=5)

        # Etichetta e pulsanti per la seconda playlist
        self.label2 = tk.Label(root, text="Playlist 2:")
        self.label2.pack(pady=5)
        self.button2 = tk.Button(root, text="Seleziona Playlist 2", command=self.seleziona_playlist2)
        self.button2.pack(pady=5)

        # Pulsante per confermare la selezione
        self.confirm_button = tk.Button(root, text="Confronta Playlist", command=self.confronta_playlist)
        self.confirm_button.pack(pady=20)

def seleziona_playlist1(self):
        # Simula la selezione dell'ID della playlist 1
        self.playlist1_id = "playlist1.txt"  # Sostituisci con la logica per selezionare l'ID
        messagebox.showinfo("Playlist 1", f"Playlist 1 selezionata: {self.playlist1_id}")

def seleziona_playlist2(self):
        # Simula la selezione dell'ID della playlist 2
        self.playlist2_id = "playlist2.txt"  # Sostituisci con la logica per selezionare l'ID
        messagebox.showinfo("Playlist 2", f"Playlist 2 selezionata: {self.playlist2_id}")

def confronta_playlist(self):
        if not self.playlist1_id or not self.playlist2_id:
            messagebox.showerror("Errore", "Seleziona entrambe le playlist prima di continuare.")
            return

        # Carica le playlist dai file
        playlist1 = self.carica_playlist(self.playlist1_id)
        playlist2 = self.carica_playlist(self.playlist2_id)

        if playlist1 and playlist2:
            # Confronta le playlist
            risultati = self.confronta_playlist_logic(playlist1, playlist2)
            # Mostra i risultati
            messagebox.showinfo("Risultati", f"Brani in comune: {len(risultati['brani_comuni'])}\n"
                                             f"Percentuale di somiglianza: {risultati['percentuale_somiglianza']:.2f}%")
            # Genera il grafico
            self.genera_grafico(risultati)
        else:
            messagebox.showerror("Errore", "Errore nel caricamento delle playlist.")

def carica_playlist(self, percorso_file):
        """
        Carica una playlist da un file di testo. Ogni riga rappresenta un brano.
        """
        try:
            with open(percorso_file, 'r') as file:
                return [line.strip() for line in file.readlines()]
        except FileNotFoundError:
            messagebox.showerror("Errore", f"Il file '{percorso_file}' non è stato trovato.")
            return []

def confronta_playlist_logic(self, playlist1, playlist2):
        """
        Confronta due playlist, identifica i brani comuni e calcola la percentuale di somiglianza.
        """
        set1 = set(playlist1)
        set2 = set(playlist2)
        brani_comuni = set1.intersection(set2)

        totale_minore = min(len(playlist1), len(playlist2))
        percentuale_somiglianza = (len(brani_comuni) / totale_minore) * 100 if totale_minore > 0 else 0

        return {
            "brani_comuni": list(brani_comuni),
            "percentuale_somiglianza": percentuale_somiglianza,
            "totale_playlist1": len(playlist1),
            "totale_playlist2": len(playlist2),
            "totale_comuni": len(brani_comuni)
        }

def genera_grafico(self, dati):
        """
        Genera un grafico che mostra il numero totale di brani in ciascuna playlist,
        il numero di brani in comune e la percentuale di somiglianza.
        """
        labels = ['Playlist 1', 'Playlist 2', 'Brani Comuni']
        valori = [dati["totale_playlist1"], dati["totale_playlist2"], dati["totale_comuni"]]

        plt.bar(labels, valori, color=['blue', 'green', 'orange'])
        plt.title(f"Somiglianza tra Playlist ({dati['percentuale_somiglianza']:.2f}%)")
        plt.ylabel("Numero di Brani")
        plt.show()


    