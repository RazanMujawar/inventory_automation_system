# Lumina & Co. - Inventory Automation Platform

## Overview

Lumina & Co. is an Inventory Automation Platform developed to automate inventory tracking, sales processing, low-stock monitoring, alert generation, and reporting.

The platform enables businesses to upload daily sales files, automatically update inventory levels, generate low-stock alerts, send email notifications, and create operational reports.

---

## Features

### Upload Sales

* Upload daily sales CSV files
* Validate file structure and data quality
* Verify product IDs against inventory database
* Prevent invalid records from entering the system

### Inventory Processing

* Load sales records into MySQL
* Update product stock levels automatically
* Maintain inventory accuracy

### Low Stock Alerts

* Detect products below reorder level
* Generate alert records
* Send automated email notifications

### Reporting

* Inventory Report
* Sales Summary Report
* Low Stock Report

### Reminder Emails

* Scheduled reminder emails for sales file submission
* HTML email templates

### Inventory Management

* View current inventory
* Restock products directly from UI
* Update inventory database instantly

### Streamlit Dashboard

* Home Page
* Upload Sales
* Show Inventory
* Restock Inventory

---

## Tech Stack

### Frontend

* Streamlit

### Backend

* Python

### Database

* MySQL

### Libraries

* Pandas
* Streamlit
* MySQL Connector
* Schedule
* SMTP Email Services

---

## Project Structure

inventory_automation_system/

├── app.py

├── database/

│ └── db_connection.py

├── modules/

│ ├── generate_alerts.py

│ ├── load_sales.py

│ ├── load_to_sales_table.py

│ ├── update_inventory.py

│ ├── reports.py

│ ├── send_email.py

│ ├── file_handler.py

│ └── logger.py

├── pages/

│ ├── upload_sales.py

│ ├── show_inventory.py

│ └── restock_inventory.py

├── scheduler/

│ └── scheduler.py

├── data/

├── processed/

├── logs/

└── images/

---

## Workflow

1. Upload Sales CSV
2. Validate File
3. Load Sales Data
4. Update Inventory
5. Generate Alerts
6. Send Email Notifications
7. Generate Reports
8. Move File to Processed Folder

---

## Future Enhancements

* Power BI Dashboard Integration
* User Authentication
* Role Based Access Control
* Product Management
* Supplier Management
* Purchase Order Automation
* AI Powered Inventory Forecasting

---

## Author

Razan Mujawar

Bachelor of Computer Science Engineering (AI & ML)

Inventory Automation Platform Project
