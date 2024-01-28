import os
import cv2
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

list_of_names = []


def delete_old_data():
    for i in os.listdir("generated-certificates/"):
        os.remove("generated-certificates/{}".format(i))


def cleanup_data():
    with open('name-data.txt') as f:
        for line in f:
            list_of_names.append(line.strip())


def generate_certificates():
    font_size = 5

    for index, name in enumerate(list_of_names):
        certificate_template_image = cv2.imread("certificate-template.jpg")
        font = cv2.FONT_HERSHEY_SIMPLEX | cv2.FONT_HERSHEY_SCRIPT_SIMPLEX
        cv2.putText(certificate_template_image, name.strip(), (1400, 1500), font, font_size, (0, 0, 0), 5, cv2.LINE_AA)
        certificate_path = "generated-certificates/{}.jpg".format(index)
        cv2.imwrite(certificate_path, certificate_template_image)
        print("Processing {} / {}".format(index + 1, len(list_of_names)))
                
               


def send_email(name, image_path):
    
    sender_email = "Enter_your_Email"
    sender_password = "Enter_your_password"
    recipient_email = "recipient_email@example.com"
    smtp_server = "smtp.gmail.com"
    smtp_port = 587

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "Certificate for {}".format(name)

    # Attach the image
    with open(image_path, 'rb') as image_file:
        img = MIMEImage(image_file.read())
    msg.attach(img)

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, msg.as_string())

    print("Email sent for {}".format(name))


def main():
   # delete_old_data()
    cleanup_data()
    generate_certificates()


if __name__ == '__main__':
    main()
