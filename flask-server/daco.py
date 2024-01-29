# daco.py
import json
from abc import ABC, abstractmethod

def checkAttempts():
    with open('secret.json', 'r') as r:
        attempts = json.load(r)
        if attempts["attempts"] == 3:
            return False
        else:
            return True
def unpacking():
    # Databaza cisiel uctov
    numbers_all_accounts = []

    with open('output.json', 'r') as f:
        data = json.load(f)
        cislo_uctu = data["accountNumber"]
        select = data["select"]
        zostatok = data["balance"]

        with open('cislaUctov.json', 'r') as f:
            data_of_accounts = json.load(f)
            data_of_accounts = data_of_accounts["ucta"]
            for number in data_of_accounts:
                numbers_all_accounts.append(number["cislo_uctu"])
            
            
        # Kontrola pri  ktorej zistujeme ci sa nachadza cislo uctu v databaze. 
        if cislo_uctu in numbers_all_accounts:
            for ucet in data_of_accounts:
                if ucet["cislo_uctu"] == cislo_uctu:
                    CurrentAccount = ucet
                    break
        else:
            return False
        
        values = {
        "ucet": CurrentAccount,
        "select": select,
        "zostatok": zostatok,
        "numbers_all_accounts": numbers_all_accounts,
        "data_of_accounts": data_of_accounts
    }

    return values


                    
    # return cislo_uctu, select, zostatok, numbers_all_accounts, data_of_accounts
def opn(ucet, select, zostatok):
    cislo_uctu = ucet["cislo_uctu"]
    suma = ucet["suma"]
    class BankovyUcet(ABC):
        def __init__(self, cislo_uctu, zostatok):
            self.__cislo_uctu = cislo_uctu
            self.__zostatok = zostatok

        @property
        def cislo_uctu(self):
            return self.__cislo_uctu

        @property
        def zostatok(self):
            return self.__zostatok

        @abstractmethod
        def vytvor_ucet(self):
            pass

        @abstractmethod
        def zobraz_stav(self):
            pass

        def vloz_peniaze(self, suma):
            if suma > 0:
                self.__zostatok += suma
                return suma, self.__cislo_uctu, self.__zostatok
            else:
                return "Vložená suma musí byť kladná."

        def vyber_peniaze(self, suma):
            if suma > self.__zostatok:
                return "Chyba. Ziadate viac ako mate na ucte"
            else:
                self.__zostatok -= suma
                return suma, self.__zostatok


    class OsobnyUcet(BankovyUcet):
        def vytvor_ucet(self):
            return f"Vytvoreny osobny ucet {self.cislo_uctu}"

        def zobraz_stav(self):
            return f"Stav na vasom osobnom ucte je {self.zostatok}"


    def selector():
        # Osetrenie v pripade ak by niekto v selecte nedal cislo
        while True:
            Q1 = select
            try:
                Q1 = int(Q1)
                break
            except ValueError:
                print("Zla volba. Skuste znovu.")

        ucet = OsobnyUcet(cislo_uctu, suma)
        # Vyber 1. volby
        if Q1 == 1:
            while True:
                vyber = zostatok
                try:
                    vyber = int(vyber)
                    if vyber < 0:
                        raise ValueError("Vyber musí byť kladné číslo.")
                    break
                except ValueError as e:
                    print(e)
            return ucet.vyber_peniaze(vyber)
        
        # Vyber 2. volby
        elif Q1 == 2:
            while True:
                vklad = input("Kolko chcete vlozit?")
                try:
                    vklad = int(vklad)
                    if vklad < 0:
                        raise ValueError("Vklad musí byť kladné číslo.")
                    break
                except ValueError as e:
                    print(e)
            return ucet.vloz_peniaze(vklad)
        # vyber 3. volby
        elif Q1 == 3:
            print("Dovidenia")
            exit()

    with open('cislaUctov.json', 'r') as f:
        data = json.load(f)
        data = data["ucta"]

    with open('secret.json', 'r') as r:
        attempts = json.load(r)
        attempts["attempts"] = 0

    with open('secret.json', 'w') as f:
        json.dump(attempts, f)

    result_from_selector = selector()
    return json.dumps(result_from_selector)
def chyba():
    with open('secret.json', 'r') as r:
        attempts = json.load(r)
        if attempts["attempts"] == 3:
            result_from_selector = "FatalError"
            return json.dumps(result_from_selector)
        else:
            result_from_selector = "Chyba"
            attempts_value = attempts.get("attempts", 0) + 1
            attempts["attempts"] = attempts_value
            with open('secret.json', 'w') as f:
                json.dump(attempts, f)
            return json.dumps(result_from_selector)
if checkAttempts():
    values = unpacking()
    # Vráti hodnoty ako reťazec
    if values:
        print(opn(values["ucet"], values["select"], values["zostatok"]))
    else:
        print(chyba())
else:
    print(chyba())

