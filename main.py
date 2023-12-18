# Imports die Niemand wirklich verstehen muss...
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Nimmt sich das momentane Datum & formatiert es zu '[Stunde:Minute:Sekunde] - '.
now = datetime.now()
prefix = "[" + now.strftime("%H:%M:%S") + "] - "
# Setzt die Headers der Anfrage (Den User-Agent), damit Ebay-Kleinanzeigen die Anfrage nicht blockt.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36 Edg/84.0.522.59',
}

#print(soup)
# Setzt einen Counter.
counter = 0

# Setzt einen zweiten Counter.
vbCounter = 0
festCounter = 0

connectedListAll = []

ePreise = []
vbPreise = []


global query, response, page, soup

def getUserInput():
    global query, prefix
    # Fragt die Query ab die Später in den URL gegeben werden soll (der Suchbegriff)
    query = input(prefix + "Bitte gebe deine Query an << ")
    # Fügt die Query in den Ebay-Kleinanzeigen URL ein.
    URL = query
    # Gibt aus welche Query gewählt wurde.
    print(prefix + "Es wird nach gesucht nach >> " + URL)
    return URL

def getHTML(URL):
    global headers
    # Gibt den HTML text der Website in eine Variable wieder.
    response = requests.get(url=URL, headers=headers)

    # Setzt den Content der Website in eine Variable.
    page = response.content
    # print(page)
    # Erstellt eine BeautifulSoup-Instanz mit dem Website-Content und einem passendem Parser.
    soup = BeautifulSoup(page, "html.parser")
    return soup


# Eine Funktion um eine Text-Datei zu beschreiben.
def writeFile(response, name, fileType):
    with open(name + fileType, "a", encoding="utf8") as f:
        f.write(response)


# Eine Funktion um den Durschnitt zu berechnen.
def calculateAverage(prices):
    count = len(prices)
    summe = calculateSum(prices)

    print(count, " ", summe)
    return summe / count


# Eine Funktion um die Summe eines Arrays zu berechnen.
def calculateSum(arr):
    result = sum(arr)
    return result


def getSearchResults(soup):
    links = soup.find_all('a', class_='ellipsis')
    prices = soup.find_all(class_="aditem-main--middle--price-shipping--price")
    linkCounter = 0
    for link in links:
        price = prices[linkCounter]
        if 'href' in link.attrs:
            print(link['href'], price)
            connectedListAll.append([price, link['href']])
            linkCounter += 1






    # Setzt die Einträge inheralb der Seach-Results und dem Table dortdrinn in eine Variable / Array.
    prices = soup.find_all(class_="aditem-main--middle--price-shipping--price")

    print(prices)

    return prices

def addPricesToArrays():
    global counter, vbCounter, festCounter, ePreise, vbPreise
    print(connectedListAll)
    for preis,link in connectedListAll:

        # Incrementiert einen Counter.
        counter = counter + 1

        # Gibt den Preis des Listings aus & fügt den Incrementierten Counter hinzu (+ formatierung).
        print("#" + str(counter) + " | " + preis.text + " | " + link)

        # Zählt wieviele Listings mit 'VB' gekennzeichnet sind.
        if ("VB" in preis.text):
            vbCounter = vbCounter + 1

            # Entfernt Chars, wenn das Euro-Zeichen vorhande ist.
            # Konvertiert außerdem den Preis in eine Int und speichert ihn in den Array 'ePreise'.
            if ("€" in preis.text):
                if ("." in preis.text):
                    vbPreise.append((
                        float(preis.text.replace(" ", "").replace("VB", "").replace("€", "").replace(".", "")), link))
                else:
                    vbPreise.append((float(preis.text.replace(" ", "").replace("VB", "").replace("€", "")), link))
        else:
            festCounter = festCounter + 1
            if ("€" in preis.text):
                if ("." in preis.text):
                    ePreise.append((float(preis.text.replace(" ", "").replace("€", "").replace(".", "")), link))
                else:
                    ePreise.append((float(preis.text.replace(" ", "").replace("€", "")), link))


def sortOutTooHighOrTooLow(averagePriceVB, averagePriceFest):

    maxPriceVB = averagePriceVB * 1.5
    minPriceVB = averagePriceVB * 0.5

    maxPriceFest = averagePriceFest * 1.5
    minPriceFest = averagePriceFest * 0.5

    to_delete_vb = []
    to_delete_fest = []

    print(averagePriceVB)

    for i, preis in enumerate(vbPreise):

        if preis[0] < minPriceVB or preis[0] > maxPriceVB:
            print(preis[0])
            to_delete_vb.append(i)

    for i, preis in enumerate(ePreise):
        print(preis[0])
        if preis[0] < minPriceFest or preis[0] > maxPriceFest:
            to_delete_fest.append(i)

    print("Max VB: " + str(maxPriceVB))
    print("Min VB: " + str(minPriceVB))
    for index in reversed(to_delete_vb):
        print("Lösche: " + str(vbPreise[index]) + " an Index: " + str(index) + " aus vbPreise")
        del vbPreise[index]


    print("Max Fest: " + str(maxPriceFest))
    print("Min Fest: " + str(minPriceFest))
    for index in reversed(to_delete_fest):
        print("Lösche: " + str(ePreise[index]) + " an Index: " + str(index) + " aus ePreise")
        del ePreise[index]







if __name__ == '__main__':
    userInputURL = getUserInput()
    htmlsoup = getHTML(userInputURL)
    #print(htmlsoup)
    results = getSearchResults(htmlsoup)
    addPricesToArrays()

    print(vbPreise)
    print(ePreise)

    vbPreisList = [preis for preis, link in vbPreise]
    ePreisList = [preis for preis, link in ePreise]

    averageVBVorSort = calculateAverage(vbPreisList)
    averageFestVorSort = calculateAverage(ePreisList)

    print("------------------------------------------------------------------------------------")
    print(prefix + f"<<<< {len(vbPreise)} Verhandelbare Listings vor aussortieren und {len(ePreise)} Feste Listings nach aussortieren >>>>")
    print(prefix + "Durschnitts-Preis der Verhandelbaren Listings vor aussortieren >> " + str(averageVBVorSort))
    print(prefix + "Durschnitts-Preis der Festen Listings vor aussortieren >> " + str(averageFestVorSort))
    print(prefix + str(ePreise))
    print(prefix + str(vbPreise))
    print("------------------------------------------------------------------------------------")

    sortOutTooHighOrTooLow(averageVBVorSort, averageFestVorSort)

    vbPreisList = [preis for preis, link in vbPreise]
    ePreisList = [preis for preis, link in ePreise]


    if(len(vbPreise) != 0):
        averageVBNachSort = calculateAverage(vbPreisList)
    else:
        averageVBNachSort = 0

    if(len(ePreise) != 0):
        averageFestNachSort = calculateAverage(ePreisList)
    else:
        averageFestNachSort = 0

    print("\n------------------------------------------------------------------------------------")
    print(prefix + f"<<<< {len(vbPreise)} Verhandelbare Listings nach aussortieren und {len(ePreise)} Feste Listings nach aussortieren >>>>")
    print(prefix + "Durschnitts-Preis der Verhandelbaren Listings nach aussortieren >> " + str(averageVBNachSort))
    print(prefix + "Durschnitts-Preis der Festen Listings nach aussortieren >> " + str(averageFestNachSort))
    print(prefix + str(ePreise))
    print(prefix + str(vbPreise))
    print("------------------------------------------------------------------------------------")



    print(prefix + "Liste von guten verhandelbaren Anzeigen:" )
    for preis, link in vbPreise:
        if preis < averageVBNachSort:
            print(prefix + str(preis) + " | " + "https://www.ebay-kleinanzeigen.de"+link)

    print(prefix + "Liste von guten festen Anzeigen:" )
    for preis, link in ePreise:
        if preis < averageFestNachSort:
            print(prefix + str(preis) + " | " + "https://www.ebay-kleinanzeigen.de" + link)












