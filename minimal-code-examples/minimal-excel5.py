#Ausführung: time python3 minimal-excel5.py oder exec(open("./minimal-excel5.py").read())
from wolf4ross import *
from functools import partial
from glob import glob

def GetNEngines(d): return (Length(d[0][1])-2)/(Card(d[0][0])-1) /ar/ int
def GetEngineNames(d): return d[0][1][2:2+GetNEngines(d)]
def GetEnginesTurnover(year): return lambda d: Transpose(d[year][5:5+12])[2:2+GetNEngines(d)] /ar/ Transpose /ar/ Total
def GetEnginesEnergy(year): return lambda d: Transpose(d[year][5:5+12])[-GetNEngines(d):] /ar/ Transpose /ar/ Total
def GetEngineSummary(year):	return lambda d: (GetEnginesTurnover(year)(d), GetEnginesEnergy(year)(d), GetEnginesTurnover(year)(d)/div/GetEnginesEnergy(year)(d));
def GetEngineSummaryAllYears(nYears): return lambda data: ((lambda d: (Flatten /c/ Transpose /c/ GetEngineSummary(d))(data)) /m/ Range(nYears))
def GetLabeledEngineSummaryAllYears(nYears, caption=None): return lambda d: If(caption, Extend(Repeat(3*GetNEngines(d)) /m/ caption, Prepend)) /c/ Prepend(Flatten(Repeat(3) /m/ GetEngineNames(d))) /c/ Prepend(Flatten(Repeat(GetNEngines(d))(('Rev','Prod','Price')))) /a/ GetEngineSummaryAllYears(nYears)(d)

mynYears = 21
mynScens = 3
myPath = 'C:\\Users\\SEC\\Documents\\CSEIP\\Resultate\\Hydropt\\'
#myAssets = ('Emo3','FMHL','KHR')
myAssets = (lambda x: x.split(myPath)) /m/ glob(myPath + '/*/') /m1r/ Last /m1r/ (lambda x: x[1:-1])

myCSVFile = 'pythonExport_all.csv'

def myPaths(asset, scen): return (lambda n: myPath + asset + "\\Poyry" + str(scen+1) + "\\export" + str(n+1) + ".xlsx") /m/ Range(mynYears)
def myData(paths): return (lambda path: GetXLSSheet(path, -1)) /m1/ paths
def mySummaries(asset): return c1(myData, partial(myPaths, asset), Range)(mynScens) /ar/ Enumerate /m1r/ (lambda d: GetLabeledEngineSummaryAllYears(mynYears, (asset, d[0]))(d[1])) /m1r/ Transpose
myTable = mySummaries /mlog/ myAssets /ar/ partial(Flatten, level=2)
WriteMatrixToCSV(myPath + myCSVFile, myTable)