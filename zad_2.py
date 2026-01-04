class Library:
    def __init__(self, city, street, zip_code, open_hours: str, phone):
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.open_hours = open_hours
        self.phone = phone
    def __str__(self):
        return f'Biblioteka w {self.city}, na ul.{self.street}, kod pocztowy: {self.zip_code}, otwarta w godzinach: {self.open_hours}, nr telefonu: {self.phone}'

class Employee:
    def __init__(self, first_name, last_name, hire_date, birth_date, city, street, zip_code, phone):
        self.first_name = first_name
        self.last_name = last_name
        self.hire_date = hire_date
        self.birth_date = birth_date
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.phone = phone
    def __str__(self):
        return f'Pracownik {self.first_name} {self.last_name}, zatrudniony {self.hire_date}, urodzony {self.birth_date}, adres: {self.city}, {self.street}, {self.zip_code}, o nr telefonu: {self.phone}'


class Book:
    def __init__(self, library, publication_date, author_name, author_surname, number_of_pages):
        self.library = library
        self.publication_date = publication_date
        self.author_name = author_name
        self.author_surname = author_surname
        self.number_of_pages = number_of_pages
    def __str__(self):
        return f'Książka z {self.library}, wydana {self.publication_date}, autor: {self.author_surname}, liczba stron: {self.number_of_pages}'


class Order:
    def __init__(self, employee, student, books, order_date):
        self.employee = employee
        self.student = student
        self.books = books
        self.order_date = order_date
    def __str__(self):
        books_description = ""
        for book in self.books:
            books_description += str(book)
        return (
            f'Zamówienie-\n'
            f'Pracownik: {self.employee}\n'
            f'Student: {self.student}\n'
            f'Książki:\n{books_description}'
            f'Data: {self.order_date}'
        )


biblioteka1 = Library('Krakow', 'Sienkiewicza', '41-333', '12-14', 663223443)
biblioteka2 = Library('Warszawa', 'Wysoka', '42-345', '15-17', 836473460)

ksiazka1 = Book(biblioteka2, '08.12.2021', 'Jan', 'Kowalski', 354)
ksiazka2 = Book(biblioteka1, '04.03.1999', 'Andrzej', 'Lech', 987)
ksiazka3 = Book(biblioteka1, '03,12,1987', 'Jerzy', 'Kula', 123)
ksiazka4 = Book(biblioteka2, '16.09.2007', 'Monika', 'Duda', 765)
ksiazka5 = Book(biblioteka2, '29.08.1998', 'Lena', 'Kowalska', 675)

pracownik1 = Employee('Eryk', 'Lis', '08.12.2021', '08.12.2000', 'Lodz', 'Waska', '21-333', 987645534)
pracownik2 = Employee('Bartosz', 'Mak', '28.11.2022', '08.06.2002', 'Wroclaw', 'Polna', '21-387', 988884554)
pracownik3 = Employee('Emil', 'Lesny', '08.03.2011', '12.12.1998', 'Lodz', 'Lesna', '21-223', 987985534)

student1 = 'Maciej Kowalski'
student2 = 'Julia Mroz'
student3 = 'Ola Nowik'

order1 = Order(pracownik1, student3, [ksiazka1, ksiazka2], '08.12.2024')
order2 = Order(pracownik3, student1, [ksiazka3, ksiazka2,ksiazka4],'08.12.2022')

print(order1)
print(order2)
