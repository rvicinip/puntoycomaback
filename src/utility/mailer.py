'''
   mailer

   Realiza el envío de correos electrónicos \n

   :copyright: Vitt Inversiones SAS - vitt.co
   :license: Vitt Inversiones SAS - vitt.co
   :author: Wiliam Arévalo Camacho
'''
import smtplib
from src import app
import traceback

def sendMail(correo, mensaje):
    '''
       sendMail: Envía un correo electrónico a los datos recibidos
    '''
    print('In sendMail:', correo)
    sender = app.config['EMAIL_USER']
    ## Envía el correo electrónico
    try:
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()
        server.login(app.config['EMAIL_USER'], app.config['EMAIL_KEY'])
        server.sendmail(sender, correo, mensaje)
        server.quit()
        return {'response':'OK', 'message': 'Correo enviado a ' + correo}
    except Exception:
        traceback.print_exc()
        return {'response':'ERROR', 'message': 'Se presentó un error al enviar el correo a ' + correo}