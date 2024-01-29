# server.py
from flask import Flask, request, jsonify
from abc import ABC, abstractmethod
import json
from helper import helper
import subprocess

app = Flask(__name__)
app.register_blueprint(helper, url_prefix="")


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    return jsonify({'result': f'Tvoje meno je {username} a heslo je {password}'})


@app.route('/api/bank', methods=['POST'])
def bank():
    try:
        data = request.get_json()
        accountNumber = data.get('accountNumber')
        select = data.get('select')
        balance = data.get('balance')

        # Kontrola chýb
        if not all([accountNumber, select, balance]):
            raise ValueError("Chýbajúce hodnoty.")
        # Vytvorenie slovníka s hodnotami
        result_dict = {
            'accountNumber': accountNumber,
            'select': select,
            'balance': balance
        }

        # Zápis do JSON súboru
        with open('output.json', 'w') as json_file:
            json.dump(result_dict, json_file)

        # Spustenie externého skriptu
        scr = subprocess.run(['python3', 'daco.py'], capture_output=True, text=True)
        if scr.returncode != 0:
            raise Exception(f"Chyba pri spustení daco.py: {scr.stderr}")
        
        # Získanie hodnôt zo skriptu
        result_from_script = json.loads(scr.stdout)
        with open('secret.json', 'r') as r:
            attempts = json.load(r)
            attempts = attempts["attempts"]

        if result_from_script == "Chyba":
            return jsonify({'result': f"Zial vas vyber nebol dokonceny spravne. Pokus {attempts}/3"})
        elif result_from_script == "FatalError":
            return jsonify({'result': "Prekroceny limit nespravnych pokusov! Prosim kontaktujte svoju banku!"})
        else:
            return jsonify({'result': f"Vas vyber bol uspesne zrealizovany! Zostatok na ucte je: {result_from_script[1]}"})


        # Vrátenie hodnôt zo skriptu
    except Exception as e:
        # Správa chýb v prípade výnimky

        return jsonify({'error': str(e)})



@app.route('/api/reset', methods=['POST'])
def reset_attempts():
    try:
        with open('secret.json', 'r') as r:
            attempts = json.load(r)

        attempts["attempts"] = 0

        with open('secret.json', 'w') as f:
            json.dump(attempts, f, indent=2)

        return jsonify({"message": "Pokusy byly resetovány."})

    except Exception as e:
        return jsonify({"error": f"Chyba při resetování pokusů: {str(e)}"}), 500



@app.route("/members")
def members():
    return {"members": ["Members1","Members2","Members3"]}


@app.route('/api/project', methods=['POST'])
def project():
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')


    return jsonify({'result': username, "heslo": password})


# API pre validaciu cisla uctu.
@app.route('/api/verify-code', methods=['POST'])
def verify_code():

    # Zapise do JSON cislo uctu
    data = request.get_json()
    code = data.get('code', '')
    NumberOfAccount = {
        'accountNumber': code
    }
    print("tu by malo byt cislo uctu", data)
        # Zápis do JSON súboru
    with open('output.json', 'w') as json_file:
        json.dump(NumberOfAccount, json_file)


    scr = subprocess.run(['python3', 'NumberOfAccount.py'], capture_output=True, text=True)
    if scr.returncode != 0:
        raise Exception(f"Chyba pri spustení daco.py: {scr.stderr}")
    result_from_script = json.loads(scr.stdout.strip())
    # Vracia hodnotu True pokial plati podmienka, ze c.u.
    # sa nachadza v zozname

    # kontroluje pocet pokusov pr zlom zadani hesla.
    with open('secret.json', 'r') as r:
        attempts = json.load(r)
        attempts = attempts["attempts"]


    if result_from_script == "Chyba":
        return jsonify({'isValid': f"Zial vas vyber nebol dokonceny spravne. Pokus {attempts}/3"})
    
    elif result_from_script == "FatalError":
        return jsonify({'isValid': "Prekroceny limit nespravnych pokusov! Prosim kontaktujte svoju banku!"})
    else:
        return jsonify({'isValid': True})


# API pre vstup vklad/vyber
@app.route('/api/process-input', methods=['POST'])
def process_input():

    # Rozbalenie aktualnych dat z JSON
    with open('output.json', 'r') as json_file:
        currentData = json.load(json_file)

    # Získání nové hodnoty ze žádosti 
    data = request.get_json()
    code = data.get('code', '')
    # code = vklad alebo vyber
    # Přidání nové hodnoty do původního JSON
    currentData['entry'] = code

    # Uložení aktualizovaného JSON zpět do souboru
    with open('output.json', 'w') as json_file:
        json.dump(currentData, json_file)
    

    return jsonify({'message': f'Zpracováno novým vstupem: {code}'})

@app.route('/api/entry-amount', methods=['POST'])
def entry_amount():

        # Rozbalenie aktualnych dat z JSON
    with open('output.json', 'r') as json_file:
        currentData = json.load(json_file)

    data = request.get_json()
    code = data.get('code', '')
    print(code)

    currentData['amount'] = code
    cislo_uctu = currentData["accountNumber"]

    # Uložení aktualizovaného JSON zpět do souboru
    with open('output.json', 'w') as json_file:
        json.dump(currentData, json_file)    

    scr = subprocess.run(['python3', 'Input_Output.py'], capture_output=True, text=True)
    if scr.returncode != 0:
        raise Exception(f"Chyba pri spustení daco.py: {scr.stderr}")
    result_from_script = json.loads(scr.stdout.strip())
    
    with open('resultJSON.json', 'w') as json_file:
        json.dump(result_from_script["bca"], json_file) 
    # print("tututuutut",result_from_script)

    scr = subprocess.run(['python3', 'SaveToJSON.py'], capture_output=True, text=True)
    if scr.returncode != 0:
        raise Exception(f"Chyba pri spustení daco.py: {scr.stderr}")

    return jsonify({'message': result_from_script["abc"]})

@app.route('/api/create-account', methods=['POST'])
def create_account():
    data = request.get_json()
    createUser = {
        "firstName": data["code"],
        "lastName": data["lastName"],
        "suma": data["amount"]
    }

    with open('createAccount.json', 'w') as json_file:
        json.dump(createUser, json_file)   

    scr = subprocess.run(['python3', 'createAccount.py'], capture_output=True, text=True)
    if scr.returncode != 0:
        raise Exception(f"Chyba pri spustení daco.py: {scr.stderr}")
    result_from_script = json.loads(scr.stdout.strip())


    

    return jsonify({'message': result_from_script })

if __name__ == "__main__":
    app.run(debug=True)
