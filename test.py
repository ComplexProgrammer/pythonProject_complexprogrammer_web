import pandas as pd
pd.read_excel(open('fulldata.xlsx', 'rb'),
              sheet_name='10.4')
print(pd)