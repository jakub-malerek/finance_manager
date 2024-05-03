from utils import string_has_numbers, string_has_special_characters
from random import randint
from datetime import datetime
from copy import deepcopy


class Account:
    def __init__(self, name, second_name, balance_cash, balance_card) -> None:
        self.name = name
        self.second_name = second_name
        self.balance_cash = balance_cash
        self.balance_card = balance_card
        self.id = self.id_generator()
        self.account_created_date = datetime.today().strftime("%Y-%m-%d")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, _name):
        self.validate_name(_name)
        self._name = _name

    @property
    def second_name(self):
        return self._second_name

    @second_name.setter
    def second_name(self, _second_name):
        self.validate_name(_second_name)
        self._second_name = _second_name

    @property
    def id(self):
        return self._id

    @property
    def balance_cash(self):
        return self._balance_cash

    @balance_cash.setter
    def balance_cash(self, _balance_cash):
        self.validate_balance(_balance_cash)
        self._balance_cash = _balance_cash

    @property
    def balance_card(self):
        return self._balance_card

    @balance_card.setter
    def balance_card(self, _balance_card):
        self.validate_balance(_balance_card)
        self._balance_card = _balance_card

    @id.setter
    def id(self, _id):
        if len(_id) == 10:
            if isinstance(_id, str):
                self._id = _id
            else:
                raise TypeError(
                    f"ID should be an string, input of type \"{type(_id)}\" was given.")
        else:
            raise ValueError("ID should be 10 numbers long.")

    @property
    def account_created_date(self):
        return self._account_created_date

    @account_created_date.setter
    def account_created_date(self, date):
        self.validate_date(date)
        self._account_created_date = date

    def validate_date(self, date_input):
        try:
            datetime.strptime(date_input, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                "Invalid date format. Date should be in the format 'YYYY-mm-dd'.")

    def validate_name(self, name_input):
        if isinstance(name_input, str):
            if not (1 <= len(name_input) <= 100):
                raise ValueError(
                    "Name or second name length should be between 1 and 100 characters.")
            if string_has_numbers(name_input):
                raise ValueError(
                    "Name or second name should contain only alphabet characters, no numbers are allowed.")
            if string_has_special_characters(name_input):
                raise ValueError(
                    "Name or second name should not contain any special characters like: !,$,@ etc.")
            return True
        else:
            raise TypeError(
                f"Name of second name should be an alphabetic word, input of type \"{type(name_input)}\" was given.")

    def validate_balance(self, balance_input):
        if not isinstance(balance_input, (float, int)):
            raise TypeError(
                f"Balance should be a number, input of type \"{type(balance_input)}\" was given")
        if not (balance_input > 0):
            raise ValueError("Balance cannot be less than 0")

    def id_generator(self):
        return str(randint(0, 9))+str(randint(100_000_000, 999_999_999))

    def account_info(self):
        return f"Name: {self.name}, Second name: {self.second_name}, Cash balance: {self.balance_cash}, Card balance: {self.balance_card}, Account created: {self.account_created_date}"


class AccountManager:
    def __init__(self):
        self.accounts = {}

    def create_account(self,  name, second_name, balance_cash, balance_card):
        self.add_account(
            Account(name, second_name, balance_cash, balance_card))

    def add_account(self, account):
        if isinstance(account, Account):
            self.accounts[account.id] = account
        else:
            raise TypeError(
                f"Account class object is expected, \"{type(account)}\" type was given.")

    def get_account(self, id):
        if id in self.accounts.keys():
            return self.accounts[id]
        else:
            raise ValueError(f"No account of given id {id} was found.")

    def display_account(self, id):
        return self.get_account(id).account_info()

    def return_accounts(self):
        return list(self.accounts.values()).copy()

    def display_accounts(self):
        for account in self.accounts.values():
            yield account.account_info()

    def update_account(self, id, **kwargs):
        account = self.get_account(id)
        account_copy = deepcopy(account_copy)
        account_attributes = [atr for atr in dir(
            account) if not atr.startswith("__") and not atr.startswith("_")]

        for attribute in kwargs:
            if attribute not in account_attributes:
                raise KeyError(
                    f"{attribute} is not an attribute of Account object.")

        try:
            if "name" in kwargs:
                account.name = kwargs["name"]
            if "second_name" in kwargs:
                account.second_name = kwargs["second_name"]
            if "balance_cash" in kwargs:
                account.balance_cash = kwargs["balance_cash"]
            if "balance_card" in kwargs:
                account.balance_card = kwargs["balance_card"]
        except Exception as e:
            print(f"There was an error: {e}\nChanges won't be applied")
        else:
            account = account_copy


if __name__ == "__main__":
    manager = AccountManager()

    ac1 = Account("John", "Doe", 1000, 2000)
    ac1.id = "1234567890"
    manager.add_account(ac1)
    print(manager.get_account("1234567890"))
    print(dir)
