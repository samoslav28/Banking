import json

def checkAttempts():
    # Načtěte aktuální data z 'output.json'
    with open('output.json', 'r') as f:
        data = json.load(f)
        cislo_uctu = data["accountNumber"]

    with open('resultJSON.json', 'r') as f:
        suma = json.load(f)

    # Načtěte seznam účtů z 'cislaUctov.json'
    with open('cislaUctov.json', 'r') as f:
        data_of_accounts = json.load(f)
        accounts = data_of_accounts["ucta"]

        # Najděte odpovídající účet a aktualizujte sumu
        for account in accounts:
            if account["cislo_uctu"] == cislo_uctu:
                account["suma"] = suma

        # Uložte aktualizovaná data zpět do 'cislaUctov.json'
        with open('cislaUctov.json', 'w') as f:
            json.dump(data_of_accounts, f, indent=2)  # Parametr indent=2 zajistí čitelný formát

# Zavolejte funkci pro kontrolu pokusů
checkAttempts()
