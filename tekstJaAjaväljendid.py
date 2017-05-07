#!/usr/bin/env python
# Autor - Jaan Teppo

# Skript eraldamaks Vikipeedia biograafiatest sünni- ja surma-aastad,
# teksti, märgendamaks tekstil ajaväljendid ja kirjutama tulemused
# eraldi failidesse kasutades Python'i moodulit pickle.
# Enne skripti kasutamist peaks biograafiad.py skripti abil olema moodustatud
# kaust, mis sisaldab Vikipeedia biograafilisi artikleid .TXT failidena.

import os,re,sys,pickle
from estnltk import Text
from pprint import pprint
from collections import defaultdict
from korrastaUnicode import korrastaUnicode
from estnltk.timex import TimexTagger


# Funktsioon eraldamaks etteantud artiklist sünni- ja surma-aasta.
# Teise parameetrina on toodud tagger, sest sünni- ja surma-aastad
# märgendatakse reeglifailiga, mis on laiendatud ka kõigile 1900 väiksematele
# aastaarvudele.
def sünniJaSurmaaasta(fail,tagger):
    sünd = "0"
    surm = "0"
    mytimextagger = tagger
    # Loeme sisse kogu faili sisu.
    with open(fail,encoding='utf8', mode='r+') as f:
        kogutext = f.read()
        kogutext = korrastaUnicode(kogutext)
    # Kasutades regex'it määrame otsitavaks osaks kategooriate loendi
    regcategories = re.compile(r'"categories": \[.*?\]',re.DOTALL)
    # Otsime kõik kategooriad
    categories = regcategories.findall(kogutext)
    # Kui leidub kategooriaid
    if (len(categories)>0):
        # Eraldame kõik kategooriad
        categories = categories[0].split("\n")
    else:
        categories = []
    # Vaatame ükshaaval kõik kategooriad läbi
    for c in categories:
        # Kui kategooria nimega sündinud
        if ("sündinud" in c.lower()):
            # Anname kategooria teksti osa EstNLTK Text klassi sisendiks, määrates ka ajaväljendite märgendaja
            textsünd = Text(c,timex_tagger = mytimextagger)
            # Märgendame ajaväljendid
            ajavsünd = textsünd.timexes
            # Kui leidub ajaväljendeid
            if (len(ajavsünd)>0):
                # Määrame sünniaastaks leiduva ajaväljendi
                sünd = ajavsünd[0]["value"]
                # 1. sajandi puhul väärtuseks 00, lisame sellele "1-99"'ga
                if(sünd =="00"):
                    sünd = sünd + "1-"+sünd+"99"
                # Kui ajaväljend määratud .ndatel vms. laiendusega, siis väärtuse osale lisame juurde "1-"+sünniväärtus uuesti+"9" 
                elif("text" in ajavsünd[0].keys() and "ndat" in ajavsünd[0]["text"]):
                    sünd = sünd+"1-"+sünd+"9"
                # Sarnaselt sajandi laiendusega on väärtuses vaid sajandi arv, et peab lisama lisaosa, et näiteks 10. sajand ei määrataks väärtusega 9
                elif("text" in ajavsünd[0].keys() and "sajand" in ajavsünd[0]["text"]):
                    # Kui sajandi laiendusel kaasas ja aasta, ehk näiteks 10. sajandi 30-ndad aastad, siis lisada vaja vaid viimane aasta number
                    if("aasta" in ajavsünd[0]["text"]):
                        sünd = sünd + "1-"+sünd+"9"
                    # Kui mitte, siis vaja lisada kaks viimast
                    else:   
                        sünd = sünd+"01-"+sünd+"99"
        # Samasugune tegevuskäik ka surnud kategooria peal
        if ("surnud" in c.lower()):
            textsurn = Text(c,timex_tagger = mytimextagger)
            ajavsurn = textsurn.timexes
            if (len(ajavsurn)>0):
                surm = ajavsurn[0]["value"]
                if(surm =="00"):
                    surm = surm + "1-"+surm+"99"
                elif("text" in ajavsurn[0].keys() and "ndat" in ajavsurn[0]["text"]):
                    surm = surm+"1-"+surm+"9"
                elif("text" in ajavsurn[0].keys() and "sajand" in ajavsurn[0]["text"]):
                    if("aasta" in ajavsurn[0]["text"]):
                        surm = surm + "1-"+surm+"9"
                    else:   
                        surm = surm+"01-"+surm+"99"
    # Tagastame sünni- ja surma-aasta
    return (sünd,surm)

# Lihtne funktsioon, mis kontrollib kas string'i saab int'iks muuta.
# Näidisena kasutatud http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float-in-python (Vaadatud 03.05.2017)
def onNumber(value):
    try:
        # Kuna tegemist on ajaväljendite "value"'dega, millest vaja on vaid esimest osa enne sidekriipsu ehk enamasti aasta osa, siis eraldame selle osa ja eemaldame ka eKr tähise
        int(value.split("-")[0].replace("BC",""))
        # Kui toimib, siis saab
        return True
    except ValueError:
        # Kui ei toimi, siis ei saa
        return False


# Lihtne funktsioon muutmaks sisendina antud stringi numbriks
def stringNumbriks(s):
    # Kontrollime, kas muutmine on võimalik
    if(onNumber(s)== False):
        # Kui ei, siis tagastame 0
        return 0
    else:
        # Kui jah, siis tagastame numbri
        return int(s.split("-")[0].replace("BC",""))

# Lihtne funktsioon, mis regex'i abil leiab teksti seest osa "start":
def otsiStart(s):
    regstart = re.compile(r'"start": [0-9]+')
    start = regstart.findall(s)
    if(len(start)>0):
        start = start[0]
        start = start.replace('"start": ',"")
        return stringNumbriks(start)
    return 0

# Funktsioon esimese argumendina etteantud loendi kirjutamiseks teise argumendina antud kausta  
# Näidisena kasutatud https://docs.python.org/3/library/pickle.html (Vaadatud 03.05.2017)
def andmedFaili(l,path):
    # Loendi esimesel kohal artikli nimi, lisame sellele .txt , et loodakse tekstifail
    s = l[0] + ".txt"
    # Kirjutame loendi faili, kasutades Pythoni pickle moodulit.
    with open(path+s,'wb') as f:
        pickle.dump(l,f)
        
# Funktsioon andmete lugemiseks failist kasutades Pythoni moodulit pickle.
def andmedFailist(fnimi):
    with open(fnimi, 'rb') as f:
        l = pickle.load(f)
    return l

# Funktsioon kirjutamaks kogu biograafiate andmete loendid etteantud kausta
def andmedFailidesse(kogubiolist,path):
    # Üks haaval kirjutame faili kasutades funktsiooni andmedFaili
    for i in kogubiolist:
        andmedFaili(i,path)


# Esmalt loome funktsiooni kogu artikli tekstiosa lugemiseks failist
def koguTekstFailist(fail):
    result = ""
    with open(fail,encoding='utf8', mode='r+') as f:
        for line in f:
            # Kuna iga fail järgib samasugust joondust saame teksti kätte vaadates
            # iga rida ükshaaval ja valides tööks rea mis algab nelja tühiku ja
            # stringiga "text":
            if line.startswith('    "text":'):
                # eemaldame tühikud algusest ja lõpust
                line = line.strip()
                # eemaldame ebavajaliku tähistuse ("text": ")
                line = line[9:-1]
                # Asendame unicodei kodeeringud vastavate märgenditega
                line = korrastaUnicode(line)
                result = result + line
    # tagastame tulemusstringi, kuhu on juurde liidetud leitud tekstide stringid
    return " ".join(filter(None,result.split("\\n")))

# Seejärel funktsioon, mis artikli tekstiosast jätab välja vastavalt teise argumendina antavast listist sõnu sisaldavate pealkirjadega sektsioonid ja nendele järgnevad
def filtreeritudTekstFailist(fail,filtrilist):
    # Esmalt eraldame kogu artikli teksti osa failist funktsiooniga koguTekstFailist
    result = koguTekstFailist(fail)
    with open(fail,encoding='utf8', mode='r+') as f:
        kogufailisisu = f.read()
        kogufailisisu = korrastaUnicode(kogufailisisu)
    # Seejärel kasutades regex'it otsime failist sektsioonide andmeid puudutava osa
    regsections = re.compile(r'"sections": \[.*\]',re.DOTALL)
    sections = regsections.findall(kogufailisisu)
    # Regex sektsioonide kohta puudutava info leidmiseks ükshaaval
    regsecsisu = re.compile(r'{.*?}',re.DOTALL)
    if(len(sections)>0):
        sections = sections[0]
    else:
        sections = ""
    secsisud = regsecsisu.findall(sections)
    # Vastavalt läbides välja jäetavate osadega listi ja seejärel iga eseme peal sektsioonide listi, kui on kattuvus, siis jätame kogutekstist alates vastava sektsiooni algusest kuni lõpuni välja
    for fil in filtrilist:
        for sec in secsisud:
            # Kui on kattuvus
            if fil.lower() in sec.lower():
                # Otsime sektsiooni teksti seest start osa ja määrame selle ärajäetava osa piiriks
                filtrijärg = otsiStart(sec)
                if(filtrijärg != 0):
                    result = result[:filtrijärg]
    # Tagastame tulemuse
    return result

# Meetod ajaväljendite märgendamiseks etteantud teksti t peal. Teise argumendina sünni- ja surma-aastad, mida kasutatakse märgendamise reeglifaili määramiseks ja kolmandaks argumendiks loend ajaväljendite märgendajatega.
# Ajaväljendi märgendajad loendina antud, et ei peaks mitme teksti korraga märgendamisel iga kord uut ajaväljendite märgendajat looma.
def ajaväljendid(t,sündsurmaastad,taggerid):
    # Sünniaasta esimesel kohal sündsurmaaastad tuple's.
    sünniaasta = sündsurmaastad[0]
    mytimextaggersuper = taggerid[0]
    mytimextaggeraverage = taggerid[1]
    mytimextaggerfourdig = taggerid[2]
    # Kui algab eKr tähisega
    if(sünniaasta.startswith("BC")):
        # Siis eemaldame tähise ja võtame kasutusele ka sünniaastad, viime mõlemad numbrikujule.
        sünniaasta = stringNumbriks(sünniaasta.replace("BC",""))
        surmaasta = stringNumbriks(sündsurmaastad[1].replace("BC",""))
        # Kui sünni- või surma-aasta väiksem kui 100
        if(sünniaasta<100 or surmaasta<100):
            # Kasutame teksti märgendamiseks kõige laiemate reeglitega märgendajat
            text = Text(t,timex_tagger = mytimextaggersuper)
            # Tagastame ajaväljendite listi, mis on saadud rakendades EstNLTK Text klassi isendile funktsiooni .timexes (Sisaldab ajaväljendite semantika sõnastikke vastavalt iga ajaväljendi kohta)
            return (text.timexes)
        # Kui sünni- või surma-aasta väiksem kui 1000
        elif(sünniaasta<1000 or surmaasta<1000):
            # Kasutame teksti märgendamiseks kolme- ja neljaarvulistele aastaarvudele laiendatud märgendajat
            text = Text(t,timex_tagger = mytimextaggeraverage)
            return (text.timexes)
        else:
            # Kõige muude sünniaastate puhul märgendame lihtsalt neljakohalistele aastaarvudele laiendatud reeglifailiga
            text = Text(t,timex_tagger = mytimextaggerfourdig)
            return (text.timexes)
    # Vastasel juhul, kui ei alga eKr tähisega
    else:
        # Kasutame ainult sünniaastat, viime numbri kujule
        sünniaasta = stringNumbriks(sünniaasta)
        if (sünniaasta == 0):
            text = Text(t)
            return (text.timexes)
        elif(sünniaasta<100):
            text = Text(t,timex_tagger = mytimextaggersuper)
            return (text.timexes)
        elif(sünniaasta<1000):
            text = Text(t,timex_tagger = mytimextaggeraverage)
            return (text.timexes)
        elif(sünniaasta<1900):
            text = Text(t,timex_tagger = mytimextaggerfourdig)
            return (text.timexes)
        # Kui sünniaasta hilisem kui 1900, siis kasutame esialgset,muutmata, EstNLTK ajaväljendite märgendaja reeglifaili.
        else:
            text = Text(t)
            return (text.timexes)

# Funktsioon, mis kogu etteantud korpusest(ette tuleb anda kaust esimese argumendina) eraldab sünni- ja surma-aastad, teksti ja märgendab ajaväljendid ja kirjutab need faili kausta, mis on ette antud teise parameetrina
def koguTekstBiograafiatest(p,u):
    path = p
    # Protsessi näitamiseks kaks muutujat
    j = 1
    kogu = len(os.listdir(path))
    # Loome ajaväljendite märgendajad vastavalt kolmele laiendatud reeglitega reeglifailile, et ei peaks korpuse iga artikli juures uut märgendajat looma.
    mytimextaggeresimene = TimexTagger( rules_file = "./reeglid/reeglidesimene.xml")
    mytimextaggerteine = TimexTagger( rules_file = "./reeglid/reeglidteine.xml")
    mytimextaggerkolmas = TimexTagger( rules_file = "./reeglid/reeglidkolmas.xml")
    taggerid = [mytimextaggeresimene,mytimextaggerteine,mytimextaggerkolmas]
    # Vaatame ükshaaval kõiki kaustas asuvaid faile, peaksid olema tekstifailid, .txt lõpuga
    for fail in os.listdir(path):
            # Progressi näitamiseks prindime palju tehtud kogu arvust iga 50 tagant välja
            if (j%50==0):
                print(str(j)+"/"+str(kogu))
            # Eraldame faili nime/artikli pealkirja, eemaldades failinimest .txt'i
            nimi = fail[:-4]
            # Eraldame sünni- ja surma-aastad funktsiooniga sünniJaSurmaaasta
            sündsurmaastad = sünniJaSurmaaasta(path+fail,mytimextaggeresimene)
            # Eraldame teksti osa funktsiooniga koguTekstFailist
            tekst = koguTekstFailist(path+fail)
            # Märgendame teksti peal ajaväljendid
            ajaväl = ajaväljendid(tekst,sündsurmaastad,taggerid)
            # Kirjutame neliku faili kasutades funktsiooni andmedFaili
            faili = (nimi,tekst,ajaväl,sündsurmaastad)
            andmedFaili(faili,u)
            j+=1
    # Lõpuks anname teada, et eraldamine ja failidesse kirjutamine lõpetatud
    print("Done!")

# Funktsioon, mis kogu etteantud korpusest(ette tuleb anda kaust) eraldab sünni- ja surma-aastad, teksti, millel on etteantud märksõnadega lõpusektsioonid välja jäetud(ette antud teise parameetrina listina), ja märgendab ajaväljendid
# ja kirjutab need faili kausta, mis on ette antud kolmanda parameetrina
def filtreeritudTekstBiograafiatest(p,filtrilist,u):
    path = p
    # Protsessi näitamiseks kaks muutujat
    j = 1
    kogu = len(os.listdir(path))
    mytimextaggeresimene = TimexTagger( rules_file = "./reeglid/reeglidesimene.xml")
    mytimextaggerteine = TimexTagger( rules_file = "./reeglid/reeglidteine.xml")
    mytimextaggerkolmas = TimexTagger( rules_file = "./reeglid/reeglidkolmas.xml")
    taggerid = [mytimextaggeresimene,mytimextaggerteine,mytimextaggerkolmas]
    # Vaatame ükshaaval kõiki kaustas asuvaid faile, peaksid olema tekstifailid, .txt lõpuga
    for fail in os.listdir(path):
            # Progressi näitamiseks prindime palju tehtud palju kogu iga 50 tagant välja
            if (j%50==0):
                print(str(j)+"/"+str(kogu))
            # Eraldame faili nime/artikli pealkirja, eemaldades failinimest .txt'i
            nimi = fail[:-4]
            sündsurmaastad = sünniJaSurmaaasta(path+fail,mytimextaggeresimene)
            # Eraldame artikli teksti jättes välja ette antud sektsioonid ja nendest hilisemad
            tekst = filtreeritudTekstFailist(path+fail,filtrilist)
            ajaväl = ajaväljendid(tekst,sündsurmaastad,taggerid)
            # Kirjutame neliku faili kasutades funktsiooni andmedFaili
            faili = (nimi,tekst,ajaväl,sündsurmaastad)
            andmedFaili(faili,u)
            j+=1
    # Lõpuks tagastame listi, mis sisaldab iga faili kohta antud nelikut
    print("Done!")
    
# Peameetod käsurealt käivitamiseks, millel tuleb esimese argumendina anda ette kaust, mis sisaldab biograafilisi artikleid ja millest soovitakse teksti eraldada ja ajaväljendid märgendada,
# teise argumendina tuleb anda kaust kuhu andmed tekstifailidena salvestatakse, kui soovitakse mingeid artikli sektsioone ja nendest hilisemaid välja jätta, siis tuleb need esitada,
# kolmanda argumendina komaga eraldatult ilma tühikuteta näiteks - kirjandus,välislingid,viited,publikatsioon
# Näiteks bakalaureusetöö statistika jaoks kogu tekstide jaoks käsureale > python tekstJaAjaväljendid.py ./biograafiad/ ./kogutekstandmed/
# või > python tekstJaAjaväljendid.py ./biograafiad/ ./filtreeritudtekstandmed/ kirjandus,välislingid,viited,publikatsioon
if __name__ == "__main__":
    try:
        p = sys.argv[1]
        u = sys.argv[2]
    except IndexError:
        print("Lugeda kasutusjuhendit tekstJaAjaväljendid_juhend.txt")
        sys.stderr.write(about) 
        sys.exit(-1)
    if not os.path.exists(p):
        print("Esimese parameetrina etteantud kausta ei leitud")
        sys.exit(-1)
    if not os.path.exists(u):
        print("Teise parameetrina etteantud kausta ei leitud")
        sys.exit(-1)
    try:
        # Kontrollin kas leidub kolmas argument, kui jah, siis moodustame sellest filtrilisti
        l = sys.argv[3]
        filtrilist = l.split(",")
        print("Alustan biograafiate sünni- ja surma-aastate, välja jäetud sektsioonidega teksti, ajaväljendite eraldamist kaustas: " + p + " asuvate artiklite peal")
        filtreeritudTekstBiograafiatest(p,filtrilist,u)
        print("Biograafiate sünni- ja surma-aastad, välja jäetud lõpusektsioonidega tekstid ja ajaväljendid eraldatud ja salvestatud kausta: " + u)
        print("Töö lõpp")
        sys.exit(-1)
    # Kui ei, siis kogu tekstide peal andmete eraldamine
    except IndexError:
        print("Alustan biograafiate sünni- ja surma-aastate, kogu artikli teksti, ajaväljendite eraldamist kaustas: " + p + " asuvate artiklite peal")
        koguTekstBiograafiatest(p,u)
        print("Biograafiate sünni- ja surma-aastad, kogu artikli tekstid ja ajaväljendid eraldatud ja salvestatud kausta: " + u)
        sys.exit(-1)

