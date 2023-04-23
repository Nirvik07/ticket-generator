from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_mail import Mail, Message
from reportlab.pdfgen import canvas
import json
import smtplib
from email.message import EmailMessage
from reportlab.lib.units import inch
import main2

file = open("config.json")
data = json.load(file)

app = Flask(__name__)

app.config['SECRET_KEY'] = 'WTF_CSRF_SECRET_KEY'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'repl.development@gmail.com'
app.config['MAIL_PASSWORD'] = 'uwhciwjrykwtdsfi'

mail = Mail(app)

class TicketForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired("Please enter your name.")])
    email = StringField('Email', validators=[DataRequired("Please enter your email address."), Email("Please enter your email address.")])
    submit = SubmitField('Generate Ticket')

@app.route('/', methods=['GET', 'POST'])
def generate_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        # Generate the ticket as a PDF
        ticket_name = form.name.data
        ticket_email = form.email.data
        ticket_filename = f'{ticket_name}.pdf'
        fn ="CSS Battle Registration.csv"
        data = main2.process_csv(fn,ticket_name,ticket_email)
        print(data)
        if data == -1:
            return 'ERROR DATA NOT FOUND!!!'
        else:
            main2.gen_ticket(data, ticket_filename)
            # p = canvas.Canvas(ticket_filename)
       
            # # say hello (note after rotate the y coord needs to be negative!)
            # #c.drawString(0.3*inch, -inch, "Hello World")
            # p.drawString(0.3*inch, -inch, f'Ticket for {ticket_name}')
            # p.drawString(0.3*inch, inch, f'Email: {ticket_email}')
            # p.save()

            # Send the ticket as a PDF attachment
            # ticket_filename = f'{ticket_name}.pdf'
            # msg = Message('Your ticket', sender='soccerultimate11@gmail.com', recipients=[ticket_email])
            # msg.attach(ticket_filename, 'application/pdf', ticket_name)
            # mail.send(msg)
            msg=EmailMessage()
            files=[(r"D:\REPL\TICKET GENERATOR\{}.pdf".format(ticket_name))]
            for file in files:
        
                with open(file,'rb') as f:
            
                    file_data=f.read()
                    file_name=f.name
            
                sub=("TICKET GENERATOR")
                msg['From']='repl.development@gmail.com'
                msg['To']=ticket_email
                msg['Subject']=sub
                msg.set_content(f"Hello {ticket_name}, Your ticket for the CSS BATTLE has arrived. Please take a look into it.")
                msg.add_attachment(file_data,maintype='application',subtype='octet-stream',filename="{}.pdf".format(ticket_name))
        
                with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
            
                    smtp.login('repl.development@gmail.com','uwhciwjrykwtdsfi')
                    smtp.send_message(msg)
                    return 'Your ticket has been generated and sent to your email!'
    return render_template('form.html', form=form)

if __name__ == '__main__':
    app.run(debug=False ,host='0.0.0.0')
