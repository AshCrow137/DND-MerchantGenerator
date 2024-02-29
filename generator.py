import glob
import json 
import random 
import os 
class Generator():
    def __init__(self,maxCost:int,itemsNumber:int,itemTypes:dict):
        self.numbers = list(range(10))
        for number in self.numbers:
            self.numbers[self.numbers.index(number)] = str(number)

        self.coinsToNumber = {'м':1,'с':10,'з':100,'э':50,'п':1000}
        self.numberToCoin = {'1':'м','10':'с','100':'з'}#,'1000':'п'} # 'э':5 - электрумовые
        self.ItemTypes = itemTypes
        self.itemsNumber = itemsNumber
        self.MaxCost = maxCost
        self.items = self.GetItemsDict()
        self.selectedItems = self.items.copy()
    def GetItemsDict(self):
        filePath = glob.glob('*/ItemLib/*.json')
        items = {}
        for path in filePath:
            name = os.path.basename(path)
            name = name.replace('.json','')
            self.ItemTypes.setdefault(name,True)
            file = open(path,'rt',encoding='utf-8')
            content = file.read()
            dictionary = json.loads(content)
            items.setdefault(name,dictionary)
            file.close()
        return items

    def CoinsToCost(self,cost:str):
            cost = cost.replace(' ','')
            resultCost = ''
            for letter in cost:
                if letter in self.numbers:
                    resultCost+=letter
                elif letter in self.coinsToNumber:
                    resultCost = int(resultCost)*self.coinsToNumber[letter]
            
            return resultCost

    def CostToCoins(self,cost:int):
        
        

        def GetReminder(self,cost:int):
            pmod = 1
            for mod in self.numberToCoin:
                intmod = int(mod)
                if cost > intmod:
                    if pmod <=intmod:
                        pmod = intmod 
            integer = cost//pmod   
            reminder = cost%pmod
            integer = str(integer) + self.numberToCoin[str(pmod)] +'м' # собираем строку из количества монет и модификатора 
            if reminder > 0:
                integer += ' ' + GetReminder(self,reminder) # если остаток от монет больше нуля, проверяем еще раз 
            return integer
        resultCost = GetReminder(self,cost)  
        return resultCost

    def CheckCost(self,items:dict):
        if not items:
            return None
        newItemType = items.copy()
        for item in items:
            cost =self.CoinsToCost( items[item])
            if cost>self.MaxCost:
                del newItemType[item]
            else:
                newItemType[item] = cost    
        if not newItemType:
            return None  
        return newItemType  

    def GetRandomItem(self,oldItemType:dict): 
        iterations = 0
        while iterations<10000:
            itemType = self.CheckCost(oldItemType)  
            if itemType:   
                item,cost = random.choice(list(itemType.items()))
                return item, cost
            iterations+=1
        else:
            print(f'No item with that cost in {oldItemType}')
            return None,None    
    def GetRandomItemType(self,possibleItemTypes:dict):
        
        if possibleItemTypes:
            selectedTypes = {}
            for key in possibleItemTypes.keys():
                if  self.ItemTypes.get(key) == True:
                    selectedTypes.setdefault(key,possibleItemTypes[key])
            if not selectedTypes:
                
                return {'Error':'No selected item types'}          
            itemType, items = random.choice(list(selectedTypes.items()))
            checked = self.CheckCost(items)
            if not checked:
                del possibleItemTypes[itemType]
                items = self.GetRandomItemType(possibleItemTypes) 
            return items
        else: 
           
            return {'Error':'Worng max cost'}
    

    def GetResultStore(self):
        resultStore = {}
        for i in range(self.itemsNumber):
            possibleItemType = self.GetRandomItemType(self.selectedItems)
            if possibleItemType.get('Error'):
                return possibleItemType
            item,cost =self.GetRandomItem(possibleItemType) # {"предмет":{"цена":10,"количество":3}}
            if item and cost:
                
                cost = self.CostToCoins(cost)
                
                if resultStore.get(item):
                    resultStore[item]["number"]+=1
                else:
                    resultStore[item] = {'cost':cost,'number':1}
                
        return resultStore 
    def UnpackStore(self,store:dict):
        text = ''
        result = []
        for item in store:
            text= '{} ценой {} количеством {}'.format(item,store[item]['cost'],store[item]['number'])
            result.append(text)
        return result
    
    