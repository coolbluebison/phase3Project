# # lib/cli.py


# from sqlalchemy import create_engine, Column, String, Integer, ForeignKey, Date, Enum
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship, sessionmaker
# from datetime import datetime, timedelta
# Base = declarative_base()

from arcanelibrary import Base, engine, Student, Book, BorrowRecord, session, datetime
import os


def welcome_menu():
    print("Welcome to The Arcane Library")
    print("-------------------------------------")
    print("You are the Librarian.")
    print("...")
    print("-------------------------------------")
    input("Are you ready to start the day? (PRESS  ENTER)")

def choice_menu():
    print("--------------------------------------")

    print("(1) See all books")
    print("(2) See all students")
    print("")
    print("(3) Add a new book")
    print("(4) Admit a new student")
    print("")
    print("(5) Record a borrowing")
    print("(6) Return a book")
    print("")
    print("(7) Show outstanding loans")
    print("(8) Show all loan history ")
    print("")
    print("(9) Destroy book")
    print("(10) Ban Student from the archives")
    print("")
    print("(11) Update a book entry")
    print("")
    print("(12) Exit the library")

    print("--------------------------------------")
    return input("What would you like to do?")

def show_books():
    all_books = session.query(Book).all()
    os.system('clear')
    for book in all_books:
        print(f"{book.id} || {book.title} by {book.author}")

def show_students():
    all_students = session.query(Student).all()
    os.system('clear')
    for student in all_students:
        print(f"{student.id} || {student.name} who is a {student.class_year}")

def add_book():
    os.system('clear')
    print("Let's start adding the book")
    print("-----------------------------------------------")
    new_book_name = input("What is the book's title?")
    print("sounds like an interesting book, and ")
    new_book_author = input("Who is the author?")
    new_book = Book(title=new_book_name, author=new_book_author)
    session.add(new_book)
    session.commit()
    os.system('clear')

def add_student():
    os.system('clear')
    print("Let's welcome the new student!!")
    print("-----------------------------------------------")
    new_student_name = input("What is the name of the student you want to admit into the archives?")
    new_student_class = input("What is the student's class? (First_year? Second_year? Third_year or Fourth_year?)")
    new_student = Student(name=new_student_name, class_year=new_student_class)
    session.add(new_student)
    session.commit()
    os.system('clear')

def destroy_book():
    os.system('clear')
    show_books()
    book_destroy_id = int(input("What is the id of the book you are trying to destroy?"))
    
    existing_borrow = session.query(BorrowRecord).filter(BorrowRecord.book_id==book_destroy_id, BorrowRecord.return_date==None).first()

    if existing_borrow:
        print("Sorry, this books is already loaned and has not been returned to the archives, we cannot destroy it at this time")
        return 
    
    book_to_destroy = session.query(Book).filter(Book.id==book_destroy_id).first()

    os.system('clear')

    double_check = input(f"Are you sure that you would like to destroy {book_to_destroy.title} by {book_to_destroy.author} ?  (Y/N)")
    if double_check.lower() == "y":
        session.delete(book_to_destroy)
        session.commit()
    else:
        return


def ban_student():
    os.system('clear')
    show_students()

    print("I've heard someone brough an open flame candle to archives... Who was it?")
    print("We will make sure to return all the books that he has borrowed!!")
    student_ban = input('Enter the id of the student who needs to be banned?')

    student_to_ban = session.query(Student).filter_by(id=student_ban).first()

    borrow_outstanding = session.query(BorrowRecord).filter(BorrowRecord.student_id == student_ban).all()

    if borrow_outstanding:
        for borrow in borrow_outstanding:
            borrow.return_date = datetime.now()

    session.delete(student_to_ban)
    session.commit()



def record_borrowing():
    # for borrowing where the book_id is the borrow_book_id 
    # if the return_date != None
    # Then go
    # Else, say this will not work and again          
    
    show_books()
    borrow_book_id = int(input("Enter the book ID to borrow:")) 
    
    existing_borrow = session.query(BorrowRecord).filter(BorrowRecord.book_id == borrow_book_id, BorrowRecord.return_date==None).all()

    if existing_borrow:
        os.system('clear')
        print("Sorry, this books is already borrowed please choose another option")
        return    
    
    book_to_borrow = session.query(Book).filter_by(id=borrow_book_id).first()

    os.system('clear')

    show_students()
    borrow_student_id = int(input("Enter the student's ID:"))
    student_borrowing = session.query(Student).filter_by(id=borrow_student_id).first()

    if book_to_borrow and student_borrowing:
        record = BorrowRecord(borrow_date=datetime.now(), return_date=None, student_id=student_borrowing.id, book_id=book_to_borrow.id)
        session.add(record)
        session.commit()
        os.system('clear')

def show_borrowings():
    all_borrowings = session.query(BorrowRecord).all()


    lines = []
    
    for borrowing in all_borrowings:
        if borrowing.return_date is None:
            book_to_borrow = session.query(Book).filter_by(id=borrowing.book_id).first()
            student_borrowing = session.query(Student).filter_by(id=borrowing.student_id).first()
            
            a_line = f"{borrowing.record_id} || {book_to_borrow.title} || borrowed by {student_borrowing.name} || borrowed on {borrowing.borrow_date}" 
            lines.append(a_line)

    os.system('clear')

    for line in lines:
        print(line)


def borrowing_history():
    all_borrowings = session.query(BorrowRecord).all()

    lines = []
    
    for borrowing in all_borrowings:

        book_to_borrow = session.query(Book).filter_by(id=borrowing.book_id).first()
        student_borrowing = session.query(Student).filter_by(id=borrowing.student_id).first()
        
        a_line = f"{borrowing.record_id} || {book_to_borrow.title} || borrowed by {'Banned Student' if borrowing.student_id==None else student_borrowing.name} || borrowed on {borrowing.borrow_date} || {'Not returned' if borrowing.return_date == None else 'returned on ' + str(borrowing.return_date)} " 
        lines.append(a_line)

    os.system('clear')

    for line in lines:
        print(line)

def return_borrowing():
    show_borrowings()
    return_book_id = int(input("Enter the book ID to return:"))

    book_to_return = session.query(BorrowRecord).filter_by(record_id=return_book_id).first()

    book_to_return.return_date = datetime.now()
    session.commit()

def update_book():
    show_books()
    print("----------------------------------------------------------------")
    book_id_edit = input("Which book would you like to edit, choose the id?")

    book_to_edit = session.query(Book).filter_by(id=book_id_edit).first()
    
    print(f"{book_to_edit.title} by {book_to_edit.author}")

    print("------------------------------------------------")

    print("Would you like to update the title of the book?")
    answer_input = input("(Y/N ?)")

    if answer_input.lower() == 'y':
        updated_title = input("What is the update title of the book?")
        book_to_edit.title = updated_title
        session.commit()
        os.system('clear')
    
    print("Would you like to update the author of the book?")
    answer_input = input("(Y/N ?)")

    if answer_input.lower() == 'y':
        updated_author = input("What is the updated author of the book?")
        book_to_edit.author = updated_author
        session.commit() 
        os.system('clear')


def main():
    # os.system('clear')
    welcome_menu()
    
    while True:

        choice = choice_menu()
        if choice == '1':
            show_books()
        elif choice == '2':
            show_students()
        elif choice == '3':
            add_book()
        elif choice == '4':
            add_student()
        elif choice == '5':
            record_borrowing()
        elif choice == '6':
            return_borrowing()
        elif choice == '7':
            show_borrowings()
        elif choice == '8':
            borrowing_history()
        elif choice == '9':
            destroy_book()
        elif choice == '10':
            ban_student()
        elif choice == '11':
            update_book()
        elif choice == '12':
            print("Have a good rest")
            break
        else:
            print("Invalid option. Please choose again.")


if __name__ == "__main__":

    os.system('clear')
    
    library = """
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%*%%%%%%%%%%%%%%%%+%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%#+%%%%%%%%%%%%%%%=%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%+-.%%%%%%%%%%%%%%-..%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%#%:.:---::-:-:--=@++%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%@*.:--:::::::::--*==%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%@@--===========++@**%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%@@--==-======++++@**%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%@%--=----===--#++@*+%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%@*::-:--=:---==%=#--%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%@%---==+--=-=+=*+#+=%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    %%%%%%%%%%%%%%%%%%%%%%%%%%%@#:-:+**=-:-**+-**+-%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
    =%%%%%%%%%%%%%%%%%%%%%%%%%%@%--:###*--+###=+@#-%%%%%%%%%%%%%%%%%%%%%%%%%%%%=-%%%%%%
    -%%%%%%%%%%%%%%%%%%%%%%%%%%@%---##%*==+%#%=+@#-%%%%%%%%%%%%%%%%%%%%%%%%%%%===#*%%%%
    ==*%%%%%%%%%%%%%%%%%%%%%%%%@%--:**#+=-=*##==@#-%%%%%%%%%%%%%%%%%%%%%%%%%%==--=#=%%%
    -*#+%%%%%%%%%%%%%%%%%%%%%%%@%:..###+:.=###::%%-%%%%%%%%%%%%%%%%%%%%%%%%%+=-====###%
    ==+%=%%%%%%%%%%%%%%%%%%%%%+----------------==--:#%%%%%%%%%%%%%%%%%%%%%%==-======*%*
    ===+%:%%%%%%%%%%%%%%%%%%%%@#+----==--=-====-++:=%%%%%%%%%%%%%%%%%%%%%%=--========+@
    ====+%-*##########*#*#####%%#------=-----===+-......................+=--====++++==+
    ==--==#-=########*#*######%%--:----==-=-=-==%+.....................----=======++++=
    ++====+%#*==-:--========++#---:--=---=-=====%%#...............=#------=============
    ##+*+==*+-----..:::-----==#=-------=========#%@-::-----==----=@#===---=============
    ===-=%%#+*#=--..::-------=%=-------==++==-==#@@=:-----====--:%@#------=--=--=-=--==
    --:---+#%=---:.::.:---:.::----::-==-=++=+=#=#@@=::::----==--:=@@@=====-.:---:--:--:
    --=%==+#@+*-:....=.....==.----::=++:=+-=*+#=#%@=:..=::---+:--.=@@++===---:=-----=-=
    ==+%+==+%=+::...:++...-++.:-:-::=+*=+*=+#+#=*%@=..-+=.---+---::@@*%====---+---+=--+
    ==-=+==+%++.:...-==...=+*..:::::=+*=++=+#+#=+%@=..+++.--+*#:-:-@@+#=======+=======+
    =-..===*@++............:+.......=+*=..-=--:-+%@=..=++.--=++:-:-@@+%+============--=
    =-::+=++%==.....................=+*-..::.:....--..=++:.:=++.:.:@@+%====-=-=-=======
    --===-##%+=........................:..........:...-==...-==....@@+#+===============
    ======##%*.................................................::--*@+%+===============
    =====+##*+--====-===========================================+++=-*#+=====++======++
    -====+**#+--===--=====--======:=====--======:-====-:-=====:-==+=:*+*===++==+===++==
    -..-==+*+=---.....-==:...-==-...-==:...-==-...-==-...-==.....:==:+++====+#=++*=+..-
    =..-==**+=--.......--..==:--.....--.:::.--.....--.....--.......-:*#*=====-==:.-=...
    =..-=+*#==--.......--.....--.....-:.....=-.....--.....--........:+=+====-..=...=:..
    -..-==**==-:.......--.....=-.....-......=-.....--.....--........-+++====-..=...=-..
    -..-==#+---........--.....=-.....-......--.....--.....:-........-+++====-..=...=-..
    ...-==#%#=-........--.....=:.....-......-:.....:-.....:-........-=+=====-..-...--..
    ------+===:........::.....-:.....-......-:.....:-......-........-=++====-----------
    ......-++=.........:......-......-.......:.............:.........---:::::::::-:::--
    .......-:........................................................:::...............
    ......:-=----:::::::-====+++=--::::::::::::::::::..................................
    @@@@@@@@@@@@@@@%%@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@#@@@@@@@@@@@@@@%*+@@%#%=-
    """

    print(library)

    main()







# go_inside ="""
#              ('-.   .-') _     .-')                                 
#            _(  OO) (  OO) )   ( OO ).                               
#  ,--.     (,------./     '._ (_)---\_)       ,----.     .-'),-----. 
#  |  |.-')  |  .---'|'--...__)/    _ |       '  .-./-') ( OO'  .-.  '
#  |  | OO ) |  |    '--.  .--'\  :` `.       |  |_( O- )/   |  | |  |
#  |  |`-' |(|  '--.    |  |    '..`''.)      |  | .--, \\_) |  |\|  |
# (|  '---.' |  .--'    |  |   .-._)   \     (|  | '. (_/  \ |  | |  |
#  |      |  |  `---.   |  |   \       /      |  '--'  |    `'  '-'  '
#  `------'  `------'   `--'    `-----'        `------'       `-----' 
#               .-') _   .-')            _ .-') _     ('-.            
#              ( OO ) ) ( OO ).         ( (  OO) )  _(  OO)           
#   ,-.-') ,--./ ,--,' (_)---\_)  ,-.-') \     .'_ (,------.          
#   |  |OO)|   \ |  |\ /    _ |   |  |OO),`'--..._) |  .---'          
#   |  |  \|    \|  | )\  :` `.   |  |  \|  |  \  ' |  |              
#   |  |(_/|  .     |/  '..`''.)  |  |(_/|  |   ' |(|  '--.           
#  ,|  |_.'|  |\    |  .-._)   \ ,|  |_.'|  |   / : |  .--'           
# (_|  |   |  | \   |  \       /(_|  |   |  '--'  / |  `---.          
#   `--'   `--'  `--'   `-----'   `--'   `-------'  `------'      
# """


# print(go_inside)




# desk ="""
#         ::.              :;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;:        
#         ::.              :;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;:        
#         ...              :;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;:        
#                     :;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;:        
#             :;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;:
#             .:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#             .:::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#             ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#             ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#             ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#             ::::::::::::::::::::::;:::;:::::;:;::;:;;;:;;:;:;:;;:;:;:::::;:;;:;:::::
#             ::...............:..:..::.:.:.:.::.:::.:.:..............................
#             .::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
#             :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::;:::::::::
#             :::::::::::::::.::::::::::::::::::::::::::::::::::::::::::::::::::::::;::
#             :::;;;::::::::: ::::::::::::::::::::::::::::::::::..::::::::::::::::::...
#             ::;;;;;:::::::.  :::::::::::::::::::::::::::::::::  :::::::::::::::::.   
#         . ..:::::::........ ........::.  . . .  ............    ............::::.   
#         . .::;+++;::.              ..     ......     .                               
#         . ..::;+$&&+;:.      .     .:    .............   ...                           
#         ...::;+X&X;;:.     ....:..   .:................    ...                        
#         ..:::;+&+::..    .. ..   ......::::.:..........:..       .................   
#         ..::::+&+....    ...:::::.::::::::::::::::::::....:::.         ...........   
#         ..::..;&;        ...:::::::::::::::......::..:::...:::..          .......    
#         .   ;&;        ...::::.............................:                       
#             ;$;          .::................................ .                     
#             +$;         ..:................................. .               ..    
#             +$; ....   ...:.................................          ....  ....   
#             ;XX+;.  .   ...:................................. .      .....:..       
#         .      :;..        ....................................              ..       
#         XXXXXXXXX+xXXXXXXXXXXX$XXXXXXXXXXXXxxxxxxxx++++++++;;;;;;;;;;;;;;:             
#         &&&&&&$$+;$&&&&&&&&&&&&&&&&&&&&&&X$$$$$XXXXXXXXXXXXXXxxxx++++++++:             
#         &&&&&&&&&$$$$&&&&&&&&&&&&&&&&&&XX$$$$$$$XXXXXXXXXXXXXxXxxxx+++++++;            
#         x++;;+++xX$&&&&&&&&&$$$$$$$$$$X$$$$$XXXXXXXXXXXXXXXxxxxxxxx++++++++:           
#         &&&&&&&&&&&&&&&&&&&&$$$$$$$$$XXXXXXXXXXXXXXXXXXXXXXxxxxxxx++++++++++:          
#         ;:;:::;;;;;;:::::;;;;;;;;;;;;;;;;;;;;;;;;;;;;:::::::::::::::::::::...  ...     
#         ..... . .  .. .  . .....................................                       
#         :::::::::::::::::::::::::::::::::::::::::::::::::..................            
#         ;:::::::::::::::::::::::::::::::::::::::::::::::::::::.............            
#         ::::::::::::::::::::::::::::::::::::::::::::::::::::::::............           
#         :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::..:.....:;::;;;;:   
#         ::::::::::::::::::::::::::::::::::::::::::::::::::::::::::..........;;;::;;:   
#         ;;;:;:::::::::::::::::::::::::::::::::::::::::::::::::::::::.......:;+++;&$XXx;
#         """

#         print(desk)