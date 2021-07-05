import bottle
import model

vislice = model.Vislice()
vislice.nalozi_igre_iz_datoteke

@bottle.get("/")

def index():
    return bottle.template("index.tpl")

@bottle.post("/nova_igra/")
def nova_igra():
    id_igre = vislice.nova_igra()
    vislice.zapisi_igre_v_datoteki()
    bottle.response.set_cookie ("id_igre", id_igre, path="/", secret=1812)
    novi_url = f"/igra/"

    bottle.redirect(novi_url)

@bottle.get("/igra/")
def pokazi_igro():
    id_igre = bottle.request.get_cookie("id_igre", secret=1812)
    trenutna_igra, trenutno_stanje = vislice.igre[id_igre]

    return bottle.template("igra.tpl", igra=trenutna_igra, stanje=trenutno_stanje)

@bottle.post("/igra/")
def ugibaj_na_igri():
    print(bottle.request)
    print(bottle.request.forms)
    ugibana = bottle.request.forms["crka"]
    id_igre = bottle.request.get_cookie("id_igre", secret=1812)
    vislice.ugibaj(id_igre, ugibana)

    vislice.zapisi_igre_v_datoteki()

    return bottle.redirect(f"/igra/")

bottle.run(reloader=True, debug=True)