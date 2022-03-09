from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont('Arial', 'ariblk.ttf'))
length = 0


def header(header, pdf):
    pdf.setTitle(str(header.date))
    pdf.setFont("Courier-Bold", 20)
    pdf.drawString(30, 820, str(header.Comp_Name))
    pdf.setFont("Courier-Bold", 11)
    pdf.drawString(30, 800, "Strasse: " + str(header.Comp_Street))
    pdf.drawString(30, 790, "Stadt: " + str(header.Comp_City))
    pdf.drawString(30, 780, "Land: " + str(header.Comp_Country))
    pdf.drawString(30, 770, "Postleitzahl: " + str(header.Comp_Zip))
    pdf.drawString(30, 760, "Telefon: " + str(header.Comp_Phone))
    pdf.setFont("Courier-Bold", 11)
    pdf.drawString(350, 780, str(header.date))


def middle(pdf):
    pdf.setFont("Courier-Bold", 11)
    # (left,bottom)
    pdf.drawString(150, 690, "Artikelname")
    pdf.drawString(345, 690, "Menge")
    pdf.drawString(390, 690, "Ankaufspreis")
    pdf.drawString(480, 690, "Zwischensumme")

    pdf.line(30, 700, 570, 700)
    pdf.line(30, 685, 570, 685)
    pdf.line(30, 700, 30, 500)  # (topl-eft,top,bottom-left,bottom) left line
    pdf.line(335, 700, 335, 500)  # item id
    pdf.line(385, 700, 385, 500)  # Quantity
    pdf.line(475, 700, 475, 500)  # productid
    pdf.line(570, 700, 570, 500)

def additem(product, pdf, ycoordinate):
    global length
    length = length + len(product.Artikelname)
    while (len(product.Artikelname) > 45):
        pdf.drawString(60, ycoordinate, product.Artikelname[:45] + "-")
        product.Artikelname = product.Artikelname[45:]
        ycoordinate = ycoordinate - 15
    pdf.drawString(60, ycoordinate, str(product.Artikelname))

    return (ycoordinate - 15)
def footer(total,pdf):
    if length > 495:
        pdf.line(30, 700, 30, 300)  # (topl-eft,top,bottom-left,bottom) left line
        pdf.line(335, 700, 335, 300)  # item id
        pdf.line(385, 700, 385, 300)  # Quantity
        pdf.line(475, 700, 475, 300)  # productid
        pdf.line(570, 700, 570, 300)

        pdf.line(30, 315, 570, 315)
        pdf.line(30, 300, 570, 300)
        pdf.drawString(390, 305, "Gesamtsumme ")
        pdf.drawString(505, 305, str(total))
        pdf.setFont("Courier-Bold", 10)
        pdf.drawString(30, 210, "Ich versichere, dass oben aufgeführte Waren mein Eigentum sind und ")
        pdf.drawString(30, 200, "keine Rechte Dritter bestehen.")
        pdf.drawString(30, 180, "Unterschrift Kunde / Verkäufer")
    else:
        pdf.line(30, 515, 570, 515)
        pdf.line(30, 500, 570, 500)
        pdf.drawString(390, 505, "Gesamtsumme ")
        pdf.drawString(505, 505, str(total))
        pdf.setFont("Courier-Bold", 10)
        pdf.drawString(30, 410, "Ich versichere, dass oben aufgeführte Waren mein Eigentum sind und ")
        pdf.drawString(30, 400, "keine Rechte Dritter bestehen.")
        pdf.drawString(30, 380, "Unterschrift Kunde / Verkäufer")
