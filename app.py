from models import Books, session, Base, engine   # import models
from datetime import datetime
import csv
import time

def clean_date(date_str):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    split_date = date_str.split(' ')
    try:
        month = int(months.index(split_date[0]) + 1)
        day = int(split_date[1].split(',')[0])
        year = int(split_date[2])
        return_date = datetime(year, month, day)
    except ValueError:
        input('''
            \n ****DATE ERRROR****
            \rThe date format should include a valid Month Day, Year from the past.
            \rEx: January 13, 2018
            \rPress Enter to try again.
            \r*************************
            \r:''')
        return

    else:
        return return_date

def clean_price(price_str):
    try:
        price_float = float(price_str)
    except ValueError:
        input('''
            \n ****PRICE ERRROR****
            \rThe price should be a number with out a currency symbol.
            \rEx: 10.99
            \rPress Enter to try again.
            \r*************************''')
    else:
        return int(price_float * 100)


def clean_id(id_str, id_options):
    try:
        book_id = int(id_str)
    except ValueError:
        input('''
            \n ****ID ERRROR****
            \rThe id should be a number.
            \rPress Enter to try again.
            \r*************************''')
        return
    else:
        if book_id in id_options:
            return book_id
        else:
            input(f'''
            \n ****ID ERRROR****
            \rOptions: {id_options}.
            \rPress Enter to try again.
            \r*************************''')
            return

def edit_check(column_name, current_value):
    print(f"\n*** EDIT {column_name} ***")
    if column_name == 'Price':
        print(f'\rCurrent Value: {current_value/100}')
    elif column_name == 'Date':
        print(f'\rCurrent Value: {current_value.strftime("%B %d, %Y")}')
    else:
        print (f'\rCurrent Value: {current_value}')

    if column_name == 'Date' or column_name == 'Price':
        while True:
            changes = input('What would you like to change the value to?')
            if column_name == 'Date':
                changes = clean_date(changes)
                if isinstance(changes, datetime):
                    return changes
            if column_name == 'Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else:
        return input('What would you like to change the value to?')
def add_csv():
    with open('suggested_books.csv') as csvfile:
        data = csv.reader(csvfile)
        for row in data:
            book_in_db = session.query(Books).filter(Books.title==row[0]).one_or_none()
            if book_in_db == None:
                title = row[0]
                author = row[1]
                date = clean_date(row[2])
                price = clean_price(row[3])
                new_book = Books(title=title, author=author,
                                date_published=date, price=price)
                session.add(new_book)
        session.commit()


    



# def edit_books():
    
# def delete_books():


# def search_books():

# def data_cleaning():

def menu_options():

    print("\n---PROGRAMMING BOOKS---\n")
    while True:
        choice_made = input(
            "\nWhat would you like to do:\n" 
            "\n\033[92m1\033[0m) Add Books \n"    
            "\033[92m2\033[0m) View Books \n"
            "\033[92m3\033[0m) Book Analysis \n" 
            "\033[92m4\033[0m) Search Books \n"
            "\033[92m5\033[0m) Exit \n" 
            "\n ENTER an option: "
            )
        if choice_made in ['1','2','3','4','5']:
            return choice_made
        else:
            input('''Please choose one of the options above.
                  \rA number from 1-5.
                  \rPress enter to try again''')

def submenu():
    while True:
        choice_made = input(
            "\nWhat would you like to do:\n"
            "\n\033[92m1\033[0m) Edit \n"
            "\033[92m2\033[0m) Delete \n"
            "\033[92m3\033[0m) Return to main menu \n"
            "\n ENTER an option: "
        )
        if choice_made in ['1', '2', '3', '4', '5']:
            return choice_made
        else:
            input('''Please choose one of the options above.
                  \rA number from 1-3.
                  \rPress enter to try again''')


def app():
    app_running = True
    while app_running:
        choice_made = menu_options()
        if choice_made == '1':
            title = input(
                'Please provide the title of the book, that you would like to add?: ')
            author = input('Please provide the author of the book: ')
            date_error = True
            while date_error:
                date_published = input('Please provide the date published (Ex: October 25, 2017: ')
                date_published = clean_date(date_published)
                if type(date_published) == datetime:
                    date_error = False
            
            price_error = True
            while price_error:
                price = input('Price (Ex: 29.99): ')
                price = clean_price(price)
                if type(price) == int:
                    price_error = False
            new_book = Books(title=title, author=author, date_published=date_published, price=price)
            session.add(new_book)
            session.commit()
            print('Book Added!')
            time.sleep(1.5)
        elif choice_made == '2':
            for book in session.query(Books):
                print(f'{book.id} | {book.title} | {book.author}' )
            input('\n Press enter to return to the main menu.')

        elif choice_made == '3':
            # Book analysis
            oldest_book = session.query(Books).order_by(Books.date_published).first()
            newest_book = session.query(Books).order_by(Books.date_published.desc()).first()
            total_books = session.query(Books).count()
            python_books = session.query(Books).filter(Books.title.like('%Python%')).count()
            print(f'''\n ****BOOOK ANALYSIS****
                  \rOldest Book: {oldest_book}\n
                    \rNewest Book: {newest_book}\n
                    \rTotal Books: {total_books}\n
                    \rNumber of python Books: {python_books}''')
            input('\nPress Enter to return to the main menu.')
        elif choice_made == '4':
            # Search book
            id_options = []
            for book in session.query(Books):
                id_options.append(book.id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \nId Options : {id_options}
                    \rBook id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_book = session.query(Books).filter(Books.id==id_choice).first()
            print(f'''
                    \n{the_book.title} by {the_book.author}
                    \rPublished: {the_book.date_published}
                    \rPrice: ${the_book.price / 100}\n''')
            sub_choice = submenu()
            if sub_choice == '1':
                # edit
                the_book.title = edit_check('Title', the_book.title)
                the_book.author = edit_check('Author', the_book.author)
                the_book.date_published = edit_check('Date', the_book.date_published)
                the_book.price = edit_check('Price', the_book.price)
                session.commit()
                print('Book Updated!')
                time.sleep(1.5)
                pass
            elif sub_choice == '2':
                # delete
                session.delete(the_book)
                session.commit()
                print('Book Deleted')
                time.sleep(1.5)
        else:
            print('Bhaj jaa')
            app_running = False


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    add_csv()
    app()

    for book in session.query(Books):
        print(book)
    
# main menu - add, search, analysis, exit, view
# add books to the database
# edit books
# delete books
# search books
# data cleaning
# loop runs program