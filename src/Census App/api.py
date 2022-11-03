import requests

# Only for Population By Religion table

class Census:
    def __init__(self) -> None:
        self.cache={}
        pass

    def getChoropleth(self,year,state,religion,sex)->None: # Not Used
        states = []
        if year+state not in self.cache:
            URL = f"https://statsindia.herokuapp.com/population_by_religion/api/get/choropleth/{state}/{year}"
            print(URL)
            self.cache[year+state]=requests.get(url = URL).json()
        states.append([state,self.cache[year+state]['State'][f'{religion}_{sex}']])
        for i in self.cache[year+state]:
            if i!='State':
                states.append([i,self.cache[year+state][i][f'{religion}_{sex}']])
        return states

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
    def getRegionList(self,year='') -> None:
        print('Getting Region List...')
        if f'region{year}' not in self.cache:
            URL = f"https://statsindia.herokuapp.com/population_by_religion/api/get/regions/{year}"
            self.cache[f'region{year}']=requests.get(url = URL).json()
        return self.cache[f'region{year}']

# print(Census().getChoropleth('2011','Jammu and Kashmir','hindu','males'))
    
