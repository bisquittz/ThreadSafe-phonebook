import tkinter as tk
from rubrica import *
from Consumatore import *
from Produttore import *
import logging

#creo una classe interfaccia
class GUI:
    def __init__(self, root):
        #assegno al parametro self.root il valore di root che verrà dato successivamente
        self.root = root
        #creo una label con relativo testo
        self.label = tk.Label(text = "Avvia più threads modificando il numero")
        #creo i bottoni che inizieranno e termineranno il processo con relativi colori e parametri
        self.btn1 = tk.Button(text="Start", background="light green", width=20, height=5)
        self.btn2 = tk.Button(text="Quit", background="light blue", width=20, height=5)
        #creo una entry nel quale verrà inserito il numero di avvio, di default 1
        integer = tk.StringVar()
        integer.set(1)
        self.num = tk.Entry(background="pink", width=20, textvariable=(str(integer)))
        #posiziono i bottoni, la entry e la label utilizzando il formato della griglia
        self.btn1.grid(row=0, column=0, padx=5, pady=5)
        self.btn2.grid(row=0, column=1, padx=5, pady=5)
        self.num.grid(row=1, column=1, padx=5, pady=5)
        self.label.grid(row=1, column=0, padx=5, pady=5)
        #collego i bottoni alle relative funzioni con il click
        self.btn1.bind("<Button-1>", self.start)
        self.btn2.bind("<Button-1>", self.quit)

    def start(self, event):
        try:
            #assegno alla variabile n1 il valore della entry self.num
            n1 = self.num.get()
            #rendo il valore di n1 un int
            n = int(n1)
            #creo una lista vuota
            threads = []
            #assegno alla variabile c la classe Rubrica
            c = Rubrica()
            #assegno all'indice il valore di 1
            i = 1
            while i <= n:
                #assegno i parametri ai diversi threads e li assegno alle rispettive variabili "d" ed "e"
                d = Produttore(c, i)
                e = Consumatore(c, i)
                #avvio i threads
                d.start()
                e.start()
                #inserisco le log dei threads all'interno della lista vuota
                threads.append(d)
                threads.append(e)
                #incremento il valore di i
                i += 1
            #eseguo la join su ogni elemento della lista
            for t in threads:
                t.join()
        except Exception:
            print("Il numero minimo di Threads è 1")

    def quit(self, event):
        #creo la funzione che chiude la finestra
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    GUI(root)
    root.mainloop()
