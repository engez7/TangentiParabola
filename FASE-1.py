"""
FASE 1: Rappresentazione del piano cartesiano

Obiettivo: Creare un grafico vuoto con assi cartesiani ben definiti
"""

import matplotlib.pyplot as plt   # Importa pyplot per la creazione di grafici
from matplotlib.ticker import MultipleLocator   # Importa MultipleLocator per impostare i tick degli assi

def configure_axes(ax):
    """
    Configura l'oggetto Axes 'ax' per il disegno del grafico.
    
    Imposta titolo, limiti, tick, spine e aspetto "equal".
    """
    # Imposta il titolo dell'asse a sinistra, con un padding di 10 punti
    ax.set_title("Piano cartesiano", pad=10)
    # Imposta i limiti: asse x e asse y
    ax.set_xlim(-20, 20)
    ax.set_ylim(-5, 10)
    # Disattiva la griglia
    ax.grid(False)
    # Imposta i tick principali ogni 5 unità su entrambi gli assi
    ax.xaxis.set_major_locator(MultipleLocator(5))
    ax.yaxis.set_major_locator(MultipleLocator(5))
    # Riposiziona le spine per far intersecare gli assi all'origine (0,0)
    ax.spines['left'].set_position(('data', 0))   # Spina sinistra a x=0
    ax.spines['right'].set_color('none')            # Nasconde la spina destra
    ax.spines['bottom'].set_position(('data', 0))   # Spina inferiore a y=0
    ax.spines['top'].set_color('none')              # Nasconde la spina superiore
    # Specifica che i tick di x sono sulla spina inferiore e quelli di y sulla sinistra
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    # Imposta l'aspetto "equal" per avere la stessa scala per x e y
    ax.set_aspect('equal', adjustable='box')

if __name__ == "__main__":
    # Creazione della figura e degli assi
    fig, ax = plt.subplots()
    configure_axes(ax)
    plt.show()
