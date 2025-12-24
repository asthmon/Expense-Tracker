The Expanse Tracker
Video Demo:  https://youtu.be/XWGZN2hDpgI

Project Description
The Expense Tracker is a dynamic, full-stack web application designed to simplify personal finance management. Developed as the final project for Harvard's CS50x, this application provides users with a powerful and intuitive dashboard to monitor their spending habits meticulously.

Built with a Flask backend and a clean, responsive frontend, the app allows users to perform full CRUD (Create, Read, Update, Delete) operations on their financial records. Beyond simple tracking, it offers robust filtering and data visualization features, enabling users to gain actionable insights into where their money is going, categorized by type and over time. It's a practical tool for anyone looking to take control of their finances.

Features
Dashboard Overview: Get a quick snapshot of your total spending and a complete list of all expenses.

Add New Expenses: Log new transactions with a description, amount, date, and category.

Full Expense Management: Edit existing expenses to correct mistakes or delete transactions you no longer need.

Advanced Filtering: Filter the expense list by a custom date range and/or specific category to find exactly what you're looking for.

Data Visualization:

By Category Chart: A visual breakdown (likely a pie or bar chart) showing your spending distribution across different categories (e.g., Food, Health, Entertainment).

Spending Over Time Graph: A line or bar chart that visualizes your expenditure trends over a selected period, helping you identify peak spending days or weeks.

How to Use the Application
1. Viewing Your Expenses
Upon loading the app, the main dashboard displays a table of your recent expenses.

The "Total" at the top summarizes the sum of all currently displayed expenses.

Use the "Filters" section to narrow down the list:

Enter a Start and End date to view expenses from a specific time frame.

Select a Category from the dropdown to see expenses only from that category.

Click "Apply" to activate the filters. Click "Reset" to clear them and view all expenses again.

2. Adding a New Expense
Locate the "Add Expense" form on the dashboard.

Fill in the required fields:

Description: Enter a brief note about the expense (e.g., "Weekly Groceries").

Amount: Input the cost of the item or service.

Date: Select the date of the transaction.

Category: Choose the most appropriate category from the dropdown menu (e.g., "Food").

Click the "Add Expense" button. The new expense will immediately appear in the expenses list, and the total will update.

3. Editing or Deleting an Expense
In the "Expenses" table, each entry has an "Edit" and "Delete" button.

To modify an expense, click the "Edit" button. This will likely open a pre-filled form where you can change any of the details. Submit the form to save your changes.

To permanently remove an expense, click the "Delete" button. This action is typically confirmed by a pop-up dialog to prevent accidental deletion.

4. Analyzing Your Spending
The "By Category" section provides a chart that visually represents your spending patterns. This helps you quickly identify your largest expense categories.

The "Spending Over Time" graph plots your expenses chronologically, allowing you to see trends, such as whether your spending increases on weekends or during specific months.

Technical Implementation
This project leverages the core concepts taught in CS50:

Backend: Implemented in Python using the Flask framework.

Database: Uses SQLite (via SQLAlchemy) to persistently store expense data, including description, amount, date, and category.

Frontend: Renders dynamic HTML templates (Jinja2) to display data from the database.

Interactivity: Handles user interactions (adding, editing, deleting, filtering) through Flask routes that process form submissions and AJAX/fetch requests.

Data Visualization: Likely utilizes a library like Chart.js to generate the interactive client-side charts based on data provided by the backend.