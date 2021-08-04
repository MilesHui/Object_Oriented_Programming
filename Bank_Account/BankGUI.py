import sys
import pickle
import logging
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

from Bank import Bank
from Transactions import Transaction, InvalidamounsError, Base
from Accounts import OverdrawError, TransactionOrderError, TransactionLimitError

import sqlalchemy
from sqlalchemy.orm.session import sessionmaker


class BankGUI:
    def __init__(self):
        self._window = tk.Tk()
        self._window.title("MY BANK")
        self._window.report_callback_exception = self.handle_exception

        self._session = Session()
        self._bank = self._session.query(Bank).first()
        if not self._bank:
            self._bank = Bank()
            self._session.add(self._bank)
            self._session.commit()
        self._selected_account = None
        self._selected_account_frame = tk.Frame(self._window)
        self._options_frame = tk.Frame(self._window)
        self._account_frame = tk.Frame(self._window)
        self._transaction_frame = tk.Frame(self._window, relief='sunken', borderwidth =2)

        self._accounts = {}
        self._transactions = {}
        self.v = tk.IntVar()
        for widget in self._selected_account_frame.winfo_children():
            widget.destroy()
        tk.Message(self._selected_account_frame, command=self._select(self._selected_account)).grid(row=0, column=0),
        tk.Button(self._options_frame, text="open account", command=self._open_account).grid(row=2, column=1, columnspan=3),
        tk.Button(self._options_frame, text="add transaction", command=self._add_transaction).grid(row=2, column=4),
        tk.Button(self._options_frame, text="<monthly triggers>", command=self._monthy_triggers).grid(row=2, column=5),
        tk.Message(self._account_frame, command = self._summary(),justify= 'left').grid(row=1, column=0, columnspan=3),

        self._selected_account_frame.grid(row=0, column = 0, columnspan=3)
        self._options_frame.grid(row=1, column=1, columnspan=2)
        self._account_frame.grid(row=2, column=1, columnspan=1, sticky="NE")
        self._transaction_frame.grid(row=2, column=2, columnspan=1, sticky="NE")


        self._window.mainloop()

    @staticmethod
    def handle_exception(exception, value, traceback):
        messagebox.showerror(message=
            "Sorry! Something unexpected happened. If this problem persists please contact our support team for assistance.")
        logging.error(f"{exception.__name__}: {repr(value)}")
        sys.exit(1)



    def _display_menu(self):

        x = self._selected_account
        for widget in self._selected_account_frame.winfo_children():
            widget.destroy()

        string_var = tk.StringVar()
        string_var.set('Selected account: '+ str(x))

        b = tk.Label(self._selected_account_frame, textvariable= string_var,
                      relief='flat').grid(row=0, column=1)



    def _summary(self):

        row = 0

        for x in self._bank.show_accounts():
            if x._id not in self._accounts:
                # sets up a dictionary of StringVars associated with the buttons created
                self._accounts[x._id] = tk.StringVar(value=str(x))
                tk.Radiobutton(self._account_frame, text=str(x), value=x._id,variable=self.v, textvariable=self._accounts[x._id],
                               command=lambda acc=x: [self._select(acc),self._list_transactions(acc)]).grid(row=row, column=1, sticky='wn')
            else:
                # reuse the old button, but set the StringVar to change its label
                self._accounts[x._id].set(str(x))
            row += 1


    def _quit(self):
        sys.exit(0)

    def _add_transaction(self):

        def add():
            try:
                t = Transaction(e2.get(), e1.get())
            # Transaction dates given in improper format
            except ValueError:
                messagebox.showerror(message="Please try again with a valid date in the format YYYY-MM-DD.")
            # Invalid amounts given
            except InvalidamounsError:
                messagebox.showerror(message="Please try again with a valid dollar amount.")


            else:

                # Listing or adding transactions when no account is selected
                try:
                    self._selected_account.add_transaction(t)
                    acct_num = self._selected_account.get_account_num()
                    self._session.commit()
                    logging.debug(f'Created transaction: {acct_num}, {float(e2.get()):,.2f}')
                except AttributeError:
                    messagebox.showerror(message="That command requires that you first select an account.")
                except OverdrawError:
                    messagebox.showerror(
                        message="This transaction could not be completed due to an insufficient account balance.")
                except TransactionLimitError:
                    messagebox.showerror(
                        message="This transaction could not be completed because the account has reached a transaction limit.")
                except TransactionOrderError as e:
                    messagebox.showerror(message=f'New transactions must be from {e.lasted_date} onward.')

            e1.destroy()
            b.destroy()
            l1.destroy()
            e2.destroy()
            l2.destroy()
            if self._selected_account:
                self._list_transactions(self._selected_account)
            self._display_menu()
            self._summary()


        l1 = tk.Label(self._options_frame, text="Date:", justify='right')
        l1.grid(row=3, column=3)
        e1 = tk.Entry(self._options_frame)
        e1.grid(row=3, column=4)
        l2 = tk.Label(self._options_frame, text="Amount:", justify='right')
        l2.grid(row=4, column=3)
        e2 = tk.Entry(self._options_frame)
        e2.grid(row=4, column=4)

        b = tk.Button(self._options_frame, text="Enter", command=add)
        b.grid(row=5, column=4)




    def _open_account(self):

        def add():

            try:
                a, acct_num = self._bank.add_account(c.get(), self._session)
                t = Transaction(e1.get())
                a.add_transaction(t)
                self._session.commit()
                logging.debug(f'Created account: <{acct_num}>')
            except InvalidamounsError:
                messagebox.showerror(message="Please try again with a valid dollar amount.")

            e1.destroy()
            b.destroy()
            l1.destroy()
            drop.destroy()
            self._summary()


        l1 = tk.Label(self._options_frame, text="Initial deposit")
        l1.grid(row=3, column=1,columnspan = 1)
        e1 = tk.Entry(self._options_frame)
        e1.grid(row=4, column=1,columnspan = 2)

        c = tk.StringVar()
        options = [
            "checking",
            "savings",
        ]
        drop = tk.OptionMenu(self._options_frame, c, *options)
        drop.grid(row=5, column=1)
        b = tk.Button(self._options_frame, text="Enter", command=add)
        b.grid(row=5, column=2)




    def _select(self,account):


        for widget in self._selected_account_frame.winfo_children():
            widget.destroy()
        string_var = tk.StringVar()
        if account:
            num = account.get_account_num()
            self._selected_account = self._bank.get_account(num)
            self._session.commit()
            for widget in self._selected_account_frame.winfo_children():
                widget.destroy()
            string_var.set('Selected account: ' + str(self._selected_account))
            tk.Label(self._selected_account_frame, textvariable=string_var, relief='flat').grid(row=0, column=1)



        else:
            tk.Button(self._selected_account_frame, text='Selected account: ',
                          relief='flat').grid(row=0, column=1)



    def _monthy_triggers(self):
        self._bank.assess_interest()
        try:
            self._bank.assess_fees()
        except OverdrawError:
            messagebox.showerror(
                message="This transaction could not be completed due to an insufficient account balance.")

        logging.debug(f'Triggered fees and interest')
        self._session.commit()
        self._summary()
        if self._selected_account:
            self._list_transactions(self._selected_account)
        self._display_menu()



    def _list_transactions(self, account):

        for widget in self._transaction_frame.winfo_children():
            widget.destroy()
        row = 0

        for x in account.get_transactions():
            if x.get_amt() >= 0:
                tk.Label(self._transaction_frame, text=x, justify='left',  relief='flat',fg='green').grid(row=row,column=1, sticky='wn')
            elif x.get_amt() < 0:
                tk.Label(self._transaction_frame, text=x, justify='left', relief='flat', fg='red').grid(row=row,
                                                                                                           column=1, sticky='wn')
            row+=1




if __name__ == "__main__":
    engine = sqlalchemy.create_engine(f"sqlite:///bank.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    # log messages to a file, ignoring anything less severe than ERROR
    logging.basicConfig(filename='bank.log', level=logging.DEBUG,
                        format='%(asctime)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %I:%M:%S')


    BankGUI()

