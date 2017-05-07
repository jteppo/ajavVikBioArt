#!/usr/bin/env python

# Autor - Jaan Teppo

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys,os
# Skript bakalaureusetöö graafikute moodustamiseks, graafikute moodustamiseks peab eelnevalt olema kausta ./statistka/ moodustatud statistikafailid skripti sagedusJaMuuStatistika.py abil.
# Eeskujuks on võetud artiklis http://pbpython.com/visualization-tools-1.html (Vaadatud 03.05.2017) postitatud Seaborni kohta käiv näide. Artikli autor Chris Moffitt.
# Iga graafiku jaoks on eraldi funktsioon, kus on kasutatud teeki Pandas, et lugeda sisse vastava graafiku jaoks csv fail, seejärel, kui ei ole soovitud kogu andmeid,
# siis määratud piirkond, millises ulatuses ja kasutades teeki Seaborn vastavalt kutsudes funktsioon graafiku tüübi jaoks, mida soovitud, on vastavalt argumentidena sisse antud statistika osad.

# Tulpdiagramm, kogu tekstide 19 sajandi kümnendite sagedusloendi pealt
def kogusajand19kümnendidgraafik():
    kymnend = pd.read_csv("./statistika/kogusajand19kümnendid.csv",sep="|")
    kymnend = kymnend.sort("kymnend",ascending = True)
    sns.set_style("darkgrid")
    bar_plot = sns.barplot(x=kymnend["kymnend"],y=kymnend["arv"],
                           palette="muted",
                           order = kymnend["kymnend"].tolist())
    ax = bar_plot.axes
    # Määrame telgede tähised, vähendame suurust
    ax.set_xticklabels(kymnend["kymnend"],size=9)
    # Määrame telgede nimed
    ax.set_ylabel('esinemiste arv')
    ax.set_xlabel('kümnend')
    plt.savefig("./graafikud/kogusajand19kümnendidgraafik.png")

# Tulpdiagramm, kogu tekstide 20 sajandi kümnendite sagedusloendi pealt
def kogusajand20kümnendidgraafik():
    kymnend = pd.read_csv("./statistika/kogusajand20kümnendid.csv",sep="|")
    kymnend = kymnend.sort("kymnend",ascending = True)
    sns.set_style("darkgrid")
    bar_plot = sns.barplot(x=kymnend["kymnend"],y=kymnend["arv"],
                           palette="muted",
                           order = kymnend["kymnend"].tolist())
    ax = bar_plot.axes
    ax.set_xticklabels(kymnend["kymnend"],size=9)
    ax.set_ylabel('esinemiste arv')
    ax.set_xlabel('kümnend')
    plt.savefig("./graafikud/kogusajand20kümnendidgraafik.png")

# Jaotusgraafik, mis näitab artiklite sünniaastate paigutust vastavalt ajaväljendite arvule kogu tekstide korpuse peal
def koguajaväljendeidjasünniaastadgraafik():
    andmed = pd.read_csv("./statistika/koguajaväljendidjasünniaasta.csv",sep="|")
    sns.set_style("darkgrid")
    reg_plot = sns.regplot(x=andmed["synd"],y=andmed["ajavaljendeid"],
                           fit_reg=False,marker='.')
    ax = reg_plot.axes
    # Piirjooned 0-1500 ajaväljendite arvul, et paremini jagunemist näha ( Välja jäetud 3 artiklit ~1600,2600,3000 ajaväljendiga)
    ax.set_ylim(0,1500)
    ax.set_ylabel("ajaväljendeid")
    ax.set_xlabel("sünniaasta")
    plt.savefig("./graafikud/koguajaväljendeidjasündgraafik.png")    


# Sünniaastate histogramm
def sünnihistogramm():
    # Sünniaastad on 
    sünnid = pd.read_csv("./statistika/kogusünniaastadhistogram.csv",sep="|")
    sns.set_style("darkgrid")
    # Kasutame funktsiooni distplot histogrammi jaoks
    dist_plot = sns.distplot(sünnid,kde=False,color="g")
    ax = dist_plot.axes
    ax.set_yscale('log')
    ax.set_ylabel('esinemiste arv (log kujul)')
    ax.set_xlabel('sünniaasta')
    plt.savefig("./graafikud/sünniaastatehistogramm.png")
# Kogu tekstide korpuse aastaarvuliste ajaväljendite histogramm
def koguaastadhistogramm():
    sünnid = pd.read_csv("./statistika/koguaastadhistogram.csv",sep="|")
    sns.set_style("darkgrid")
    dist_plot = sns.distplot(sünnid,kde=False,color="g")
    ax = dist_plot.axes
    # Logaritmilisele kujule y-telg
    ax.set_yscale('log')
    ax.set_ylabel('esinemiste arv (log kujul)')
    ax.set_xlabel('aasta')
    # Määrame x-telje tähised, et iga samm oleks 500 aasta tagant, nagu oli sünniaastatel ja vähendame kirjasuurust
    ax.set_xticklabels([-4000,-3500,-3000,-2500,-2000,-1500,-1000,-500,0,500,1000,1500,2000,2500,3000,3500,4000],size=9)
    ax.set_xticks([-4000,-3500,-3000,-2500,-2000,-1500,-1000,-500,0,500,1000,1500,2000,2500,3000,3500,4000])
    plt.savefig("./graafikud/koguaastatehistogramm.png")    


# Tulpdiagramm kümnest kõige enam levinud surma-aastast
def surmaaaastadgraafik():
    andmed = pd.read_csv("./statistika/kogusurmaaastad.csv",sep="|")
    andmed = andmed.sort("arv",ascending = False)[1:11]
    sns.set_style("darkgrid")
    bar_plot = sns.barplot(x=andmed["arv"],y=andmed["surmaaasta"],
                           palette="muted",orient="h",
                           order = andmed["surmaaasta"].tolist())
    ax = bar_plot.axes
    ax.set_ylabel('surma-aasta')
    ax.set_xlabel('esinemiste arv')
    plt.savefig("./graafikud/surmaaastadgraafik.png")


# Järgnevad funktsioonid on graafikute jaoks, mida töös otseselt ei kasutatud, aga uurimise käigus siiski loodi
# Tulpdiagramm kümnest kõige enam levinud ajaväljendi väärtusest välja jäetud sektsioonidega tekstide korpusel
def filtreeritudvaluegraafik():
    andmed = pd.read_csv("./statistika/lisa/filtreeritudsagedusloendvalue.csv",sep="|")
    andmed = andmed.sort("arv",ascending = False)[:10]
    sns.set_style("darkgrid")
    bar_plot = sns.barplot(x=andmed["arv"],y=andmed["value"],
                           palette="muted",orient="h",
                           order = andmed["value"].tolist())
    plt.savefig("./graafikud/lisa/filtreeritudvaluegraafik.png")

# Tulpdiagramm kümnest kõige enam levinud sünniaastast
def sünniaastadgraafik():
    andmed = pd.read_csv("./statistika/kogusünniaastad.csv",sep="|")
    # Esikohal määramata sünniaastaga artiklid, ehk see välja jäetud
    andmed = andmed.sort("arv",ascending = False)[1:11]
    sns.set_style("darkgrid")
    bar_plot = sns.barplot(x=andmed["arv"],y=andmed["synniaasta"],
                           palette="muted",orient="h",
                           order = andmed["synniaasta"].tolist())
    plt.savefig("./graafikud/lisa/sünniaastadgraafik.png")

# Jaotusgraafik, mis väljendab sõnade arve artiklist ja vastavalt ajaväljendite arve
def sõnujaajaväljendeidgraafik():
    andmed = pd.read_csv("./statistika/lisa/kogusõnadejaajaväljenditearv.csv",sep="|")
    sns.set_style("darkgrid")
    reg_plot = sns.regplot(x=andmed["sonu"],y=andmed["ajavaljendeid"])
    ax = reg_plot.axes
    # Testitud piirkondade piiramisega, et paremini näha jagunemist
    ax.set_ylim(0,100)
    ax.set_xlim(0,2000)           
    plt.savefig("./graafikud/lisa/kogusõnujaajaväljendeidgraafik.png")

# Jaotusgraafik, mis näitab artiklite sünniaastate paigutust vastavalt ajaväljendite arvule välja jäetud sektsioonidega tekstide korpuse peal
def filtreeritudajaväljendeidjasünniaastadgraafik():
    andmed = pd.read_csv("./statistika/filtreeritudajaväljendidjasünniaasta.csv",sep="|")
    sns.set_style("darkgrid")
    reg_plot = sns.regplot(x=andmed["synd"],y=andmed["ajavaljendeid"],
                           fit_reg=False,marker = '.')
    ax = reg_plot.axes
    ax.set_ylim(0,600)
    ax.set_ylabel("ajaväljendeid")
    ax.set_xlabel("sünniaasta")
    plt.savefig("./graafikud/lisa/filtreeritudajaväljendeidjasündgraafik.png") 
# Tulpdiagramm välja jäetud lõpusektsioonidega tekstidega andmete pealt moodustatud sajandite sagedusloendist
def filtreeritudsajandidgraafik():
    sajandid = pd.read_csv("./statistika/filtreeritudsagedusloendsajandid.csv",sep="|")
    sajandid = sajandid.sort("sajand",ascending = True)[:22]
    # Määratud graafiku taust/stiil
    sns.set_style("darkgrid")
    # Kasutatud tulpdiagrammi loomiseks vastavat funktsiooni
    bar_plot = sns.barplot(x=sajandid["sajand"],y=sajandid["arv"],
                           palette="muted",
                           order = sajandid["sajand"].tolist())
    # Graafiku salvestamine .png failina kausta graafikud
    plt.savefig("./graafikud/lisa/filtreeritudsajandidgraafik.png")
# Tulpdiagramm, kogu tekstidega andmete pealt loodud sajandite sagedusloendist
def kogusajandidgraafik():
    sajandid2 = pd.read_csv("./statistika/kogusagedusloendsajandid.csv",sep="|")
    sajandid2 = sajandid2.sort("sajand",ascending = True)[:22]
    sns.set_style("darkgrid")
    bar_plot = sns.barplot(x=sajandid2["sajand"],y=sajandid2["arv"],
                           palette="muted",
                           order = sajandid2["sajand"].tolist())
    ax = bar_plot.axes
    # Määratud y-skaala logaritmiliseks
    ax.set_yscale('log')
    plt.savefig("./graafikud/lisa/kogusajandidgraafik.png")

# Tulpdiagramm, välja jäetud lõpusektsioonidega tekstide 19 sajandi kümnendite sagedusloendi pealt
def filtreeritudsajand19kümnendidgraafik():
    kymnend = pd.read_csv("./statistika/filtreeritudsajand19kümnendid.csv",sep="|")
    kymnend = kymnend.sort("kymnend",ascending = True)
    sns.set_style("darkgrid")
    bar_plot = sns.barplot(x=kymnend["kymnend"],y=kymnend["arv"],
                           palette="muted",
                           order = kymnend["kymnend"].tolist())
    ax = bar_plot.axes
    ax.set_xticklabels(kymnend["kymnend"],size=9)
    plt.savefig("./graafikud/lisa/filtreeritudsajand19kümnendidgraafik.png")

# Tulpdiagramm, välja jäetud lõpusektsioonidega tekstide 19 sajandi kümnendite sagedusloendi pealt
def filtreeritudsajand20kümnendidgraafik():
    kymnend = pd.read_csv("./statistika/filtreeritudsajand20kümnendid.csv",sep="|")
    kymnend = kymnend.sort("kymnend",ascending = True)
    sns.set_style("darkgrid")
    bar_plot = sns.barplot(x=kymnend["kymnend"],y=kymnend["arv"],
                           palette="muted",
                           order = kymnend["kymnend"].tolist())
    ax = bar_plot.axes
    ax.set_xticklabels(kymnend["kymnend"],size=9)
    plt.savefig("./graafikud/lisa/filtreeritudsajand20kümnendidgraafik.png")

# Välja jäetud sektsioonidega tekstide korpuse aastaarvuliste ajaväljendite histogramm
def filtreeritudaastadhistogramm():
    sünnid = pd.read_csv("./statistika/filtreeritudaastadhistogram.csv",sep="|")
    sns.set_style("darkgrid")
    dist_plot = sns.distplot(sünnid,kde=False,color="g")
    ax = dist_plot.axes
    ax.set_yscale('log')
    ax.set_ylabel('esinemiste arv')
    ax.set_xlabel('aasta')
    ax.set_xticklabels([-4000,-3500,-3000,-2500,-2000,-1500,-1000,-500,0,500,1000,1500,2000,2500,3000,3500],size=9)
    ax.set_xticks([-4000,-3500,-3000,-2500,-2000,-1500,-1000,-500,0,500,1000,1500,2000,2500,3000,3500])
    plt.savefig("./graafikud/lisa/filtreeritudaastatehistogramm.png")
# Tulpdiagramm kümnest kõige enam levinud ajaväljendi väärtusest kogu tekstide korpusel 
def koguvaluegraafik():
    andmed = pd.read_csv("./statistika/lisa/kogusagedusloendvalue.csv",sep="|")
    # Esimesed 10
    andmed = andmed.sort("arv",ascending = False)[:10]
    sns.set_style("darkgrid")
    # orient = horisontaalse suunaga, et parem väljanägemine
    bar_plot = sns.barplot(x=andmed["arv"],y=andmed["value"],
                           palette="muted",orient="h",
                           order = andmed["value"].tolist())
    plt.savefig("./graafikud/lisa/koguvaluegraafik.png")

# Peameetod graafikute loomise välja kutsumiseks käsurealt, sisestavate käskude jaoks vaadata graafikud_juhend.txt faili
if __name__ == "__main__":
    try:
        p = sys.argv[1]
        # Kontrollime kausta graafikud olemasolu
        if not os.path.exists("./graafikud/"):
            print("Skriptiga samas kaustas puudub kaust graafikud, palun luua kaust enne skripti taaskäivitamist!")
            sys.exit(-1)
        # Kontrollime kaustas graafikud kausta lisa olemasolu
        if not os.path.exists("./graafikud/lisa/"):
            print("Skriptiga samas kaustas asuvas kaustas graafikud puudub kaust lisa, palun luua enne skripti taaskäivitamist!")
            sys.exit(-1)
        # Sünniaastate histogrammi loomiseks
        if(p=="-sünnihistogramm"):
            sünnihistogramm()
            print("Loodi sünniaastate histogramm kausta ./graafikud/ nimega sünniaastatehistogramm.png")
            sys.exit(-1)
        # Kogu tekstide aastaarvuliste ajaväljendite histogrammi loomiseks
        if(p=="-koguaastadhistogramm"):
            koguaastadhistogramm()
            print("Loodi kogu tekstide korpuse aastaarvuliste ajaväljendite histogramm kausta ./graafikud/ nimega koguaastatehistogramm.png")
            sys.exit(-1)
        # Surma-aastate graafiku jaoks
        elif(p=="-surmaaastadgraafik"):
            surmaaaastadgraafik()
            print("Loodakse surma-aastate 10 sagedama esinemise graafik kausta ./graafikud/ nimega surmaaastadgraafik.png")
            sys.exit(-1)
        # Sünniaastate ja ajaväljendite arvu graafiku jaoks
        elif(p=="-koguajaväljendeidjasünniaastadgraafik"):
            koguajaväljendeidjasünniaastadgraafik()
            print("Loodi artiklite ajaväljendite arvud vastavalt sünniaastatele kogu tekstide korpuse peal graafik kausta ./graafikud/ nimega koguajaväljendeidjasündgraafik.png")
            sys.exit(-1)
        # 19 sajandi kümnendite jaotuse graafiku jaoks
        elif(p=="-kogusajand19kümnendidgraafik"):
            kogusajand19kümnendidgraafik()
            print("Loodi kogu tekstide korpuse 19. sajandi kümnendite jagunemise graafik kausta ./graafikud/ nimega kogusajand19kümnendidgraafik.png")
            sys.exit(-1)
        # 20 sajandi kümnendite jaotuse graafiku jaoks
        elif(p=="-kogusajand20kümnendidgraafik"):
            kogusajand20kümnendidgraafik()
            print("Loodi kogu tekstide korpuse 20. sajandi kümnendite jagunemise graafik kausta ./graafikud/ nimega kogusajand20kümnendidgraafik.png")
            sys.exit(-1)
        # 10 enam levinud väärtuse välja jäetud sektsioonidega tekstide peal
        elif(p=="-filtreeritudvaluegraafik"):
            filtreeritudvaluegraafik()
            print("Loodi välja jäetud lõpusektsioonidega tekstide korpuse 10 enam levinud väärtuse graafik kausta ./graafikud/lisa/ nimega filtreeritudvaluegraafik.png")
            sys.exit(-1)
        # 10 enam levinud väärtuse kogu tekstide peal
        elif(p=="-koguvaluegraafik"):
            koguvaluegraafik()
            print("Loodi kogu tekstide korpuse 10 enam levinud väärtuse graafik kausta ./graafikud/lisa/ nimega koguvaluegraafik.png")
            sys.exit(-1)
        # 10 enam levinud sünniaastat
        elif(p=="-sünniaastadgraafik"):
            sünniaastadgraafik()
            print("Loodi 10 enam levinud sünniaasta graafik kausta ./graafikud/lisa/ nimega sünniaastad.png")
            sys.exit(-1)
        # Sõnade arvude jaotus ja vastavate ajaväljendite arvude jaotus graafik
        elif(p=="-sõnujaajaväljendeidgraafik"):
            sõnujaajaväljendeidgraafik()
            print("Loodi artiklite sõnade arvude ja vastavalt ajaväljendite arvude graafik kausta ./graafikud/lisa/ nimega sõnujaajaväljendeidgraafik.png")
            sys.exit(-1)
        # Sünniaastate ja ajaväljendite jaotus välja jäetud sektsioonidega korpuse peal
        elif(p=="-filtreeritudajaväljendeidjasünniaastadgraafik"):
            filtreeritudajaväljendeidjasünniaastadgraafik()
            print("Loodi artiklite ajaväljendite arvud vastavalt sünniaastatele välja jäetud sektsioonidega tekstide korpuse peal graafik kausta ./graafikud/lisa/ nimega filtreeritudajaväljendeidjasündgraafik.png")
            sys.exit(-1)
        # Välja jäetud sektsioonidega korpuse sajandite jaotus
        elif(p=="-filtreeritudsajandidgraafik"):
            filtreeritudsajandidgraafik()
            print("Loodi välja jäetud lõpusektsioonidega korpuse sajandite jagunemise graafik kausta ./graafikud/lisa/ nimega filtreeritudsajandidgraafik.png")
            sys.exit(-1)
        # Kogu tekstidega korpuse sajandite jaotus
        elif(p=="-kogusajandidgraafik"):
            kogusajandidgraafik()
            print("Loodi välja jäetud sektsioonidega tekstidega korpuse sajandite jagunemise graafik kausta ./graafikud/lisa/ nimega kogusajandidgraafik.png")
            sys.exit(-1)
        # 19 sajandi kümnendite jaotuse graafiku jaoks välja jäetud lõpusektsioonidega teksti peal
        elif(p=="-filtreeritudsajand19kümnendidgraafik"):
            filtreeritudsajand19kümnendidgraafik()
            print("Loodi kogu tekstide korpuse 19. sajandi kümnendite jagunemise graafik kausta ./graafikud/lisa/ nimega filtreeritudsajand19kümnendidgraafik.png")
            sys.exit(-1)
        # 20 sajandi kümnendite jaotuse graafiku jaoks välja jäetud lõpusektsioonidega
        elif(p=="-filtreeritudsajand20kümnendidgraafik"):
            filtreeritudsajand20kümnendidgraafik()
            print("Loodi välja jäetud sektsioonidega tekstide korpuse 20. sajandi kümnendite jagunemise graafik kausta ./graafikud/lisa/ nimega filtreeritudsajand20kümnendidgraafik.png")
            sys.exit(-1)
        # Välja jäetud lõpusektsioonidega tekstide aastaarvuliste ajaväljendite histogrammi loomiseks
        elif(p=="-filtreeritudaastadhistogramm"):
            filtreeritudaastadhistogramm()
            print("Loodi välja jäetud lõpusektsioonidega tekstide korpuse aastaarvuliste ajaväljendite histogramm kausta ./graafikud/lisa/ nimega filtreeritudaastatehistogramm.png")
            sys.exit(-1)
        else:
            print("Sisestatud sisendit ei tuntud lubatud käsuna, palun vaadake graafikud_juhend.txt faili lubatud käskude jaoks")
            sys.exit(-1)
    except IndexError:
        print("Lugeda kasutusjuhendit graafikud_juhend.txt")
        sys.stderr.write(about) 
        sys.exit(-1)
    except OSError:
        print("Graafiku moodustamiseks statistika faili ei leitud, palun vastavalt juhendis sagedusJaMuuStatistika_juhend.txt toodud näidetele luua vajalikud statistika failid enne graafikute skripti käivitamist")
        sys.exit(-1)
    except Exception as e:
        print("Tekkis viga andmete töötlusel, palun vaadata ja järgida skriptiga samas kaustas asuvaid juhendeid.")
        sys.exit(-1)
    
