import os
os.environ["OCTAVE_EXECUTABLE"] = "C:\\Octave\\Octave-4.2.2\\bin\\octave-cli.exe"

from flask import Flask
from oct2py import octave

app = Flask(__name__)

@app.route('/')
def index():
	octave.eval('x = struct("y", {1, 2}, "z", {3, 4});')
	x = octave.pull('x')
	return str(x[0, 1].z)

