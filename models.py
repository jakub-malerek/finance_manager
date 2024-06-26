from utils import string_has_numbers, string_has_special_characters, get_attributes_and_values, validate_date, random_string_generator
from config import ITEM_CATEGORIES

from random import randint
from datetime import datetime
from typing import Union
import warnings


class Account:
    id_index = 1

    def __init__(self, name, second_name, balance_cash, balance_card, testing_id=False) -> None:
        self.testing_id = testing_id

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
    def id(self, _id: str):
        if self.testing_id:
            self._id = Account.id_index
            Account.id_index += 1
            self.testing_id = False
        elif len(_id) == 10:
            if isinstance(_id, str):
                if _id.isnumeric():
                    self._id = _id
                else:
                    raise ValueError("ID should be made of digits only.")
            else:
                raise TypeError(
                    f"ID should be an string, input of type {type(_id)} was given.")
        else:
            raise ValueError("ID should be 10 digit long.")

    @property
    def account_created_date(self):
        return self._account_created_date

    @account_created_date.setter
    def account_created_date(self, date):
        validate_date(date)
        self._account_created_date = date

    def validate_name(self, name_input):
        if isinstance(name_input, str):
            if not (1 <= len(name_input) <= 100):
                raise ValueError(
                    "Name or second name length should be between 1 and 100 characters.")
            if string_has_numbers(name_input):
                raise ValueError(
                    "Name or second name should contain only alphabet characters, numbers are not allowed.")
            if string_has_special_characters(name_input):
                raise ValueError(
                    "Name or second name should not contain any special characters like: !,$,@ etc.")
            return True
        else:
            raise TypeError(
                f"Name of second name should be an alphabetic word, input of type {type(name_input)} was given.")

    def validate_balance(self, balance_input):
        if not isinstance(balance_input, (float, int)):
            raise TypeError(
                f"Balance should be a number, input of type {type(balance_input)} was given")
        if not (balance_input >= 0):
            raise ValueError("Balance cannot be less than 0")

    def id_generator(self):
        return str(randint(0, 9))+str(randint(100_000_000, 999_999_999))

    def account_info(self):
        return f"Name: {self.name}, Second name: {self.second_name}, Cash balance: {self.balance_cash}, Card balance: {self.balance_card}, Account created: {self.account_created_date}"


class AccountManager:
    """
    The AccountManager class manages a collection of accounts and provides methods for creating, updating, deleting, and filtering accounts.

    Attributes:
        accounts (dict): A dictionary that stores the accounts, where the key is the account ID and the value is the Account object.

    Methods:
        create_account: Creates a new account and adds it to the manager.
        add_account: Adds an account to the finance manager.
        update_account: Updates the attributes of an account.
        delete_account: Deletes an account from the finance manager.
        get_account: Retrieves an account by its ID.
        filter_account_name: Filters accounts based on the provided attributes and values.
        filter_account_balance: Filters accounts based on the specified balance criteria.
    """

    def __init__(self):
        self.accounts = {}

    # create_account is basically constructor for Account class plus adds that created accound to the manager
    def create_account(self, name: str, second_name: str, balance_cash: Union[int, float], balance_card: Union[int, float], testing_id=False) -> None:
        """
        Creates a new account with the given name, second name, balance in cash, and balance in card.

        Args:
            name (str): The name of the account holder.
            second_name (str): The second name of the account holder.
            balance_cash (float): The initial balance in cash for the account.
            balance_card (float): The initial balance in card for the account.

        Returns:
            None
        """
        self.add_account(
            Account(name, second_name, balance_cash, balance_card, testing_id=testing_id))

    # in case there are accounts created outside of AccountManager and create_account method, there is separate method for adding account

    def add_account(self, account: Account) -> None:
        """
        Adds an account to the finance manager.

        Parameters:
        - account: An instance of the Account class.

        Raises:
        - TypeError: If the provided account is not an instance of the Account class.

        """
        if isinstance(account, Account):
            self.accounts[account.id] = account
        else:
            raise TypeError(
                f"Account class object is expected, {type(account)} type was given.")

    def update_account(self, id: str, fields: dict[str, Union[str, int, float]]) -> None:
        """
        Update the account with the given ID using the provided keyword arguments.

        Args:
            id (int): The ID of the account to update.
            **kwargs: Keyword arguments representing the attributes to update and their new values.

        Raises:
            KeyError: If any of the provided attributes are not valid attributes of the Account model.
            Exception: If an unexpected error occurs while updating the account.

        Returns:
            None
        """
        account = self.get_account(id)
        backup = get_attributes_and_values(account)

        try:
            for key, value in fields.items():
                if hasattr(account, key):
                    if key == "id":
                        original_id = getattr(account, "id")
                        setattr(account, "id", value)
                        self.accounts[value] = account
                        del self.accounts[original_id]
                    else:
                        setattr(account, key, value)
                else:
                    raise KeyError(
                        f"{key} is not a valid attribute of Account.")
        except KeyError as e:
            for key, value in backup.items():
                account.testing_id = True
                setattr(account, key, value)
            raise KeyError(f"Failed to update account: {e}") from e
        except TypeError as e:
            for key, value in backup.items():
                account.testing_id = True
                setattr(account, key, value)
            raise e
        except ValueError as e:
            for key, value in backup.items():
                account.testing_id = True
                setattr(account, key, value)
            raise e
        except Exception as e:
            for key, value in backup.items():
                account.testing_id = True
                setattr(account, key, value)
            raise Exception(
                "Failed to update account due to an unexpected error.") from e

    def delete_account(self, id: str, account_created_date: str, name: str, second_name: str) -> None:
        """
        Deletes an account from the finance manager.

        Args:
            id (int): The ID of the account to be deleted.
            account_created_date (str): The created date of the account to be deleted.
            name (str): The name of the account to be deleted.
            second_name (str): The second name of the account to be deleted.

        Raises:
            ValueError: If the account details do not match, the account cannot be deleted.
        """
        account = self.get_account(id)
        if account.account_created_date == account_created_date and account.name == name and account.second_name == second_name:
            del self.accounts[id]
        else:
            raise ValueError("Account details do not match; cannot delete.")

    def get_account(self, id: str) -> Account:
        """
        Retrieve an account by its ID.

        Args:
            id (int): The ID of the account to retrieve.

        Returns:
            Account: The account object corresponding to the given ID.

        Raises:
            ValueError: If no account with the given ID is found.
        """
        if id in self.accounts.keys():
            return self.accounts[id]
        else:
            raise ValueError(f"No account of given ID {id} was found.")

    # Future improvements regarding more advanced search capabilities
    def filter_account_name(self, pattern_search: str = False, **kwargs: dict[str, str]) -> list[Account]:
        """
        Filters accounts based on the provided attributes and values.

        Args:
            pattern_search (bool, optional): Specifies whether to perform pattern search or exact match. Defaults to False.
            **kwargs: Keyword arguments representing the attributes and values to filter the accounts.

        Returns:
            list: A list of accounts that match the specified attributes and values.

        Raises:
            AttributeError: If an invalid attribute is provided.
            TypeError: If a non-string value is provided for the search.

        """
        possible_attributes_search = [
            "name", "second_name"]

        if len(kwargs) < 1:
            return self.get_accounts()

        for attribute in kwargs:
            if attribute not in possible_attributes_search:
                raise AttributeError(
                    f"Account has no {attribute} attribute.")

        for attribute, value in kwargs.items():
            if not isinstance(value, str):
                raise TypeError(
                    f"String values are expected for the search, {type(value)} was given for {attribute} attribute")

        accounts_found = []

        for account in self.get_accounts():
            match = True
            for attribute, value in kwargs.items():
                account_value = getattr(account, attribute)
                if pattern_search:
                    if value not in account_value:
                        match = False
                        break
                else:
                    if account_value != value:
                        match = False
                        break
            if match:
                accounts_found.append(account)

        return accounts_found

    def filter_account_balance(self, total: bool = False, total_under: bool = False, cash_under: bool = False, card_under: bool = False, **kwargs: dict[str, Union[int, float]]) -> list[Account]:
        """
        Filters the accounts based on the specified balance criteria.

        Args:
            total (bool, optional): If True, filters the accounts based on the total balance. Defaults to False.
            total_under (bool, optional): If True, filters the accounts with a total balance under the specified value.
                Defaults to False.
            cash_under (bool, optional): If True, filters the accounts with a cash balance under the specified value.
                Defaults to False.
            card_under (bool, optional): If True, filters the accounts with a card balance under the specified value.
                Defaults to False.
            **kwargs: Additional keyword arguments for filtering the accounts based on specific balance attributes.
                Only 'balance_card' and 'balance_cash' attributes are expected.

        Returns:
            list: A list of accounts that match the specified balance criteria.

        Raises:
            AttributeError: If an invalid attribute is provided in kwargs.
            TypeError: If a non-numeric value is provided for a balance attribute.

        """
        possible_attributes = ["balance_card", "balance_cash"]

        for attribute in kwargs:
            if attribute not in possible_attributes:
                raise AttributeError(
                    f"Only 'balance_card' and 'balance_cash' attributes are expected, '{attribute}' was given.")

        for attribute, value in kwargs.items():
            if not isinstance(value, (int, float)):
                raise TypeError(
                    f"Numeric values are expected for the search, {type(value)} was given for {attribute} attribute")

        def check_balance(account, attribute, value, under):
            account_value = getattr(account, attribute)
            return account_value < value if under else account_value > value

        accounts_found = []

        if total:
            if "balance_card" in kwargs and "balance_cash" in kwargs:
                total_value = sum(
                    (kwargs["balance_card"], kwargs["balance_cash"]))
                for account in self.get_accounts():
                    account_sum = account.balance_card + account.balance_cash
                    match = account_sum < total_value if total_under else account_sum > total_value
                    if match:
                        accounts_found.append(account)
            else:
                raise AttributeError(
                    "Both 'balance_card' and 'balance_cash' are required for total balance filtering.")
        else:
            for account in self.get_accounts():
                match = True
                if "balance_card" in kwargs:
                    match = match and check_balance(
                        account, "balance_card", kwargs["balance_card"], card_under)
                if "balance_cash" in kwargs:
                    match = match and check_balance(
                        account, "balance_cash", kwargs["balance_cash"], cash_under)
                if match:
                    accounts_found.append(account)

        return accounts_found

    def filter_account_date(self, start_date: str = None, end_date: str = None) -> list[Account]:
        """
        Filters the accounts based on the provided start_date and end_date. Or if account creation date equals start_date if only start_date provided

        Args:
            start_date (str, optional): The start date in the format 'YYYY-MM-DD'. Defaults to None.
            end_date (str, optional): The end date in the format 'YYYY-MM-DD'. Defaults to None.

        Returns:
            list: A list of accounts that fall within the specified date range.
        """
        def parse_date(date_str):
            return datetime.strptime(date_str, "%Y-%m-%d")

        if start_date:
            validate_date(start_date)
            start_date = parse_date(start_date)
            if end_date:
                validate_date(end_date)
                end_date = parse_date(end_date)
        else:
            raise ValueError(
                "Wrong arguments: either both start_date and end_date or start_date only should be provided, None of these were provided")

        if not start_date and end_date:
            raise ValueError(
                "Wrong arguments: either both start_date and end_date or start_date only should be provided, only end_date was provided")

        accounts_found = []

        for account in self.get_accounts():
            account_created_date = parse_date(account.account_created_date)
            if start_date and end_date:
                if (start_date <= account_created_date <= end_date):
                    accounts_found.append(account)
            elif start_date:
                if account_created_date == start_date:
                    accounts_found.append(account)

        return accounts_found

    def get_accounts(self) -> list[Account]:
        return list(self.accounts.values())


class Transaction:
    PAYMENT_METHODS = ["CARD", "CASH"]
    ITEM_CATEOGIRES = ITEM_CATEGORIES

    transaction_id_index = 1

    def __init__(self, user_id, cost, payment_method, item, quantity, item_category, vendor, testing_id=False):
        self.testing_id = testing_id

        self.user_id = user_id
        self.transaction_id = random_string_generator(length=20)
        self.cost = cost
        self.payment_method = payment_method
        self.item = item
        self.quantity = quantity
        self.item_category = item_category
        self.vendor = vendor
        self.transaction_date = datetime.today().strftime("%Y-%m-%d")

    @property
    def transaction_id(self):
        return self._transaction_id

    @transaction_id.setter
    def transaction_id(self, _transaction_id):
        if self.testing_id:
            self._transaction_id = Transaction.transaction_id_index
            Transaction.transaction_id_index += 1
            self.testing_id = False
        elif isinstance(_transaction_id, str):
            if len(_transaction_id) == 20:
                self._transaction_id = _transaction_id
            else:
                raise ValueError(
                    "ID for transaction should be exactly 20 characters long.")
        else:
            raise TypeError("ID for transaction should be of type string.")

    @property
    def cost(self):
        return self._cost

    @cost.setter
    def cost(self, _cost):
        if isinstance(_cost, (int, float)):
            if _cost > 0:
                self._cost = _cost
            else:
                raise ValueError("Cost of transaction cannot be less than 0.")
        else:
            raise TypeError(
                "Value of cost should be either integer or float number.")

    @property
    def payment_method(self):
        return self._payment_method

    @payment_method.setter
    def payment_method(self, _payment_method):
        if _payment_method in Transaction.PAYMENT_METHODS:
            self._payment_method = _payment_method
        else:
            raise ValueError("Avaible payment methods are either card or cash")

    @property
    def item(self):
        return self._item

    @item.setter
    def item(self, _item):
        if isinstance(_item, str):
            self._item = _item
        else:
            raise TypeError("Value for item field should be a string")

    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, _quantity):
        if isinstance(_quantity, int):
            if _quantity > 0:
                self._quantity = _quantity
            else:
                raise ValueError("Quantity cannot be less than 0.")
        else:
            raise TypeError("Quantity value must be an integer.")

    @property
    def item_category(self):
        return self._item_category

    @item_category.setter
    def item_category(self, _item_category):
        if _item_category in Transaction.ITEM_CATEOGIRES:
            self._item_category = _item_category
        else:
            raise ValueError(
                f"Category {_item_category} is not supported category.")

    @property
    def vendor(self):
        return self._vendor

    @vendor.setter
    def vendor(self, _vendor):
        if isinstance(_vendor, str):
            self._vendor = _vendor
        else:
            TypeError("Value for vendor should be of type string.")

    @property
    def transaction_date(self):
        return self._transaction_date

    @transaction_date.setter
    def transaction_date(self, _transaction_date):
        validate_date(_transaction_date)
        self._transaction_date = _transaction_date

    def transaction_info(self):
        return f"Transaction ID: {self.transaction_id} \n item/service: {self.item} | category: {self.item_category} | quantity: {self.quantity} | cost: {self.cost} |  method of payment: {self.payment_method.lower()} | bought from: {self.vendor}"


class TransactionManager:
    def __init__(self, account_manager: AccountManager):
        self.transacations = {}
        self.account_manager = account_manager

    @property
    def account_manager(self):
        return self._account_manager

    @account_manager.setter
    def account_manager(self, _account_manager):
        if isinstance(_account_manager, AccountManager):
            self._account_manager = _account_manager
        else:
            raise TypeError(
                f"AccountManager instance is expected, {type(_account_manager)} type was given")

    def create_transaction(self, user_id, cost, payment_method, item, quantity, item_category, vendor, testing_id=False):
        self.validate_account(user_id)
        self.add_transcation(Transaction(
            user_id, cost, payment_method, item, quantity, item_category, vendor, testing_id=testing_id))

    def add_transcation(self, transaction: Transaction) -> None:
        """
        Adds a transaction to the transaction manager.

        Args:
            user_id (str): The ID of the user.
            transaction (Transaction): The transaction to be added.

        Raises:
            ValueError: If the user with the given ID does not exist.

        """

        if isinstance(transaction, Transaction):
            user_id = transaction.user_id
            self.validate_account(user_id)
            if user_id in self.transacations.keys():
                self.transacations[user_id].append(transaction)
            else:
                self.transacations[user_id] = [transaction]

            account = self.account_manager.get_account(user_id)

            self.update_balance(account, transaction)
        else:
            raise TypeError(
                f"Transaction object is expected, {type(transaction)} instance was given")

    def validate_account(self, user_id: str) -> None:
        try:
            self.account_manager.get_account(user_id)
        except ValueError as e:
            raise ValueError(
                f"Transaction was not registered, account with ID {user_id} does not exist.") from e

    def update_balance(self, account: Account, transaction: Transaction, reverse=False):
        if not reverse:
            if transaction.payment_method == "CARD":
                account.balance_card -= transaction.cost
            else:
                account.balance_cash -= transaction.cost
        else:
            if transaction.payment_method == "CARD":
                account.balance_card += transaction.cost
            else:
                account.balance_cash += transaction.cost

    def get_user_transactions(self, user_id):
        self.validate_account(user_id)

        user_transactions = self.transacations.get(user_id)

        if user_transactions is None:
            warnings.warn("There are no transactions for this user!")

        return user_transactions

    def get_user_transaction(self, user_id, transaction_id) -> Transaction:
        self.validate_account(user_id)

        transactions = self.get_user_transactions(user_id)

        for transaction in transactions:
            if transaction.transaction_id == transaction_id:
                return transaction

    def reverse_transaction(self, user_id, transaction_id):
        transactions = self.get_user_transactions(user_id)

        account = self.account_manager.get_account(user_id)

        for index, transaction in enumerate(transactions):
            if transaction.transaction_id == transaction_id:
                self.update_balance(account, transaction, reverse=True)
                del self.transacations[user_id][index]


def get_input_attributes():
    dummy_account = Account("dummyName", "dummySName", 1, 1, testing_id=True)

    account_attributes_values = get_attributes_and_values(
        dummy_account)

    account_attributes_all = list(account_attributes_values.keys())

    account_mutable_attributes = [
        attr for attr in account_attributes_all if attr not in ["testing_id", "id_index"]]

    dummy_transcation = Transaction(
        1, 1, "CARD", "d", 1, "CLOTHING", "d", testing_id=True)

    transaction_attributes_values = get_attributes_and_values(
        dummy_transcation)

    transaction__attributes_all = list(transaction_attributes_values.keys())

    transaction_mutable_attributes = [attr for attr in transaction__attributes_all if attr.islower()
                                      and attr not in ["transaction_id_index", "testing_id"]]

    account_mutable_attributes_and_types = {k: type(
        v) for k, v in account_attributes_values.items() if k in account_mutable_attributes}
    transaction_mutable_attributes_and_types = {k: type(
        v) for k, v in transaction_attributes_values.items() if k in transaction_mutable_attributes}

    for attr, type_ in account_mutable_attributes_and_types.items():
        if type_ == int:
            account_mutable_attributes_and_types[attr] = [
                int, float]

    account_mutable_attributes_and_types["id"] = [int, str]

    transaction_mutable_attributes_and_types["transaction_id"] = [
        int, str]

    transaction_mutable_attributes_and_types["user_id"] = [
        int, str]

    return {"account": account_mutable_attributes_and_types, "transaction": transaction_mutable_attributes_and_types}


input_attributes = get_input_attributes()

account_attributes_and_types = input_attributes.get("account")
transaction_attributes_and_types = input_attributes.get("transaction")


if __name__ == "__main__":

    print(account_attributes_and_types)
