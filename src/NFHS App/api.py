import requests

# we need to replace / with ` cause we will pass strings in urls
def clean(str):
    return str.replace('/','`')

class NFHSReport:
    def __init__(self) -> None:
        self.cache={}

    def getData(self,category,indicator,typology) -> None:
        print('Getting Data...')
        typology=typology.lower()
        print(category,indicator,typology)
        category,indicator=clean(category),clean(indicator)
        if category+indicator+typology not in self.cache:
            URL = f"https://statsindia.herokuapp.com/nfhs/5/api/get/data/{category}/{indicator}/{typology}"
            self.cache[category+indicator+typology]=requests.get(url = URL).json()
        return self.cache[category+indicator+typology]

    
    # states : [district] format
    def getIndicators(self) -> None:
        print('Getting Indicator List...')
        URL = f"https://statsindia.herokuapp.com/nfhs/5/api/get/indicators"
        return requests.get(url = URL).json()
