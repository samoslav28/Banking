import random
import string
import json

def createAccount():
    with open('createAccount.json', 'r') as f:
        newUser = json.load(f)

    numbers_all_accounts = []
    with open('cislaUctov.json', 'r') as f:
        data_of_accounts = json.load(f)
        data_of_accounts = data_of_accounts.get("ucta", [])

    while True:
        first_two_letters = random.choices(string.ascii_uppercase, k=2)
        random_numbers = ''.join(random.choices(string.digits, k=10))
        cislo_uctu = ''.join(first_two_letters) + random_numbers

        for number in data_of_accounts:
            numbers_all_accounts.append(number["cislo_uctu"])

        if cislo_uctu not in numbers_all_accounts:
            firstName = newUser["firstName"]
            lastName = newUser["lastName"]
            suma = int(newUser["suma"])

            # Porovnanie cisla uctu
            if any(account["cislo_uctu"] == cislo_uctu for account in data_of_accounts):
                return json.dumps({
                "abc": "Chyba: Účet s daným číslom už existuje.",
                "bca" : None
            })

            # Porovnanie mena a priezviska
            if any(account.get("first_name") == firstName and account.get("last_name") == lastName for account in data_of_accounts):
                return json.dumps({
                "abc": "Chyba: Účet s daným menom a priezviskom už existuje.",
                "bca" : None
            })

            dataOfJSON = {"first_name": firstName,
                          "last_name": lastName,
                          "cislo_uctu": cislo_uctu,
                          "suma": suma}

            data_of_accounts.append(dataOfJSON)

            with open('cislaUctov.json', 'w') as f:
                json.dump({"ucta": data_of_accounts}, f, indent=2)


            return json.dumps({
                "abc": "Účet bol vytvorený.",
                "bca" : cislo_uctu
            })

if __name__ == "__main__":
    result = createAccount()
    print(result)
