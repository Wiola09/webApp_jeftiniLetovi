import os
import smtplib
import ssl
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from os.path import basename
from konstante import gmail, mail_primalac, MAIL_PASSWORD

smtp_server = 'smtp.gmail.com'
smtp_port = 587
gmail = "miroslavzeljkovic@gmail.com"
mail_primalac = "miroslav.zeljkovic@ems.rs"


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.

    # Replace with your own gmail account
    # mail_primalac = 'jelena.djuricic@ems.rs'
    # mail_primalac = 'nebojsa.dragutinovic@ems.rs'

    def prilog_maila(self, message):
        # attachment_path = f"c:\\Users\\Miroslav\\OpenAI\\EXEL 2 open\\Napravljeni nalozi\\{naziv_dokumenta}"
        # attachment_path = f"/opt/render/project/src/static/db/{naziv_dokumenta}"

        # varijanta za slanje sa racunara
        putanja_radna = os.getcwd()
        print(putanja_radna, "test_putanje")

        attachment_path = f"d"
        # attachment_path = f"{putanja_radna}/{naziv_dokumenta}"
        # [Errno 2] No such file or directory: '/opt/render/project/src/static/db/Nalog Broj 85_23 za Miroslav Zeljković dana 2023-03-20 odlazak na objekat DV ekipa Bajina Bašta.xlsx'

        print(os.getcwd(), "test_putanje")
        try:
            with open(attachment_path, "rb") as attachment:

                # p = MIMEApplication(attachment.read(), _subtype="xlsx")   # !!! Imao sam problem sa enkodingom naziva
                # fajla, jedva resih sa basename(attachment_path)

                p = MIMEApplication(
                    attachment.read(),
                    Name=basename(attachment_path)
                )

                p.add_header('Content-Disposition', "attachment; filename= %s" % attachment_path.split("\\")[-1])

                message.attach(p)

        except Exception as e:
            print(str(e))
        return message

    def posalji_mail(self, text, naslov):
        message = MIMEMultipart('mixed')
        message['From'] = 'Pretraga jeftinih letova <{sender}>'.format(sender="test")
        message['To'] = "test@ems.rs"
        message['CC'] = 'test2@ems.rs'
        message['Subject'] = f"Akcije pažnja {naslov}!!!"

        msg_content = f'<h4>Поштовани,' \
                      f'<br> {text[0]}.' \
                      f'<br> {text[1]} ' \
                      f'<br> {text[2]}</h4>\n'

        body = MIMEText(msg_content, 'html')
        message.attach(body)
        # !!!! Dodavanje priloga, ovde ne koristim stavio poziv pod komentar
        # message = self.prilog_maila(message)

        msg_full = message.as_string()
        context = ssl.create_default_context()

        #  za slanje na vise mail adresa smtplib prihvata listu !!!!
        # mail_primalac = [miroslav.zeljkovic@ems.rs, 'miroslavzeljkovic@gmail.com']
        # mail_primalac = mail_za_slanje
        print(mail_primalac, "листа")
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.ehlo()
            server.starttls(context=context)
            server.ehlo()
            server.login(gmail, MAIL_PASSWORD)

            server.sendmail(gmail, mail_primalac, msg_full)
            server.quit()

        print("email sent out successfully")
