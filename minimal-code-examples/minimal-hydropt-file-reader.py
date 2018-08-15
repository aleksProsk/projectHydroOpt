import os
os.environ["OCTAVE_EXECUTABLE"] = "C:\\Octave\\Octave-4.2.2\\bin\\octave-cli.exe"

from oct2py import octave

filepath = 'C:\\Users\\SEC\\Documents\\Alperia\\HydroptModel\\vsm.mod'
octave.eval("load('" + filepath + "', '-mat')")
#x = octave.pull('x')
#return str(x[0, 1].z)
octave.eval("revenue = Data.Asset(1).ScenarioWaterManager.Result.OverallRevenue;")
x = octave.pull('revenue')
print(str(x))
#x = octave.pull('Data.Asset(1).ScenarioWaterManager.Result.OverallRevenue') --> erzeugt fehler
data = octave.pull('Data')
x = data.Asset.ScenarioWaterManager.Result.OverallRevenue
print(str(x))