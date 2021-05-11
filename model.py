import json

STEVILO_DOVOLJENIH_NAPAK = 10
PRAVILNA_CRKA, PONOVLJENA_CRKA, NAPACNA_CRKA = '+', 'o', '-'
ZMAGA, PORAZ, ZACETEK = 'w', 'x', 's'

class Vislice:
    datoteka_s_stanjem = "stanje.json"

    def __init__(self):
        self.igre = {}
        self.max_id = 0

    def prost_id_igre(self):
        self.max_id +=1
        return self.max_id

    """prost_id_igre_drugace(self):
        m = max(self.igre.keys())
        return m + 1
    """

    def nova_igra(self,):
        nov_id = self.prost_id_igre()
        sveza_igra = nova_igra()

        self.igre[nov_id] = (sveza_igra, ZACETEK)

        return nov_id

    def ugibaj(self, id_igre, crka):
        igra, _ = self.igre[id_igre]

        novo_stanje = igra.ugibaj(crka)

        self.igre[id_igre] = (igra, novo_stanje)

    def nalozi_igre_iz_datoteke(self):
        with open(self.datoteka_s_stanjem, encoding='utf8') as f:
            igre = json.load(f)
        for id_igre in igre:
            geslo = igre[id_igre]['geslo']
            stanje = igre[id_igre]['stanje']
            crke = igre[id_igre]['crke']

            igra = Igra(geslo)
            igra.crke = crke

            self.igre[int(id_igre)] = (igra, stanje)

    def zapisi_igre_v_datoteki(self):
        igre = {}
        for id_igre in self.igre:
            igra, stanje = self.igre[id_igre]
            igra_slovar = {'geslo': igra.geslo, 'crke': igra.crke, 'stanje': stanje}
            igre[id_igre] = igra_slovar
        with open(self.datoteka_s_stanjem, 'w', encoding='utf8') as f:
            json.dump(igre, f)
class Igra:
    def __init__(self, geslo, crke=None):
        self.geslo = geslo
        self.crke = crke or list()

    def napacne_crke(self):
        return [c for c in self.crke if c.upper() not in self.geslo.upper()]

    def pravilne_crke(self):
        return [c for c in self.crke if c.upper() in self.geslo.upper()]

    def stevilo_napak(self):
        return len(self.napacne_crke())

    def poraz(self):
        return self.stevilo_napak() > STEVILO_DOVOLJENIH_NAPAK
    
    def zmaga(self):
        return not self.poraz() and len(self.pravilne_crke()) == len(set(self.geslo))

    def pravilni_del_gesla(self):
        pravilno = ''
        for c in self.geslo.upper():
            if c in self.crke:
                pravilno += c
            else:
                pravilno += '_'
        return pravilno

        # return ''.join([c if c in self.crke else '_' for c in self.geslo.upper()])

    def nepravilni_ugibi(self):
        return ' '.join(self.napacne_crke())

    def ugibaj(self, crka):
        crka = crka.upper()
        if crka in self.crke:
            return PONOVLJENA_CRKA
        elif crka in self.geslo.upper():
            self.crke.append(crka)
            if self.zmaga():
                return ZMAGA
            else: 
                return PRAVILNA_CRKA
        else:
            self.crke.append(crka)
            if self.poraz():
                return PORAZ
            else:
                return NAPACNA_CRKA

with open('besede.txt', encoding='utf-8') as f:
    bazen_besed = f.read().split()

import random

def nova_igra():
    geslo = random.choice(bazen_besed)
    return Igra(geslo)