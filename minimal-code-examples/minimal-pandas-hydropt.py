from pandas import DataFrame
import numpy as np
from oct2py import octave

def load_hydopt_data(filepath):
	octave.eval("load('" + filepath + "', '-mat')") #todo: separate octave instanz für jeden user
	data = octave.pull('Data')
	return data
	
data = load_hydopt_data('C:\\Users\\SEC\\Documents\\Alperia\\HydroptModel\\vsm.mod')
result = data.Asset.ScenarioWaterManager.Result

tinterval = [np.min(result.DateNum), np.max(result.DateNum)]

values = np.hstack((
	result.MonthlyEnergyPeak, 
	result.MonthlyEnergyOffPeak,
	result.MonthlyEnergyPeak+result.MonthlyEnergyOffPeak
))

df = DataFrame(
	values,
	columns=['Peak [MWh]', 'Offpeak [MWh]', 'Total [MWh]'])

print(df)

#print(result)