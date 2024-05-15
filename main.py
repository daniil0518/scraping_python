import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import time
import os
from dotenv import load_env

load_env()

EMAIL_SENDER=os.getenv("EMAIL_SENDER")
EMAIL_RECEIVER=os.getenv("EMAIL_RECEIVER")
PASSWORD=os.getenv("PASSWORD")
SMTP_SERVER=os.getenv("SMTP_SERVER")
SMTP_SERVER_PORT=os.getenv("SMTP_SERVER_PORT")

def scrape_shopify_websites():
    # Scrape the Shopify website directory
    url = "https://www.myip.ms/browse/sites/1/own/376714"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the list of websites
    websites = []
    for link in soup.find_all('a', href=True):
        if 'www.shopify.com' in link['href']:
            websites.append(link['href'])
    
    return websites

def send_email(websites):
    # Set up email configuration
    email_sender = EMAIL_SENDER
    email_receiver = EMAIL_RECEIVER
    password = PASSWORD

    # Compose email message
    message = MIMEMultipart()
    message['From'] = email_sender
    message['To'] = email_receiver
    message['Subject'] = 'Daily Alert: New Shopify Websites'

    # Create email body
    body = "New Shopify Websites:\n\n"
    for website in websites:
        body += website + '\n'
    
    # Attach email body
    message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send email
    server = smtplib.SMTP(SMTP_SERVER, SMTP_SERVER_PORT)
    server.starttls()
    server.login(email_sender, password)
    text = message.as_string()
    server.sendmail(email_sender, email_receiver, text)
    server.quit()

def main():
    # Initially get the list of Shopify websites
    previous_websites = scrape_shopify_websites()

    while True:
        # Scrape the current list of Shopify websites
        current_websites = scrape_shopify_websites()

        print(current_websites)

        # Compare with the previous list to identify new websites
        new_websites = set(current_websites) - set(previous_websites)

        if new_websites:
            # Send email alert with new websites
            send_email(new_websites)
            print("Email sent with daily alert.")

        # Update the previous list for the next iteration
        previous_websites = current_websites

        # Wait for 24 hours before checking again
        time.sleep(86400)

if __name__ == "__main__":
    main()