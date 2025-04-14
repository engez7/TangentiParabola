import numpy as np                          # Importa NumPy per operazioni numeriche
import matplotlib.pyplot as plt             # Importa pyplot per la creazione di grafici
from matplotlib.animation import FuncAnimation  # Importa FuncAnimation per l'animazione
from matplotlib.widgets import Button, TextBox    # Importa widget interattivi (pulsante e casella di testo)
from matplotlib.ticker import MultipleLocator     # Importa MultipleLocator per impostare i tick degli assi

###############################################################################
# PARAMETRI DI DEFAULT
###############################################################################
a = 1                   # Coefficiente della parabola (formula: y = a x^2)
num_tangenti = 50       # Numero totale di tangenti da disegnare
frequenza_disegno = 1   # Intervallo (in millisecondi) tra i frame dell'animazione

###############################################################################
# VETTORI DI BASE
###############################################################################
# Array di 400 punti equispaziati tra -40 e 40 per l'asse x
x_vals = np.linspace(-20, 20, 100)


###############################################################################
# FUNZIONE DI CONFIGURAZIONE DEGLI ASSI
###############################################################################
def configure_axes(ax):
    """
    Configura l'oggetto Axes 'ax' per il disegno del grafico.
    
    Imposta titolo, limiti, tick, spine e aspetto "equal".
    """
    # Imposta il titolo dell'asse a sinistra, con un padding di 10 punti
    ax.set_title("Envelope of parabola tangent lines", pad=10)
    # Imposta i limiti: asse x da -30 a 30 e asse y da -10 a 20
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

###############################################################################
# FUNZIONE PER CALCOLARE LA TANGENTE
###############################################################################
def tangente(m, x):
    """
    Calcola la retta tangente alla parabola y = a x^2.
    Formula: y = m*x - (m^2)/(4*a)
    
    Parametri:
      - m: coefficiente angolare della tangente
      - x: valore (o array) per l'asse x
      
    Restituisce:
      - I valori di y corrispondenti alla retta tangente
    """
    return m * x - (m**2) / (4 * a)

###############################################################################
# FUNZIONE DI ANIMAZIONE
###############################################################################
def animate(i):
    """
    Funzione chiamata per ogni frame dell'animazione.
    Disegna progressivamente le tangenti alla parabola.
    
    Parametri:
      - i: indice del frame corrente
      
    Restituisce:
      - Una lista vuota (richiesta da FuncAnimation)
    """
    if i < len(m_vals):
        m = m_vals[i]                     # Seleziona il coefficiente angolare corrente
        y_tang = tangente(m, x_vals)        # Calcola i valori della tangente per x_vals
        # Disegna la tangente in rosso, con trasparenza (alpha=0.3) e spessore 0.8
        ax.plot(x_vals, y_tang, color="red", alpha=0.3, linewidth=0.8)
    if i == len(m_vals) - 1:
        # Se 'a' è intero, converte in int per evitare decimali inutili
        a_display = int(a) if a.is_integer() else a
        # Aggiunge il testo con l'equazione della parabola nell'angolo in alto a destra (coordinate normalizzate)
        ax.text(
            0.7, 0.9,                    # Coordinate in ax.transAxes
            f"$y = {a_display}x^2$",       # Testo (usa LaTeX per l'esponente)
            transform=ax.transAxes,       # Specifica che le coordinate sono relative all'asse
            ha='center',                  # Allineamento orizzontale: centro
            va='center',                  # Allineamento verticale: centro
            fontsize=14,                  # Dimensione del font
            color='black',                # Colore del testo
            bbox=dict(facecolor='white', edgecolor='none', pad=5)  # Riquadro bianco attorno al testo
        )
    return []  # Restituisce una lista vuota (necessario per FuncAnimation)

###############################################################################
# FUNZIONE PER AVVIARE L'ANIMAZIONE (EVENTO "DISEGNA")
###############################################################################
def start_animation(event):
    """
    Funzione chiamata al clic del pulsante "Disegna".
    Legge i valori inseriti dall'utente, pulisce il grafico, aggiorna il vettore dei coefficienti
    e avvia l'animazione.
    
    Parametri:
      - event: evento generato dal clic (non usato direttamente)
    """
    global a, num_tangenti, m_vals, ani
    try:
        a = float(textbox_a.text)             # Legge il valore di 'a' dalla TextBox e lo converte in float
        num_tangenti = int(textbox_num.text)    # Legge il numero di tangenti e lo converte in intero
    except ValueError:
        print("Invalid input. Using default values.")
        return

    # Pulisce il grafico: rimuove tutti gli artisti precedenti
    ax.clear()
    # Ripristina la configurazione degli assi con la funzione definita
    configure_axes(ax)
    # Aggiorna il vettore dei coefficienti m: genera 'num_tangenti' valori equispaziati da -10 a 10
    m_vals = np.linspace(-1, 1, num_tangenti)
    # Crea l'animazione:
    #   - fig: la figura su cui animare
    #   - animate: funzione chiamata per ogni frame
    #   - frames: numero totale di frame (uguale a len(m_vals))
    #   - interval: tempo in millisecondi tra i frame
    #   - blit: se True, ridisegna solo le parti modificate (qui False per semplicità)
    #   - repeat: se True, l'animazione si ripete (qui False)
    ani = FuncAnimation(
        fig,
        animate,
        frames=len(m_vals),
        interval=frequenza_disegno,
        blit=False,
        repeat=False
    )
    plt.draw()  # Richiede il ridisegno della figura

###############################################################################
# BLOCCO PRINCIPALE
###############################################################################
if __name__ == "__main__":
    # Creazione della figura e impostazione del titolo della finestra
    fig = plt.figure()
    fig.canvas.manager.set_window_title("Envelope")
    
    # Aggiunge l'area (oggetto Axes) per il grafico; i parametri sono in coordinate normalizzate:
    # [margine sinistro, margine inferiore, larghezza, altezza]
    ax = fig.add_axes([0.1, 0.35, 0.8, 0.6])
    # Configura l'asse con la funzione configure_axes
    configure_axes(ax)
    
    ###############################################################################
    # DISPOSIZIONE DEI CONTROLLI: TEXTBOX E PULSANTE
    ###############################################################################
    # L'idea è quella di mantenere il posizionamento originale:
    # - La TextBox per "Coefficiente a" viene posizionata in [0.35, 0.18, 0.05, 0.05]
    # - La TextBox per "Numero di tangenti" in [0.35, 0.11, 0.05, 0.05]
    # - Il pulsante "Disegna" in [0.375, 0.03, 0.25, 0.08], centrato orizzontalmente.
    
    # Crea la prima TextBox per "Coefficiente a"
    # Le coordinate [0.545, 0.125, 0.05, 0.05] sono in unità normalizzate: [left, bottom, width, height]
    axbox_a = fig.add_axes([0.5, 0.2, 0.05, 0.05])
    textbox_a = TextBox(axbox_a, 'Parabola equation: $y = a x^2$ - Coefficient a: ', initial=str(a), label_pad=0)
    # La label "a:" comparirà nella TextBox (con label_pad=0 per minimizzare lo spazio tra label e campo)

    # Crea la seconda TextBox per "Numero di tangenti"
    axbox_num = fig.add_axes([0.5, 0.14, 0.05, 0.05])
    textbox_num = TextBox(axbox_num, 'Tangent lines number: ', initial=str(num_tangenti), label_pad=0)
        
    axbutton = fig.add_axes([0.375, 0.03, 0.25, 0.08])
    button = Button(axbutton, 'Draw the envelope')
    # Collega il clic del pulsante alla funzione start_animation
    button.on_clicked(lambda event: start_animation(event))
    
    # Visualizza la finestra con il grafico e i widget
    plt.show()

