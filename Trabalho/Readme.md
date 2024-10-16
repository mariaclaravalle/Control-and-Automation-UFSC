
# Book Loan System

## Description

The Book Loan System is a software application that allows users to register, consult available book titles, and manage book loans using a QR code scanner. It is designed to streamline the process of borrowing and returning books in a library-like environment.

## Installation

Before using the system, you need to install the following modules:

```bash
pip install PySimpleGUI
pip install pyzmq
```
> **Note**: PySimpleGUI is no longer free, but you can use the free trial for 30 days.


## How to Use
Register: After installing the necessary modules, you can register yourself in the system.
Access the System: Once registered, you can log in to access the system.
Consult Available Titles: Use the system to check the books available for loan.
## Features
Consult Available Titles: The system allows you to check the books available for loan.
Book Loan: To loan a book, the system assumes that you are using a QR code scanner as a peripheral (as if you were at the library with your chosen book) and randomly selects a book for you.
Reservation and Return: After reserving a book, you can return it later.
Check Reservations: The system allows you to view your reserved books and any debts for overdue books.
## Considerations
We suppose that there's a QR code scanner available (generate with the periferic fonction) that will indicate the book that the you want to loan for the loan functionality to work properly.


License
This project is licensed under the MIT License. See the LICENSE file for more details.
