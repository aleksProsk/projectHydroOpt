#Ausführung: time python3 minimal-excel2.py

from __future__ import print_function
from os.path import join, dirname, abspath, isfile
import xlrd, xlwt
from xlutils.copy import copy as xl_copy

import re

import csv

from math import inf

import collections

from pathlib import Path # für inline-io
from functools import lru_cache, reduce, partial

import infix
import funcy


def Length(x):
	try:
		return len(x) if not isinstance(x, str) else 0
	except:
		return 0

def AtomQ(x): return Length(x) == 0

def isvector(x): return isinstance(x, collections.Iterable) and not AtomQ(x)
#bsp.: isvector(['a']) -> True; isvector('abc') -> False

@infix.div_infix
def m(f,x): return list(map(f,x)) if isvector(x) else f(x)

import multiprocess
@infix.div_infix
def mp(f,x): 
	pool = multiprocess.Pool()
	result = list(pool.map(f,x)) if isvector(x) else f(x)
	pool.close()
	pool.join()
	return result
	
def Identity(x): return x

def baseN(num,b=62,numerals="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"): 
	return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def baseNs(num,b=62,numerals="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"): 
	return ('-' if num < 0 else '+') + baseN(abs(num),b,numerals)

def LogProgress(jobid, caption, i, n, item = None, elapsedTime = 0):
	remainingTime = elapsedTime*(n/i - 1) if i > 0 else None
	print(baseN(jobid) + " / " + caption + ": " + str(round(i/n*100,1)) + "%" + ' at ' + str(item) + ((", remaining time: " + str(round(remainingTime/60,1)) + " min") if remainingTime is not None else ""))

import dis
def GetFID(f):
	try:
		result = str(list(dis.Bytecode(f)))
	except:
		result = str(f)
	return hash(result)

from random import randint
def random_with_N_digits(n):
	range_start = 10**(n-1)
	range_end = (10**n)-1
	return randint(range_start, range_end)

@infix.div_infix
def mplog(f,x): 
	result = []
	pool = multiprocess.Pool()
	jobid = random_with_N_digits(6)
	if Length(f) > 0: #wenn f = [f0, f1], dann nehmen wir an, dass f[0] die Bezeichnung und f[1] die Funktion ist
		myf = f[1]
		mycaption = f[0]
	else:
		myf = f
		mycaption = baseNs(GetFID(myf))
		
	if isvector(x): 
		startTime = time.perf_counter()
		LogProgress(jobid, mycaption, 0, Length(x), x[0])
		for i, item in enumerate(pool.imap(myf,x), 1):
			result.append(item)
			LogProgress(jobid, mycaption, i, Length(x), x[i] if i < Length(x) else 'end', time.perf_counter() - startTime)
	else:
		result = myf(x)
		
#	enumerate(pool.map(f,x)) if isvector(x) else f(x)
	pool.close()
	pool.join()
	return result

@infix.div_infix
def mlog(f,x): #bsp.:  ["sin", math.sin] /mlog/ Range(5)
	result = []
	jobid = random_with_N_digits(6)
	if Length(f) > 0: #wenn f = [f0, f1], dann nehmen wir an, dass f[0] die Bezeichnung und f[1] die Funktion ist
		myf = f[1]
		mycaption = f[0]
	else:
		myf = f
		mycaption = baseNs(GetFID(myf))
	if isvector(x): 
		startTime = time.perf_counter()
		LogProgress(jobid, mycaption, 0, Length(x), x[0])
		for i, item in enumerate(map(myf,x), 1):
			result.append(item)
			LogProgress(jobid, mycaption, i, Length(x), x[i] if i < Length(x) else 'end', time.perf_counter() - startTime)
	else:
		result = myf(x)
	return result

@infix.div_infix
def M(f,g): return lambda x: f /m/ g(x)
#Beispiel:  
#mym = [[1, 2], ['a', 4]]
#(print /M/ Identity /M/ Identity)(myM)
#ist das gleiche wie
#(lambda a: (print /m/ a)) /m/ myM

@infix.div_infix
def c(*f): return funcy.compose(*f)
# Beispiel: (math.sin /c/ math.cos /c/ math.tan) /m/ [1,2,3]

@infix.div_infix
def a(f,x): return f(x)

def getel(idx): return lambda l: reduce(operator.getitem, idx, l)

def getels(idxlst): return lambda l: ((lambda idx: getel(idx)(l)) /m/ idxlst)

#bsp.: somelist = ['index0', ['index10', 'index11', ['index120', 'index121', ['index1220']]]]
#indices = [1, 2, 2, 0]
#getel([1,2,2,0])(somelist)
#getels([[1,2,2,0],[1,2,1]])(somelist)

def split(s): return lambda x: x.split(s)

depth = lambda L: (isinstance(L, list) or isinstance(L, tuple)) and max(map(depth, L))+1

Depth = depth

def transpose(v): return list(map(list, zip(*v))) if (isvector(v) and depth(v) > 1) else v

Transpose = transpose

def MergeMatrices(m1, m2): return Transpose /m/ Transpose([m1, m2])

def Constant(x): return lambda a: x
#Constant(10)(1) -> 10

@infix.div_infix
def div(x,y): return transpose((lambda z: z[0]/z[1]) /m/ transpose([x,y]))
#bsp.: [3,4]/div/[1,2]

def Map(f, item, level=1):
	if level == inf:
		level = Depth(item)
	if level == 0:
		return f(item)
	else:
		return (lambda i: Map(f,i,level-1)) /m/ item 	#das gleiche wie return [Map(f, i, level - 1) for i in item]

def MapDeep(f, l): return Map(f, l, level=inf)

def Plus(x): return lambda l: (MapDeep(lambda a: x+a, l) if AtomQ(x) else Plus(l)(x))
#bsp.: Plus(3)(Range(3)), Plus(Range(3))(3)

def Times(x): return lambda l: (MapDeep(lambda a: x*a, l) if AtomQ(x) else Times(l)(x))
#bsp.: (Plus(Range(3)) /c/ Times(3)) /m/ Range(3) --> [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

def NumberedMatrix(nRows, nCols): return (Plus(Range(nCols)) /c/ Times(nCols)) /m/ Range(nRows)

def TupleFromContMatIndex(nCols): return lambda contIdx: [contIdx//nCols, contIdx%nCols]
#bsp.: TupleFromContMatIndex(4)(6)

def NumberedTupleMatrix(nRows, nCols): return MapDeep(TupleFromContMatIndex(nCols), NumberedMatrix(nRows, nCols))

def MatrixDimensions(m): return [Length(m), Length(m[0])]

def PrependMatrixIndices(m): return MergeMatrices(NumberedTupleMatrix(*MatrixDimensions(m)), m)

def Enumerate(x): return list(enumerate(x))


def prepend(x): return lambda l: [x] + l

Prepend = prepend

def flatten(lis, level=inf):
	"""Given a list, possibly nested to any level, return it flattened."""
	new_lis = []
	if level==inf:
		level = Depth(lis)
	for item in lis:
		if type(item) == type([]) and level > 0:
			new_lis.extend(flatten(item, level-1))
		else:
			new_lis.append(item)
	return new_lis

Flatten = flatten

def Range(n): return list(range(n))

def Total(x): return sum /m/ Transpose(x)

def Repeat(n): return lambda x: [x]*n

DeleteDuplicates = list /c/ set
Card = Length /c/ DeleteDuplicates #Cardinality

def IncrementString(s): #Inkrementierung des s, falls möglich
	match = re.search('[0-9]+$', s)
	if match is not None:
		splitIdx = match.span()[0]
		lastNo = int(s[splitIdx:])
		return s[:splitIdx] + str(lastNo+1) 
	else:
		return s + "2"

def If(test, rt, rf=Identity): return rt if test else rf
#funktionales if, liefert Identitätsabbildung als default

import time

def timeme(method):
	def wrapper(*args, **kw):
		startTime = time.process_time()
		result = method(*args, **kw)
		endTime = time.process_time()
		print((endTime - startTime)*1000,'ms')
		return result
	return wrapper

@lru_cache(maxsize=4)
def ExcelWorkbookFromFile(fname): return xlrd.open_workbook(fname)
def ExcelSheetFromFile(fname, index): return ExcelWorkbookFromFile(fname).sheet_by_index(index)
def MatrixFromExcelSheet(xl_sheet): return (lambda i:((lambda c: c.value) /m/ xl_sheet.row(i))) /m/ Range(xl_sheet.nrows)
def GetXLSSheet(path, index): return MatrixFromExcelSheet(ExcelSheetFromFile(path, index))
def WriteMatrixToXLSSheet(m, sheet): Map(lambda x: sheet.write(x[0][0],x[0][1],x[1]), PrependMatrixIndices(m), 2)

def GetXLSBookWithNewSheetAtEnd(path, sheetName = None):
	isNew = not isfile(path)
	book = xlwt.Workbook(encoding="utf-8") if isNew else xl_copy(xlrd.open_workbook(path, formatting_info=True))
	if sheetName is None and not isNew: sheetName = IncrementString(book.get_sheet(-1).name)
	if sheetName is None: sheetName = "Sheet 1"
	book.add_sheet(sheetName)
	return book

def WriteMatrixToNewXLSSheet(path, m, sheetName = None):
	book = GetXLSBookWithNewSheetAtEnd(path, sheetName)
	WriteMatrixToXLSSheet(m, book.get_sheet(-1))
	book.save(path)

def WriteMatrixToCSV(path, m):
	with open(path, "w") as f: (csv.writer(f)).writerows(m)
	f.close()

def GetNEngines(d): return int((Length(d[0][1])-2)/(Card(d[0][0])-1))
def GetEngineNames(d): return d[0][1][2:2+GetNEngines(d)]
def GetEnginesTurnover(year): return lambda d: Total(Transpose(Transpose(d[year][5:5+12])[2:2+GetNEngines(d)]))
def GetEnginesEnergy(year): return lambda d: Total(Transpose(Transpose(d[year][5:5+12])[-GetNEngines(d):]))
def GetEngineSummary(year):	return lambda d: [GetEnginesTurnover(year)(d), GetEnginesEnergy(year)(d), GetEnginesTurnover(year)(d)/div/GetEnginesEnergy(year)(d)];
def GetEngineSummaryAllYears(nYears): return lambda data: ((lambda d: (Flatten /c/ Transpose /c/ GetEngineSummary(d))(data)) /m/ Range(nYears))
#def GetLabeledEngineSummaryAllYears(nYears, caption=None): return lambda d: If(caption, Prepend(Repeat(3*GetNEngines(d))(caption))) /a/ Prepend(Flatten(Repeat(3) /m/ GetEngineNames(d))) /a/ GetEngineSummaryAllYears(nYears)(d)
def GetLabeledEngineSummaryAllYears(nYears, caption=None): return lambda d: If(caption, Prepend(Repeat(3*GetNEngines(d)) /m/ caption)) /c/ Prepend(Flatten(Repeat(3) /m/ GetEngineNames(d))) /a/ GetEngineSummaryAllYears(nYears)(d)

mynYears = 2
mynScens = 2
myAsset = 'Emo3'
def myPaths(scen): return (lambda n: "C:\\Users\\SEC\\Documents\\CSEIP\\Resultate\\Hydropt\\" + myAsset + "\\Poyry" + str(scen+1) + "\\export" + str(n+1) + ".xlsx") /m/ Range(mynYears)
def myData(paths): return (lambda path: GetXLSSheet(path, -1)) /mplog/ paths

summaries = GetLabeledEngineSummaryAllYears(mynYears, myAsset) /m/ (myData /mlog/ (myPaths /m/ Range(mynScens)))
(lambda m: WriteMatrixToNewXLSSheet('C:\\Users\\SEC\\Documents\\CSEIP\\Resultate\\Hydropt\\Emo3\\pythonExportTest2.xls', Transpose(m))) /m/ summaries
(lambda m: WriteMatrixToCSV('C:\\Users\\SEC\\Documents\\CSEIP\\Resultate\\Hydropt\\Emo3\\pythonExportTestScen' + str(m[0]+1) + '.csv', Transpose(m[1]))) /m/ Enumerate(summaries)
