#!/usr/bin/env python

import sqlite3
import os

file = open('SwissFoodCompDataV50_4.csv','r')
for line in file:
    dbFields = line.split('#')
    break
file.close()

i = 0
valueIndices = []
creatingString = 'CREATE TABLE naerwerte ('
insertString = 'INSERT INTO naerwerte VALUES('
for fieldName in dbFields:
    if ( ('unit' not in fieldName.lower() ) and ( 'value' not in fieldName.lower() ) and ( 'matrix' not in fieldName.lower() ) ):
        if fieldName.split(',')[1] == 'N':
            dbFieldType = 'FLOAT'
            insertString += '?, '
        else:
            dbFieldType = 'TEXT'
            insertString += '?, '
        creatingString += "%s %s, " % (fieldName.split(',')[0].replace(' ','_').replace('.','').replace(',','_').replace('-','_'), dbFieldType)
        valueIndices.append(i)
    i += 1
        
creatingString = creatingString[0:-2] + ')'
insertString = insertString[0:-2] + ')'

print creatingString
print valueIndices

os.system('rm SwissFoodCompDataV50.sqlite')
db = sqlite3.connect('SwissFoodCompDataV50.sqlite')
cur = db.cursor()

db.execute(creatingString)

file = open('SwissFoodCompDataV50_4.csv','r')
insertValues = []
i = 0
for line in file:
    if i > 0:
        values = line.split('#')
        insert_values_tmp = []
        for j in valueIndices:
            insert_values_tmp.append(unicode(values[j],'utf-8'))
        
        insertValues.append(insert_values_tmp)
    i += 1
file.close()
        
for j in range(i-1):
    cur.execute(insertString, insertValues[j])
        
db.commit()
db.close()

