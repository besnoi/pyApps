import sqlite3

class Census:
    def __init__(self) -> None:
        self.conn = sqlite3.connect("census.sqlite")
        self.cursor = self.conn.cursor()
    
    # Get States/UT List
    def getStateList(self) -> list:
        rows = self.cursor.execute("SELECT state FROM 'population_by_religion' WHERE year='2011' AND district=''").fetchall()
        rows.sort()
        for i,v in enumerate(rows):
            rows[i]=rows[i][0]
        return rows

    # Get District List
    def getDistrictList(self) -> list:
        rows = self.cursor.execute("SELECT state,district FROM 'population_by_religion' WHERE year='2011'AND district!=''").fetchall()
        rows.sort()
        return rows

    # Get List of Years for which Census is Unavailable
    def getYearList(self,state,district) -> list:
        rows = self.cursor.execute(
            f"SELECT year FROM 'population_by_religion' WHERE state='{state}' AND district='{district}'").fetchall()
        for i,v in enumerate(rows):
            rows[i]=rows[i][0]
        return rows

    # Get Male Population for a particular year
    def getMalePopulation(self,state,district,year) -> list:
        return self.cursor.execute(
            f"""SELECT total_males,hindu_males,muslim_males,christian_males,sikh_males,buddhist_males,jain_males,other_males,atheist_males
                FROM 'population_by_religion' WHERE year='{year}' AND state='{state}' AND district='{district}'""").fetchall()[0]
    
    # Get Female Population for a particular year
    def getFemalePopulation(self,state,district,year) -> list:
        return self.cursor.execute(
            f"""SELECT total_females,hindu_females,muslim_females,christian_females,sikh_females,buddhist_females,jain_females,other_females,atheist_females
                FROM 'population_by_religion' WHERE year='{year}' AND state='{state}' AND district='{district}'""").fetchall()[0]
    
    # Get Total Population for a particular year
    def getTotalPopulation(self,state,district,year) -> list:
        return self.cursor.execute(
            f"""SELECT total_females+total_males,hindu_males+hindu_females,muslim_males+muslim_females,christian_males+christian_females,
                sikh_males+sikh_females,buddhist_males+buddhist_females,jain_males+jain_females,other_males+other_females,atheist_males+atheist_females
                FROM 'population_by_religion' WHERE year='{year}' AND state='{state}' AND district='{district}'""").fetchall()[0]

