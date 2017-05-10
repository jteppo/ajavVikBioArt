#!/usr/bin/env python

# Autor - Jaan Teppo
import os,sys,pickle
from estnltk import Text
from pprint import pprint
from collections import defaultdict
from random import randint

# Skript võrdluskorpuse moodustamiseks, kahe artikli vahelise ajaväljendite põhise kauguse arvutamiseks, artiklile viie sarnasema artikli leidmiseks ajaväljendite põhise kauguse põhjal ja juhusliku valikuga x artiklile sarnasema 5
# artikli leidmiseks ajaväljendite põhise kauguse põhjal


# Lihtne funktsioon vaatamaks, kas etteantud väärtus stringina on number
def onNumber(value):
    try:
        int(value.split("-")[0].replace("BC",""))
        return True
    except ValueError:
        return False
    # Juba numbrite korral
    except AttributeError:
        return True
# Funktsioon, mis vastavalt etteantud stringile tagastab esimesest sidekriipsust vasakpoole osa numbrina(Kui võimalik)
def stringNumbriks(s):
    if(onNumber(s)== False):
        return 0
    else:
        try:
            if(s.startswith("BC")):
               return (0-int(s.split("-")[0].replace("BC","")))
            else:
               return int(s.split("-")[0].replace("BC",""))
        # Juba numbrite korral
        except AttributeError:
            return s
# Funktsioon lugemaks andmeid failist Pythoni mooduli pickle abil
def andmedFailist(fnimi):
    with open(fnimi, 'rb') as f:
        l = pickle.load(f)
    return l
# Funktsioon kirjutamaks andmeid failist Pythoni mooduli pickle abil
def andmedFaili(l,path):
    s = l[0] + ".txt"
    with open(path+s,'wb') as f:
        pickle.dump(l,f)
# Funktsioon lugemaks kogu etteantud kausta sisu ühte loendisse kasutades funktsiooni andmedFailist
def andmeteLoend(path):
    result = []
    for fail in os.listdir(path):
        k = andmedFailist(path+fail)
        result.append(k)
    return result
# Funktsioon sorteerimiseks aastast ja kuust või aastast ja kuust ja kuupäevast või ka ajavahemike koosnevate ajaväljendite(stringide) puhul, tagastatakse stringi väärtus, mis arvestab ka kuu osa või ka kuupäeva osa
def sortimisfunktsioon(val):
    jupid = val.split("-")
    aasta = stringNumbriks(val)
    # Kui koosneb kahest osast, ehk aastast ja kuust
    if(len(jupid)==2):
        # Kuu osa jagame 100'ga ja liidame aasta osale
        kuu = stringNumbriks(jupid[1])/100
        return (aasta+kuu)
    # Kui koosneb kolmest osast ehk aastast ja kuust ja kuupäevast
    elif(len(jupid)==3):
        # Kuu osa jagame 100'ga, päeva osa 10000 ja liidame aasta osale
        kuu = stringNumbriks(jupid[1])/100
        päev = stringNumbriks(jupid[2])/10000
        return(aasta+kuu+päev)
    # Vastasel juhul tagastame aasta
    else:
        return aasta

# Funktsioon, mis argumendina ette antud faili(artikli) puhul eraldab vastavalt vajadusele ajaväljendid ja grupeerib need    
def artiklist(artikkel):
    # Vastavad loendid vajalike gruppide jaoks
    aastad = []
    aastadKuud = []
    aastadKuudKuupäevad = []
    ajavahemikud = []
    # läbime ajaväljendite loendi, mis andmetekorpuse failides oli loendis kolmandal kohal
    for ajaväljend in artikkel[2]:
        # Käsitleme kalendrilise toimumisajaga(DATE) ajaväljendeid
        if(ajaväljend["type"]=="DATE"):
            # Mis on absoluutsed
            if(ajaväljend["temporal_function"]==False):
                # Loeme väärtused
                val = ajaväljend["value"]
                # Arvame välja ajaväljendid, mis pole piisavalt täpselt esitatud, näiteks 20. sajand
                if not("text" in ajaväljend.keys() and ("ndat" in ajaväljend["text"] or "sajand" in ajaväljend["text"])):
                    # Aasta osa, kasutades funktsioon stringNumbriks
                    aasta = stringNumbriks(val)
                    # Lisame aastate loendisse
                    aastad.append(aasta)
                    # Eraldame osadeks
                    jupid = val.split("-")
                    # Kui rohkem kui ühest osast koosnev
                    if(len(jupid)>1):
                        # Lisame kaks esimest osa kuude loendisse
                        aastadKuud.append((jupid[0]+"-"+jupid[1]))
                    # Kui rohkem kui kahest jupist koosnev
                    if(len(jupid)>2):
                        # Lisame väärtuse kuupäevade loendisse
                        aastadKuudKuupäevad.append(val)
        # Käsitleme ja ajavahemikke, mille otspunktid on aastad
        elif(ajaväljend["type"]=="DURATION" and ajaväljend["value"]=="PXXY"):
            if(ajaväljend["temporal_function"]==True):
                # Leiame otspunktide algus ja lõpp-punktid
                algus = ajaväljend["begin_point"]
                lõpp = ajaväljend["end_point"]
                algusv = ""
                algusabs = False
                lõppv = ""
                lõppabs = False
                # Läbime uuesti ajaväljendite loendit
                for aj in artikkel[2]:
                    # Kui ajaväljendi identifikaator läheb kokku määratud otspunktiga
                    if(aj["tid"]==algus):
                        # Määrame väärtuse
                        algusv = aj["value"]
                        # Määrame, kas tegemist on absoluutsega
                        if(aj["temporal_function"]==False):
                            algusabs=True
                    if(aj["tid"]==lõpp):
                        lõppv = aj["value"]
                        if(aj["temporal_function"]==False):
                            lõppabs=True
                    # Kui mõlemad otspunktid leitud
                    if(algusv != "" and lõppv != ""):
                        break
                # Loome ajavahemiku mõlemast otspunktist
                ajv = str(algusv) + "-" + str(lõppv)
                # Kui mõlemad otspunktid absoluutsed
                if(algusabs==True and lõppabs==True):
                    # Siis lisame ajavahemike hulka
                    ajavahemikud.append(ajv)
    # Määrame artikli alumise piiri, millele liidame 15 ja ülemise piir, vastavalt sünni- ja surma-aastatele
    alumine = stringNumbriks(artikkel[3][0])+15
    ülemine = stringNumbriks(artikkel[3][1])
    # Kui surma-aasta määramata
    if(stringNumbriks(ülemine) == 0):
        # Kui sünni-aasta viimase 115 aasta sees
        if(stringNumbriks(alumine) > 1915):
            # Siis ülemine piir 2016
            ülemine = 2016
    # Tagastame artikli nime,alumise piiri, ülemise piiri, aastate loendi, aasta ja kuude loendi, aasta ja kuu ja kuupäevade loendi ja ajavahemikud
    return (artikkel[0],alumine,ülemine,aastad,aastadKuud,aastadKuudKuupäevad,ajavahemikud)

# Funktsioon, mis võimaldab esimese argumendina etteantud korpuse kaustast asuvatel failidel moodustada uus korpus teise argumendina antud kausta võrdlemiseks, mis sisaldab vastavalt funktsioonile artiklist võrdlemiseks vajalikke
#tulemusi,kolmanda argumendina antud minimaalne aastaliste ajaväljendite arv ehk minimaalne võrdlemiseks sobivate ajaväljendite arv, mida artikkel peab sisaldama, neljanda argumendina antud sünniaasta alumine piir, millest sünniaasta
#peab hilisem olema ja viienda argumendina sünniaasta ülemine piir, millest sünniaasta peab varasem olema
def moodustakorpus(algkaust,tulemuskaust,aastatearv,sünnivahemikalumine,sünnivahemikülemine):
    # Loeme kõik korpuse kausta failid loendisse
    algandmed = andmeteLoend(algkaust)
    # Läbime kõik artikli failid
    for art in algandmed:
        # Eraldame vajaliku info artiklist kasutades funktsioon artiklist
        artikl = artiklist(art)
        # Kui vastab nõuetele
        if((artikl[1]-15)>=sünnivahemikalumine and (artikl[1]-15)<=sünnivahemikülemine and len(artikl[3])>=aastatearv and artikl[1] != 15):
            # Kirjutame vastavad andmed eraldi TXT-faili ette antud moodustatava korpuse kausta
            andmedFaili(artikl,tulemuskaust)

# Funktsioon kahe artikli vahelise kauguse leidmiseks, artiklid peavad olema pärit moodustatud võrdluskorpuse kaustast või funktsiooniga artiklist läbi töötletud.
def kaugusfunktsioon(artikkel1,artikkel2):
    # Loeme mõlema artikli aastate loendid
    artikkel1Aastad = artikkel1[3]
    artikkel2Aastad = artikkel2[3]
    # Loeme mõlema artikli aastast ja kuust koosnevate ajaväljendite loendid
    artikkel1AastadKuud = artikkel1[4]
    artikkel2AastadKuud = artikkel2[4]
    # Loeme mõlema artikli aastast, kuust ja kuupäevast koosnevate ajaväljendite loendid
    artikkel1AastadKuudKuupäevad = artikkel1[5]
    artikkel2AastadKuudKuupäevad = artikkel2[5]
    # Loeme mõlema artikli ajavahemike loendid 
    artikkel1Ajavahemikud = artikkel1[6]
    artikkel2Ajavahemikud = artikkel2[6]
    # Loome loenditest hulkade ühendi, et saada vastavate ajaväljendite esinemised esimeses või teises artiklis
    esinevadAastad = list(set(artikkel1Aastad + artikkel2Aastad))
    # Sorteerime vastavad loodud hulgad, mis on selleks uuesti loendi kujule viidud, aastad võib sorteerida tavaliset sort() funktsiooniga, sest need on numbrilisel kujul
    esinevadAastad.sort()
    esinevadAastadKuud = list(set(artikkel1AastadKuud + artikkel2AastadKuud))
    # Ülejäänute puhul peab kasutama loodud funktsiooni sorteerimise jaoks, mis ajaväljendid stringide kujul vastavalt väärtustab
    esinevadAastadKuud.sort(key=sortimisfunktsioon)
    esinevadAastadKuudKuupäevad = list(set(artikkel1AastadKuudKuupäevad + artikkel2AastadKuudKuupäevad))
    esinevadAastadKuudKuupäevad.sort(key=sortimisfunktsioon)
    esinevadAjavahemikud = list(set(artikkel1Ajavahemikud + artikkel2Ajavahemikud))
    esinevadAjavahemikud.sort(key=sortimisfunktsioon)
    # Muutujad nelja erineva arvutatava kauguse jaoks
    kaugus = 0
    kauguskuud = 0
    kauguskuudpäev = 0
    kaugusajavahemikud = 0
    # Esimene summa, aastaarvuliste ajaväljendite peal arvutatav, tsükkel (summa), kus i on nullist kuni elementide arvuni hulgas esinevadAastad - 1
    for i in range(0,len(esinevadAastad)):
        # Vahesumma muutuja
        vahesum = 0
        # tsükkel(summa) kus j on nullist kuni i-ni
        for j in range(0,i+1):
            # Määrame j-ile vastava elemendi hulgast esinevadAastad
            a = esinevadAastad[j]
            # Vahesummale liidame elemendi esinemise esimeses artiklis lahutada esinemine teises artiklis
            vahesum += artikkel1Aastad.count(a) - artikkel2Aastad.count(a)
        # Liidame kogusummale vahesumma absoluutväärtuse
        kaugus += abs(vahesum)
    # Samasugune summa aastast ja kuust koosnevate ajaväljendite peal
    for i in range(0,len(esinevadAastadKuud)):
        vahesum = 0
        for j in range(0,i+1):
            a = esinevadAastadKuud[j]
            vahesum += artikkel1AastadKuud.count(a) - artikkel2AastadKuud.count(a)
        kauguskuud += abs(vahesum)
    # Samasugune summa aastast , kuust ja kuupäevast koosnevate ajaväljendite peal
    for i in range(0,len(esinevadAastadKuudKuupäevad)):
        vahesum = 0
        for j in range(0,i+1):
            a = esinevadAastadKuudKuupäevad[j]
            vahesum += artikkel1AastadKuudKuupäevad.count(a) - artikkel2AastadKuudKuupäevad.count(a)
        kauguskuudpäev += abs(vahesum)
    # Samasugune summa ajavahemike peal
    for i in range(0,len(esinevadAjavahemikud)):
        vahesum = 0
        for j in range(0,i+1):
            a = esinevadAjavahemikud[j]
            vahesum += artikkel1Ajavahemikud.count(a) - artikkel2Ajavahemikud.count(a)
        kaugusajavahemikud += abs(vahesum)
    # Kui aastast ja kuust koosnevaid ajaväljendeid esines
    if(len(esinevadAastadKuud)>0):
        # Siis nende peal leitud kauguse korrutame läbi täisarvuga aastaarvuliste ajaväljendite hulga elementide arvust jagada aastast ja kuust koosnevate ajaväljendite elementide arvuga, et tõsta aastast ja kuust koosnevate
        # ajaväljendite kauguste väärtust ja võtta rohkem arvesse ka artiklite vastavate ajaväljendite sisalduse struktuuri. Mida rohkem kokkulangevaid, seda madalam kaugus, mida rohkem aastast ja kuust koosnevaid ajaväljendeid
        # seda madalam korrutatav tegur ja läbi selle madalam kaugus.
        kauguskuud = kauguskuud * int(len(esinevadAastad)/len(esinevadAastadKuud))
    # Sama aastast, kuust ja kuupäevast koosnevate ajaväljenditega ja nende pealt arvutatava kauguseda
    if(len(esinevadAastadKuudKuupäevad)>0):
        kauguskuudpäev = kauguskuudpäev * int(len(esinevadAastad)/len(esinevadAastadKuudKuupäevad))
    # Sama ajavahemikega
    if(len(esinevadAjavahemikud)>0):
        kaugusajavahemikud = kaugusajavahemikud * int(len(esinevadAastad)/len(esinevadAjavahemikud))
    # Kogu kaugus moodustub nende nelja arvutatava kauguse summana
    kaugus = kaugus+kauguskuud+kauguskuudpäev+kaugusajavahemikud
    # Tagastame kogu kauguse
    return kaugus

# Funktsioon, mis leiab kahe artikli vahel kattuvad ajaväljendid, kus artiklid on pärit loetud võrdluskorpusest või saadud andmete korpusest failidest, mis on läbi töödeldud funktsiooniga artiklist
def kattuvadväljendid(artikkel1,artikkel2):
    # Loeme vastavad loendid mõlemast artiklist
    artikkel1Aastad = artikkel1[3]
    artikkel2Aastad = artikkel2[3]
    artikkel1AastadKuud = artikkel1[4]
    artikkel2AastadKuud = artikkel2[4]
    artikkel1AastadKuudKuupäevad = artikkel1[5]
    artikkel2AastadKuudKuupäevad = artikkel2[5]
    artikkel1Ajavahemikud = artikkel1[6]
    artikkel2Ajavahemikud = artikkel2[6]
    # Leimae kahe artikli vaheliste esinevate aastaarvuliste ajaväljendite hulkade ühisosa, mis moodustavad kattuvad aastaarvulise ajaväljendid
    aastadKattuvad = list(set(artikkel1Aastad).intersection(set(artikkel2Aastad)))
    # Sama aastast ja kuust koosnevate puhul
    aastadKuudKattuvad = list(set(artikkel1AastadKuud).intersection(set(artikkel2AastadKuud)))
    # Sama aastast, kuust ja kuupäevast koosnevate puhul
    aastadKuudKuupäevadKattuvad = list(set(artikkel1AastadKuudKuupäevad).intersection(set(artikkel2AastadKuudKuupäevad)))
    # Sama ajavahemike puhul
    ajavahemikudKattuvad = list(set(artikkel1Ajavahemikud).intersection(set(artikkel2Ajavahemikud)))
    # Liidame kõik hulgad, mis on uuesti viidud loendite kujule kokku
    kokkuseotud = aastadKattuvad + aastadKuudKattuvad + aastadKuudKuupäevadKattuvad + ajavahemikudKattuvad
    # Tagastame koguloendi
    return kokkuseotud

# Funktsioon , mis esimese parameetrina etteantud artiklile(võrdluskorpusest või funktsiooniga artiklist läbi töödeldud andmekorpusest) leiab viis sarnasemat artiklit ajavahemike kauguse mõttes vastavalt funktsioonil kaugusfunktsioon
# Teise parameetrina ette antud korpus ehk võrdluskorpus, mille seest sarnaseid otsitakse ja kolmanda parameetrina miinimum ajaväljendite arv, mis kahes artiklis peavad kattuma.
def leiaSarnased(artikkel,korpus, miinimumkattuvaid = 0):
    # Väljastame artikli nime
    print("###################################################################")
    print("artikkel - "+artikkel[0])
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # Sarnasemad 5
    print("Sarnasemad 5:")
    # Määrame artikli alumise ja ülemise piiri
    aluminepiir = artikkel[1]
    üleminepiir= artikkel[2]
    sarnasemad5 = []
    # Loeme korpuse
    # Läbime ükshaaval võrdluskorpusest artiklid
    for artikl in korpus:
        # Määrame võrreldava artikli piirid
        alumineart = artikl[1]
        ülemineart = artikl[2]
        # Kui artikli nimi ei võrdu võrreldava artikli nimega
        if (artikl[0] != artikkel[0]):
            # Kui võrreldava artikli alumine piir või ülemine piir jäävad otsitava artikli piiride vahele.
            if((alumineart >= aluminepiir and alumineart <=üleminepiir) or (ülemineart >= aluminepiir and ülemineart <=üleminepiir)):
                # Kui kahe artikli vahel kattuvate ajaväljendite arv on suurem või võrdne minimaalse nõutuga
                if(len(kattuvadväljendid(artikkel,artikl))>=miinimumkattuvaid):
                    # Määrame võrreldava artikli nime
                    nimi = artikl[0]
                    # Arvutame kahe artikli vahelise kauguse kasutades kaugusfunktsiooni
                    kaugus = kaugusfunktsioon(artikkel,artikl)
                    # Kui sarnasema 5 loendis on vähem kui 5 artiklit
                    if(len(sarnasemad5) <5):
                        # Siis lisame loendisse artikli ja kauguse
                        sarnasemad5.append((artikl,kaugus))
                    # Vastasel juhul
                    else:
                        # Võrdleme sarnasema viie loendis viimasel kohal olevat kaugust leitud hetke artikli kaugusega, kui viimasel kohal kaugus on suurem, siis vahetame hetke leitud artikli ja kauguse viimasele kohale loendis
                        if(sarnasemad5[4][1] > kaugus):
                            sarnasemad5[4] = (artikl,kaugus)
                            # Sorteerime loendi vastavalt kaugustele, et väiksemad kaugused eespool
                            sarnasemad5.sort(key = lambda x: x[1])
    # Sorteerime veelkord, et kui ei leitud üle viie sarnasema, siis oleks kaugused sorteeritud
    sarnasemad5.sort(key = lambda x: x[1])
    # Väljastame ekraanile vastavalt ajaväljendite põhjal leitud kauguse poolest viis sarnasemat
    for sarnane in sarnasemad5:
        # Leitud artikli nimi ja kaugus
        print(sarnane[0][0] + ", kaugus:" + str(sarnane[1]))
        # Kattuvad ajaväljendid
        print("Kattuvad ajaväljendid:")
        print(kattuvadväljendid(artikkel,sarnane[0]))
        print("--------------------------------------------------------------------")
    print("###################################################################")

# Funktsioon valimaks esimese parameetrina antud korpuse peal juhuslikult valitud kolmanda parameetrina antud arvu artikleid, millel on leitud viis sarnasemat artiklit ajaväljendite põhise kauguse järgi, kus igal sarnasemal artiklil
# peab olema vähemalt teise parameetrina antud arv otsitava artikliga kattuvaid ajaväljendeid 
def juhuslikud(korpuskaust,juhuslikke=1,miinimumkattuvaid=0):
    # Juhuslike loend
    juhux = []
    korpus = andmeteLoend(korpuskaust)
    # Seni kuni loendi pikkus on väiksem, kui parameetrina antavate artiklite pikkus
    while(len(juhux)<juhuslikke or len(korpus)==len(juhux)):
        # Juhuslik number nullist kuni korpuses olevate artiklite arvuni lahutada 1
        juhunumb = randint(0,len(korpus)-1)
        # Kui juba antud artikkel ei leidu juhuslikult valitud artiklite seas
        if(korpus[juhunumb] not in juhux):
            # Lisame loendisse
            juhux.append(korpus[juhunumb])
    # Läbime juhuslikud valitud artiklite loendi
    for j in juhux:
        # kasutades funktsiooni leiaSarnased leiame igale juhuslikult valitud artiklile viis sarnasemat.
        leiaSarnased(j,korpus,miinimumkattuvaid)
                       


if __name__ == "__main__":
    try:
        p = sys.argv[1]
        if(p=="-moodustakorpus"):
            try:
                algkaust = sys.argv[2]
                tulemuskaust = sys.argv[3]
                ajav = sys.argv[4]
                sündalu = sys.argv[5]
                sündüle = sys.argv[6]
            except IndexError:
                print("Ette antud puudulik arv argumente antud käsu täitmiseks, palun vaadata skripti kasutusjuhendit failist sarnased_juhend.txt!")
                sys.exit(-1)
            if not os.path.exists(algkaust):
                print("Esimese parameetrina etteantud algkausta ei leitud")
                sys.exit(-1)
            if not os.path.exists(tulemuskaust):
                print("Teise parameetrina etteantud sihtkausta ei leitud")
                sys.exit(-1)
            try:
                ajav = int(ajav)
                sündalu = int(sündalu)
                sündüle = int(sündüle)
            except ValueError:
                print("Kolmanda, neljanda ja viienda parameetrina ette antavad väärtused peavad olema täisarvulisel kujul!")
                sys.exit(-1)
            print("Moodustatakse võrdluskorpus kausta: " + algkaust + " artiklitest kausta: " + tulemuskaust + " , millel on vähemalt: " + str(ajav) + " võrreldavat ajaväljendit ja mille sünniaasta on hilisem aastast: " + str(sündalu)+
                  " ja varasem aastast: "+ str(sündüle))
            moodustakorpus(algkaust,tulemuskaust,ajav,sündalu,sündüle)
            sys.exit(-1)
        elif(p=="-kaugusfunktsioon"):
            try:
                esimeneartikkel = sys.argv[2].replace("_"," ")
                teineartikkel = sys.argv[3].replace("_"," ")
            except IndexError:
                print("Ette antud puudulik arv argumente antud käsu täitmiseks, palun vaadata skripti kasutusjuhendit failist sarnased_juhend.txt!")
                sys.exit(-1)
            if not os.path.exists(esimeneartikkel):
                print("Esimese parameetrina etteantud artiklit ei leitud")
                sys.exit(-1)
            if not os.path.exists(teineartikkel):
                print("Teise parameetrina etteantud artiklit ei leitud")
                sys.exit(-1)
            esimeneartikkel = andmedFailist(esimeneartikkel)
            teineartikkel = andmedFailist(teineartikkel)
            kaugus = kaugusfunktsioon(esimeneartikkel,teineartikkel)
            print("Kahe ette antud artikli ajaväljendite põhjal arvutatav kaugus on: " + str(kaugus))
            sys.exit(-1)
        elif(p=="-leiasarnased"):
            try:
                artikkel1 = sys.argv[2].replace("_"," ")
                võrdluskorpus1 = sys.argv[3]
            except IndexError:
                print("Ette antud puudulik arv argumente antud käsu täitmiseks, palun vaadata skripti kasutusjuhendit failist sarnased_juhend.txt!")
                sys.exit(-1)
            if not os.path.exists(artikkel1):
                print("Esimese parameetrina etteantud artiklit ei leitud")
                sys.exit(-1)
            if not os.path.exists(võrdluskorpus1):
                print("Teise parameetrina etteantud korpuse kausta ei leitud")
                sys.exit(-1)
            artikkel = andmedFailist(artikkel1)
            võrdluskorpus = andmeteLoend(võrdluskorpus1)
            try:
                miinimumkattuvaid = sys.argv[4]
                try:
                    miinimumkattuvaid = int(miinimumkattuvaid)
                    print("Leitakse artiklile: " + artikkel1 + "viis ajaväljendite põhjal sarnasemat võrdluskorpusest: "+ võrdluskorpus1 + ", millel on vähemalt: "+str(miinimumkattuvaid) + " kattuvat ajaväljendit.")
                    leiaSarnased(artikkel,võrdluskorpus,miinimumkattuvaid)
                    sys.exit(-1)
                except ValueError:
                    print("Kolmanda parameetrina ette antud miinimum kattuvate ajaväljendite arv peab olema täisarvulisel kujul")
                    sys.exit(-1)
            except IndexError:
                print("Leitakse artiklile: " + artikkel1 + "viis ajaväljendite põhjal sarnasemat võrdluskorpusest: "+ võrdluskorpus1 + ", millel on vähemalt 0 kattuvat ajaväljendit.")
                leiaSarnased(artikkel,võrdluskorpus)
                sys.exit(-1)
        elif(p=="-juhuslikud"):
            try:
                võrdluskorpus = sys.argv[2]
            except IndexError:
                print("Ette antud puudulik arv argumente antud käsu täitmiseks, palun vaadata skripti kasutusjuhendit failist sarnased_juhend.txt!")
                sys.exit(-1)
            if not os.path.exists(võrdluskorpus):
                print("Esimese parameetrina etteantud korpuse kausta ei leitud")
                sys.exit(-1)
            try:
                juhuslikke = sys.argv[3]
            except IndexError:
                print("Väljastatakse võrdluskorpusest: "+võrdluskorpus + " 1 juhuslikult valitud artikli 5 sarnasemat artiklit, millega valitud artiklil on vähemalt: 0 kattuvat ajaväljendit.")
                juhuslikud(võrdluskorpus)
                sys.exit(-1)
            try:
                juhuslikke = int(juhuslikke)
            except ValueError:
                print("Teise parameetrina ette antud juhuslike artiklite arv peab olema esitatud täisarvuna!")
                sys.exit(-1)
            try:
                miinimum = sys.argv[4]
            except IndexError:
                print("Väljastatakse võrdluskorpusest: "+võrdluskorpus + " " + str(juhuslikke) + " juhuslikult valitud artikli 5 sarnasemat artiklit, millega valitud artiklil on vähemalt: 0 kattuvat ajaväljendit.")
                juhuslikud(võrdluskorpus,juhuslikke)
                sys.exit(-1)
            try:
                miinimum = int(miinimum)
            except ValueError:
                print("Kolmanda parameetrina ette antud miinimum kattuvate ajaväljendite arv peab olema esitatud täisarvuna!")
                sys.exit(-1)
            print("Väljastatakse võrdluskorpusest: "+võrdluskorpus + " " + str(juhuslikke) + " juhuslikult valitud artikli 5 sarnasemat artiklit, millega valitud artiklil on vähemalt: "+ str(miinimum) + " kattuvat ajaväljendit.")
            juhuslikud(võrdluskorpus,juhuslikke,miinimum)
            sys.exit(-1)
        else:
            print("Esimese argumendina tuleb anda käsk -moodustakorpus või -kaugusfunktsioon või -leiasarnased või -juhuslikud, täpsema kasutusinfo jaoks vaata faili sarnased_juhend.txt!")
            sys.exit(-1)
    except IndexError:
        print("Esimese argumendina tuleb anda käsk -moodustakorpus või -kaugusfunktsioon või -leiasarnased või -juhuslikud, täpsema kasutusinfo jaoks vaata faili sarnased_juhend.txt!")
        sys.stderr.write(about)
        sys.exit(-1)
    


