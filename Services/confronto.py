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
            return [
                {
                    "nome": line.split(" - ")[0].strip(),
                    "artista": line.split(" - ")[1].strip(),
                    "popolarita": int(line.split(" - ")[2].strip()),
                    "genere": line.split(" - ")[3].strip() if len(line.split(" - ")) > 3 else "Sconosciuto"
                }
                for line in file.readlines()
            ]
    except FileNotFoundError:
        messagebox.showerror("Errore", f"Il file '{percorso_file}' non è stato trovato.")
        return []

def confronta_playlist_logic(self, playlist1, playlist2):
        """
        Confronta due playlist, identifica i brani comuni, calcola la percentuale di somiglianza,
        analizza gli artisti in comune e confronta i generi musicali.
        """
        set1 = set(playlist1)
        set2 = set(playlist2)
        brani_comuni = set1.intersection(set2)

        totale_minore = min(len(playlist1), len(playlist2))
        percentuale_somiglianza = (len(brani_comuni) / totale_minore) * 100 if totale_minore > 0 else 0

        # Calcola la frequenza degli artisti in ciascuna playlist
        artisti_playlist1 = [brano['artista'] for brano in playlist1 if 'artista' in brano]
        artisti_playlist2 = [brano['artista'] for brano in playlist2 if 'artista' in brano]

        artisti_comuni = set(artisti_playlist1).intersection(set(artisti_playlist2))
        frequenza_artisti = {
            artista: {
                "playlist1": artisti_playlist1.count(artista),
                "playlist2": artisti_playlist2.count(artista)
            }
            for artista in artisti_comuni
        }

        # Calcola la frequenza dei generi musicali
        generi_playlist1 = [brano.get('genere', 'Sconosciuto') for brano in playlist1 if 'genere' in brano]
        generi_playlist2 = [brano.get('genere', 'Sconosciuto') for brano in playlist2 if 'genere' in brano]

        frequenza_generi = {}
        for genere in set(generi_playlist1 + generi_playlist2):
            frequenza_generi[genere] = {
                "playlist1": generi_playlist1.count(genere),
                "playlist2": generi_playlist2.count(genere)
            }

        popolarita_plapist1 = [brano['popolarita'] for brano in playlist1 if 'popolarita' in brano]
        popolarita_plapist2 = [brano['popolarita'] for brano in playlist2 if 'popolarita' in brano]

        media_popolarita1 = sum(popolarita_plapist1) / len(popolarita_plapist1) if popolarita_plapist1 else 0
        media_popolarita2 = sum(popolarita_plapist2) / len(popolarita_plapist2) if popolarita_plapist2 else 0

        return {
            "brani_comuni": list(brani_comuni),
            "percentuale_somiglianza": percentuale_somiglianza,
            "totale_playlist1": len(playlist1),
            "totale_playlist2": len(playlist2),
            "totale_comuni": len(brani_comuni),
            "media_popolarita1": media_popolarita1,
            "media_popolarita2": media_popolarita2,
            "frequenza_artisti": frequenza_artisti,
            "frequenza_generi": frequenza_generi
        }

def genera_grafico(self, dati):
    """
    Genera grafici per visualizzare i dati di confronto tra le playlist.
    """
    labels = ['Playlist 1', 'Playlist 2', 'Brani Comuni']
    valori = [dati["totale_playlist1"], dati["totale_playlist2"], dati["totale_comuni"]]

    plt.figure(figsize=(15, 10))

    # Grafico 1: Numero di brani
    plt.subplot(2, 2, 1)
    plt.bar(labels, valori, color=['blue', 'green', 'orange'])
    plt.title(f"Somiglianza tra Playlist ({dati['percentuale_somiglianza']:.2f}%)")
    plt.ylabel("Numero di Brani")

    # Grafico 2: Popolarità media
    labels_popolarita = ['Playlist 1', 'Playlist 2']
    valori_popolarita = [dati["media_popolarita1"], dati["media_popolarita2"]]
    plt.subplot(2, 2, 2)
    plt.bar(labels_popolarita, valori_popolarita, color=['blue', 'green'])
    plt.title("Popolarità Media")

    # Grafico 3: Artisti in comune
    artisti = list(dati["frequenza_artisti"].keys())
    frequenze_playlist1 = [dati["frequenza_artisti"][artista]["playlist1"] for artista in artisti]
    frequenze_playlist2 = [dati["frequenza_artisti"][artista]["playlist2"] for artista in artisti]

    x = range(len(artisti))
    plt.subplot(2, 2, 3)
    plt.bar(x, frequenze_playlist1, width=0.4, label='Playlist 1', color='blue', align='center')
    plt.bar(x, frequenze_playlist2, width=0.4, label='Playlist 2', color='green', align='edge')
    plt.xticks(x, artisti, rotation=45, ha='right')
    plt.title("Artisti in Comune e Frequenza")
    plt.ylabel("Frequenza")
    plt.legend()

    # Grafico 4: Distribuzione dei generi
    generi = list(dati["frequenza_generi"].keys())
    frequenze_generi1 = [dati["frequenza_generi"][genere]["playlist1"] for genere in generi]
    frequenze_generi2 = [dati["frequenza_generi"][genere]["playlist2"] for genere in generi]

    x = range(len(generi))
    plt.subplot(2, 2, 4)
    plt.bar(x, frequenze_generi1, width=0.4, label='Playlist 1', color='blue', align='center')
    plt.bar(x, frequenze_generi2, width=0.4, label='Playlist 2', color='green', align='edge')
    plt.xticks(x, generi, rotation=45, ha='right')
    plt.title("Distribuzione dei Generi Musicali")
    plt.ylabel("Frequenza")
    plt.legend()

    plt.tight_layout()
    plt.show()


