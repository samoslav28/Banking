import json
from abc import ABC, abstractmethod

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
            return json.dumps({
                "abc": f"Vložená suma je {suma} a celkový zostatok na účte {self.__cislo_uctu} je {round(self.__zostatok,2)} EUR.",
                "bca": round(self.__zostatok,2)})
        else:
            return json.dumps({
                "abc": "Vložená suma musí byť kladná.",
                "bca": self.__zostatok})

    def vyber_peniaze(self, suma):
        if suma > self.__zostatok:
            return json.dumps({
                "abc": "Chyba. Ziadate viac ako mate na ucte",
                "bca": self.__zostatok})
        else:
            self.__zostatok -= suma
            return json.dumps({
                "abc": f"Vyber zrealizovany. Vybrali ste {suma} Na vasom konte je {round(self.__zostatok,2)}",
                "bca": round(self.__zostatok,2)})



class OsobnyUcet(BankovyUcet):
    def vytvor_ucet(self):
        return f"Vytvoreny osobny ucet {self.cislo_uctu}"

    def zobraz_stav(self):
        return f"Stav na vasom osobnom ucte je {self.zostatok}"

def unpacking():
    numbers_all_accounts = []
    with open('output.json', 'r') as r:
        data = json.load(r)
        numberAccount = data["accountNumber"]
        select = data["entry"]
        zostatok = data["amount"]

        with open('cislaUctov.json', 'r') as f:
            data_of_accounts = json.load(f)
            data_of_accounts = data_of_accounts["ucta"]
            for number in data_of_accounts:
                numbers_all_accounts.append(number["cislo_uctu"])
            
        # Kontrola pri  ktorej zistujeme ci sa nachadza cislo uctu v databaze. 
        if numberAccount in numbers_all_accounts:
            for ucet in data_of_accounts:
                if ucet["cislo_uctu"] == numberAccount:
                    CurrentAccount = ucet
                    return CurrentAccount, select, zostatok
        else:
            return False
        

# přiřazení výsledků z funkce unpacking
CurrentAccount, select, zostatok = unpacking()

def selector(CurrentAccount, select, zostatok):
    Q1 = select
    ucet = OsobnyUcet(cislo_uctu, suma)

    if Q1 == "vyber":
        while True:
            try:
                vyber = int(zostatok)
                if vyber < 0:
                    return json.dumps("Vyber musí byť kladné číslo.")
                break
            except ValueError as e:
                print(e)
        return ucet.vyber_peniaze(vyber)
    
    elif Q1 == "vklad":
        while True:
            vklad = suma
            try:
                vklad = int(zostatok)
                if vklad < 0:
                    return json.dumps ("Vklad musí byť kladné číslo.")
                break
            except ValueError as e:
                print(e)
        return ucet.vloz_peniaze(vklad)

    elif Q1 == "3":
        print("Dovidenia")
        exit()

# zde byste měli mít definice cislo_uctu a suma
cislo_uctu = CurrentAccount["cislo_uctu"]
suma = CurrentAccount["suma"]

# volání funkce selector s předanými hodnotami
result_from_selector = selector(CurrentAccount,select, zostatok)
print(result_from_selector)
