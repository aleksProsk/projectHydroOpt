#Ausführung: time python3 minimal-excel2.py
from wolf4ross import *
def GetNEngines(d): return (Length(d[0][1])-2)/(Card(d[0][0])-1) /ar/ int
def GetEngineNames(d): return d[0][1][2:2+GetNEngines(d)]
def GetEnginesTurnover(year): return lambda d: Transpose(d[year][5:5+12])[2:2+GetNEngines(d)] /ar/ Transpose /ar/ Total
def GetEnginesEnergy(year): return lambda d: Transpose(d[year][5:5+12])[-GetNEngines(d):] /ar/ Transpose /ar/ Total
def GetEngineSummary(year):	return lambda d: (GetEnginesTurnover(year)(d), GetEnginesEnergy(year)(d), GetEnginesTurnover(year)(d)/div/GetEnginesEnergy(year)(d));
def GetEngineSummaryAllYears(nYears): return lambda data: ((lambda d: (Flatten /c/ Transpose /c/ GetEngineSummary(d))(data)) /m/ Range(nYears))
def GetLabeledEngineSummaryAllYears(nYears, caption=None): return lambda d: If(caption, Extend(Repeat(3*GetNEngines(d)) /m/ caption, Prepend)) /c/ Prepend(Flatten(Repeat(3) /m/ GetEngineNames(d))) /a/ GetEngineSummaryAllYears(nYears)(d)

mynYears = 2
mynScens = 2
myAsset = 'Emo3'

def myPaths(scen): return (lambda n: "C:\\Users\\SEC\\Documents\\CSEIP\\Resultate\\Hydropt\\" + myAsset + "\\Poyry" + str(scen+1) + "\\export" + str(n+1) + ".xlsx") /m/ Range(mynYears)
def myData(paths): return (lambda path: GetXLSSheet(path, -1)) /m1/ paths
summaries = c1(myData, myPaths, Range)(mynScens) /ar/ Enumerate /m1r/ (lambda d: GetLabeledEngineSummaryAllYears(mynYears, (myAsset, d[0]))(d[1]))
WriteMatrixToCSV('C:\\Users\\SEC\\Documents\\CSEIP\\Resultate\\Hydropt\\Emo3\\pythonExportTestScenb.csv', Transpose /m/ summaries /ar/ partial(Flatten, level=1))

#summaries = (lambda d: GetLabeledEngineSummaryAllYears(mynYears, (myAsset, d[0]))(d[1])) /m/ Enumerate(myData /m1/ (myPaths /m/ Range(mynScens)))
#summaries = myData /c1/ myPaths /c1/ Range /a/ mynScens /ar/ Enumerate /m1r/ (lambda d: GetLabeledEngineSummaryAllYears(mynYears, (myAsset, d[0]))(d[1]))