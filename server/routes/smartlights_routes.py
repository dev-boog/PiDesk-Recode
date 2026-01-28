from flask import Blueprint, render_template, jsonify, request
import json
import subprocess
import colorsys

smartlight_routes = Blueprint("smartlights", __name__)

class SmartLightController:
    @staticmethod
    def run(cmd, device_name="Desk LED Strip"):
        with open("./config.json", "r", encoding="utf-8") as f:
            config = json.load(f)
        
        device = config.get("smartlights", {}).get(device_name)
     
        command = [
            "kasa",
            "--host", device["ip"],
            "--username", device["username"],
            "--password", device["password"]
        ]
        
        command.extend(cmd.split())
        
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout
        except subprocess.CalledProcessError as e:
            return f"Error running kasa command:\n{e.stderr}"

@smartlight_routes.before_request
def check_config():
    with open("./config.json", "r") as f:
        config = json.load(f)

    for device_name, device in config.get("smartlights", {}).items():
        for field, value in device.items():
            if value in ("", None):
                return render_template("error.html", error_title="Required Field Missing!", error_description=f"You're missing the required field for {field}! Please edit the config.json to resolve this error.", redirect="index")

@smartlight_routes.route('/smartlights')
def smartlights():
    with open("./config.json", "r") as f:
        config = json.load(f)
        
    smartlights = config["smartlights"]
    return render_template('smart_lights.html', smartlights=smartlights)

@smartlight_routes.route('/smartlights/on')
def smartlights_on():
    device_name = request.args.get("device")
    
    output = SmartLightController.run("on", device_name=device_name)
    
    redirection = request.args.get("redirection")
    if redirection is None:
        return render_template('smart_lights.html', smartlights=json.load(open("./config.json"))["smartlights"])
    else:
        return render_template(redirection)

@smartlight_routes.route('/smartlights/off')
def smartlights_off():
    device_name = request.args.get("device")
    
    output = SmartLightController.run("off", device_name=device_name)
    
    redirection = request.args.get("redirection")
    if redirection is None:
        return render_template('smart_lights.html', smartlights=json.load(open("./config.json"))["smartlights"])
    else:
        return render_template(redirection)

@smartlight_routes.route('/smartlights/change_color')
def change_color():
    device_name = request.args.get("device")
    hex_color = request.args.get("color")
    
    if not device_name:
        return jsonify({"error": "Device name is required"}), 400
    if not hex_color:
        return jsonify({"error": "Color parameter is required"}), 400
    
    hex_color = hex_color.lstrip('#')  
    if len(hex_color) != 6:
        return jsonify({"error": "Invalid hex color format"}), 400
    
    try:
        r = int(hex_color[0:2], 16) / 255
        g = int(hex_color[2:4], 16) / 255
        b = int(hex_color[4:6], 16) / 255
        
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        h = round(h * 360)
        s = round(s * 100)
        v = round(v * 100) 
        
        output = SmartLightController.run(f"light hsv {h} {s} {v}", device_name=device_name)
        return "", 204
    except ValueError as e:
        print(f"ValueError: {e}")
        return jsonify({"error": f"Invalid color format: {str(e)}"}), 400
    except Exception as e:
        print(f"Exception: {e}")
        return jsonify({"error": f"Failed to change color: {str(e)}"}), 500