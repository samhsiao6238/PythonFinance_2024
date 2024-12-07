#
# Author: Jackie Chang
# E-mail: ching040@gmail.com
# LineID: jackiechang040
#

import pandas as pd
data = {'one': [1, 2, 3, 4, 5], 'two': [2, 4, 6, 8, 10]}
df = pd.DataFrame(data)
print(df)
df = df.reindex(index=[0, 2, 4])
print(df)
