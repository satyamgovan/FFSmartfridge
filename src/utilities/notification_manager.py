import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from tkinter import messagebox
from src.utilities.database_manager import DatabaseManager

database_manager = DatabaseManager('../../database/database.db')


class EmailSender:

    def __init__(self):
        self.database_manager = database_manager
        self.sender_email = "satyamtandel48@gmail.com"
        self.sender_password = "nqdzczqcbocdyccj"

    def send_email(self):
        # Fetch email addresses of head chefs from the database
        head_chef_emails = self.database_manager.fetch_head_chef_emails()

        if not head_chef_emails:
            messagebox.showerror("Error", "No head chef found.")
            return

        for head_chef_email in head_chef_emails:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["Subject"] = "Requesting Assistance"

            body = ("Someone needs assistance\n"
                    "Thank you,")
            message.attach(MIMEText(body, "plain"))

            # Set the "To" header for the current head chef
            to_email = head_chef_email[0]
            message["To"] = to_email

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)

                # Send email to the current head chef
                server.sendmail(self.sender_email, to_email, message.as_string())

        messagebox.showinfo("Information", "Request has been sent.")

    def send_email_expiry(self, subject, body, to_email):
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["Subject"] = subject

        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            # Send email
            server.sendmail(self.sender_email, to_email, message.as_string())

    def send_expiry_notification_email(self, expiring_items):
        head_chef_emails = self.database_manager.fetch_head_chef_emails()

        if not head_chef_emails:
            messagebox.showerror("Error", "No head chef found.")
            return

        for head_chef_email in head_chef_emails:
            body = "Expiry Reminder:\n"
            for food_name, days_until_expiry in expiring_items:
                body += f"{food_name} will expire in {days_until_expiry} days.\n"

            # Send expiration notification to the current head chef
            self.send_email_expiry("Expiry Reminder", body, head_chef_email[0])

        messagebox.showinfo("Information", "Expiration notifications have been sent")

    def send_custom_email(self, to_email, subject, body):
        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = to_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, to_email, message.as_string())

        except Exception as e:
            print(f"Error sending custom email to {to_email}: {e}")

    def send_low_quantity_notification(self, low_quantity_items):
        try:
            if not low_quantity_items:
                # No low quantity items to notify about
                return

            notification_message = "Low Quantity Notification:\n"

            for item in low_quantity_items:
                item_id, current_quantity, threshold = item[0], item[4], item[-1]
                item_name = self.database_manager.fetch_item_name(item_id)
                notification_message += f"{item_name} has {current_quantity} units left. Threshold: {threshold}\n"

            # Fetch head chef emails
            head_chef_emails = self.database_manager.fetch_head_chef_emails()

            if not head_chef_emails:
                raise ValueError("No head chef found.")

            # Send a single low quantity notification email to head chefs
            for head_chef_email in head_chef_emails:
                self.send_custom_email(head_chef_email[0], "Low Quantity Notification", notification_message)

        except Exception as e:
            print(f"Error during send_low_quantity_notification: {e}")
            messagebox.showerror("Error", f"Error sending low quantity notification: {e}")

    def send_attachment_email(self, to_email, subject, body, attachment_path):
        try:
            message = MIMEMultipart()
            message["From"] = self.sender_email
            message["To"] = to_email
            message["Subject"] = subject

            message.attach(MIMEText(body, "plain"))

            # Attach the PDF file
            with open(attachment_path, "rb") as file:
                attachment = MIMEApplication(file.read(), _subtype="pdf")
                attachment.add_header("Content-Disposition",
                                      f"attachment; filename={os.path.basename(attachment_path)}")
                message.attach(attachment)

            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)

                # Send email with attachment
                server.sendmail(self.sender_email, to_email, message.as_string())

        except Exception as e:
            print(f"Error sending email with attachment to {to_email}: {e}")

