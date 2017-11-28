# coding: utf8

import csv
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
 
from private import mail, address, volunteerTeamName, bankCheckName, bankCheckAddress, gmailAddress, gmailPassword 
from datetime import datetime

def addOrder(mailBody, row):
    mailBody += "Référence de votre commande " + row[0]
    if row[12] != "":
        mailBody += "\nAPIVAR quantité : " + row[12]
    if row[16] != "":
        mailBody += "\nAPISTAN quantité : " + row[16]
    if row[19] != "":
        mailBody += "\nAPIGUARD quantité : " + row[19]
    if row[22] != "":
        mailBody += "\nAPILIFE quantité : " + row[22]
    if row[25] != "":
        mailBody += "\nMAQS quantité : " + row[25]
    if row[28] != "":
        mailBody += "\nAPI BIOXAL quantité : " + row[28]
    return mailBody

def addSignature(mailBody):
    mailBody += "\n\nCordialement"
    mailBody += "\nL’équipe des bénévoles du " + volunteerTeamName + ", en charge de la gestion des commandes."
    return mailBody

def addHeader(mailBody):
    mailBody = "Madame/Monsieur " + row[1] + " " + row[2] + ", \n\n"
    return mailBody

def isOrderOk(row):
    if row[41].lower() == "ok" and row[42].lower() == "ok":
        return True
    elif row[41].lower() == "not ok" and row[42].lower() == "ok":
        return False
    #todo handle error
    return False

def sendMail(toAddress, body, orderName):
    print("Envoi du mail pour la commande " + orderName)
    msg = MIMEMultipart()
    msg['From'] = mail
    msg['To'] = toAddress
    msg['Subject'] = "Votre commande de médicament"
    body = mailBody
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(gmailAddress, gmailPassword)
    text = msg.as_string()
    server.sendmail(gmailAddress, toAddress, text)
    server.quit()
    print("Mail pour la commande " + row[0] + " envoyé")
    
with open(sys.argv[1], "r", encoding='utf8') as f:
    csvReader = csv.reader(f)
    for row in csvReader:
        mailBody = ""
        mailBody = addHeader(mailBody)
        if isOrderOk(row):
            mailBody += "Nous avons le plaisir de vous confirmer la prise en compte  de votre commande des médicaments ci dessous :\n"
        else:
            mailBody += "Nous sommes au regret de vous informer, que votre commande de médicament ci dessous N’EST PAS PRISE en compte car votre règlement ne nous est pas parvenu à ce jour :\n"
        mailBody = addOrder(mailBody, row)
        
        if isOrderOk(row):
            mailBody += "\n\nVous avez choisi le mode de livraison suivant : "
            if row[31] == "R":
                mailBody += "Retrait"
                mailBody += "\nDate du retrait : " + row[32] + " à l’adresse suivante : " + address
                mailBody += "\nHeure des permanences : "
                if datetime.strptime(row[32], "%d/%m/%Y").isoweekday() == 5:
                    mailBody += "vendredi de 9H00 à 16H30"
                elif datetime.strptime(row[32], "%d/%m/%Y").isoweekday() == 6:
                    mailBody += "samedi de 9H00 à 12H00"
            elif row[31] == "LP":
                mailBody += "Livraison Postale"
                mailBody += "\nMerci de noter que l’expédition par voie postale se fera à partir du : JJ/MM/AA"
                mailBody += "\nVotre adresse d’expédition est la suivante : « contenu des cellules " + row[4] + " " + row[5] + " " + row[6]
        else :
            mailBody += "A défaut de réception de votre règlement pour un montant de " + row[35] + " SOUS HUIT JOURS nous annulerons votre commande."
            mailBody += "Merci de nous faire parvenir votre règlement par chèque SIGNE à l’ordre du : " + bankCheckName + ", à l’adresse suivante : " + bankCheckAddress 
        mailBody += "\n\nSi vous constatez une erreur concernant la confirmation de votre commande (Quantité , adresse, date de livraison, …) nous vous remercions de nous écrire immédiatement à l’adresse suivante : " + mail + " en nous indiquant PRECISEMENT la  correction que vous souhaiteriez faire."
        mailBody = addSignature(mailBody)
        sendMail(gmailAddress, mailBody, row[0])


