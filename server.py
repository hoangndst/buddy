from flask import Flask, render_template
from threading import Thread
app = Flask(
	__name__,
	template_folder='templates',
	static_folder='static'
)

@app.route('/')
def home():
  return render_template("index.html")

def run():
  app.run(host='0.0.0.0', port=8080)

def activate():
  a = Thread(target=run)
  a.start()