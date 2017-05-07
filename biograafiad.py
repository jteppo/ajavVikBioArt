#!/usr/bin/env python

# Autor - Jaan Teppo
import string,os,re,shutil,sys
from korrastaUnicode import korrastaUnicode

# Skript biograafiate tõstmiseks sisendkaustast uude kausta nimega biograafiad
# Skript on mõeldud töö alustamiseks tekstifailist "Biograafiad.txt", mis peaks
# asuma etteantud kaustas p. Skript töötab rekursiivselt läbi linkidena mainitud
# failid sisendkaustast.
def findBio(s,p,u):
    path = p # Määrame tee kaustani
    faililist = os.listdir(path) # Koostame listi kaustas asuvatest failidest
    #List mittebiograafiatest, mis olid sattunud biograafiate loendite alla.
    ignore = ["Õpetatud Eesti Selts","Tallinna Tehnikaülikool","Nobeli füüsikaauhind","Nobeli meditsiiniauhind","Frankism","Laos","Luure Keskagentuur","Ameerika Riikide Konföderatsioon","Suurbritannia",
              "Venemaa","Eesti NSV Riikliku Julgeoleku Komitee","Keenia","Parkinsoni seadus","Lordi","Trooja","Kaitsepolitsei","Polkovnik",
              "Eestimaa kubermang","Ameerika Ühendriigid","1247","1475","1521","Kanada","924","4. sajand","5. sajand","1808","1821","1875","1889","1906","1932","1947","1930","1932","1947","1958","1981"]
    # Kui sisendkaustas ei leidu kausta nimega biograafiad, kuhu hakatakse
    # biograafiaid liigutama, siis luuakse see kaust
    #if not os.path.exists('./biograafiad'):
    #   os.makedirs('./biograafiad')
    # Kui sisendstring sisaldab stringi Biograafiad ja selline fail on kaustas olemas
    if ("Biograafiad" in s) and ((s+".txt") in faililist):
        # Loeme failist kogu teksti
        with open(path+s+".txt",encoding='utf8', mode='r+') as f:
            text = f.read()
        # Kasutame regexit, et leida failist kõik sisemised lingid
        regintlink = re.compile(r'"internal_links": \[.*?\]',re.DOTALL)
        intlinks = regintlink.findall(text)
        # Kasutame regexit, et leida linkide(meie kaustas failide) tiitlid
        regtitle = re.compile(r'"title":.*,')
        # Vaatame ükshaaval läbi kõik leitud sisemised lingid
        läbitud = []
        for l in intlinks:
            # Otsime igast tiitlid
            titles = regtitle.findall(l)
            for i in titles:
                # Asendame töötluse käigus tekkinud märgenduse, et tiitlist jääks
                # alles vaid lingi(faili) nimi/tiitel
                title = re.sub('("title": |["(),])','',i)
                # Kuna tekstis on sees veel unicode'i kodeering, siis tuleb need
                # asendada vastavate märkidega, selleks kasutame meetodit korrasta-
                # Unicode failist korrastaUnicode.py
                title = korrastaUnicode(title)
                # lisame tiitlile .txt, et võrrelda seda kaustas asuvate failidega
                # ja kui selline fail leidub kaustas , siis see ümber tõsta kausta
                # biograafiad
                nimi = title + '.txt'
                if nimi in faililist:
                    # Kui tiitel sisaldab Biograafiad, siis tuleb uuesti välja
                    # kutsuda antud funktsioon vastava parameetriga
                    if "Biograafiad" in title:
                        findBio(title,p,u)
                        läbitud.append(title)
                    # Vastasel juhul on tegemist biograafiaga, mis tuleb liigutada
                    # kausta biograafiad
                    else:
                        # Kuna osad tiitlid esinevad rohkem kui korra, siis
                        # võib juhtuda olukord, kus fail on juba liigutada
                        # sellisel juhul püüame erandi ja ei tee midagi
                        if nimi[:-4] not in ignore:
                            try:
                                shutil.move(path+nimi,u)
                            except shutil.Error:
                                pass
        # Kuna osades Biograafiate failides on lisatähistega
        # lingid valesti märgendatud, siis igaks juhuks lisame
        # lisatingimuse, et vaadata ka läbi ka populaarsemate lisa-
        # tähtedega esinemisi(Näiteks Biograafiad Ta vms.)
        for a in ['a','b','l','n','c','t','e','o','u','i']:
                            if ((s+a not in läbitud) and (s + a + ".txt" in faililist)):
                                findBio(s+a,p,u)

# Loome main meetodi, et saaks skripti jooksutada käsurealt andes esimseks
# parameetriks töödeldava kausta (kust otsitakse biograafiad, peab sisaldama
# faili Biograafiad.txt ) ja teiseks kausta kuhu soovitakse biograafiad liigutada
# ( Näiteks python biograafiad.py ./corp/ ./biograafiad/ ). 
if __name__ == "__main__":
    try:
        p = sys.argv[1]
        u = sys.argv[2]
    except IndexError:
        print("Lugeda kasutusjuhendit biograafiad_juhend.txt")
        sys.stderr.write(about)
        sys.exit(-1)
    if not os.path.exists(p):
        print("Esimese parameetrina etteantud kausta ei leitud")
        sys.exit(-1)
    # Kui kausta kuhu soovitakse liigutada biograafiad ei eksisteeri, siis see luuakse
    if not os.path.exists(p):
        print("Teise parameetrina etteantud kausta ei leitud")
        sys.exit(-1)
    print("Alustan biograafiate liigutamist sisendkaustast: "+ p + " kausta: " + u)
    findBio("Biograafiad",p,u)
    print("Biograafiad liigutatud kausta: "+p+", töö lõpp")
    sys.exit(-1)

