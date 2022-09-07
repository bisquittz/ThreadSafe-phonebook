# Assegnamento 2  aa 2021-22 622AA modulo programmazione 9 crediti
# Gruppo: 2 persone
# Nome: Giorgia, Andrea
# Cognome : D'Antoni, Vitiello
# Matricola : 620020, 517059
# email: g.dantoni@studenti.unipi.it , a.vitiello5@studenti.unipi.it
# telefono: 3294742243, 3297737198
import random
from threading import Condition
from queue import Queue
queue = Queue(maxsize=3)
cond = Condition()


class Rubrica:
    """ Costruttore: crea una rubrica vuota rappresentata come
        dizionario di contatti vuoto """

    def __init__(self):
        """ crea una nuova rubrica vuota """
        self.rub = {}

    def __str__(self):
        """ Serializza una rubrica attraverso una stringa
        con opportuna codifica (a scelta dello studente) """
        # attraverso un ciclo  for scorro gli elementi della lista
        # e li codifico in modo che risulti sottoforma di stringa come key : value
        listastringa = ""
        for key, value in (self.rub.items()):
            listastringa += str(key) + ":" + str(self.rub[key]) + "\n"
        return listastringa

    def __eq__(self, r):
        """stabilisce se due rubriche contengono
        esattamente le stesse chiavi con gli stessi dati"""
        # eseguo un ciclo for su entrambi i diozionari in modo da trasformare tutti i valori in interi e e renderli uguali
        for key, value in self.rub.items():
            (self.rub[key]) = int(self.rub[key])
        for key, value in r.rub.items():
            (r.rub[key]) = int(r.rub[key])

        # si utilizza l'operatore di uguaglianza per vedere se il contenuto è lo stesso
        # e non se puntano alla stessa memoria(in quel caso di utilizzerebbe is)
        if self.rub == r.rub:
            return True
        else:
            return False

    def __add__(self, r):
        """crea una nuova rubrica unendone due (elimina i duplicati)
        e la restituisce come risultato --
        se ci sono contatti con la stessa chiave nelle due rubriche
        ne riporta uno solo """
        # creo una nuova rubrica
        nuovaRubrica = Rubrica()
        cond.acquire()
        # assegno al suo dizionario la somma dei dizionari senza doppioni di chiavi
        # quando non ci sono gli stessi contatti in r e sel esegui il push degli elementi all interno della nuova rubrica
        nuovaRubrica.rub = {} if any(
            self.rub[contatti] != r.rub[contatti] for contatti in self.rub.keys() & r.rub) else {**self.rub, **r.rub}

        cond.release()
        return nuovaRubrica
        # se i dizionari self.rub e r.rub sono uguali mi forza il push all'interno delle chiavi ricordiamoci che else pusha lo stesso i dati all internno eliminando i dati con stesse chivai

    def load(self, nomefile):
        """ carica da file una rubrica eliminando il
        precedente contenuto di self """
        # rimuovo il contenuto di self
        self.rub.clear()
        # apro e leggo ("r") un nuovo file
        infile = open((nomefile), "r")
        # lo divido per linee
        lines = infile.readlines()
        # per ogni riga divido i suoi "elementi" ogni volta che si incontra il segno ":"
        # (come formattato in store)
        for i in lines:
            items = i.split(":")
            # assegno ogni items che si è creato ad una variabile
            # assegno alla key entrambi le variabili di nome e cognome
            nome = (items[0])
            cognome = (items[1])
            key = (nome, cognome)
            # assegno a value l'ultimo elemento
            value = items[2]
            self.rub[key] = value

        infile.close()

    def inserisci(self, nome, cognome, dati):
        """ inserisce un nuovo contatto con chiave (nome,cognome)
        restituisce "True" se l'inserimento è andato a buon fine e "False"
        altrimenti (es chiave replicata) -- case insensitive """
        # creo una variabile keyins in cui inserisco il parametro nome e cognome(.lower poichè sennò
        # la seconda riga del test la inserisce comunque)
        global cond
        cond.acquire()
        keyins = (nome.lower(), cognome.lower())

        # controllo se keyins è già presente in self.rub
        if keyins in self.rub:
            cond.release()
            return False
        else:
            # se non lo è aggiungo la nuova chiave e il nuovo valore(dati)
            self.rub[keyins] = dati
            cond.notify_all()
            cond.release()
            return True

    def modifica(self, nome, cognome, newdati):
        """ modifica i dati relativi al contatto con chiave (nome,cognome)
        sostituendole con "newdati" -- restituisce "True" se la modifica
        è stata effettuata e "False" altrimenti (es: la chiave non è presente )"""
        # assegno i parametri nome e cognome alla variabile key_to_look
        global cond
        cond.acquire()

        key = (nome, cognome)
        key_to_look = (nome, cognome)
        # controllo che sia presente una chiave uguale alla mia variabile key_to_look
        if key == key_to_look:
            # se esiste assegno a quella chiave un nuovo valore(newdati)
            self.rub[key] = newdati
            cond.notify_all()
            cond.release()
            return True
        cond.notify_all()
        cond.release()
        return False

    def cancella(self, nome, cognome):
        """ il contatto con chiave (nome,cognome) esiste lo elimina
        insieme ai dati relativi e restituisce True -- altrimenti
        restituisce False """
        # assegno ad una variabile key_to_delete i parametri nome e cognome
        global cond
        cond.acquire()

        key = (nome, cognome)
        key_to_delete = (nome, cognome)
        # controllo se in self.rub è presente una chiave uguale a key_to_delete
        while key in self.rub:
            if key == key_to_delete:
                # se è presente la elimino
                self.rub.pop(key)
            cond.notify_all()
            cond.release()
            return True

        cond.notify_all()
        cond.release()
        return False

    def cerca(self, nome, cognome):
        """ restitusce i dati del contatto se la chiave e' presente
        nella rubrica e "None" altrimenti -- case insensitive """
        # assegno ad una variabile key_to_search i parametri nome e cognome
        global cond
        cond.acquire()
        key_to_search = (nome, cognome)
        key = (nome, cognome)
        # controllo se in self.rub è presente una chiave uguale a key_to_search
        while key in self.rub:
            if key == key_to_search:
                # se è presente ne ritorno il suo valore
                cond.notify_all()
                cond.release()
                return (self.rub[key])
        cond.notify_all()
        cond.release()
        return None

    def store(self, nomefile):
        """ salva su file il contenuto della rubrica secondo
        un opportuno formato (a scelta dello studente)"""
        # il formato da me scelto
        # prevede un contatto per linea
        # nome:cognome:telefono\n
        # apro in scrittura un file
        # ogni chiave/valore presente in self.rub lo riscrivo con la formattazione da me scelta
        # apro un file in cui scrivere (w)
        oout = open(nomefile, "w")
        # creo una stringa vuota dove inserire il contenuto formattato
        stri = ""
        # eseguo un ciclo for sugli items di self.rub e ne aggiungo i vari elementi alla stringa
        for key, value in self.rub.items():
            stri += str(key[0]) + ":" + str(key[1]) + ":" + str(self.rub[key]) + "\n"
        # scrivo nel file di output il contenuto di stri
        oout.write(stri)
        oout.close()

    def ordina(self, crescente=True):
        # creo una lista vuota di stringhe
        # assegno ogni chiave/valore in self.rub alla lista con l'adeguata formattazione
        global cond
        cond.acquire()
        try:
            stringa = ""
            mega_list = []  # lista vuota che contine tutto il mio dizionario
            for d, values in self.rub.items():  # per ogni chiave e valore contenuto in self.rub prendimi le chiavi in una sequenza senza punti e o altro
                keys = str(d).replace('(', '').replace(')', '').replace('\'', '').split(
                    ',')  # rimpiazzo e divido le mie chiavi eliminando tutto quello che non mi serve
                temp = keys[0]  # creo una variabile temporanea dove salvare la chiave al posto 0
                keys[0] = keys[1]  # inverto le chiavi nome cognome cognome nome
                keys[1] = temp  # a tempo gli diamo la chiave con posto 1 ora
                keys.append(values)  # aggiungo alle chiavi i loro valori
                mega_list.append(keys)  # creo una lista con i dati sopra
            mega_list = sorted(mega_list)  # metto in ordine la lista
            if not crescente:  # se non crescente
                mega_list.reverse()  # trucchetto .reverse mi mette in ordine contrario al primo (crescente) la lista
            for e in mega_list:
                stringa += f"{e[0]} {e[1]} {str(e[2])} \n"  # seleziono il formato in cui vedere i miei dati :) fine!
        finally:
            cond.notify()
            cond.release()
        return stringa  # ritorna la stringa

    def suggerisci(self, nome, cognome):
        """Il metodo suggerisci viene invocato da un thread per
        effettuare un suggerimento di un contatto nella rubrica.
        Prende come parametro il nome ed il cognome del contatto e
        lo inserisce in una coda (di lunghezza massima 3).
        Non si puo' inserire un elemento nella coda se la coda e' piena.
        """
        #richiamo le variabili globali
        global queue
        global cond
        #genero un numero random da assegnare come parametro al metodo inserisci
        num = random.randint(1023, 456782)
        key = (nome, cognome)
        #assegno i parametri
        self.inserisci(nome, cognome, num)
        cond.acquire()
        try:
            #se la coda è piena attendo
            while queue.full():
                cond.wait(4)
            #inserisco la chiave nella coda se libera
            queue.put(key)
        finally:
            #risveglio e rilascio
            cond.notify()
            cond.release()

    def suggerimento(self):
        """Il metodo suggerimento viene invocato da un thread per
        ottenere un suggerimento recuperato dalla rubrica.
        Il thread legge gli elementi presenti in una coda
        di lunghezza 3. Se la coda è vuota, attende l'inserimento di
        un elemento, altrimenti prende il primo elemento della
        coda e lo stampa.
                global queue
        global cond
        cond.acquire()
        while queue.empty():
            cond.wait()
        queue.get()
        cond.notify_all()
        cond.release()
        time.sleep(random.random())"""
        #richiamo le variabili globali
        global queue
        global cond
        cond.acquire()
        try:
            #se la coda è vuota attendo e stampo
            while queue.empty():
                cond.wait(4)
            #se sono presenti elementi nella coda li prendo
            queue.get()
        finally:
            #risveglio e rilascio
            cond.notify_all()
            cond.release()






