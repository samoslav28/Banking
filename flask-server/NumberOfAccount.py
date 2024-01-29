# daco.py
import json

def checkAttempts():
    with open('secret.json', 'r') as r:
        attempts = json.load(r)
        if attempts["attempts"] == 3:
            result_from_script = "FatalError"
            return json.dumps(result_from_script)
        else:
            return unpacking()
        
def unpacking():
    # Databaza cisiel uctov
    numbers_all_accounts = []
    with open('output.json', 'r') as f:
        data = json.load(f)
        cislo_uctu = data["accountNumber"]



        with open('cislaUctov.json', 'r') as f:
            data_of_accounts = json.load(f)
            data_of_accounts = data_of_accounts["ucta"]
            for number in data_of_accounts:
                numbers_all_accounts.append(number["cislo_uctu"])
            
            
        # Kontrola pri  ktorej zistujeme ci sa nachadza cislo uctu v databaze. 
        if cislo_uctu in numbers_all_accounts:
            result_from_script = True
            with open('secret.json', 'r') as r:
                attempts = json.load(r)
                # Změna hodnoty attempts na 0
                attempts["attempts"] = 0

                with open('secret.json', 'w') as r:
                    # Uložení změněných dat zpět do souboru
                    json.dump(attempts, r)
            return json.dumps(result_from_script)

        else:
            return chyba()
        

def chyba():
    with open('secret.json', 'r') as r:
        attempts = json.load(r)
        if attempts["attempts"] == 3:
            result_from_script = "FatalError"
            return json.dumps(result_from_script)
        else:
            result_from_script = "Chyba"
            attempts_value = attempts.get("attempts", 0) + 1
            attempts["attempts"] = attempts_value
            with open('secret.json', 'w') as f:
                json.dump(attempts, f)
            return json.dumps(result_from_script)
        
print(checkAttempts())
