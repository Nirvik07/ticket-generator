from io import StringIO
import random
import re

# Process CSV files
import csv

# Generate PDFs using ReportLab
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import *
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch, mm
from reportlab.graphics.barcode import code39
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab_qrcode import QRCodeImage

PAGE_HEIGHT= 6 * inch
PAGE_WIDTH= 8 * inch
styles = getSampleStyleSheet()
Title = "CSS BATTLE"
pagesize = (8* inch, 6* inch)
pdfmetrics.registerFont(TTFont('aAkhirTahun', 'aAkhirTahun.ttf'))

def process_csv(fname,name,email):
    ''' Process a csv file containing lastname and firstname.
    Return a list of lists containing lastname, firstname, and random identifier
    '''
    #data =  []
    #choices = range(100000)
    csvfile = csv.reader(open(fname))
    # throw away header
    #csvfile.next()
    for row in csvfile:
        #print(row)
        if row[2].lower() == name.lower() and row[1].lower() == email.lower():
        # newdata = [row[0],row[1],row[2],row[3],row[4],row[1][:7].upper() +'-'+str(random.choice(choices))]
        # #if DEBUG: print(newdata)
        # data.append(newdata)
            return row
    return -1

def docPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold', 10)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - (.25 * inch), Title)
    canvas.setFont('Times-Roman',20)
    canvas.drawString(inch,inch, "Page %d" % (doc.page,))
    canvas.restoreState()

def ticketPage(canvas, doc ):
    canvas.saveState()
    H = 6 * inch
    W = 8 * inch
    canvas.drawImage('Frame 1.png', 0, 0, width = W, height = H)
    canvas.restoreState()

def gen_key(data, fn):
    doc = SimpleDocTemplate(fn)
    Story = []
    tabledata = []
    style = styles["Normal"]
    tabledata.append(['Participant Name','Registration No','Present'])
    for row in data:
        tabledata.append(["%s" % ( row[2]), "%s" % row[4],"[                ]"])
    t=Table(tabledata, colWidths= 2 * inch, repeatRows=1)
    Story.append(t)
    doc.build(Story, onFirstPage=docPage, onLaterPages=docPage)

def gen_ticket(row,fn):
    "CSS BATTLE TICKET"
    doc = SimpleDocTemplate(fn,pagesize=pagesize)
    Story = []
    styleN = styles["Normal"]
    styleH = styles['Heading1']
    qr = QRCodeImage(row[4], size=0.9 * inch)
    tabledata = []
    tabledata.append(["%s" % ( ""), "%s" % (""),])

    tabledata.append(["%s" % ( row[2].upper()), "%s" % (row[2].upper()),])
    tabledata.append([[qr], "%s" % row[4],])

    t=Table(tabledata, colWidths=  4 * inch, rowHeights=  1 *inch, repeatRows=2)
    t.setStyle(TableStyle([('ALIGN',(0,0),(-1,-1),'RIGHT'),
                        ('VALIGN',(0,0),(-1,-1),'TOP'),
                        ('FONTSIZE',(0,0),(-1,-1), 20),

                        ('VALIGN',(0,0),(0,-1),'TOP'),
                        ('ALIGN',(0,0),(0,-1),'CENTER'),
                        ('FONTSIZE',(0,0),(0,-1), 20),

                        ('ALIGN',(0,-1),(-1,-1),'RIGHT'),
                        ('VALIGN',(0,-1),(-1,-1),'TOP'),
                        ('FONTSIZE',(0,-1),(-1,-1), 20),
                        ]))
    Story.append(t)
    # #Story.append(Paragraph("CSS BATTLE TICKET",styleH))
    #Story.append(Spacer(inch, .2 * inch))
    # Story.append(Paragraph("%s" % ( row[2]), styleN))
    # Story.append(Spacer(1 * inch, .25 * inch))
    # #Story.append(Paragraph("Student email:  %s" % ( row[1]), styleN))
    # Story.append(Spacer(1 * inch, .25 * inch))
    #Story.append(Spacer(1 * inch, .25 * inch))
    # Story.append(Spacer(4* inch, 0))
    # Story.append(Paragraph("%s" % (row[4]), styleN))
    # Story.append(Spacer(1 * inch, .5 * inch))
    #Story.append(Spacer(1 * inch, 0.5 * inch))
    #Story.append(Spacer(1 * inch, .6 * inch))
    # #Story.append(Paragraph("Date : 28th April 2023" , styleN))
    # qr = QRCodeImage(row[4], size=inch)
    # Story.append(qr)
    doc.build(Story, onFirstPage=ticketPage, onLaterPages=ticketPage)
    return


# create an re to get rid of non-word chars for file names
#pattern = re.compile('[W_]+')

data=[]
#data = process_csv('CSS Battle Registration.csv')
csvfile = csv.reader(open("CSS Battle Registration.csv"))
for row in csvfile:
    newdata= [row[1],row[2],row[3],row[4],row[5],row[7]]
    data.append(newdata)
# for row in data:
#     fname =  pattern.sub('-', row[2] + '-'+ row[4]).lower()
#     fname += ".pdf"
#gen_ticket(row, fname)
gen_key(data, "keyfile.pdf")