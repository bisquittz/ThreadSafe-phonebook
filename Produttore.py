import threading
import time
import logging
import rubrica


class Produttore(threading.Thread):

    def __init__(self, rub, i):
        super().__init__(name="Produttore"+str(i))
        self.c = rub

    def run(self):
        logger = logging.getLogger()
        syslog = logging.StreamHandler()
        formatter = logging.Formatter('[%(threadName)s] %(asctime)s \n %(message)s')

        syslog.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(syslog)
        logger.debug(self.c)
        self.c.inserisci("gigi", "rossi", 3456789)
        self.c.inserisci("Gigi", "rossi", 3456789)
        self.c.inserisci("mario", "rossi", 3478999)

        time.sleep(2)

        self.c.inserisci("mario romualdo", "rossi", 3475599)
        self.c.inserisci("Alberto", "Alberti", 3475599)
        self.c.inserisci("Carlo", "Carli", 3475591)
        self.c.inserisci("Ubaldo", "Ubaldi", 3475511)


        time.sleep(2)
        logger.debug(self.c)

        time.sleep(5)
        logger.debug(self.c)

        items_produced = 0
        while items_produced < 10:

            self.c.suggerisci("Ubaldo_"+str(items_produced), "ubaldi")

            items_produced +=1
        time.sleep(2)
        logger.debug("==========> Produttore: Cerca Ubaldo Ubaldi")
        if(self.c.cerca("Ubaldo", "Ubaldi") == None):
            logger.debug("==========> Produttore: Nome non trovato")
        else:
            logger.debug("==========> Produttore: TROVATO Ubaldo Ubaldi")
            self.c.cancella("ubaldo", "ubaldi")

        time.sleep(2)
        logger.debug(self.c)