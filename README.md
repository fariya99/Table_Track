# Table_Track
Restaurant Management system
Overview
"Table Track" is a Tkinter-based desktop application designed to manage restaurant operations like order taking, billing, menu editing, sales tracking, and customer records using text files instead of a database.

Key Features
User-Friendly GUI: Sidebar navigation, top bar title, and dynamic content area.

Order Management: Takes orders, validates input, saves to files, and generates bills.

Menu Management: Add or delete menu items; updates menu.txt.

Sales & Revenue: Tracks daily sales from sales.txt and summarizes in revenue.txt.

Customer Records: Stores unique customer info with real-time search.

Bill Viewer: Displays last bill; allows PDF export using ReportLab.

Exit Button: Closes the application.

File Usage
Uses menu.txt, orders.txt, bill.txt, sales.txt, customers.txt, and revenue.txt for data storage.

Ensures safe file handling with checks and context managers.

Validation & Error Handling
Validates names, contact numbers, and prices.

Handles file errors and PDF generation issues using try-except blocks.


