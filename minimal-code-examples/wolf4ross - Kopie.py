import re
from math import inf
import collections
from functools import lru_cache, reduce, partial
import infix
import funcy
import dis
from random import randint
import multiprocess
import time
from functools import partial

from os.path import join, dirname, abspath, isfile
import xlrd, xlwt
from xlutils.copy import copy as xl_copy
import csv

VECTOR = tuple
def Vectorize(x): return (x,)

def StringQ(x): return isinstance(x, str)

def VectorQ(x): return isinstance(x, collections.Iterable) and not StringQ(x) #isinstance(x, list) or isinstance(x, tuple)

def AtomQ(x): return not VectorQ(x)

def Length(x): return len(x) if VectorQ(x) else 0

#def VectorQ(x): return isinstance(x, collections.Iterable) and not AtomQ(x)
#bsp.: VectorQ(['a']) -> True; VectorQ('abc') -> False

@infix.div_infix
def m(f,x): return VECTOR(map(f,x)) if VectorQ(x) else f(x)

@infix.div_infix
def mp(f,x): 
	pool = multiprocess.Pool()
	result = VECTOR(pool.map(f,x)) if VectorQ(x) else f(x)
	pool.close()
	pool.join()
	return result

def Identity(x): return x

def baseN(num,b=62,numerals="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"): 
	return ((num == 0) and numerals[0]) or (baseN(num // b, b, numerals).lstrip(numerals[0]) + numerals[num % b])

def baseNs(num,b=62,numerals="0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"): 
	return ('-' if num < 0 else '+') + baseN(abs(num),b,numerals)

def LogProgress(jobid, caption, i, n, item = None, elapsedTime = 0, showArg = False, minTime = 2):
	remainingTime = elapsedTime*(n/i - 1) if i > 0 else None
	#logging von maximal 10 Iterationsschritten
	doLog = (0 == i%max(1, n//10) and remainingTime > minTime) if remainingTime is not None else True
	jobCaption = baseN(jobid)
	if doLog: print(jobCaption + " / " + caption + ": " + str(int(i/n*100)) + "%" + ((' at ' + str(item)) if showArg else '')  + ((", remaining time: " + str(round(remainingTime/60,1)) + " min") if remainingTime is not None else ""))
	if i+1 == n: print(jobCaption + " / " + caption + " is done")

def GetFID(f):
	try:
		result = str(VECTOR(dis.Bytecode(f)))
	except:
		result = str(f)
	return hash(result)

def random_with_N_digits(n):
	range_start = 10**(n-1)
	range_end = (10**n)-1
	return randint(range_start, range_end)

@infix.div_infix
def mlog(f,x): #bsp.:  ["sin", math.sin] /mlog/ Range(5)
	result = []
	jobid = random_with_N_digits(6)
	if Length(f) > 0: #wenn f = [f0, f1], dann nehmen wir an, dass f[0] die Bezeichnung und f[1] die Funktion ist
		myf = f[1]
		mycaption = f[0]
	else:
		myf = f
		mycaption = baseNs(GetFID(myf)) + " (" + myf.__name__ + ")"
	if VectorQ(x): 
		startTime = time.perf_counter()
		LogProgress(jobid, mycaption, 0, Length(x), x[0])
		for i, item in enumerate(map(myf,x), 1):
			result.append(item)
			LogProgress(jobid, mycaption, i, Length(x), x[i] if i < Length(x) else 'end', time.perf_counter() - startTime)
	else:
		result = myf(x)
	return VECTOR(result)

@infix.div_infix
def mplog(f,x): 
	result = []
	try:
		pool = multiprocess.Pool()
		jobid = random_with_N_digits(6)
		if Length(f) > 0: #wenn f = [f0, f1], dann nehmen wir an, dass f[0] die Bezeichnung und f[1] die Funktion ist
			myf = f[1]
			mycaption = f[0]
		else:
			myf = f
			mycaption = baseNs(GetFID(myf)) + " (" + myf.__name__ + ")"
		if VectorQ(x): 
			startTime = time.perf_counter()
			LogProgress(jobid, mycaption, 0, Length(x), x[0])
			for i, item in enumerate(pool.imap(myf,x), 1):
				result.append(item)
				LogProgress(jobid, mycaption + "*", i, Length(x), x[i] if i < Length(x) else 'end', time.perf_counter() - startTime)
		else:
			result = myf(x)
			
	#	enumerate(pool.map(f,x)) if VectorQ(x) else f(x)
		pool.close()
		pool.join()
	except:
		result = f /mlog/ x
	return VECTOR(result)

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
def cr(*f): return funcy.rcompose(*f)

@infix.div_infix
def a(f,x): return f /m0/ x #return f(x)

@infix.div_infix
def ar(x,f): return x /m0r/ f #return f(x)

def Getel(idx): return lambda l: reduce(operator.getitem, idx, l)

def Getels(idxlst): return lambda l: ((lambda idx: getel(idx)(l)) /m/ idxlst)

#bsp.: somelist = ['index0', ['index10', 'index11', ['index120', 'index121', ['index1220']]]]
#indices = [1, 2, 2, 0]
#getel([1,2,2,0])(somelist)
#getels([[1,2,2,0],[1,2,1]])(somelist)

def Depth(v): return int(Length(v) and max(map(Depth, v))+1) #int, damit FALSE in 0 konvertiert wird (für Fall, dass Argument atomic ist)

def Transpose(v): return VECTOR(map(VECTOR, zip(*v))) if (VectorQ(v) and Depth(v) > 1) else v

def MergeMatrices(m1, m2): return Transpose /m/ Transpose(VECTOR((m1, m2)))

def Constant(x): return lambda a: x
#Constant(10)(1) -> 10

@infix.div_infix
def div(x,y): return Transpose((lambda z: z[0]/z[1]) /m/ Transpose(VECTOR((x,y))))
#bsp.: [3,4]/div/[1,2]

def Timing(f, args):
	result = None
	startTime = time.process_time()
	result = f(args) if AtomQ(args) else f(*args)
	dt = (time.process_time() - startTime)
	return (dt, result)

def map_autop(f, v, minItems=3, minParTime=10, minLogTime=3):
	p = Identity
	par = False
	remainingExecutionTime = 0
	if len(v) >= minItems:
		funcTime = 0
		if (minParTime > 0):
			timedResult = Timing(f, Vectorize(v[0]))
			funcTime = timedResult[0]
			p = Prepend(timedResult[1])
			v = v[1:]
		remainingExecutionTime = (len(v)-1)*funcTime
	return p(mapx(f, v, False, remainingExecutionTime >= minLogTime, remainingExecutionTime >= minParTime))

def mapx(f, v, autopar=False, log=False, par=False, autopar_minItems=3, autopar_minParTime=10, autopar_minLogTime=3):
	result = None
	if autopar:
		result = map_autop(f,v, autopar_minItems, autopar_minParTime, autopar_minLogTime)
	else:
		if not log and not par: result = f /m/ v
		if not log and par: result = f /mp/ v
		if log and not par: result = f /mlog/ v
		if log and par: result = f /mplog/ v
	return result
 
def Map(f, item, level=1, autopar=True, log=False, par=False, autopar_minItems=3, autopar_minParTime = 10, autopar_minLogTime = 3):
	if level==1 and AtomQ(f) and VectorQ(item): return mapx(f, item, autopar, log, par, autopar_minItems, autopar_minParTime, autopar_minLogTime)
	if level==0 and VectorQ(f): return mapx(lambda g: g(item), f, autopar, log, par, autopar_minItems, autopar_minParTime, autopar_minLogTime)
	if level==0 and AtomQ(f): return f(item)
	level = min(level, Depth(item))
	return ((f /m/ item) if level == 0 else VECTOR(Map(f, i, level - 1) for i in item)) if AtomQ(f) else Map(lambda g: Map(g, item, level), f, inf)

def MapDeep(f, l): return Map(f, l, inf)

#https://mtomassoli.wordpress.com/2012/03/18/currying-in-python/
def Curry(func, unique = True, minArgs = None):
	""" Generates a 'curried' version of a function. """
	def g(*myArgs, **myKwArgs):
		def f(*args, **kwArgs):
			if args or kwArgs:  # some more args!
				# Allocates data to assign to the next 'f'.
				newArgs = myArgs + args
				newKwArgs = dict.copy(myKwArgs)
 
				# If unique is True, we don't want repeated keyword arguments.
				if unique and not kwArgs.keys().isdisjoint(newKwArgs):
					raise ValueError("Repeated kw arg while unique = True")
 
				# Adds/updates keyword arguments.
				newKwArgs.update(kwArgs)
 
				# Checks whether it's time to evaluate func.
				if minArgs is not None and minArgs <= len(newArgs) + len(newKwArgs):
					return func(*newArgs, **newKwArgs)  # time to evaluate func
				else:
					return g(*newArgs, **newKwArgs)	 # returns a new 'f'
			else:							   # the evaluation was forced
				return func(*myArgs, **myKwArgs)
		return f
	return g

def CurrySwap(f): return lambda *x: lambda *y: f(*y)(*x)

def Apply(f, v=()): return f(*v)

#def ApplyAfter(f, v=()): return lambda *x: f(*x)(*v) 

@infix.div_infix
def m0(a,b): return Map(a, b, 0)

@infix.div_infix
def m1(a,b): return Map(a, b)
#bsp.: (math.sin, math.cos) /m1/ (0,math.pi)

@infix.div_infix
def minf(a,b): return MapDeep(a, b)

@infix.div_infix
def m0r(a,b): return b /m0/ a

@infix.div_infix
def m1r(a,b): return b /m1/ a

@infix.div_infix
def minfr(a,b): return b /minf/ a

def Composify(f, a, *b): return CurrySwap(c(Curry(f)(a), *b))()

@infix.div_infix
def c0(a,*b): return Composify(m0, a, *b) #lambda *x: m0(a,b(*x)) 

@infix.div_infix
def c1(a,*b): return Composify(m1, a, *b) #lambda *x: m1(a,b(*x)) 

@infix.div_infix
def cinf(a,*b): return Composify(minf, a, *b) #lambda *x: minf(a,b(*x))

@infix.div_infix
def c0r(b,*a): return Composify(m0, *a, b)  #lambda *x: m0(a,b(*x)) #CurrySwap(Curry(m0)(a) /c/ b)()

@infix.div_infix
def c1r(b,*a): return  Composify(m1, *a, b) #lambda *x: m1(a,b(*x)) 

@infix.div_infix
def cinfr(b,*a): return Composify(minf, *a, b) #lambda *x: minf(a,b(*x))

def Reverse(a): return VECTOR(reversed(a))

def ReverseArguments(f): return lambda *x: f(*Reverse(VECTOR(x)))

def Plus(x): return lambda l: (MapDeep(lambda a: x+a, l) if AtomQ(x) else Plus(l)(x))
#bsp.: Plus(3)(Range(3)), Plus(Range(3))(3)

def Times(x): return lambda l: (MapDeep(lambda a: x*a, l) if AtomQ(x) else Times(l)(x))
#bsp.: (Plus(Range(3)) /c/ Times(3)) /m/ Range(3) --> [[0, 1, 2], [3, 4, 5], [6, 7, 8]]

def NumberedMatrix(nRows, nCols): return (Plus(Range(nCols)) /c/ Times(nCols)) /m/ Range(nRows) if nCols else Range(nRows)

def TupleFromContinuousMatIndex(nCols): return lambda contIdx: VECTOR((contIdx//nCols, contIdx%nCols))
#bsp.: TupleFromContinuousMatIndex(4)(6)

def NumberedTupleMatrix(nRows, nCols): return MapDeep(TupleFromContinuousMatIndex(nCols), NumberedMatrix(nRows, nCols))

def MatrixDimensions(m): return VECTOR((Length(m), Length(m[0])))

def PrependMatrixIndices(m): return MergeMatrices(NumberedTupleMatrix(*MatrixDimensions(m)), m)

def Enumerate(x): return VECTOR(enumerate(x))

def Prepend(x): return lambda v: Vectorize(x) + (v if VectorQ(v) else Vectorize(v))

def Append(x): return lambda v: (v if VectorQ(v) else Vectorize(v)) + Vectorize(x)

def Extend(x, f=Append): return cr(*(f /m/ x))

def Flatten(v, level=inf):
	new_lis = VECTOR()
	level = min(level,Depth(v))
	for item in v: new_lis = Extend(Flatten(item, level-1))(new_lis) if VectorQ(item) and level > 0 else Append(item)(new_lis)
	return new_lis

def Range(n): return VECTOR(range(n))

def Total(x): return sum /m/ Transpose(x) if Depth(x) > 1 else sum(x) if Depth(x) else x

def Repeat(n): return lambda x: Vectorize(x)*n

def Last(x): return x[-1]
#bsp.: NumberedMatrix(3,4) /m0r/ Last

def First(x): return x[0]

DeleteDuplicates = VECTOR /c/ set
Card = Length /c/ DeleteDuplicates #Cardinality

def If(test, rt, rf=Identity): return rt if test else rf
#funktionales if, liefert Identitätsabbildung als default

@lru_cache(maxsize=4)
def ExcelWorkbookFromFile(fname): return xlrd.open_workbook(fname)
def ExcelSheetFromFile(fname, index): return ExcelWorkbookFromFile(fname).sheet_by_index(index)
def MatrixFromExcelSheet(xl_sheet): return (lambda i:((lambda c: c.value) /m/ xl_sheet.row(i))) /m/ Range(xl_sheet.nrows)
def GetXLSSheet(path, index): return MatrixFromExcelSheet(ExcelSheetFromFile(path, index))
def WriteMatrixToXLSSheet(mat, sheet): Map(lambda x: sheet.write(x[0][0],x[0][1],x[1]), PrependMatrixIndices(mat), 2)

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

import math
def _runtests():
	n = 0
	def npp():
		nonlocal n
		n+=1
		return n
	
	printme = lambda x: print /c/ str /c/ Prepend(x)
	
	"Test" /m0r/ printme(npp())
	VECTOR([1,2,3]) /m0r/ printme(npp())
	Depth(1) /m0r/ printme(npp())
	Depth(NumberedMatrix(3,3)) /m0r/ printme(npp())
	Prepend(3)(Range(3)) /m0r/ printme(npp())
	(math.sin /mlog/ Range(5)) /m0r/ printme(npp())
	(["sin", math.sin] /mlog/ Range(5)) /m0r/ printme(npp())
	(("sin", math.sin) /mlog/ Range(5)) /m0r/ printme(npp())
	Map(math.sin, Range(10), log=True) /m0r/ printme(npp())
	Map(math.sin, Range(10), log=True, par=True) /m0r/ printme(npp())
	Map(math.sin, Range(10), log=False, par=True) /m0r/ printme(npp())
	Map(math.sin, Range(10), autopar=True) /m0r/ printme(npp())
	Map(math.sin, Range(10), autopar=True, autopar_minItems=0, autopar_minTime=0) /m0r/ printme(npp())
	Map(math.sin, NumberedMatrix(3,3), level=inf, autopar=True, autopar_minItems=0, autopar_minTime=0) /m0r/ printme(npp())
	Enumerate(math.sin /m1/ (math.cos /m1/ Range(3))) /ar/ printme(npp())
	math.sin /c1/ math.cos /c1/ Range /a/ 3 /ar/ Enumerate /ar/ printme(npp())

#_runtests()

