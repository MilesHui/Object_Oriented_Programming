from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, FLOAT, BOOLEAN
Base = declarative_base()
from sqlalchemy.types import TypeDecorator

class InvalidamounsError(Exception):
    pass


class MyTime(TypeDecorator):
    impl = String

    def __init__(self, length=None, format="%Y-%m-%d", **kwargs):
        super().__init__(length, **kwargs)
        self.format = format

    def process_literal_param(self, value, dialect):
        # allow passing string or time to column
        if isinstance(value, str):
            value = datetime.strptime(value, self.format).time()

        # convert python time to sql string
        return value.strftime(self.format) if value is not None else None

    process_bind_param = process_literal_param

    def process_result_value(self, value, dialect):
        # convert sql string to python time
        return datetime.strptime(value, self.format).date() if value is not None else None



class Transaction(Base):

    __tablename__ = "transaction"
    _amt = Column(FLOAT)
    _id = Column(Integer, primary_key=True)
    _account_id = Column(Integer, ForeignKey("account._id"))
    _date = Column(MyTime(length=10))
    _exempt = Column(BOOLEAN)




    def __init__(self, amt, date=None, exempt=False):

        if date is None:
            self._date = datetime.now().date()
        else:
            self._date = datetime.strptime(date, "%Y-%m-%d").date()

        try:
            self._amt = float(amt)
        except ValueError:
            raise InvalidamounsError


        self._exempt = exempt

    def __str__(self):
        return f"{self._date}, ${self._amt:,.2f}"

    def is_exempt(self):
        return self._exempt

    def in_same_day(self, other):
        return self._date == other._date

    def in_same_month(self, other):
        return self._date.month == other._date.month and self._date.year == other._date.year

    def __radd__(self, other):
        # allows us to use sum() with transactions
        # return other + self._amt

        return  other + self._amt

    def check_balance(self, balance):
        return self._amt >= 0 or balance > abs(self._amt)

    def get_amt(self):
        return self._amt




