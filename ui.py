from models import AccountManager, TransactionManager, account_attributes_and_types, transaction_attributes_and_types


class AdminPanel:
    def __init__(self, account_manager: AccountManager, transaction_manager: TransactionManager):
        self.account_manager = account_manager
        self.transaction_manager = transaction_manager

    def _initialize_account(self, message):
        id = input(f"Account's ID to {message}: ")

        if len(id) == 1:
            id = int(id)

        try:
            account = self.account_manager.get_account(id)
        except ValueError:
            print(f"Account of ID {id} doesn't exist.")
            return
        else:
            return account, id

    def create_account(self):
        print("--- CREATE ACCOUNT ---")
        try:
            name = input("Name: ")
            second_name = input("Second name: ")

            try:
                cash_balance = float(input("Current cash balance: "))
                card_balance = float(input("Current card balance: "))
            except ValueError as e:
                print("Balance needs to be a numeric value!")
                return

            self.account_manager.create_account(
                name, second_name, cash_balance, card_balance, testing_id=True)

        except ValueError as e:
            print(f"Failed to create account: {e}")
            return
        else:
            print("- Account was created -")

    def delete_account(self):
        print("--- DELETE ACCOUNT ---")

        account, id = self._initialize_account("delete")

        if account:
            print("-- Provide account information for verification --")
            date = input("Account creation date (YYYY-MM-DD): ")
            name = input("Name: ")
            second_name = input("Second name: ")

            self.account_manager.delete_account(id, date, name, second_name)

            print("- Account was deleted -")
        else:
            return

    def update_account(self):
        print("--- UPDATE ACCOUNT ---")

        account, id = self._initialize_account("update")
        if account:

            # exclude attributes for testing and development purposes
            possible_information_to_update = list(
                account_attributes_and_types.keys())
            for index, information in enumerate(possible_information_to_update):
                if information in ["id_index", "testing_id"]:
                    del possible_information_to_update[index]

            possible_information_to_update = {
                k: v for k, v in enumerate(possible_information_to_update)}

            chocie_string = "\n".join(
                [f"{k} -> \"{v}\"" for k, v in possible_information_to_update.items()])

            information_to_update = []
            submit_number = len(possible_information_to_update)
            quit_number = submit_number+1
            print(f"Choose which account's information you want to update:\n{
                chocie_string}\n{submit_number} -> SUBMIT \n{quit_number} -> CANCEL")

            should_continue = True
            while should_continue:
                information_index = int(input("Number: "))
                if information_index in possible_information_to_update.keys():
                    if information_index not in information_to_update:
                        information_to_update.append(information_index)
                    else:
                        print(f"{possible_information_to_update.get(
                            information)} was already chosen.")

                elif information_index == submit_number:
                    should_continue = False
                elif information_index == quit_number:
                    return
                else:
                    print("Invalid number, choose valid information number!")
                    print(f"{chocie_string}\n{
                          submit_number} -> SUBMIT \n{quit_number} -> CANCEL")

            information_to_update_values = {}
            for field in information_to_update:
                new_information = input(
                    f"New value for \"{possible_information_to_update.get(field)}\": ")

                try:
                    if isinstance(getattr(account, possible_information_to_update.get(field)), (int, float)) and possible_information_to_update.get(field) != "id":
                        new_information = float(new_information)
                except ValueError as e:
                    print(f"""Numeric value for {possible_information_to_update.get(field)} is expected.
                          - Account was not updated - """)
                    return
                information_to_update_values[possible_information_to_update.get(
                    field)] = new_information
            try:
                self.account_manager.update_account(
                    id=id, fields=information_to_update_values)
            except Exception as e:
                print(
                    f"- Some error occured, account was not updated - \n {e}")
            else:
                print("- Account was updated -")
        else:
            return

    def add_transcation(self):
        print("--- ADD TRANSACTION ---")

        account, id = self._initialize_account("add transaction")

        if account:

            required_transaction_fields = list(
                transaction_attributes_and_types.keys())
            required_transaction_fields = [field for field in required_transaction_fields if field not in [
                "transaction_date", "transaction_id"]]
            required_transaction_field_types = {
                field: type for field, type in transaction_attributes_and_types.items() if field in required_transaction_fields}

        transaction_info = {}

        print("Provide transaction information:")

        for field in required_transaction_fields:

            transaction_info[field] = input(f"{field}: ")


if __name__ == "__main__":
    account_manager = AccountManager()
    transaction_manager = TransactionManager(account_manager=account_manager)

    admin_panel = AdminPanel(account_manager, transaction_manager)

    admin_panel.create_account()
    admin_panel.update_account()
    print(account_manager.get_account("1112223334").account_info())
    admin_panel.delete_account()
    print("end")
