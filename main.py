#              _                 _
# _   _ _ __ | | ___   __ _  __| | ___ _ __
# | | | | '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|
# | |_| | |_) | | (_) | (_| | (_| |  __/ |
#  \__,_| .__/|_|\___/ \__,_|\__,_|\___|_|
#       |_|

# © 2021-today ParliamoDiPC
# Protected by MIT License. (https://opensource.org/licenses/MIT)
# https://github.com/ParliamoDiPC/uploader

# Use Fasm.ga! https://www.fasm.ga

############################### Packages

from flask import Flask, render_template, request, send_from_directory
import json, os, string, random, shutil

############################### Setting up basic things

app = Flask("uploader", template_folder = os.path.abspath("pages"))

site = "https://upload.com/" # Replace with your site (END THE URL WITH A BACKSLASH)

############################### Site home

@app.route("/")
def main():
	return "There's nothing here.<br><br>Based on <a href=\"https://github.com/ParliamoDiPC/uploader\" style=\"font-family: monospace\">uploader</a>"

############################### File URLs

@app.route("/<file>", strict_slashes = False)
def fileget(file):
	try:
		with open("data.json", "r") as f:
			jsonfile = json.load(f)
			return send_from_directory(jsonfile[file]["name"], jsonfile[file]["file"])
	except:
		return render_template("404.html")

@app.route("/txt/<file>", strict_slashes = False)
def txt_fileget(file):
	try:
		with open("data.json", "r") as f:
			jsonfile = json.load(f)
			if not request.args.get("enable_html"): return render_template("text.html", text = jsonfile[file]["text"], code = file)
			if not request.args.get("enable_html") == "1": return render_template("text.html", text = jsonfile[file]["text"], code = file)
			return render_template("text_html.html", text = jsonfile[file]["text"], code = file)
	except:
		return render_template("404.html")

############################### Upload APIs

@app.route("/upload", methods = ["POST"])
def upload():
	if not request.headers["password"] == os.getenv("password"): return "Unauthorized" # Remove this if you want to make this uploader public
	with open("data.json", "r+") as file:
		code = "".join(random.choice(string.ascii_letters) for i in range(10))
		try:
			f = request.files["file"]
			os.mkdir(code)
			f.save(f.filename)
			shutil.move(f.filename, code + "/" + f.filename)
			file_data = json.load(file)
			file_data.update({ code: { "name": code, "file": f.filename } })
			file.seek(0)
			json.dump(file_data, file, indent = 4)
			return site + code
		except:
			return "Error"

@app.route("/txtupload", methods = ["POST"])
def txtupload():
	if not request.headers["password"] == os.getenv("password"): return "Unauthorized" # Remove this if you want to make this uploader public
	with open("data.json", "r+") as file:
		code = "".join(random.choice(string.ascii_letters) for i in range(10))
		try:
			f = request.form["text"]
			file_data = json.load(file)
			file_data.update({ code: { "name": code, "text": f } })
			file.seek(0)
			json.dump(file_data, file, indent = 4)
			return site + "txt/" + code
		except:
			return "Error"
		
############################### Robots.txt file

@app.route("/robots.txt")
def robots():
	return send_from_directory(app.root_path, "robots.txt")

############################### Start webserver

if __name__ == "__main__":
	app.run("0.0.0.0")
