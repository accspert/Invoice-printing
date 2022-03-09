from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter, landscape
from datetime import datetime
from datetime import date
import os

class reportObj:
    def __init__(self, type, table, date_from = 0, date_to = 0):
        if(type == "sales"):
            headers = ("Verkaufsdatum", "Verkaufsmenge", "Artikelname", "Einkaufspreis", "Verkaufspreis", "Zwischensumme")
            table.insert(0, headers)
            
            # append the difference of buying price and selling price in every tuple inside sales list
            for i in range(1, len(table)):
                table[i] = table[i] + (table[i][4] - table[i][3],)
                
            self.data = table
            self.date_from = date_from
            self.date_to = date_to
        
        elif(type == "buy"):
            headers = ("Datum und Uhrzeit","Artikelname", "Menge", "Einkauf Preis")
            table.insert(0, headers)
            self.data = table
            self.date_from = date_from
            self.date_to = date_to
        
        elif(type == "stock"):
            headers = ("ArtikelID", "Artikelname", "Menge", "Einkauf Preis", "Verkaufspreis")
            table.insert(0, headers)
            self.data = table
            # set self.date to todays date
            self.date = datetime.today().strftime('%Y-%m-%d')
    
    def generate_stock_report(self, file_name):
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']
        styleH4 = styles['Heading4']
        story = []

        doc = SimpleDocTemplate(
            file_name,
            pagesize=landscape(A4),
            bottomMargin=.4 * inch,
            topMargin=.6 * inch,
            rightMargin=.8 * inch,
            leftMargin=.8 * inch)

        text_content = "Lagerbestand"
        P = Paragraph(text_content, styleH)
        story.append(P)
        
        # printing the day
        text_content = datetime.now().strftime('%a')
        P = Paragraph(text_content, styleN)
        story.append(Spacer(1, 0.3*cm))
        story.append(P)
        
        # printing the date and time
        text_content = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        P = Paragraph(text_content, styleN)
        story.append(Spacer(1, 0.3*cm))
        story.append(P)
        
        t=Table(self.data, None, hAlign='LEFT')
        t=Table(self.data, (3*cm,14*cm,3*cm,3*cm,3*cm), None, hAlign='LEFT')
        story.append(Spacer(1, 0.5*cm))
        story.append(t)
        
        # calculate the total amount of the purchase
        total_amount = 0
        for i in range(1, len(self.data)):
            total_amount += self.data[i][3]
        
        text_content = "Gesamtsumme: " + str(total_amount)
        P = Paragraph(text_content, styleH4)
        story.append(Spacer(1, 0.7*cm))
        story.append(P)

        
        doc.build(
            story
        )
        
        # open the file in the default program
            # for linux:
        # os.system("xdg-open " + file_name)
            # for window:
        os.startfile(file_name)
    
    def generate_buy_report(self, file_name):
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']
        styleH4 = styles['Heading4']
        story = []

        doc = SimpleDocTemplate(
            file_name,
            pagesize=letter,
            bottomMargin=.4 * inch,
            topMargin=.6 * inch,
            rightMargin=.8 * inch,
            leftMargin=.8 * inch)

        text_content = "Einkauf"
        P = Paragraph(text_content, styleH)
        story.append(P)
        
        # printing the date and time
        text_content = "Vom " + str(self.date_from) + " Bis " + str(self.date_to)
        P = Paragraph(text_content, styleN)
        story.append(Spacer(1, 0.3*cm))
        story.append(P)
        
        t=Table(self.data, (6*cm,4*cm,3*cm,4*cm), None, hAlign='LEFT')
        story.append(Spacer(1, 0.5*cm))
        story.append(t)
        
        # calculate the total amount of the purchase
        total_amount = 0
        for i in range(1, len(self.data)):
            total_amount += self.data[i][3]
        
        text_content = "Gesamtsumme Einkauf: " + str(total_amount)
        P = Paragraph(text_content, styleH4)
        story.append(Spacer(1, 0.7*cm))
        story.append(P)
        
        # # printing
        # text_content = "Ich versichere, dass oben aufgeführte Waren mein Eigentum sind und keine Rechte Dritter bestehen"
        # P = Paragraph(text_content, styleN)
        # story.append(Spacer(1, 0.3*cm))
        # story.append(P)
        
        # # printing
        # text_content = "Unterschrift Kunde / Verkäufer"
        # P = Paragraph(text_content, styleN)
        # story.append(Spacer(1, 2.0*cm))
        # story.append(P)
        
        doc.build(
            story
        )
        
        # open the file in the default program
            # for linux:
        # os.system("xdg-open " + file_name)
            # for window:
        os.startfile(file_name)
    
    def generate_sales_report(self, file_name):
        styles = getSampleStyleSheet()
        styleN = styles['Normal']
        styleH = styles['Heading1']
        story = []

        doc = SimpleDocTemplate(
            file_name,
            pagesize=letter,
            bottomMargin=.4 * inch,
            topMargin=.6 * inch,
            rightMargin=.8 * inch,
            leftMargin=.8 * inch)

        text_content = "Verkauf"
        P = Paragraph(text_content, styleH)
        story.append(P)
        
        text_content = "Vom " + str(self.date_from) + " Bis " + str(self.date_to)
        P = Paragraph(text_content, styleN)
        story.append(Spacer(1, 0.3*cm))
        story.append(P)
        
        t=Table(self.data, (3*cm,3*cm,3*cm,3*cm,3*cm,3*cm), None, hAlign='LEFT')
        story.append(Spacer(1, 0.5*cm))
        story.append(t)
        
        # calculate the total amount of the sales
        total_amount = 0
        for i in range(1, len(self.data)):
            total_amount += self.data[i][4]

        text_content = "Summe Verkauf: " + str(total_amount)
        P = Paragraph(text_content, styleN)
        story.append(Spacer(1, 0.5*cm))
        story.append(P)
        
        # calculate the total amount of the purchase
        total_amount = 0
        for i in range(1, len(self.data)):
            total_amount += self.data[i][3]
        
        text_content = "Summe Einkauf: " + str(total_amount)
        P = Paragraph(text_content, styleN)
        story.append(P)
        
        # calculate the total amount of the difference
        total_amount = 0
        for i in range(1, len(self.data)):
            total_amount += self.data[i][5]
        
        text_content = "Summe Marge: " + str(total_amount)
        P = Paragraph(text_content, styleN)
        story.append(P)
        
        doc.build(
            story
        )
        
        # open the file in the default program
        # for linux:
        # os.system("xdg-open " + file_name)
        # for window:
        os.startfile(file_name)
