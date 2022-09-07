import threading
import time
import logging
import rubrica



# Consumatore Thread Class
class Consumatore(threading.Thread):
    def __init__(self, rub, i):
        super().__init__(name="Consumatore"+str(i))
        self.c = rub

    def run(self):

        logger = logging.getLogger()
        syslog = logging.StreamHandler()
        formatter = logging.Formatter('[%(threadName)s] %(asctime)s \n %(message)s')

        syslog.setFormatter(formatter)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(syslog)


        logger.debug(self.c)
        self.c.modifica("gigi", "rossi", 11111111)

        time.sleep(2)

        self.c.cancella("alberto", "alberti")

        time.sleep(2)
        self.c.inserisci("rossano", "rosso", 3478999)
        self.c.modifica("mario romualdo", "rossi", 2222222)
        self.c.inserisci("alberto", "alberti", 3475599)
        time.sleep(2)

        self.c.inserisci("Carlo", "Carli", 3475591)
        self.c.inserisci("ubaldo", "ubaldi", 3475511)

        time.sleep(3)

        self.c.cancella("alberto", "alberti")
        self.c.cancella("ubaldo", "ubaldi")
       #self.c.inserisci("agnese", "maria", 12345)

        time.sleep(1)

        items_produced = 0
        while items_produced < 10:
            self.c.suggerimento()
            items_produced +=1

        logger.debug(self.c.ordina(crescente=False))
        logger.debug(self.c)