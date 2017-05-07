#!/usr/bin/env python
# Autor - Jaan Teppo

import os,re,sys,pickle,csv
from estnltk import Text
from pprint import pprint
from collections import defaultdict

# Skript ajaväljendite andmete korpuse põhjal statistika moodustamiseks, enne skripti kasutamist peab olema loodud andmete korpused(kaustad) kasutades skripti tekstJaAjaväljendid.py


# Lihtne funktsioon leidmaks ette antud arvu sajandit
def sajand(aasta):
    # Rekursiivselt, kui aasta jõuab väiksemast ühest tagastatakse null
    if aasta < 1:
        return 0
    # Senikaua kuni suurem, siis tulemusele üks juurde ja aastast 100 vähemaks
    else:
        return sajand(aasta-100)+1
# Lihtne funktsioon leidmaks kas etteantud string, mis on mõeldud kui ajaväljendi "value", et kas selle esimene sidekriipsu vasakult osa on number
def onNumber(value):
    try:
        int(value.split("-")[0].replace("BC",""))
        return True
    except ValueError:
        return False

# Lihtne funktsioon, mis muudab etteantud stringi numbriks
def stringNumbriks(s):
    if(onNumber(s)== False):
        # Kui ei ole võimalik otse numbriks muuta, tagastatakse 0
        return 0
    else:
        # Kui on , tagastatakes sidekriipsu vasakpoolseim osa numbrina
        return int(s.split("-")[0].replace("BC",""))

# Lihtne funktsioon, mis etteantud arvul määrab millisesse kümnendisse see kuulub ja tagastab etteantud eesliidese, millelele on liidetud kümnend ja "0-ndad".
def kümnend(eesliide,a):
    küm = a % 100
    küm = küm // 10
    return (eesliide + str(küm)+"0-ndad")

# Funktsioon, mis etteantud sünni- ja surma-aastale(tuple'na) määrab grupi kuhu vastavalt sünni- ja surma-aastatele kuuluks artikkel
def grupp(ss):
    sünd = stringNumbriks(ss[0])
    surm = stringNumbriks(ss[1])
    if(ss[0].startswith("BC")):
        if(sünd<100 or surm<100):
            return "grupp 1"
        elif(sünd<1000 or surm<1000):
            return "grupp 2"
        else:
            return "grupp 3"
    elif(sünd==0):
        return "grupp 0"
    else:
        if(sünd<100):
            return "grupp 1"
        elif(sünd<1000):
            return "grupp 2"
        elif(sünd<1900):
            return "grupp 3"
        else:
            return "grupp 4"
# Samasugune funktsioon, aga rakendatud etteantud aastale, mis määrab grupi kuhu artikkel kuulus
def gruppaasta(aa):
    if(aa==0):
        return "grupp 0"
    elif(aa<-999):
        return "grupp 3"
    elif(aa<-99):
        return "grupp 2"
    elif(aa<100):
        return "grupp 1"
    elif(aa<1000):
        return "grupp 2"
    elif(aa<1900):
        return "grupp 3"
    else:
        return "grupp 4"
# Funktsioon andmete lugemiseks ette antud failist, kasutades Pythoni moodulit pickle
def andmedFailist(fnimi):
    with open(fnimi, 'rb') as f:
        l = pickle.load(f)
    return l
# Funktsioon kogu ette antud kausta andmete lugemiseks kasutades funktsiooni andmedFailist
def andmeteLoend(path):
    result = []
    for fail in os.listdir(path):
        k = andmedFailist(path+fail)
        result.append(k)
    return result
# Funktsioon, lugemaks kokku sageduse ja moodustamaks sünni- ja surma-aastaid puudutavat statistikat etteantud andmekogul(listil, mis on loetud mingist kaustast funktsiooniga andmeteLoend)
def sünniJaSurmaAastadSagedus(andmed):
    # Moodustame sõnastikud sagedusloendite jaoks
    sünniaastad = defaultdict(int)
    surmaaastad = defaultdict(int)
    sünniaastadsajandid = defaultdict(int)
    # Muutujad lugemaks kas sünniaasta oli määramata, aga surm mitte ja kas mõlemad olid määramata
    sündnullsurmmitte = 0
    sündjasurmnull = 0
    # Muutuja leidmaks artiklite arvu, kus surma-aasta määramata ja sünniaasta viimase 100 aasta sees
    surmnullsündviimasesajasees = 0
    # Muutujad varaseima ja hiliseima sünni aastate leidmiseks
    varaseimsünd = "0"
    varaseimsündnimi = ""
    hiliseimsünd = "0"
    hiliseimsündnimi = ""
    # Loend moodustamaks andmeid sünniaastate histogrammiks
    histogramlistsünd = []
    # Läbime andmete loendi ükshaaval, kasutades vaid esimes kohal olevaid muutujaid ehk nimesid ja viimasel kohal muutujaid ehk sünni- ja surma-aastaid.
    for(n,_,_,ss) in andmed:
        # Eraldi muutuja sünniaastaks
        sünd = ss[0]
        # Eraldi muutuja surma-aastaks
        surm = ss[1]
        # Määrame sünniaasta numbrilise kuju
        histsünd = stringNumbriks(sünd)
        # Kui sünniaasta sisaldab eKr tähist
        if(sünd.startswith("BC")):
            # Lahutame nullist sünniaasta arvulise tähise, et saada sünniaasta miinus märgiga
            histsünd = 0 - stringNumbriks(sünd)
            # Kontrollime, kas tegemist varasema kui hetkel varaseim määratud sünniaasta
            if(stringNumbriks(sünd.replace("BC",""))>stringNumbriks(varaseimsünd)):
                # Kui jah, siis määrame sünniaasta ja artikli nime varaseimaks
                varaseimsünd = sünd
                varaseimsündnimi = n
        # Kontrollime kas sünniaasta on hiliseim kui olemasolev hiliseim sünd
        if(stringNumbriks(sünd) > stringNumbriks(hiliseimsünd)):
            # Kui jah, määrame uue hiliseima
            hiliseimsünd = sünd
            hiliseimsündnimi = n
        # Kui sünniaasta on arvuliselt määratav, ehk ei võrdu nulliga
        if(histsünd != 0):
            # Siis lisame sünniaastate histogrammi loendisse
            histogramlistsünd.append(histsünd)
        # Suurendame sünniaastate sagedussõnastikus antud sünni-aasta arvu ühe võrra
        sünniaastad[sünd] += 1
        # Sama surma-aasta puhul
        surmaaastad[surm] += 1
        # Määrame sünniaasta sajandi
        sündsajand = sajand(histsünd)
        # Suurendame sünniaastate sajandite sagedusloendi sõnastikus antud sajandit ühe võrra
        sünniaastadsajandid[sündsajand] +=1
        # Kui sünniaasta määramata, aga surma-aasta mitte
        if(histsünd == 0 and stringNumbriks(surm) != 0):
            # Suurendame loenduri muutujat ühe võrra
            sündnullsurmmitte += 1
        # Kui surma-aasta määramata
        if(stringNumbriks(surm)==0):
            # Aga sünniaasta viimase 100 aasta sees
            if(histsünd>1915):
                # Suurendame loenduri muutujat
                surmnullsündviimasesajasees +=1
    # Prindime välja, mitmel artiklil korpuses oli sünniaasta määramata, aga surmaaasta määratud
    print("Sünniaasta määramata, aga surmaaasta määratud artiklite arv: "+
          str(sündnullsurmmitte))
    # Prindime välja, mitmel artiklil korpuses oli surma-aasta määramata ja sünniaasta viimase saja aasta sees
    print("Surmaaasta määramata, aga sünniaasta viimase saja aasta sees: "+
          str(surmnullsündviimasesajasees))
    # Prindime välja varaseima sünniaastaga artikli detailid
    print("Varaseim sünniaasta - " + varaseimsünd+ " - " + varaseimsündnimi)
    # Sama ka hiliseima sünniaastaga artikli puhul
    print("Hiliseim sünniaasta - " + hiliseimsünd+ " - " + varaseimsündnimi)
    # Tagastame sünniaastate sagedussõnastiku, surmaaastate sagedussõnastiku, sünniaastate histogrammi loendi, sünniaastate sajandite sagedussõnastiku.
    return (sünniaastad,surmaaastad,histogramlistsünd,sünniaastadsajandid)


# Funktsioon, mis ette antud andmete loendi peal koostab loendid artiklite sõnade arvudega, ajaväljendite arvudega ja sünniaastatega
def sõnadeJaAjaväljenditeArv(andmed):
    # Muutujad loodavate loendite jaoks
    sõnadearvud = []
    ajaväljenditearvud = []
    sünniaastad = []
    # Läbime andmeteloendi ükshaaval
    for(n,t,i,ss) in andmed:
        # Anname teksti sisse EstNLTK Text klassile
        text = Text(t)
        # Määrame sünniaasta
        sünd = ss[0]
        # Viime sünniaasta numbrilisele kujul, eKr aastate puhul miinus märgiga
        if(sünd.startswith("BC")):
            sünd = 0 - stringNumbriks(sünd)
        else:
            sünd = stringNumbriks(sünd)
        # Kasutame EstNLTK Texti klassi sõnade arvu leidmiseks
        sõnadearv = len(text.word_texts)
        # Määrame ajaväljendite arvu
        ajaväljenditearv = len(i)
        # Lisame vastavatesse loenditesse
        sünniaastad.append(sünd)
        sõnadearvud.append(sõnadearv)
        ajaväljenditearvud.append(ajaväljenditearv)
    # Tagastame vastavad loendid
    return (sõnadearvud,ajaväljenditearvud,sünniaastad)

# Funktsioon, millele antakse parameetritena ette ühe artikli tekst, ajaväljendite loend ja grupp ja mis tagastab vastalt uurimise all oleva statistika loendid või loendurid      
def ajainfo(t,l,g):
    # Loend ajaväljendite tekstiosade jaoks
    ajatext = []
    # Loend ajaväljendite väärtuste jaoks
    ajavalue = []
    # Loend ajaväljendite tüüpide/liikide jaoks
    ajatype = []
    # Loend esinevate aastaarvuliste ajaväljendite sajandite jaoks
    sajandid = []
    # Loend 19 sajandi kümnenditeks
    sajand19kümnendid = []
    # Loend 20 sajandi kümnenditeks
    sajand20kümnendid = []
    # Loend 21 sajandi kümnenditeks
    sajand21kümnendid = []
    # Loend kõigi esinevate aastaarvuliste ajaväljendite aasta osadeks
    aastadhistogramm = []
    # granulaarsuste sagedussõnastik
    granulaarsus = defaultdict(int)
    # Relatiivsete DATE tüüpi ajaväljendite loendur
    relatiivseid = 0
    # Absoluutsete DATE tüüpi ajaväljendite loendur
    absoluutseid = 0
    for i in l:
        # Kui text on olemas sõnastikus
        if ("text" in i.keys()):
            tt = i["text"]
            # Ajavahemikel jääb sidekriips stringi lõppu, seda me ei soovi seega
            # eemaldame
            if (tt.endswith("-")):
                tt = tt[:-1]
            ajatext.append(tt)
            # Kui tegemist on ajavahemikuga, siis lisatakse küll selle jupid
            # listi, aga terviku puhul pole sõnastikus eraldi texti välja toodud
            # seega peame selle ise määrama ja seejärel listi lisama
            if("type" in i.keys() and i["type"]=="DURATION"):
                tt = t[(i["start"]):(i["end"])]
                ajatext.append(tt)
        # Lisame value'd eraldi teise listi
        if ("value" in i.keys()):
            ajavalue.append(i["value"])
        # Lisame type'd eraldi kolmandasse listi
        if("type" in i.keys()):
            tüüp = i["type"]
            ajatype.append(tüüp)
            # Kui tüüp on "DATE" ehk kalendrilise toimumisajaga
            if(tüüp == "DATE"):
                # Kui tegemist on absoluutse kalendrilise toimumisajaga ajaväljendiga
                if(i["temporal_function"]==False):
                    # Suurendame absoluutsete loendurit ühe võrra
                    absoluutseid += 1
                    # Määrame väärtuse
                    val = i["value"]
                    # Kui sisaldab nädala tähist
                    if("W" in val):
                        # Lisame granulaarsussõnastikus nädalale ühe juurde
                        granulaarsus["nädal"] +=1
                    # Kui koosneb kolmest sidekriipsust
                    elif(len(val.split("-"))==3):
                        # Siis päeva granulaarsusega
                        granulaarsus["päev"] +=1
                    # Kui kahest 
                    elif(len(val.split("-"))==2):
                        # Siis kuu
                        granulaarsus["kuu"] +=1
                    # Kui ühest
                    elif(len(val.split("-"))==1):
                        # Siis aasta
                        granulaarsus["aasta"] +=1
                    # Kui ajaväljend on lihtsalt 1. sajand, siis väärtus "00" ja lisame sellele "1", et funktsioon paigutaks selle esimesse sajandisse
                    if(val =="00"):
                        val = val + "1"
                    # Kui sisaldab "ndat", näiteks 1930'ndatel, siis vaja väärtusele liita "1", et paigutatakse õigesse sajandisse
                    elif("text" in i.keys() and "ndat" in i["text"]):
                        val = val+"1"
                    # Kui sisaldab "ndat", näiteks 3. sajandil, siis vaja samuti vastavalt kas on ka kümnendi täpsus toodud näiteks 3. sajandi 40'ndatel aastatel tuleb juurde liita "1" või kui lihtsalt sajand, siis "01"
                    elif("text" in i.keys() and "sajand" in i["text"]):
                        if("aasta" in i["text"]):
                            val = val + "1"
                        else:   
                            val = val+"01"
                    # Kui väärtusel on eKr tähis
                    if (val.startswith("BC")):
                        # Siis sajandite loendis tähistame kõiki eKr -1'ga
                        sajandid.append(-1)
                        # Muudame aastate histogrammiks väärtuse negatiivseks
                        val = 0 - stringNumbriks(val)
                        # Lisame aastate histogrammi
                        aastadhistogramm.append(val)
                    # Vastasel juhul
                    else:
                        # Aasta arvuliselt
                        aa = stringNumbriks(val)
                        # Sajandi number
                        sa = sajand(aa)
                        # Lisame sajandite loendisse
                        sajandid.append(sa)
                        # Lisame aastate histogrammi loendisse
                        aastadhistogramm.append(aa)
                        # Kui tegemist 19 sajandiga, siis määrame ka kümnendi
                        if(sa == 19):
                            # Kui tegemist ei ole ise lisatud sajandi osaga, et näiteks tegemist ei ole ajaväljendiga "19. sajand"
                            if not(val.endswith("01") and val != i["value"]):
                                # Siis määrame kümnendi ja lisame 19 sajandi kümnendite loendisse
                                sajand19kümnendid.append(kümnend("18",aa))
                        # Sama 20 sajandi puhul
                        elif(sa == 20):
                            if not(val.endswith("01") and val != i["value"]):  
                                sajand20kümnendid.append(kümnend("19",aa))
                        # Sama 21 sajandi puhul
                        elif(sa == 21):
                            if not(val.endswith("01") and val != i["value"]): 
                                sajand21kümnendid.append(kümnend("20",aa))
                # Kui Temporal_function = True, siis tegemist relatiivsega
                else:
                    # Suurendame vastavat loendurit
                    relatiivseid +=1
    # Tagastame tekstide loendi, valuede loendi, tüüpide loendi, sajandite loendi, absoluutsete DATE ajaväljendite arvu, relatiivsete DATE ajaväljendite arvu, aastate loendi histogrammi jaoks, granulaarsuste sõnastiku
    # 19 sajandi kümnendid, 20 sajandi kümnendid ja 21 sajandi kümendid ja kõige lõpuks grupi , kuhu artikkel kuulus
    return (ajatext,ajavalue,ajatype,sajandid,absoluutseid,relatiivseid,
            aastadhistogramm,granulaarsus,sajand19kümnendid,
            sajand20kümnendid,sajand21kümnendid,g)

# Määrame ette antud andmete peal, mis on saadud funktsiooniga andmeteLoend korpuse kaustal iga artikli kohta uuritava ajaväljendite info, mis on saadud funktsiooni ajainfo kasutades
def ajainfolistkõik(andmed):
    result = []
    # Iga artikli puhul
    for (_,t,i,ss) in andmed:
        # Grupi määramine sünni- ja surma-aastate põhjal
        g = grupp(ss)
        # Ajainfo määramine kasutades funktsiooni ajainfo, andes ette artikli teksti, ajaväljendite loendi ja grupi
        inf = ajainfo(t,i,g)
        # Lisame tulemuslisti
        result.append(inf)
    # Tagastame tulemuse
    return result


# Meetod, mis kogu korpuse artiklite peal moodustatud ajainfot puudutavad loendi sagedussõnastikeks muudab või kokku liidab või muutujad kokku liidab, ette antud parameetriks loend, mis saadud funktsiooniga ajainfolistkõik
def ajasagedus(l):
    # Tekstide sagedussõnastik
    resultajat = defaultdict(int)
    # Väärtuste sagedussõnastik
    resultajav = defaultdict(int)
    # Tüüpide/liikide sagedussõnastik
    resultajatype = defaultdict(int)
    # Sajandite sagedussõnastik
    resultsajandid = defaultdict(int)
    # Granulaarsuste sagedussõnastik
    resultgranulaarsus = defaultdict(int)
    # 19 sajandi kümnendite sagedussõnastik
    resultsajand19kümnendid = defaultdict(int)
    # 20 sajandi kümnendite sagedussõnastik
    resultsajand20kümnendid = defaultdict(int)
    # 21 sajandi kümnendite sagedussõnastik
    resultsajand21kümnendid = defaultdict(int)
    # Vastavalt sünni- ja surma-aastate puhul gruppidesse jaotatud artiklite aastaarvuliste ajaväljendite kuuluvus vastavatesse gruppidesse sagedussõnastikud
    resultgrupi0jaotus = defaultdict(int)
    resultgrupi1jaotus = defaultdict(int)
    resultgrupi2jaotus = defaultdict(int)
    resultgrupi3jaotus = defaultdict(int)
    resultgrupi4jaotus = defaultdict(int)
    # Kogu korpuse absoluutsete DATE tüüpi ajaväljendite arv
    absoluutsed = 0
    # Kogu korpuse relatiivsete DATE tüüpi ajaväljendite arv
    relatiivsed = 0
    # Kogu aastaliste ajaväljendite loend histogrammi koostamiseks
    koguaastadhistogramm = []
    # Iga ette antud loendi element on vastavalt ühe artikli andmete põhjal saadud rakendades funktsiooni ajainfo tulemus
    for (ajatext,ajavalue,ajatype,sajandid,absoluutseid,relatiivseid,aastadhistogramm,granulaarsus,sajand19kümnendid,sajand20kümnendid,sajand21kümnendid,g) in l:
        # Läbime artikli ajaväljendite tekstide loendi ja suurendame vastava kogu korpuse sagedussõnastikke 
        for i in ajatext:
            resultajat[i] +=1
        # Läbime artikli ajaväljendite väärtuste loendi ja suurendame vastavalt kogu korpuse sagedussõnastikke elemente
        for ii in ajavalue:
            resultajav[ii] +=1
        # Läbime artikli ajaväljendite tüüpide loendi ja suurendame vastavalt kogu korpuse sagedussõnastikke elemente        
        for iii in ajatype:
            resultajatype[iii] += 1
        # Läbime artikli ajaväljendite sajandite loendi ja suurendame vastavalt kogu korpuse sagedussõnastikke elemente
        for iiii in sajandid:
            resultsajandid[iiii] += 1
        # Läbime artikli ajaväljendite 19 sajandi kümnendite loendi ja suurendame vastavalt kogu korpuse sagedussõnastikke elemente
        for iiiii in sajand19kümnendid:
            resultsajand19kümnendid[iiiii] += 1
        # Läbime artikli ajaväljendite 20 sajandi kümnendite loendi ja suurendame vastavalt kogu korpuse sagedussõnastikke elemente
        for iiiiii in sajand20kümnendid:
            resultsajand20kümnendid[iiiiii] += 1
        # Läbime artikli ajaväljendite 21 sajandi kümnendite loendi ja suurendame vastavalt kogu korpuse sagedussõnastikke elemente
        for iiiiiii in sajand21kümnendid:
            resultsajand21kümnendid[iiiiiii] += 1
        # Määrame vastavalt artiklite aastaarvuliste ajaväljendite loendi põhjal nende kuuluvused sünni- ja surma-aastate põhjal moodustatud grupidesse
        for aa in aastadhistogramm:
            # Ja lisame eelnevalt sünni- ja surma-aasta põhjal määratud grupi jaotusesse
            if(g=="grupp 0"):
                resultgrupi0jaotus[gruppaasta(aa)] +=1
            elif(g=="grupp 1"):
                resultgrupi1jaotus[gruppaasta(aa)] +=1
            elif(g=="grupp 2"):
                resultgrupi2jaotus[gruppaasta(aa)] +=1
            elif(g=="grupp 3"):
                resultgrupi3jaotus[gruppaasta(aa)] +=1
            elif(g=="grupp 4"):
                resultgrupi4jaotus[gruppaasta(aa)] +=1
        # Kuna granulaarsuste põhjal oli igal artiklil juba sagedussõnastikud moodustatud, siis tuleb need lihtsalt kogutulemusse otsa liita
        resultgranulaarsus["nädal"] += granulaarsus["nädal"]
        resultgranulaarsus["päev"] += granulaarsus["päev"]
        resultgranulaarsus["kuu"] += granulaarsus["kuu"]
        resultgranulaarsus["aasta"] += granulaarsus["aasta"]
        # Sama ka absoluutsete ja relatiivsete DATE tüüpi ajaväljendite arvudega
        absoluutsed += absoluutseid
        relatiivsed += relatiivseid
        # Kogu aastate põhjal moodustatava histogrammi loendiks piisab kui vastavalt iga artikli aastaarvuliste ajaväljendite loendid kokku liita
        koguaastadhistogramm = koguaastadhistogramm + aastadhistogramm
    # Gruppide jaotuste sõnastikud paneme eraldi ühte loendisse
    resultgruppidejaotused = [resultgrupi0jaotus,resultgrupi1jaotus,resultgrupi2jaotus,resultgrupi3jaotus,resultgrupi4jaotus]
    # Tagastame vastavalt tekstide sagedussõnastiku, väärtuste sagedussõnastiku, sajandite sagedussõnastiku, absoluutsete DATE tüüpi ajaväljendite arvu, relatiivsete DATE tüüpi ajaväljendite arvu,
    # kogu aastaarvuliste ajaväljendite loendi histogrammiks, granulaarsuste sagedussõnastiku, 19 sajandi kümnendite sagedussõnastiku, 20 sajandi kümnendite sagedussõnastiku, 21 sajandi kümendite sagedussõnastiku
    # ja gruppide sagedusõnastikest koosneva loendi.
    return (resultajat,resultajav,resultajatype,resultsajandid,absoluutsed,relatiivsed,koguaastadhistogramm,
            resultgranulaarsus,resultsajand19kümnendid,resultsajand20kümnendid,resultsajand21kümnendid,resultgruppidejaotused)

# Funktsioon, mis kirjutaks etteantud sagedussõnastiku ette antud TXT-faili, esinemiste arvu kahanevas järjekorras
def kõikfaili(sagedusl,failinimi,header):
    out = []
    # Järjestame sagedussõnastiku ja viime ta loendi kujule, esinemiste arvu kahanemise järjekorras, esinemiste arv ja nimi/tüüp eraldatud tab'iga
    for i,j in sorted(sagedusl.items(), key = lambda x: x[1], reverse=True):
        out.append(u'{}\t{}'.format(j,i))
    sagedusfail = open(failinimi,'w',encoding='utf8')
    # Kirjutame faili pealise
    sagedusfail.write(header+"\n")
    # Vastavalt sagedusloendi elemendid kirjutame erinevatele ridadele
    for s in out:
        sagedusfail.write(s+"\n")
    sagedusfail.close()
# Funktsioon, mis kirjutaks etteantud sagedussõnastiku ette antud CSV-faili, esinemiste arvu kahanevas järjekorras
def kõikfailicsv(sagedusl,failinimi,header):
    out = []
    # Sagedussõnastiku muudame sagedusloendiks, kus elemendid tuple'dena vastavalt esinemiste arv ja nimi/tüüp
    for i,j in sorted(sagedusl.items(), key = lambda x: x[1], reverse=True):
        out.append((j,i))
    # Kirjutame vastavalt csvfaili
    with open(failinimi, 'w', newline='') as csvfile:
        # Esinemiste arv ja nimi/tüüp eraldatud |'ga, iga sagedusloendi esinemine eraldi real
        spamwriter = csv.writer(csvfile, delimiter='|',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # Kirjutame etteantud pealise faili
        spamwriter.writerow(header)
        for s in out:
            spamwriter.writerow(s)
# Kuna sõnad ja ajaväljendite arvud pole sagedussõnastikena vaid kahe loendina, siis eraldi funktsioon nende kirjutamiseks TXT-i faili
def sõnadjaajaväljenditearvudfaili(sõnadjaaja,failinimi,header):
    # Loendid sõnade arvudega vastavalt iga artikli kohta
    sõnadarvud = sõnadjaaja[0]
    # Loendid ajaväljendite arvudega vastavalt iga artikli kohta
    ajavälarvud = sõnadjaaja[1]
    # Faili kirjutamini sarnaselt nagu kõikfaili puhul
    sagedusfail = open(failinimi,'w',encoding='utf8')
    # Faili pealis
    sagedusfail.write(header+"\n")
    # Koos faili kirjutamiseks ühendame loendite elemendid paaridena
    for s,a in zip(sõnadarvud,ajavälarvud):
        sagedusfail.write(str(s)+"\t"+str(a)+"\n")
    sagedusfail.close()
# Sama CSV-faili puhul
def sõnadjaajaväljenditearvudfailicsv(sõnadjaaja,failinimi,header):
    sõnadarvud = sõnadjaaja[0]
    ajavälarvud = sõnadjaaja[1]
    with open(failinimi, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(header)
        for s,a in zip(sõnadarvud,ajavälarvud):
            spamwriter.writerow((s,a))
# Funktsioon ka ajaväljendite ja sünniaastate CSV-faili kirjutamiseks
def ajaväljenditejasünniaastafailicsv(sõnadjaaja,failinimi,header):
    # Sünniaastate loend
    sünniaasta = sõnadjaaja[2]
    # Ajaväljendite arvude loend
    ajavälarvud = sõnadjaaja[1]
    with open(failinimi, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # Faili pealis
        spamwriter.writerow(header)
        # Koos faili kirjutamiseks ühendame loendite elemendid paaridena, eraldi ridadele iga paar
        for s,a in zip(sünniaasta,ajavälarvud):
            # Kui sünni-aasta ei võrdu nulliga, ehk kui sünniaasta ei ole määramata
            if(s!=0):
                spamwriter.writerow((s,a))

# Funktsioon histogrammi loendi elementide kirjutamiseks CSV-faili
def histogramlistfailicsv(histogramlist,failinimi,header):
    with open(failinimi, 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter='|',quotechar='|', quoting=csv.QUOTE_MINIMAL)
        # Pealis faili
        spamwriter.writerow(header)
        # iga element eraldi reale
        for s in histogramlist:
            spamwriter.writerow([s])
        

# Funktsioon, mis kogu esimese parameetrina antud kausta andmete peal moodustab statistika/sagedusloendid ja kirjutab vastavalt failidesse või kuvab ekraanile, Teise argumendina andmete täpsustus, kui on näiteks mitu korpust
# näiteks kogu tekstidega andmetega korpus ja välja jäetud/filtreeritud tekstidega andmete korpus, viimase parameetrina tõeväärtus, kas soovitakse salvestada ka lisastatistikat, ehk statistikat, mida bakalaureusetöös otseselt ei
# esitatud või ei mainitud.
def skriptkõikfaili(p,andmetetäpsustus,lisa = False):
    # Kogu ette antud kausta andmete loend
    andmed = andmeteLoend(p)
    # Kogu etteantud kausta andmete ajainfo loendite loend
    ajainf = ajainfolistkõik(andmed)
    # Kogu etteantud kausta andmete sagedussõnastike ja muu statiska moodustamine
    ajasagedusinf = ajasagedus(ajainf)
    # Erinevad sagedussõnastikud või loendid eraldi muutujatesse vastavalt funktsiooni ajasagedus tulemustele
    ajatypesagedus = ajasagedusinf[2]
    sajandidsagedus = ajasagedusinf[3]
    absoluutseid = ajasagedusinf[4]
    relatiivseid = ajasagedusinf[5]
    aastadhistogramm = ajasagedusinf[6]
    granulaarsus = ajasagedusinf[7]
    sajand19kümnendid = ajasagedusinf[8]
    sajand20kümnendid = ajasagedusinf[9]
    sajand21kümnendid = ajasagedusinf[10]
    gruppidejaotused = ajasagedusinf[11]
    # Sünni- ja surma-aastate statistika kogu korpuse peal
    sündjasurmaastad = sünniJaSurmaAastadSagedus(andmed)
    # Sünni- ja surma-aastate sagedussõnastikud või loendid erinevatesse muutujatesse
    sünniaastadsagedus = sündjasurmaastad[0]
    surmaaastadsagedus = sündjasurmaastad[1]
    sündhistogramm = sündjasurmaastad[2]
    sündsajandid = sündjasurmaastad[3]
    # Loendid kogu korpuse sõnade arvudega, ajaväljendite arvudega ja sünniaastatega vastavalt funktsiooni sõnadeJaAjaväljenditeArv tagastatud tulemustena
    sõnadejaajaväljenditearv = sõnadeJaAjaväljenditeArv(andmed)
    # Kirjutame ajaväljendite tüüpide/liikide sagedusloendid vastavalt failidesse sagedusloendtype.txt ja sagedusloendtype.csv, lisatud pealisesse ka "DATE" tüüpi relatiivsete ja absoluutsete ajaväljendite arvu, et kirjutatakse tekstifaili.
    kõikfaili(ajatypesagedus,"./statistika/"+andmetetäpsustus+"sagedusloendtype.txt",'arv'+'\t'+'type'+'\n'+'Absoluutseid "DATE" tüüpi ajaväljendeid: '+str(absoluutseid)+'\n'+'relatiivseid "DATE" tüüpi ajaväljendeid: '+str(relatiivseid))
    kõikfailicsv(ajatypesagedus,"./statistika/"+andmetetäpsustus+"sagedusloendtype.csv",["arv","type"])
    # Kirjutame aastaarvuliste ajaväljendite sajandid sagedusloendid vastavalt failidesse sagedusloendsajandid.txt ja sagedusloendsajandid.csv
    kõikfaili(sajandidsagedus,"./statistika/"+andmetetäpsustus+"sagedusloendsajandid.txt","arv"+"\t"+"sajand")
    kõikfailicsv(sajandidsagedus,"./statistika/"+andmetetäpsustus+"sagedusloendsajandid.csv",["arv","sajand"])
    # Kirjutame sünniaastate sagedusloendid vastavalt failidesse sünniaastad.txt ja sünniaastad.csv
    kõikfaili(sünniaastadsagedus,"./statistika/"+andmetetäpsustus+"sünniaastad.txt","arv"+"\t"+"sünniaasta")
    kõikfailicsv(sünniaastadsagedus,"./statistika/"+andmetetäpsustus+"sünniaastad.csv",["arv","synniaasta"])
    # Kirjutame surma-aastate sagedusloendid vastavalt failidesse surmaaastad.txt ja surmaaastad.csv
    kõikfaili(surmaaastadsagedus,"./statistika/"+andmetetäpsustus+"surmaaastad.txt","arv"+"\t"+"surmaaasta")
    kõikfailicsv(surmaaastadsagedus,"./statistika/"+andmetetäpsustus+"surmaaastad.csv",["arv","surmaaasta"])
    # Kirjutame ajaväljendite granulaarsuste sagedusloendid vastavalt failidesse granulaarsus.txt ja granulaarsus.csv
    kõikfaili(granulaarsus,"./statistika/"+andmetetäpsustus+"granulaarsus.txt","arv"+"\t"+"granulaarsus")
    kõikfailicsv(granulaarsus,"./statistika/"+andmetetäpsustus+"granulaarsus.csv",["arv","granulaarsus"])
    # Kirjutame 19 sajandi kümnendite sagedusloendid vastavalt failidesse sajand19kümnendid.txt ja sajand19kümnendid.csv
    kõikfaili(sajand19kümnendid,"./statistika/"+andmetetäpsustus+"sajand19kümnendid.txt","arv"+"\t"+"kümnend")
    kõikfailicsv(sajand19kümnendid,"./statistika/"+andmetetäpsustus+"sajand19kümnendid.csv",["arv","kymnend"])
    # Kirjutame 20 sajandi kümnendite sagedusloendid vastavalt failidesse sajand20kümnendid.txt ja sajand20kümnendid.csv
    kõikfaili(sajand20kümnendid,"./statistika/"+andmetetäpsustus+"sajand20kümnendid.txt","arv"+"\t"+"kümnend")
    kõikfailicsv(sajand20kümnendid,"./statistika/"+andmetetäpsustus+"sajand20kümnendid.csv",["arv","kymnend"])
    # Kirjutame 21 sajandi kümnendite sagedusloendid vastavalt failidesse sajand21kümnendid.txt ja sajand21kümnendid.csv
    kõikfaili(sajand21kümnendid,"./statistika/"+andmetetäpsustus+"sajand21kümnendid.txt","arv"+"\t"+"kümnend")
    kõikfailicsv(sajand21kümnendid,"./statistika/"+andmetetäpsustus+"sajand21kümnendid.csv",["arv","kymnend"])
    # Kirjutame sünniaastate sajandite sagedusloendid vastavalt failidesse sünniaastadsajandid.txt ja sünniaastadsajandid.csv
    kõikfaili(sündsajandid,"./statistika/"+andmetetäpsustus+"sünniaastadsajandid.txt","arv"+"\t"+"sajand")
    kõikfailicsv(sündsajandid,"./statistika/"+andmetetäpsustus+"sünniaastadsajandid.csv",["arv","sajand"])
    # Kirjutame sünniaastate histogrammi jaoks loodud loendi faili sünniaastadhistogramm.csv
    histogramlistfailicsv(sündhistogramm,"./statistika/"+andmetetäpsustus+"sünniaastadhistogram.csv",["synd"])
    # Kirjutame aastaarvuliste ajaväljendite histogrammi jaoks loodud loendi faili aastadhistogramm.csv
    histogramlistfailicsv(aastadhistogramm,"./statistika/"+andmetetäpsustus+"aastadhistogram.csv",["aasta"])
    # Kirjutame loendid, mis sisaldavad vastavalt artiklite ajaväljendite arvu ja sünniaastaid faili ajaväljendidjasünniaasta.csv
    ajaväljenditejasünniaastafailicsv(sõnadejaajaväljenditearv,"./statistika/"+andmetetäpsustus+"ajaväljendidjasünniaasta.csv",["synd","ajavaljendeid"])
    # Väljastame ekraanile eraldi absoluutsete "DATE" tüüpi ajaväljendite ja relatiivsete "DATE" tüüpi ajaväljendite arvu
    print('Absoluutseid "DATE" tüüpi ajaväljendeid: '+str(absoluutseid))
    print('Relatiivseid "DATE" tüüpi ajaväljendeid: '+str(relatiivseid))
    # Järgnev osa lisastatistika jaoks, mida otseselt lõputöös ei kajastatud/kasutatud, aga töö käigus siiski loodi.
    if(lisa==True):
        # Vastavad muutujad erinevate sagedussõnastike jaoks
        ajatekstsagedus = ajasagedusinf[0]
        ajavaluesagedus = ajasagedusinf[1]
        gruppidejaotused = ajasagedusinf[11]
        grupi0jaotus = gruppidejaotused[0]
        grupi1jaotus = gruppidejaotused[1]
        grupi2jaotus = gruppidejaotused[2]
        grupi3jaotus = gruppidejaotused[3]
        grupi4jaotus = gruppidejaotused[4]
        # Kirjutame ajaväljendite tekstide sagedusloendid vastavalt failidesse sagedusloendtext.txt ja sagedusloendtext.csv
        kõikfaili(ajatekstsagedus,"./statistika/lisa/"+andmetetäpsustus+"sagedusloendtext.txt","arv"+"\t"+"text")
        kõikfailicsv(ajatekstsagedus,"./statistika/lisa/"+andmetetäpsustus+"sagedusloendtext.csv",["arv","text"])
        # Kirjutame ajaväljendite väärtuste sagedusloendid vastavalt failidesse sagedusloendvalue.txt ja sagedusloendvalue.csv
        kõikfaili(ajavaluesagedus,"./statistika/lisa/"+andmetetäpsustus+"sagedusloendvalue.txt","arv"+"\t"+"value")
        kõikfailicsv(ajavaluesagedus,"./statistika/lisa/"+andmetetäpsustus+"sagedusloendvalue.csv",["arv","value"])
        # Kirjutame grupi 0( määramata sünniaastaga artiklite) aastaarvuliste ajaväljendite jagunemise sagedusloendid vastavalt failidesse grupi0jaotus.txt ja grupi0jaotus.csv
        kõikfaili(grupi0jaotus,"./statistika/lisa/"+andmetetäpsustus+"grupi0jaotus.txt","arv"+"\t"+"grupp")
        kõikfailicsv(grupi0jaotus,"./statistika/lisa/"+andmetetäpsustus+"grupi0jaotus.csv",["arv","grupp"])
        # Kirjutame grupi 1( 2 kohalise sünniaastaga artiklite) aastaarvuliste ajaväljendite jagunemise sagedusloendid vastavalt failidesse grupi1jaotus.txt ja grupi1jaotus.csv
        kõikfaili(grupi1jaotus,"./statistika/lisa/"+andmetetäpsustus+"grupi1jaotus.txt","arv"+"\t"+"grupp")
        kõikfailicsv(grupi1jaotus,"./statistika/lisa/"+andmetetäpsustus+"grupi1jaotus.csv",["arv","grupp"])
        # Kirjutame grupi 2( 3 kohalise sünniaastaga artiklite) aastaarvuliste ajaväljendite jagunemise sagedusloendid vastavalt failidesse grupi2jaotus.txt ja grupi2jaotus.csv
        kõikfaili(grupi2jaotus,"./statistika/lisa/"+andmetetäpsustus+"grupi2jaotus.txt","arv"+"\t"+"grupp")
        kõikfailicsv(grupi2jaotus,"./statistika/lisa/"+andmetetäpsustus+"grupi2jaotus.csv",["arv","grupp"])
        # Kirjutame grupi 3( 4 kohalise sünniaastaga, 1900 varasemad, artiklite) aastaarvuliste ajaväljendite jagunemise sagedusloendid vastavalt failidesse grupi3jaotus.txt ja grupi3jaotus.csv
        kõikfaili(grupi3jaotus,"./statistika/lisa/"+andmetetäpsustus+"grupi3jaotus.txt","arv"+"\t"+"grupp")
        kõikfailicsv(grupi3jaotus,"./statistika/lisa/"+andmetetäpsustus+"grupi3jaotus.csv",["arv","grupp"])
        # Kirjutame grupi 4( 1900 hilisemad sünniaastaga artiklite) aastaarvuliste ajaväljendite jagunemise sagedusloendid vastavalt failidesse grupi4jaotus.txt ja grupi4jaotus.csv
        kõikfaili(grupi4jaotus,"./statistika/lisa/"+andmetetäpsustus+"grupi4jaotus.txt","arv"+"\t"+"grupp")
        kõikfailicsv(grupi4jaotus,"./statistika/lisa/"+andmetetäpsustus+"grupi4jaotus.csv",["arv","grupp"])
        # Kirjutame loendid, mis sisaldavad vastavalt artiklite sõnade arvu ja ajaväljendite arvu failidesse sõnadejaajaväljenditearv.txt ja sõnadejaajaväljenditearv.csv
        sõnadjaajaväljenditearvudfaili(sõnadejaajaväljenditearv,"./statistika/lisa/"+andmetetäpsustus+"sõnadejaajaväljenditearv.txt","sõnu"+"\t"+"ajaväljendeid")
        sõnadjaajaväljenditearvudfailicsv(sõnadejaajaväljenditearv,"./statistika/lisa/"+andmetetäpsustus+"sõnadejaajaväljenditearv.csv",["sonu","ajavaljendeid"])
    

# Peameetod käsurealt käivitamiseks, millel tuleb esimese argumendina anda ette kaust, mis sisaldab biograafiliste artiklite andmeid, mis on saadud skripti tekstJaAjaväljendid tulemusena ja mille peal moodustatakse statistika,
# teise parameetrina andmete täpsustus, mis saab olema iga moodustatud statistikafaili eesliiteks näiteks "kogu" või "filtreeritud", et moodustatava statistika kaustas oleks võimalik eristada erinevaid statistikafaile, kui andmete
# jaoks on loodud mitu korpust. Kolmandaks argumendiks võib lisada -lisa ,kui soovitakse, et moodustataks ka lisa statistika, mida bakalaureusetöös ei kajastatud või millest ei kirjutatud, aga mis siiski moodustatud sai.
# Näiteks käsurealt > python sagedusJaMuuStatistika.py ./kogutekstandmed/ kogu
# või > python sagedusJaMuuStatistika.py ./kogutekstandmed/ kogu -lisa
# või > python sagedusJaMuuStatistika.py ./filtreeritudtekstandmed/ filtreeritud
# või > python sagedusJaMuuStatistika.py ./filtreeritudtekstandmed/ filtreeritud - lisa
if __name__ == "__main__":
    try:
        p = sys.argv[1]
        t = sys.argv[2]
    except IndexError:
        print("Lugeda kasutusjuhendit sagedusJaMuuStatistika_juhend.txt")
        sys.stderr.write(about) 
        sys.exit(-1)
    # Kontrollin kas esimese parameetrina kaust eksisteerib
    if not os.path.exists(p):
        print("Esimese parameetrina etteantud kausta ei leitud")
        sys.exit(-1)
    # Kontrollin kas kaust statistika eksisteerib
    if not os.path.exists("./statistika/"):
        print("Skriptiga samas kaustas peab olema kausta nimega statistika , palun luua kaust enne skripti käivitamist")
        sys.exit(-1)
    try:
        # Kontrollin ,kas kolmanda argumendina antud -lisa, mis tähendab, et soovitakse moodustada ka lisastatistikat
        l = sys.argv[3]
        if(l=="-lisa"):
            if not os.path.exists("./statistika/lisa/"):
                print("Skriptiga samas kaustas peab olema kausta nimega statistika, mille sees peab olema kaust nimega lisa , palun luua kaust enne skripti käivitamist")
                sys.exit(-1)
            print("Alustan statistika moodustamist kausta: " + p + " andmete peal, mis kirjutatakse skriptiga samas kaustas asuvasse kausta statistika, igal statistika failil on eesliide: " + t)
            print("Moodustatakse ka lisa statistika kausta statistika sees asuvasse kausta lisa")
            skriptkõikfaili(p,t,True)
        else:
            print("Alustan statistika moodustamist kausta: " + p + " andmete peal, mis kirjutatakse skriptiga samas kaustas asuvasse kausta statistika, igal statistika failil on eesliide: " + t)
            skriptkõikfaili(p,t)
        print("Töö lõpp!")
        sys.exit(-1) 
    except IndexError:
        print("Alustan statistika moodustamist kausta: " + p + " andmete peal, mis kirjutatakse skriptiga samas kaustas asuvasse kausta statistika, igal statistika failil on eesliide: " + t)
        skriptkõikfaili(p,t)
        print("Töö lõpp!")
        sys.exit(-1)


        
