import requests

# Only for Population By Religion table

class Census:
    def __init__(self) -> None:
        self.cache={}
        self.data={}
        pass

    def getAllData(self)->None: # Not Used
        URL = "https://statsindia.herokuapp.com/population_by_religion/api/get/all"
        self.data=requests.get(url = URL).json()

    def getData(self,state,district) -> None:
        if state+district not in self.cache:
            URL = f"https://statsindia.herokuapp.com/population_by_religion/api/get/data/{state}/{district}"
            self.cache[state+district]=requests.get(url = URL).json()
        return self.cache[state+district]

    def getPieChart(self,state,district,year,category) -> None:
        data = self.getData(state,district)[str(year)]
        if category=='Male':
            return [data['total_males'],data['hindu_males'],data['muslim_males'],data['christian_males'],data['sikh_males'],data['buddhist_males'],
            data['jain_males'],data['other_males'],data['atheist_males']]
        elif category=='Female':
            return [data['total_females'],data['hindu_females'],data['muslim_females'],data['christian_females'],data['sikh_females'],data['buddhist_females'],
            data['jain_females'],data['other_females'],data['atheist_females']]
        elif category=='Total':
            return [data['total_males']+data['total_females'],data['hindu_males']+data['hindu_females'],data['muslim_males']+data['muslim_females'],data['christian_males']+data['christian_females'],
            data['sikh_males']+data['sikh_females'],data['buddhist_males']+data['buddhist_females'],
            data['jain_males']+data['jain_females'],data['other_males']+data['other_females'],data['atheist_males']+data['atheist_females']]
        else:
            if category=='Others':
                category = 'other'
            elif category=='Unspecified':
                category = 'atheist'
            category = category.lower()
            return [data[f'{category}_males']+data[f'{category}_females'],data[f'{category}_males'],data[f'{category}_females']]
    



    def getYearList(self,state,district) -> None:
        print('Getting Year List...')
        years = []
        data = self.getData(state,district)
        for i in data:
            years.append(int(i))
        return years
    
    # states : [district] format
    def getRegionList(self) -> None:
        print('Getting Region List...')
        URL = f"https://statsindia.herokuapp.com/population_by_religion/api/get/regions"
        return requests.get(url = URL).json()


    