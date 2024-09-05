import logging
import os
from tkinter import messagebox
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from ..utilities.notification_manager import EmailSender


class HealthAndSafetyLogic:
    def __init__(self, window_manager, access_control, db_manager, notification_manager, entry_widget):
        self.window_manager = window_manager
        self.access_control = access_control
        self.db_manager = db_manager
        self.notification_manager = notification_manager
        self.entry_widget = entry_widget

    @staticmethod
    def insert_text(widget, text):
        if widget:
            widget.insert("end", text)
            widget.insert("end", "\n")
        else:
            logging.warning("Attempting to insert text into a non-existent text widget.")

    def display_user_access_logs(self):
        try:
            # Clear the entry widget
            self.window_manager.clear_text_widget(self.entry_widget)

            introduction_text = """
            # Health and Safety Report Introduction

            ## Overview
            Welcome to the annual Health and Safety Report for the FFsmart system developed by Spiders. This report provides an in-depth analysis of the health and safety aspects associated with the FFsmart smart fridge.

            ## Health and Safety Considerations
            The FFsmart system prioritises health and safety in various ways, ensuring compliance with industry standards. Key considerations include:

            1. **Secure Access Logs:**
            """

            # Fetch all user sessions from the sessions table
            sessions = self.db_manager.get_all_sessions()

            if sessions:
                introduction_text += "## User Access Sessions\n"
                for session in sessions:
                    session_id, user_role, user_id, start_time, end_time = session
                    introduction_text += f"Session ID: {session_id}\n"
                    introduction_text += f"User Role: {user_role}\n"
                    introduction_text += f"User ID: {user_id}\n"
                    introduction_text += f"Start Time: {start_time}\n"
                    introduction_text += f"End Time: {end_time}\n\n"
            else:
                introduction_text += "No user sessions available.\n"

            introduction_text += """
            2. **Order logs**
               - Automated tracking of food items, and placing the order every monday.
            """

            # Fetch all orders from the orders table
            orders = self.db_manager.select_all("orders")

            if orders:
                introduction_text += "## Order Logs\n"
                for order in orders:
                    order_id, item_id, supplier_id, order_details, order_date, accumulated_quantity, item_name = order
                    introduction_text += f"Order ID: {order_id}\n"
                    introduction_text += f"Item ID: {item_id}\n"
                    introduction_text += f"Supplier ID: {supplier_id}\n"
                    introduction_text += f"Order Details: {order_details}\n"
                    introduction_text += f"Order Date: {order_date}\n"
                    introduction_text += f"Accumulated Quantity: {accumulated_quantity}\n"
                    introduction_text += f"Item Name: {item_name}\n\n"
            else:
                introduction_text += "No order logs available.\n"

            # Fetch system.log file path from the utility folder
            system_log_path = os.path.join("../utilities", "system.log")

            if os.path.isfile(system_log_path):
                with open(system_log_path, "r") as system_log_file:
                    system_logs = system_log_file.read()
                introduction_text += """
            3. **System error logs:**
               - The system stores all the errors encountered in the log file:.
            """
                introduction_text += system_logs
            else:
                introduction_text += "No system error logs available."

            introduction_text += """
            4. **Expiry Notifications:**
               - The system notifies the head chef in advance of food item expiry, allowing for removal.
               """
            expiry_logs = self.db_manager.select_all("expirylog")

            if expiry_logs:
                introduction_text += "## Expiry log\n"
                for expiry_log in expiry_logs:
                    expiry_id, food_name, expiry_date, item_id = expiry_log
                    introduction_text += f"Expiry ID: {expiry_id}\n"
                    introduction_text += f"Food Name: {food_name}\n"
                    introduction_text += f"Expiry Date: {expiry_date}\n"
                    introduction_text += f"Item ID: {item_id}\n\n"
            else:
                introduction_text += "No expiry notifications available.\n"

            self.insert_text(self.entry_widget, introduction_text)
        except Exception as e:
            logging.error(f"Error while retrieving User Access Logs: {e}")
            messagebox.showerror("Error",
                                 f"Failed to retrieve User Access Logs. Check system logs for details. Error: {e}")

    def generate_pdf(self, content, pdf_filename='health_and_safety.pdf'):
        try:
            pdf_path = os.path.join(os.path.dirname(__file__), pdf_filename)

            # Create a PDF file
            pdf = SimpleDocTemplate(pdf_path, pagesize=letter)

            styles = getSampleStyleSheet()
            normal_style = styles['Normal']

            paragraphs = [Paragraph(line, normal_style) for line in content.split('\n')]

            # Build the PDF document
            pdf.build(paragraphs)

            messagebox.showinfo("Information", f"PDF created successfully: {pdf_path}")

            return pdf_path

        except Exception as e:
            logging.error(f"Error while generating PDF: {e}")
            messagebox.showerror("Error", f"Failed to generate PDF. Check system logs for details. Error: {e}")
            return None

    def send_pdf_to_head_chef(self, pdf_path):
        try:
            email_sender = EmailSender()

            head_chef_emails = self.db_manager.fetch_head_chef_emails()

            if not head_chef_emails:
                messagebox.showerror("Error", "No head chef found.")
                return

            for head_chef_email in head_chef_emails:
                email_sender.send_attachment_email(
                    head_chef_email[0],
                    "Health and Safety Report",
                    "Please find attached the Health and Safety Report.",
                    pdf_path
                )

            messagebox.showinfo("Information", "PDF sent to head chefs successfully.")

        except Exception as e:
            logging.error(f"Error while sending PDF to head chef: {e}")
            messagebox.showerror("Error", f"Failed to send PDF to head chef. Check system logs for details. Error: {e}")

    def generate_and_send_pdf(self, content):
        pdf_path = self.generate_pdf(content)
        if pdf_path:
            self.send_pdf_to_head_chef(pdf_path)
