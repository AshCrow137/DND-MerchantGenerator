import tkinter
from tkinter import ttk
import generator

numbers = list(range(10))
for number in numbers:
    numbers[numbers.index(number)] = str(number)

def GenerateCommand():
    ClearContentFrame()

    selectedTypes = {'armor':bool(bArmor.get()),
                     'weapon':bool(bWeapon.get()),
                     'tools':bool(bTools.get()),
                     'equipment':bool(bEquipment.get())}
    succes = True
    for type in selectedTypes:
        if selectedTypes[type]:
            break
    else:
        ShowErrorMessage('Пожалуйста, выберите хотя бы один тип предметов')
        succes = False

    itemNumber = int(itemNumberEntry.get())
    if itemNumber<=0:
        ShowErrorMessage('Пожалуйста, укажите количество предметов больше нуля')
        succes = False
    goldCoins = goldCoinsEntry.get() if goldCoinsEntry.get() else 0
    silverCoins = silverCoinsEntry.get() if silverCoinsEntry.get() else 0
    copperCoins = copperCoinsEntry.get() if copperCoinsEntry.get() else 0
    
    resultCost = int(goldCoins)*100 +int(silverCoins)*10 +int(copperCoins)
    if resultCost <=0:
        ShowErrorMessage('Пожалуйста, укажите стоимость предметов больше нуля')
        succes = False
    
    if succes:
        store = generator.Generator(resultCost,itemNumber,selectedTypes)
        resultStore = store.GetResultStore()
        if resultStore.get('Error'):
            ShowErrorMessage('Невозможно сгенерировать предметы по заданным параметрам')
            return
        CreateContentTreeView(resultStore)

def CreateContentTreeView(resultStore:dict):
    content = []
    for item in resultStore: #{"item":{"cost":10,"number":3}}
        content.append((item,resultStore[item]['number'],resultStore[item]['cost']))
    headers = ('Name','Number','Cost')
    tree = ttk.Treeview(master=contentFrame,columns=headers,show='headings',height=21)
    tree.grid(column=0,row=0)
    tree.heading('Name',text='Название',anchor='w')
    tree.heading('Number',text='Количество',anchor='w')
    tree.heading('Cost',text='Стоимость',anchor='w')

    tree.column("#1", stretch='no', width=290)
    tree.column("#2", stretch='no', width=80)
    tree.column("#3", stretch='no', width=90)

    for resultItem in content:
        tree.insert('','end',values=resultItem)
    scrollbar = ttk.Scrollbar(master=contentFrame,orient='vertical',command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.grid(column=1,row=0,sticky='ns')

def ShowErrorMessage(message:str):
    errorLabel = ttk.Label(master=contentFrame,text=message,wraplength=300)
    errorLabel.pack(anchor='center',pady=5)

def ClearContentFrame():
    content = contentFrame.pack_slaves()
    content.extend(contentFrame.grid_slaves())
    for object in content:
        object.destroy()

def CheckLetters(string:str):
    for l in string:
        if l not in numbers:
            return False
    return True

def CheckIfOnlyInt(input):
    if len(input)>5:
        return False
    elif CheckLetters(input):
        return True
                        
    elif input == "": 
        return 0

    else:
        return False

# store = generator.Generator(5000,150,{'armor':True,'weapon':True,'tools':True,'equipment':True})
# UnpackedStore = store.UnpackStore(store.GetResultStore(store.selectedItems))


root = tkinter.Tk()
bArmor = tkinter.IntVar(value=1)
bWeapon = tkinter.IntVar(value=1)
bTools = tkinter.IntVar(value=1)
bEquipment = tkinter.IntVar(value=1)
root.title('Генератор торговцев')
root.geometry('720x480')
# root.minsize(720,720)
root.resizable(False,False)

#Frames
mainframe = ttk.Frame(borderwidth=1,relief='solid',width=700,height=700)
mainframe.pack(anchor='center',fill="both",padx=10,pady=10)
settingsFrame = ttk.Frame(borderwidth=1,relief='solid',master=mainframe,height=680,width=200)
settingsFrame.pack_propagate(False)
settingsFrame.pack(side='left',fill='both',padx=5,pady=5)
contentFrame = ttk.Frame(borderwidth=1,relief='solid',master=mainframe,height=680,width=500)
contentFrame.pack_propagate(False)
contentFrame.pack(side='right',fill='both',padx=5,pady=5)

##Checkboxes
armorCheckbox = ttk.Checkbutton(master = settingsFrame,text = 'Броня',onvalue=True,offvalue=False,padding=5,variable=bArmor)
armorCheckbox.pack(anchor='nw')
weaponCheckbox = ttk.Checkbutton(master = settingsFrame,text = 'Оружие',onvalue=True,offvalue=False,padding=5,variable=bWeapon)
weaponCheckbox.pack(anchor='nw')
toolCheckbox = ttk.Checkbutton(master = settingsFrame,text = 'Инструменты',onvalue=True,offvalue=False,padding=5,variable=bTools)
toolCheckbox.pack(anchor='nw')
equipmentCheckbox = ttk.Checkbutton(master = settingsFrame,text = 'Снаряжение',onvalue=True,offvalue=False,padding=5,variable=bEquipment)
equipmentCheckbox.pack(anchor='nw')

#Entery
check = (root.register(CheckIfOnlyInt),'%P')
itemFrame = ttk.Frame(master=settingsFrame)
itemFrame.pack(anchor='nw',fill='x',padx=10,pady=5)
itemNumberEntry = ttk.Entry(master=itemFrame,validate='key',validatecommand=check,width=5)
itemNumberEntry.insert(0,'5')
itemNumberEntry.grid(row=0,column=0)
itemLabel = ttk.Label(master=itemFrame,text= 'Количество предметов')
itemLabel.grid(row=0,column=1)

#Coins
coinsFrame = ttk.Frame(master=settingsFrame)
copperCoinsEntry = ttk.Entry(master=coinsFrame,validate='key',validatecommand=check,width=5)
silverCoinsEntry = ttk.Entry(master=coinsFrame,validate='key',validatecommand=check,width=5)
goldCoinsEntry   = ttk.Entry(master=coinsFrame,validate='key',validatecommand=check,width=5)
copperCoinsLabel = ttk.Label(master=coinsFrame,text='мм')
silverCoinsLabel = ttk.Label(master=coinsFrame,text='см')
goldCoinsLabel = ttk.Label(master=coinsFrame,text='зм')
copperCoinsEntry.insert(0,'0')
silverCoinsEntry.insert(0,'0')
goldCoinsEntry.insert(0,'100')

costtextLabel = ttk.Label(master=coinsFrame,text='Максимальная стоимость')
costtextLabel.grid(column=0,columnspan=3,padx=5)
goldCoinsEntry.grid(column=0,row=1,padx=5)
silverCoinsEntry.grid(column=1,row=1,padx=10)
copperCoinsEntry.grid(column=2,row=1,padx=10)
goldCoinsLabel.grid(column=0,row=2,padx=10)
silverCoinsLabel.grid(column=1,row=2,padx=10)
copperCoinsLabel.grid(column=2,row=2,padx=10)

coinsFrame.pack(anchor='nw',fill='x',padx=5,pady=5)

generateButton = ttk.Button(master=settingsFrame,text='Сгенерировать',command=GenerateCommand)
generateButton.pack(anchor='n',pady=20,padx=5)
root.mainloop()