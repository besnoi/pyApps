import sqlite3

class NHFSReport:
    def __init__(self):
        self.conn = sqlite3.connect("nfhs.sqlite")
        self.cursor = self.conn.cursor()
    def getData(self,category,indicator,typology='total'): # type in ['total','urban','rural']
        rows = self.cursor.execute(f"SELECT state,{typology} FROM 'nfhs5' WHERE indicator=='{indicator}' AND category=='{category}'").fetchall()
        object=[]
        for i in rows:
            state = i[0].lower()
            if state == 'arunachal pradesh':
                state = 'arunanchal pradesh' # :/ typo on highcharts side
            if state == 'dadra and nagar haveli and daman and diu': # :/ highcharts treat them as seperate territories
                object.append(['daman and diu',i[1]])
                object.append(['dadara and nagar havelli',i[1]])
            else:
                object.append([state,i[1]])
        return object
    def getIndicators(self):
        object = {}
        rows = self.cursor.execute("SELECT category,indicator FROM 'nfhs5' WHERE state=='India'").fetchall()
        for i in rows:
            if i[0] not in object:
                object[i[0]] = []
            object[i[0]].append(i[1])
        return object

report = NHFSReport()
print(report.getData('Tobacco Use and Alcohol Consumption among Adults (age 15 years and above)','Women age 15 years and above who consume alcohol (%)'))


# print(report.getIndicators())



