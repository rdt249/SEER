import pandas as pd
import numpy as np

df = pd.DataFrame()
i = 0
for thr in np.linspace(1,100,10):
    for sat in np.linspace(1e-6,1e-3,10):
        df = df.append([['TestDevice'+str(i),'Test','SEE','Bendel',thr,sat,'','']])
        i += 1
df.columns = ['Device','Description','Effect','Model','Threshold','Saturation','Width','Shape']
df.to_csv('test_devices.csv',index=False)
print(df)