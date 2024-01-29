from flask import Blueprint
import subprocess

helper = Blueprint("helper", __name__)

@helper.route("/helper")
def help():
    print("som tu")
    result = subprocess.run(['python3', 'daco.py'], capture_output=True, text=True)

    return result.stdout
