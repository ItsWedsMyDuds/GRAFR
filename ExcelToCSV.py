import os
import pandas as pd
import xlsxwriter


#print("input")

#i have no clue what im doing

mainDir ="C:\\Users\\rnaka\\desktop"
os.chdir(mainDir)
file = 'test.xlsm'

df = pd.DataFrame({'Data':[10,20,30,20,15,30,45]})

writer = pd.ExcelWriter('hmm.xlsx',engine = 'xlsxwriter')
df.to_excel(writer,sheet_name='Sheet1')

workbook = writer.book
worksheet = writer.sheets['Sheet1']