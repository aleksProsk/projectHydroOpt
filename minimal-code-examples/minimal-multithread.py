from multiprocessing.dummy import Pool as ThreadPool 
pool = ThreadPool(4)
results = pool.map(lambda x: round(x**(1/2)), range(100))
print(results)