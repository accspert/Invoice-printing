from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('Arial', 'ariblk.ttf'))

def rightalingn(pdf, string, left, right, ycoordinate):
    length = len(string)
    totalLength = (right - left) / 7
    print(totalLength)
    spaces = int(totalLength - length)
    print(spaces)
    pdf.drawString(right, ycoordinate, " " * spaces)
    left = left + (7 * spaces)
    pdf.drawString(left, ycoordinate, string)


def header(header, pdf):
    pdf.setTitle(header.date + "Rechnung")

    pdf.setFont("Courier-Bold", 20)
    pdf.drawString(30, 820, str(header.Comp_Name))
    pdf.setFont("Courier-Bold", 11)
    pdf.drawString(30, 800, "Strasse: "+str(header.Comp_Street))
    pdf.drawString(30, 790, "Stadt: "+str(header.Comp_City))
    pdf.drawString(30, 780, "Land: "+str(header.Comp_Country))
    pdf.drawString(30, 770, "Postleitzahl: "+str(header.Comp_Zip))
    pdf.drawString(30, 760, "Telefon: "+str(header.Comp_Phone))

    pdf.setFont("Courier-Bold", 20)
    pdf.drawString(30, 725, "Kunde :")

    pdf.setFont("Courier-Bold", 11)
    pdf.drawString(30, 710, "Name: "+str(header.Customer_Name) )
    pdf.drawString(30, 695, "Kunden Id: "+str(header.Customer_Id) )
    pdf.drawString(30, 680, "Strasse : "+str(header.Cust_street) )
    pdf.drawString(30, 665, "Stadt: "+str(header.Cust_City)  )
    pdf.drawString(30, 650, "Datum: " + str(header.date))

    pdf.setFont("Arial", 20)
    pdf.setFillColor(HexColor('#4A49A3'))
    pdf.drawString(400, 800, "Rechnung")
    pdf.setFillColor(colors.black)
    pdf.setFont("Courier-Bold", 11)
    pdf.drawString(350, 780, "Rechnungs#: " + str(int(header.InvoiceNumber)))


def middle(pdf):

    pdf.setFont("Courier-Bold", 11)


    #(left,bottom)
    pdf.drawString(35, 625, "Id")
    pdf.drawString(85, 625, "Menge")
    pdf.drawString(142, 625, "Artikel ID")
    pdf.drawString(220, 625, "Beschreibung")
    pdf.drawString(325, 625, "Preis")
    pdf.drawString(385, 625, "MwSt")
    pdf.drawString(430, 625, "Netto")
    pdf.drawString(492, 625, "Brutto")

    pdf.line(30, 635, 570, 635)
    pdf.line(30, 620, 570, 620)
    pdf.line(30, 635, 30, 150)#(topl-eft,top,bottom-left,bottom) left line
    pdf.line(80, 635, 80, 150)#item id
    pdf.line(140, 635, 140, 150)#Quantity
    pdf.line(210, 635, 210, 150)#productid
    pdf.line(318, 635, 318, 150)
    pdf.line(370, 635, 370, 150)
    pdf.line(428, 635, 428, 150)
    pdf.line(490, 635, 490, 150)
    pdf.line(570, 635, 570, 150)

    pdf.line(30, 150, 570, 150)




def additem(product, pdf, ycoordinate):
    while (len(product.description) > 15):
        pdf.drawString(230, ycoordinate, product.description[:15] + "-")
        product.description = product.description[15:]
        ycoordinate = ycoordinate - 15
    pdf.drawString(230, ycoordinate, str(product.description))
    return (ycoordinate - 15)

def footer(pdf, total,Net_Total, ycoordinate):
    pdf.drawString(280, 130, "Netto Total: ")
    pdf.drawString(360, 130, str(Net_Total))
    pdf.drawString(420, 130, "Brutto Total: ")
    pdf.drawString(520, 130, str(total))
    pdf.setFont("Courier-Bold", 10)
    pdf.setFillColor(HexColor('#6969B3'))

    pdf.drawString(50, 50, "6 Monate Garantie. Es gelten die Allgemeinen Geschäftsbedingungen.")

