import sys
import pickle
import logging

from Bank import Bank
from Transactions import Transaction, InvalidamounsError, Base
from Accounts import OverdrawError, TransactionOrderError, TransactionLimitError

import sqlalchemy
from sqlalchemy.orm.session import sessionmaker


class BankCLI():
    def __init__(self):
        self._session = Session()
        # self._bank = Bank()
        self._bank = self._session.query(Bank).first()
        logging.debug(f'Loaded from bank.db')
        if not self._bank:
            self._bank = Bank()
            self._session.add(self._bank)
            self._session.commit()
            logging.debug(f'Saved to bank.db')
        self._selected_account = None
        self._choices = {
            "open account": self._open_account,
            "summary": self._summary,
            "select account": self._select,
            "list transactions": self._list_transactions,
            "add transaction": self._add_transaction,
            "<monthly triggers>": self._monthy_triggers,
            "save": self._save,
            "load": self._load,
            "quit": self._quit,
        }


    def _display_menu(self):
        print(f"Currently selected account: {self._selected_account}")
        options = ", ".join(self._choices.keys())
        print('Enter command')
        print(options)

    def run(self):        
        """Display the menu and respond to choices."""

        while True:
            self._display_menu()
            choice = input(">")
            action = self._choices.get(choice)
            if action:
                action()
            else:
                print("{0} is not a valid choice".format(choice))


    def _summary(self):
        for x in self._bank.show_accounts():
            print(x)


    def _load(self):
        with open("save.pickle", "rb") as f:
            self._bank = pickle.load(f)
            logging.debug(f'Loaded from bank.pickle')

    def _save(self):
        
        with open("save.pickle", "wb") as f:
            pickle.dump(self._bank, f)
            logging.debug(f'Saved to bank.pickle')

    def _quit(self):
        sys.exit(0)

    def _add_transaction(self):

        date = input("Date? (YYYY-MM-DD)\n>")
        amount = input("Amount?\n>")

        try:
            t = Transaction(amount, date)
        # Transaction dates given in improper format
        except ValueError:
            print("Please try again with a valid date in the format YYYY-MM-DD.")
        # Invalid amounts given
        except InvalidamounsError:
            print("Please try again with a valid dollar amount.")
        except Exception as err:
            print(
                "Sorry! Something unexpected happened. If this problem persists please contact our support team for assistance.")
            logging.error(f"{exception.__name__}: {repr(value)}")
            sys.exit(1)

        else:

            # Listing or adding transactions when no account is selected
            try:
                self._selected_account.add_transaction(t)
                acct_num = self._selected_account.get_account_num()
                self._session.commit()
                logging.debug(f'Created transaction: {acct_num}, {float(amount):,.2f}')
                logging.debug(f'Saved to bank.db')
            except AttributeError:
                print("That command requires that you first select an account.")
            except OverdrawError:
                print("This transaction could not be completed due to an insufficient account balance.")
            except TransactionLimitError:
                print("This transaction could not be completed because the account has reached a transaction limit.")
            except TransactionOrderError as e:
                print(f'New transactions must be from <{e.lasted_date}> onward.')




    def _open_account(self):
        type = input("Type of account? (checking/savings)\n>")
        initial_deposit = input("Initial deposit amount?\n>")
        # a, acct_num = self._bank.add_account(type, self._session)
        try:
            a, acct_num = self._bank.add_account(type, self._session)
        except Exception as err:
            print("Sorry! Something unexpected happened. If this problem persists please contact our support team for assistance.")
            logging.error(f"{exception.__name__}: {repr(value)}")
            sys.exit(1)

        # Invalid amounts given
        try:
            t = Transaction(initial_deposit)
            a.add_transaction(t)
            self._session.commit()
            logging.debug(f'Created account: {acct_num}')
            logging.debug(f'Created transaction: {acct_num}, {float(initial_deposit):,.2f}')
            logging.debug(f'Saved to bank.db')
        except InvalidamounsError:
            print("Please try again with a valid dollar amount.")
        except Exception as err:
            print("Sorry! Something unexpected happened. If this problem persists please contact our support team for assistance.")
            logging.error(f"{exception.__name__}: {repr(value)}")
            sys.exit(1)



        self._summary()


    def _select(self):
        self._summary()
        try:
            num = int(input("Enter account number\n>"))
        except Exception as err:
            print("Sorry! Something unexpected happened. If this problem persists please contact our support team for assistance.")
            logging.error(f"{exception.__name__}: {repr(value)}")
            sys.exit(1)
        self._selected_account = self._bank.get_account(num)
        self._session.commit()
        logging.debug(f'Saved to bank.db')


    def _monthy_triggers(self):
        self._bank.assess_interest()
        try:
            self._bank.assess_fees()
        except OverdrawError:
            messagebox.showerror(
                message="This transaction could not be completed due to an insufficient account balance.")
        except Exception as err:
            print("Sorry! Something unexpected happened. If this problem persists please contact our support team for assistance.")
            logging.error(f"{exception.__name__}: {repr(value)}")
            sys.exit(1)
        logging.debug(f'Triggered fees and interest')
        self._session.commit()
        logging.debug(f'Saved to bank.db')

    def _list_transactions(self):
        # Listing or adding transactions when no account is selected
        # for x in self._selected_account.get_transactions():
        #     print(x)
        try:
            for x in self._selected_account.get_transactions():
                print(x)
        except AttributeError:
            print("That command requires that you first select an account.")



if __name__ == "__main__":
    engine = sqlalchemy.create_engine(f"sqlite:///bank.db")
    Base.metadata.create_all(engine)

    Session = sessionmaker()
    Session.configure(bind=engine)

    # log messages to a file, ignoring anything less severe than ERROR
    logging.basicConfig(filename='bank.log', level=logging.DEBUG,
                        format='%(asctime)s|%(levelname)s|%(message)s', datefmt='%Y-%m-%d %I:%M:%S')

    BankCLI().run()

