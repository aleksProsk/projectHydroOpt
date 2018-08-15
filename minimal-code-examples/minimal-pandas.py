from pandas import DataFrame
import numpy as np

df2 = DataFrame(np.random.randn(10, 5))
df3 = DataFrame(np.random.randn(10, 5), columns=['a', 'b', 'c', 'd', 'e'])
df4 = DataFrame(np.transpose([[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3],[1, 2, 3]]), columns=['a', 'b', 'c', 'd', 'e'])
rows=df3.to_dict('records')
columns=sorted(df3.columns)

print(np.random.randn(10, 5))
print(df2)
print(df3)
print(rows)
print(columns)
print(df4)