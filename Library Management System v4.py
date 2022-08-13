from os import system
import mysql.connector
import datetime
import random
import time
db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root",
                database="library")
mycursor = db.cursor()
#Secondary Functions

def guidelines():
        print("General guidelines: \n"
              "-> All issued books must be returned within 14 days of issuing.\n"
              "-> A fine of ruppees 30 will be levied from users who do not return the book within a month of issuing and ruppees 200 for every month after that.\n"
              "-> If a book is not returned within 5 months of issuing it will lead to a permanent cancellation of your library card followed by a potential visit from a collecting officer.\n"
              "-> Any defacement to the book may result in suspension of your library card or a fine or both.\n")

#Main Functions
def bookWrite():
        global AdminLogin
        if AdminLogin == True:
                print("*" * 50, "ENTER BOOKS", "*" * 50)
        else:
                print("ERROR: Access denied.")
                raise NameError
        system('cls')
        while True:
                try:
                        print("Please enter the details of book\n")
                        book_id = int(input("Book ID: "))
                        book_name = str(input("Book name: "))
                        book_genre = input("Book genre: ")
                        book_author = input("Name of the author: ")
                        book_publisher = input("Name of publisher: ")
                        book_count = int(input("Number of copies: "))
                        book_summary = input("Enter a short summary for the book: ")
                        print("\n")

                        cmnd = "INSERT into books values (%s,%s,%s,%s,%s,%s,%s,0)"
                        val = (book_id, book_name, book_genre, book_author, book_publisher, book_count, book_summary)
                        mycursor.execute(cmnd, val)
                        ch1 = input("Confirm entry? (y/n): ")
                        if ch1 == 'y' or ch1 == 'Y' or ch1 == 'YES' or ch1 == 'yes':
                                db.commit()
                                print("SUCCESS: The new records were stored in the database.")
                        elif ch1 == 'n' or ch1 == 'N' or ch1 == 'NO' or ch1 == 'no':
                                print("ABORTED: This record was not entered into the database.")
                        else:
                                print("Interpreting input as 'no'. This record was not entered into database.")
                except:
                        print("ERROR: You have entered an invalid input for one of the fields. Please check your input and try again.\n"
                                 "-> Book ID should be unique and less than 3 digits.\n"
                                 "-> Only integer inputs are allowed in Book ID and number of copies\n"
                                 "-> The string inputs may not exceed 40 characters.\n\n")
                ch = input("Would you like to enter another record? (y/n): ")
                ("\n\n")
                if ch=='y':
                        system('cls')
                        continue
                elif ch=='n' :
                        break
                else:
                        print("Interpretting vague input as NO.")
                        break
        ch2 = input("Press enter to return to main menu...")
        system('cls')

def bookEdit():
        if AdminLogin == True:
                pass
        else:
                erc = 1
        system('cls')
        print("*" * 50, "UPDATE BOOK", "*" * 50)
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password ="root",
                database="library")
        mycursor = db.cursor()
        try:
                id = int(input("Enter the ID of the book you'd like to edit: "))
                cmnd = "select * from books where id = %s"
                id1 = (id,)
                mycursor.execute(cmnd,id1)
                p = mycursor.fetchall()
                print(p)
                if len(p) == 0:
                        raise NameError
                else:
                        print("Please enter NEW details of book")
                        book_name = input("Book name: ")
                        book_genre = input("Book genre: ")
                        book_author = input("Name of the author: ")
                        book_publisher = input("Name of publisher: ")
                        book_count = input("Number of copies: ")
                        book_summary = input("Enter new summary: ")
                        book_issued = int(input("Enter number of times the book was issued: "))
                        cmnd = "update books set name=%s, genre=%s, author=%s, publisher=%s, count=%s, summary = %s, issued = %s where id=%s"
                        val = (book_name, book_genre, book_author, book_publisher, book_count, book_summary, book_issued, id)
                        mycursor.execute(cmnd,val)
                        ch1 = input("Save changes (y/n): ")
                        if ch1 == 'y':
                                db.commit()
                                print("SUCCESS: Changes were saved\n\n")
                        elif ch1 == 'n':
                                print("ABORTED: Changes were not saved")
                        else:
                                print("ABORTED: Interpreting answer as NO. Changes were not saved.")
                        ch = input("Press enter to continue...")
        except:
                if erc == '1':
                        print("ERROR: Access denied.")
                else:
                        print("ERROR: The record was not updated due to some error.\n"
                        "-> The book ID you entered might not exist.\n\n")
                ch = input("Press enter to continue...")
        system('cls')

def allBooks():
        system('cls')
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password ="root",
                database="library")
        mycursor = db.cursor()
        mycursor.execute("select * from books")
        l1 = mycursor.fetchall()
        print("ID   Name")
        for i in l1:
                print(i[0],"  ",i[1])
        ch=input("Press enter to continue...")
        system('cls')

def bookInfo():
        system('cls')
        print("*" * 50, "BOOK INFORMATION", "*" * 50)
        db = mysql.connector.connect(
                host="localhost",
                user="root",
                password ="root",
                database="library")
        mycursor = db.cursor()
        try:
                cmnd = "select * from books where id = %s"
                id1 = input("Enter ID: ")
                if id1 == '':
                        raise NameError
                else:
                        id = (id1,)
                mycursor.execute(cmnd, id)
                l1 = mycursor.fetchone()
                if l1[5] == 0:
                        av = "not available"
                        print(" Book name: ", l1[1], "\n", "Written by: ", l1[3], "\n", "Publisher: ", l1[4] , "\n", "Genre", l1[2], "\n", "Status: ", av, "\n", "Number of times issued: ", l1[7], "\n\n",l1[6], "\n")
                else:
                        av = "available"
                        print(" Book name: ", l1[1], "\n", "Written by: ", l1[3], "\n", "Publisher: ", l1[4] , "\n", "Genre", l1[2], "\n", "Status: ", av, "\n", "Number of copies available: ", l1[5], "\n", "Number of times issued: ", l1[7],"\n\n", l1[6])
        except NameError:
                print("ERROR: This input cannot be left empty.")
        except:
                print("ERROR: This book ID is not registered in the library. Please try again.")
        print('\n\n')
        ch=input("Press enter to continue...")
        system('cls')

def issueBooks():
        system('cls')
        try:
                global cardid
                global AdminLogin
                if AdminLogin == True:
                        cardid = input("Please enter cardid: ")
                else:
                        pass
                cmnd = "select * from users where cardid = %s"
                val = (cardid,)
                mycursor.execute(cmnd,val)
                userlist = mycursor.fetchone()
                if userlist[4] >=2:
                        erc = 1
                        raise MathError
                else:
                        pass
                print("\n")
                id = input("Enter the book ID of the book you would like to issue: ")
                id1 = (id,)
                cmnd = "select * from books where id = %s"
                mycursor.execute(cmnd, id1)
                blist = mycursor.fetchone()
                if len(blist) == 0:
                        erc = 2
                        raise MathError
                if blist[5] == 0:
                        print("ERROR: This book is not available in the library at this moment. Please try again later.")
                else:
                        cmnd = "update books set count = %s where id = %s"
                        val = (blist[5]-1, id)
                        mycursor.execute(cmnd, val)
                        cmnd = "update users set totalbooksissued = %s , booksinposession = %s where cardid = %s"
                        val = (userlist[3] + 1, userlist[4] + 1, cardid)
                        mycursor.execute(cmnd, val)
                        cmnd = "update books set issued = %s where id = %s"
                        val = (blist[7]+1,id)
                        mycursor.execute(cmnd,val)
                        if userlist[6] == -1:
                                cmnd = "update users set book1 = %s where cardid = %s"
                                val = (id, cardid)
                                mycursor.execute(cmnd,val)
                        else:
                                cmnd = "update users set book2 = %s where cardid = %s"
                                val = (id, cardid)
                                mycursor.execute(cmnd,val)
                        date_issue = datetime.date.today()
                        date_return = date_issue + datetime.timedelta(14)
                        db.commit()
                        print("SUCCESS: The book", blist[1], " has been issued to the holder of cardID: ", cardid,
                              "\n\n")
                        ch1 = input("Would you like to print a reciept for your issued book? (y/n): ")
                        if ch1 == 'y' or ch1 == 'Y' or ch1 == 'YES' or ch1 == 'yes':
                                print("\n\n")
                                print(" Book ID:  ", id, "\n",
                                      "Book name: ", blist[1], "\n",
                                      "Issued to ID: ", cardid, "\n",
                                      "Issued on: ", date_issue, "\n",
                                      "Return by: ", date_return, "\n", "\n")
                        else:
                                print('Skipped reciept\n')

                        guidelines()



        except:
                if erc == 1:
                        print("ALERT: Users may only issue 2 books at a time. Please try again after returning your current books.")
                else:
                        print("ERROR: This book ID does not exist in the library.")
        ch=input('Press enter to continue...')
        system('cls')

def returnBooks():
        system('cls')
        print("*" * 50, "RETURN A BOOK", "*" * 50)
        try:
                global cardid
                global AdminLogin
                if AdminLogin == True:
                        cardid = input("Please enter cardID: ")
                else:
                        pass
                cmnd = "select * from users where cardid = %s"
                val = (cardid,)
                mycursor.execute(cmnd, val)
                userlist = mycursor.fetchone()
                if userlist[6] == -1 and userlist[7] == -1:
                        print("ALERT: You have not issued any books currently. Please try again later.")
                elif userlist[6] == -1:
                        cmnd = "select * from books where id = %s"
                        val = (userlist[7],)
                        mycursor.execute(cmnd, val)
                        p = mycursor.fetchone()
                        print("Enter 1 to return: ", p[1])
                        print("Press enter if you do not want to return this book. ")
                        ch1 = input("")
                        if ch1 == '1':
                                cmnd = "update books set count = %s where id = %s"
                                val = (p[5]+1,userlist[7])
                                mycursor.execute(cmnd,val)
                                cmnd = "update users set booksinposession = %s where cardid = %s"
                                val = (userlist[4]-1, cardid)
                                mycursor.execute(cmnd, val)
                                cmnd = "update users set book2 = -1 where cardid = %s"
                                val = (cardid,)
                                mycursor.execute(cmnd,val)
                                db.commit()
                                print("SUCCESS: You have successfully returned the book: ", p[1])
                        else:
                                print("ALERT: Skipped book return.")
                                pass
                elif userlist[7] == -1:
                        cmnd = "select * from books where id = %s"
                        val = (userlist[6],)
                        mycursor.execute(cmnd, val)
                        p = mycursor.fetchone()
                        print("Enter 1 to return: ", p[1])
                        print("Press enter if you do not want to return this book. ")
                        ch1 = input("")
                        if ch1 == '1':
                                cmnd = "update books set count = %s where id = %s"
                                val = (p[5]+1,userlist[6])
                                mycursor.execute(cmnd,val)
                                cmnd = "update users set booksinposession = %s where cardid = %s"
                                val = (userlist[4]-1, cardid)
                                mycursor.execute(cmnd, val)
                                cmnd = "update users set book1 = -1 where cardid = %s"
                                val = (cardid,)
                                mycursor.execute(cmnd, val)
                                db.commit()
                                print("SUCCESS: You have successfully returned the book: ", p[1])
                        else:
                                print("ALERT: Skipped book return.")
                                pass
                else:
                        cmnd = "select * from books where id = %s"
                        val = (userlist[6],)
                        mycursor.execute(cmnd, val)
                        p = mycursor.fetchone()
                        print("Enter 1 to return: ", p[1])
                        cmnd = "select * from books where id = %s"
                        val = (userlist[7],)
                        mycursor.execute(cmnd, val)
                        k = mycursor.fetchone()
                        print("Enter 2 to return: ", k[1])
                        print("Press enter if you do not want to return this book. ")
                        ch1 = input("")
                        if ch1 == '1':
                                cmnd = "update books set count = %s where id = %s"
                                val = (p[5] + 1, userlist[7])
                                mycursor.execute(cmnd, val)
                                cmnd = "update users set booksinposession = %s where cardid = %s"
                                val = (userlist[4] - 1, cardid)
                                mycursor.execute(cmnd, val)
                                cmnd = "update users set book2 = -1 where cardid = %s"
                                val = (cardid,)
                                mycursor.execute(cmnd, val)
                                db.commit()
                                print("SUCCESS: You have successfully returned the book: ", p[1])
                        elif ch1 == '2':
                                cmnd = "update books set count = %s where id = %s"
                                val = (k[5] + 1, userlist[7])
                                mycursor.execute(cmnd, val)
                                cmnd = "update users set booksinposession = %s where cardid = %s"
                                val = (userlist[4] - 1, cardid)
                                mycursor.execute(cmnd, val)
                                cmnd = "update users set book2 = -1 where cardid = %s"
                                val = (cardid,)
                                mycursor.execute(cmnd, val)
                                db.commit()
                                print("SUCCESS: You have successfully returned the book: ",k[1])
                        else:
                                print("ALERT: Skipped book return.")
        except:
                print("ERROR: Please enter a valid book ID.\n\n")
        ch = input('Press enter to continue...')
        system('cls')

def deleteBook():
        global cardid
        global AdminLogin
        if AdminLogin == True:
                print("*" * 50, "DELETE BOOK", "*" * 50)
                print("1 Delete by ID\n2 Delete by name")
                ch1 = input("")
                if ch1 == '1':
                        id = input("Enter the ID of the book you want to delete: ")
                        cmnd1 = "select id, name from books where id = %s"
                        val1 = (id,)
                        mycursor.execute(cmnd1, val1)
                        p = mycursor.fetchall()
                        if len(p) == 0:
                                print("ERROR: The book ID you entered does not exist. Please try again.")
                        else:
                                print("Book ID: ", p[0][0])
                                print("Book name: ", p[0][1])
                                ch1 = input("Confirm deletion? (y/n): ")
                                if ch1 == 'y':
                                        cmnd = "delete from books where ID = %s"
                                        val = (id,)
                                        mycursor.execute(cmnd, val)
                                        db.commit()
                                        print("SUCCESS: The book with ID: ", id, " has been deleted.\n\n")
                                elif ch1 == 'n':
                                        print("ABORTED: Deletion of the book was cancelled.\n\n ")
                                else:
                                        print("ABORTED: Interpreting vague answer as NO. Deleteion was cancelled.\n\n")
                elif ch1 == '2':
                        id = input("Enter the NAME of the book you want to delete: ")
                        cmnd1 = "select id, name from books where name = %s"
                        val1 = (id,)
                        mycursor.execute(cmnd1, val1)
                        p = mycursor.fetchall()
                        if len(p) == 0:
                                print("ERROR: The book name you entered does not exist. Please try again.")
                        else:
                                print("Book ID: ", p[0][0])
                                print("Book name: ", p[0][1])
                                ch1 = input("Confirm deletion? (y/n): ")
                                if ch1 == 'y' or ch1 == 'Y' or ch1 == 'YES' or ch1 == 'yes':
                                        cmnd = "delete from books where ID = %s"
                                        val = (id,)
                                        mycursor.execute(cmnd, val)
                                        db.commit()
                                        print("SUCCESS: The book with ID: ", id, " has been deleted.\n\n")
                                elif ch1 == 'n' or ch1 == 'N' or ch1 == 'NO' or ch1 == 'no':
                                        print("ABORTED: Deletion of the book was cancelled.\n\n ")
                                else:
                                        print("ABORTED: Interpreting vague answer as NO. Deleteion was cancelled.\n\n")
                else:
                        print("ERROR: Please enter a valid option. (1/2)")
                ch = input('Press enter to continue...')
        else:
                print("ERROR: Access denied.")
                ch1 = input("Press any key to continue...")
        system('cls')

def registerUser():
        system('cls')
        while True:
                try:
                        print("*" * 50, "REGISTER NEW USERS", "*" * 50)
                        print("Please enter the details of the user\n")

                        while True:
                                cardID = random.randint(100, 999)
                                cmnd2 = "select * from users where cardID = %s"
                                val2 = (cardID,)
                                mycursor.execute(cmnd2, val2)
                                k = mycursor.fetchall()
                                if len(k) == 0:
                                        break
                                else:
                                        cardID = random.randint(100, 999)
                        print(cardID)
                        username = str(input("Enter username: "))
                        password = str(input("Enter Password: "))
                        cpassword = str(input("Confirm Password: "))
                        if password == '':
                                raise NameError
                        elif password == cpassword:
                                print("\n Passwords match. Please proceed")
                                if len(password) <= 5:
                                        print("Password strength: Low\n")
                                elif len(password) <=8:
                                        print("Password strength: Medium\n")
                                else:
                                        print("Password strength: High\n")
                                date_issue = datetime.date.today()
                                cmnd = "INSERT into users values (%s,%s,%s,0,0,%s,-1,-1)"
                                val = (cardID, username, date_issue, password)
                                mycursor.execute(cmnd, val)
                                ch1 = input("Confirm entry? (y/n): ")
                                if ch1 == 'y' or ch1 == 'Y' or ch1 == 'YES' or ch1 == 'yes':
                                        db.commit()
                                        print("SUCCESS: The new user was registered.")
                                        ch1 = input("Would you like to print a reciept? (y/n): ")
                                        if ch1 == 'y' or ch1 == 'Y' or ch1 == 'YES' or ch1 == 'yes':
                                                print("\n\n")
                                                print(" Card ID: ", cardID, "\n",
                                                      "Password: ", password, "\n",
                                                      "Username: ", username, "\n",
                                                      "Issued on: ", date_issue, "\n")
                                        else:
                                                print('Skipped reciept')
                                elif ch1 == 'n' or ch1 == 'N' or ch1 == 'NO' or ch1 == 'no':
                                        print("ABORTED: Registration cancelled.\n")
                                else:
                                        print("Interpreting input as 'no'. Registration cancelled.\n")
                        else:
                                print("\nPasswords do not match. Please try again.\n")
                        print("\n")

                except:
                        print(
                                "ERROR: You have entered an invalid input for one of the fields. Please check your input and try again.\n"
                                "-> Username and Password cannot be left empty\n"
                                "-> The string inputs may not exceed 40 characters.\n\n")
                ch = input("Would you like to register another user? (y/n): ")
                ("\n\n")
                if ch == 'y':
                        system('cls')
                        continue
                elif ch == 'n':
                        break
                else:
                        print("Interpretting vague input as NO.")
                        break
        ch2 = input("Press enter to return to main menu...")
        system('cls')

def editUser():
 system('cls')
 global AdminLogin
 global cardid
 try:
        print("*" * 50, "EDIT USER INFO", "*" * 50)
        if AdminLogin == True:
                cardid = int(input("Enter cardID: "))
        else:
                pass
        print("\n\n")
        cmnd = "select * from users where cardid = %s"
        val = (cardid,)
        mycursor.execute(cmnd, val)
        k = mycursor.fetchall()
        if len(k) == 0:
                print("ERROR: This user is not registered with us in the library.")
        else:
                print("Card ID: ", cardid)
                print("Username: ", k[0][1])
                print("Current Password: ", k[0][5])
                print("Date of Issue: ", k[0][2])
                print("Total books issued: ", k[0][3])
                print("Books currently in posession: ", k[0][4])
                print("*"*100)
                print("Please enter NEW details of the user\n")
                username = input("Enter new username: ")
                npass = input("Enter new password: ")
                if AdminLogin == True:
                        tbooks = int(input("Total books issued: "))
                        posession = int(input("Books in posession: "))
                        cmnd2 = "update users set username = %s, totalbooksissued = %s, booksinposession = %s, password = %s where cardid = %s"
                        val2 = (username,tbooks,posession,npass,cardid)
                        mycursor.execute(cmnd2,val2)
                else:
                        cmnd2 = "update users set username = %s, password = %s where cardid = %s"
                        val2 = (username, npass, cardid)
                print("\n\n")
                ch1 = input("Confirm edit? (y/n): ")
                if ch1 == 'y' or ch1 == 'Y' or ch1 == 'YES' or ch1 == 'yes':
                        mycursor.execute(cmnd2, val2)
                        db.commit()
                        print("SUCCESS: The new records were edited in the database.")
                elif ch1 == 'n' or ch1 == 'N' or ch1 == 'NO' or ch1 == 'no':
                        print("ABORTED: This record was not edited into the database.")
                else:
                        print("Interpreting vague input as 'no'. This record was not edited into database.")
                ch = input("Press Enter to continue...")
 except MathError:
         print("ERROR: Wrong cardID and/or password combination. Please try again.")
 except:
         print("ERROR: Something went wrong. Please check your inputs and try again.")
         print("-> Card ID must be correctly input")
         print("-> Total books issued and books in posession should be integers")

 system('cls')

def allUser():
        system('cls')
        print("*" * 50, "ALL USERS", "*" * 50)
        mycursor.execute("select * from users")
        l1 = mycursor.fetchall()
        if AdminLogin == True:
                print("CardID   Username    Password\n")
                for i in l1:
                        print(i[0], "  ", i[1], "    ", i[5])
        if AdminLogin == False:
                print("CardID   Username")
                for i in l1:
                        print(i[0], "  ", i[1])
        ch = input("Press enter to continue...")
        system('cls')

def infoUser():
 global AdminLogin
 global cardid
 system('cls')
 try:
        if AdminLogin == True:
                cardid = input("Enter cardid: ")
        else:
                pass
        print("*"*50,"USER INFO",'*'*50)
        print("\n")
        cmnd = "select * from users where cardid = %s"
        val = (cardid,)
        mycursor.execute(cmnd, val)
        k = mycursor.fetchall()
        if len(k) == 0:
                print("ERROR: This user is not registered with us in the library.")
        else:
                print("Card ID: ", cardid)
                print("Username: ", k[0][1])
                print("Current Password: ", k[0][5])
                print("Date of Issue: ", k[0][2])
                print("Total books issued: ", k[0][3])
                print("Books currently in posession: ", k[0][4])

 except:
         print("ERROR: CardID is necessary to display user info. Please enter a valid card ID")
 ch = input("Press Enter to continue...")
 system('cls')

def deleteUser():
        global AdminLogin
        if AdminLogin == True:
                system('cls')
                print("*" * 50, "DELETE USER", "*" * 50)
                id = input("Enter the cardID of the user you want to delete: ")
                cmnd1 = "select cardid, username from users where cardid = %s"
                val1 = (id,)
                mycursor.execute(cmnd1, val1)
                p = mycursor.fetchall()
                if len(p) == 0:
                        print("ERROR: The cardID you entered does not exist. Please try again.")
                else:
                        print("Card ID: ", p[0][0])
                        print("Username: ", p[0][1])
                        ch1 = input("Confirm deletion? (y/n): ")
                        if ch1 == 'y' or ch1 == 'Y' or ch1 == 'YES' or ch1 == 'yes':
                                cmnd = "delete from users where cardid = %s"
                                val = (id,)
                                mycursor.execute(cmnd, val)
                                db.commit()
                                print("SUCCESS: The user with ID: ", id, " has been deleted.\n\n")
                        elif ch1 == 'n' or ch1 == 'N' or ch1 == 'NO' or ch1 == 'no':
                                print("ABORTED: Deletion of the user was cancelled.\n\n ")
                        else:
                                print("ABORTED: Interpreting vague answer as NO. Deleteion was cancelled.\n\n")
                ch = input("Press Enter to continue...")
                system('cls')
        else:
                print("ERROR: Access denied.")
                ch1 = input("Press enter to continue...")

#Menu

def Login():
 global p
 erc = 0
 try:
        global AdminLogin
        global loginfo
        print(

"                                     ██╗░░░░░██╗██████╗░██████╗░░█████╗░██████╗░██╗██╗░░░██╗███╗░░░███╗\n"
"                                     ██║░░░░░██║██╔══██╗██╔══██╗██╔══██╗██╔══██╗██║██║░░░██║████╗░████║\n"
"                                     ██║░░░░░██║██████╦╝██████╔╝███████║██████╔╝██║██║░░░██║██╔████╔██║\n"
"                                     ██║░░░░░██║██╔══██╗██╔══██╗██╔══██║██╔══██╗██║██║░░░██║██║╚██╔╝██║\n"
"                                     ███████╗██║██████╦╝██║░░██║██║░░██║██║░░██║██║╚██████╔╝██║░╚═╝░██║\n"
"                                     ╚══════╝╚═╝╚═════╝░╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░░╚═╝╚═╝░╚═════╝░╚═╝░░░░░╚═╝\n\n")
        print("                                              Welcome user. Please login or sign up to continue \n\n")
        print("                                                           1. PRESS 1 TO LOG IN AS ADMINISTRATOR")
        print('                                                           2. PRESS 2 TO LOG IN AS A USER       ')
        print("                                                           3. PRESS 3 TO VIEW RULES, TERMS AND CONDITIONS")
        print("                                                           4. PRESS 4 TO REGISTER AS A NEW USER.")
        print("                                                           5. PRESS 5 TO EXIT.")
        ch = input("                                                         ENTER HERE: ")
        system('cls')
        if ch == '1':
                system('cls')
                password = input("Enter administrator password: ")
                if password == 'abcd':
                        print("Fetching data")
                        for i in range(5):
                                time.sleep(0.3)
                                print(".",end='')
                        print("\n\n")
                        print("Welcome Administrator. Please proceed.\n")


                        ch1 = input("Press enter to continue...")
                        AdminLogin = True
                        loginfo = True
                else:
                        print("The password you entered was incorrect. Please return to homescreen and try again.")
                        ch1 = input("Press enter to continue...")
        elif ch == '2':
                system('cls')
                global cardid
                AdminLogin = False
                cardid = input("Please enter your card ID: ")
                password = input("Please enter your password: ")
                cmnd = "select * from users where cardid = %s"
                val = (cardid,)
                mycursor.execute(cmnd, val)
                k = mycursor.fetchone()
                if len(k) == 0:
                        erc = 1
                        raise MathError
                if k[5] == password:
                        print("Welcome, ", k[1], ". Please proceed.\n")
                        loginfo = True
                        ch1=input("Press enter to continue...")
                else:
                        erc=1
                        raise MathError
        elif ch == '3':
                print("Hello user, welcome to Librarium.\n"
                      "We at Librarium believe that book serve as a vital source of information and guidance for anyone regardless of age. We believe that a pleasant environment and a good book reading session can have a \n"
                      "massively positive impact on one's life and therefore we strive to present our customers with the same. \n")
                print("Librarium has many features that make it the perfect place to spend time working on yourself or your studies. Some of the sailent features of the library are:\n"
                      "-> 24/7 open reading space for registered customers\n"
                      "-> Over 2,000 books from a wide variety of generes to choose from\n"
                      "-> Coffee and tea served in reading spaces\n"
                      "-> Fully A/C facility\n"
                      "-> Sound proof walls for maximum focus\n")
                guidelines()
                ch = input("Press enter to continue...")
        elif ch == '4':
                registerUser()
        elif ch == '5':
                p = 1
 except:
        print("ERROR: Wrong ID or password. Please try again.")
        ch1 = input("Press enter to return to homescreen...")

 system('cls')

def Menu(choice):
 global loginfo
 global AdminLogin
 system('cls')
 try:
        if choice == 1:
         if AdminLogin == True:
                print("*" * 30, "LIBRARY MANAGEMENT SYSTEM v3.2.6 by Hardik Bhatia", "*" * 30)
                print("\n******************* MANAGE BOOKS *******************\n")
                print("1. Enter new books")
                print("2. Edit book information")
                print("3. Delete a book")
                ch1 = int(input(""))
                if ch1 == 1:
                        bookWrite()
                elif ch1 == 2:
                        bookEdit()
                elif ch1 == 3:
                        deleteBook()
                else:
                        raise NameError
         else:
                print("Access Denied.")
                ch1 = input("Press enter to return to main menu...")
                system('cls')
        elif choice ==2:
                print("*" * 30, "LIBRARY MANAGEMENT SYSTEM v3.2.6 by Hardik Bhatia", "*" * 30)
                print("\n******************* BOOK INFORMATION *******************\n")
                print("1. List of all books")
                print("2. Check full details of a book")
                ch1 = int(input(""))
                if ch1 == 1:
                        allBooks()
                elif ch1 == 2:
                        bookInfo()
                else:
                        raise NameError
        elif choice == 3:
                print("*" * 30, "LIBRARY MANAGEMENT SYSTEM v3.2.6 by Hardik Bhatia", "*" * 30)
                print("\n******************* ISSUE / RETURN BOOK *******************\n")
                print("1. Issue a book")
                print("2. Return a book")
                ch1 = int(input(""))
                if ch1 == 1:
                        issueBooks()
                elif ch1 == 2:
                        returnBooks()
                else:
                        raise NameError
        elif choice == 4:
                print("*" * 30, "LIBRARY MANAGEMENT SYSTEM v3.2.6 by Hardik Bhatia", "*" * 30)
                print("\n******************* MANAGE USERS *******************\n")
                print("1. Register users")
                print("2. Edit user details")
                print("3. Details of user")
                print("4. List of all users")
                print("5. Delete users")
                ch1 = int(input(""))
                if ch1 == 1:
                        registerUser()
                elif ch1 ==2:
                        editUser()
                elif ch1 == 3:
                        infoUser()
                elif ch1 == 4:
                 if AdminLogin == True:
                        allUser()
                 else:
                        print("Access denied.")
                        ch1 = input("Press enter to return to main menu")
                        system('cls')
                elif ch1 ==5:
                        if AdminLogin == True:
                                deleteUser()
                        else:
                                print("Access denied.")
                                ch1 = input("Press enter to return to main menu")
                                system('cls')
                else:
                        raise NameError
        elif choice == 5:
                loginfo = False
        else:
                print("ERROR: Please enter a valid number to perform an operation.")
                ch = input("Press Enter to continue...")
                system('cls')
 except:
         print("Please enter a valid input according to the given options.")
         ch = input("Press Enter to continue...")
         system('cls')

def mainmenu():
        global loginfo
        global AdminLogin
        print("*" * 30, "LIBRARY MANAGEMENT SYSTEM v3.2.6 by Hardik Bhatia", "*" * 30)
        print("Please enter the serial number of the function you would like to perform.")
        print("1. Manage books")
        print("2. Book Information")
        print("3. Issue / Return a book")
        print("4. Manage users")
        print("5. Log out and return to homescreen")
        try:
                x = int(input(""))
                Menu(x)
        except:
                print("ERROR: Please enter a valid number to perform an operation.")
                ch=input("Press Enter to continue...")
                system('cls')

p = 0
while True:
        AdminLogin = False
        loginfo = False
        Login()
        while loginfo == True:
                mainmenu()
        if p == 1:
                break
        else:
                pass
