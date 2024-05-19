from models import AccountManager, TransactionManager, account_attributes


class AdminPanel:
    def __init__(self, account_manager: AccountManager, transaction_manager: TransactionManager):
        self.account_manager = account_manager
        self.transaction_manager = transaction_manager

    def create_account(self):
        print("--- CREATE ACCOUNT ---")
        name = input("Name: ")
        second_name = input("Second name: ")

        cash_balance = float(input("Current cash balance: "))
        card_balance = float(input("Current card balance: "))

        self.account_manager.create_account(
            name, second_name, cash_balance, card_balance, testing_id=True)

        print("- Account was created -")

    def delete_account(self):
        print("--- DELETE ACCOUNT ---")
        id = input("Account's ID to delete: ")
        print("-- Provide account information for verification --")
        date = input("Account creation date (YYYY-MM-DD): ")
        name = input("Name: ")
        second_name = input("Second name: ")

        self.account_manager.delete_account(id, date, name, second_name)

        print("- Account was deleted -")

    def update_account(self):

        # exclude attributes for testing and development purposes
        possible_information_to_update = account_attributes
        for index, information in enumerate(possible_information_to_update):
            if information in ["id_index", "testing_id"]:
                del possible_information_to_update[index]

        possible_information_to_update = {
            k: v for k, v in enumerate(possible_information_to_update)}

        chocie_string = " | ".join(
            [f"\"{k}\" for \"{v}\"" for k, v in possible_information_to_update])

        id = input("Account's ID to update: ")
        information_to_update = []
        submit_number = len(possible_information_to_update)+1
        quit_number = submit_number+1
        print(f"""Choose what account's information you want to update:
              {chocie_string} | {submit_number} to submit | {quit_number} to cancel""")

        should_continue = True
        while should_continue:
            information_index = int(input("Number: "))
            if information_index in possible_information_to_update.keys():
                if information_index not in information_to_update:
                    information_to_update.append(information_index)
                elif information_index == submit_number:
                    should_continue = False
                elif information_index == quit_number:
                    return
                else:
                    print(f"{possible_information_to_update.get(
                        information)} was already chosen.")
            else:
                print("Invalid number, choose valid information number!")
                print(chocie_string)

        information_to_update_values = {}
        for field in information_to_update:
            new_information = input(
                f"New value for \"{possible_information_to_update.get(field)}\"")

            if isinstance(possible_information_to_update.get(field), (int, float)):
                new_information = float(new_information)

            information_to_update_values[possible_information_to_update.get(
                field)] = new_information

        self.account_manager.update_account(
            id=id, **information_to_update_values)

        print("- Account was updated -")
