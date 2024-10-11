import csv
import re
from tabulate import tabulate

# Read the CSV file
csv_file = 'emd.csv'  # Update with your actual CSV file path
csv_string = ''

with open(csv_file, mode='r', encoding="utf-8") as file:
    csv_string = file.read()
    
    
csv_string = csv_string.split('\n')

# Open the CSV file
# rows = cols

# with open(csv_file, 'r') as file:
#     for line in file:
#         rows.append(line)
    
# print(csv_string)
# print(rows[:5])        



# a) Calcular as Idades extremas dos registos no dataset
patternOne = r'\d+,'
maxAge = 0
minAge = 100


# b) Calcular a distribuição por Género no total;
patternTwo = r'(M|F),'
male = 0
female = 0

# c) Calcular a distribuição por Modalidade em cada ano e no total, devendo apresentar as Modalidades por ordem alfabética;
patternThree = r'(?:[^,]*,){8}([^,]+)'

categories = {}


# d) Calcular a percentagem de Aptos e não aptos por ano;
patternFit = r'(true|false)$'
patternDate = r'\d{4}-\d{2}-\d{2}'

years = {}


for line in csv_string:
    
    # a) Calcular as Idades extremas dos registos no dataset    
    matchAge = re.findall(patternOne, line)
    if matchAge:
        idade = int(matchAge[-1].replace(',', ''))
        maxAge = max(maxAge, idade)
        minAge = min(minAge, idade)
    
    # b) Calcular a distribuição por Género no total;
    matchGender = re.findall(patternTwo, line)
    if matchGender:
        if matchGender[-1] == 'M':
            male += 1
        elif matchGender[-1] == 'F':
            female += 1
            
    # c) Calcular a distribuição por Modalidade em cada ano e no total, devendo apresentar as Modalidades por ordem alfabética;
    matchCategory = re.findall(patternThree, line)
    if matchCategory:
        if matchCategory[0] not in categories:
            categories[matchCategory[0]] = 1

        categories[matchCategory[0]] += 1 
    
    categories = dict(sorted(categories.items(), key=lambda item: item[0]))
    
    # d) Calcular a percentagem de Aptos e não aptos por ano;
    matchFit = re.search(patternFit, line)
    matchDate = re.search(patternDate, line)
    
    if matchFit and matchDate:
        year = re.split('-', matchDate.group(0))[0]
        isFit = matchFit.group(0)

        if year not in years:
            years[year] = { 'fit': 0, 'unfit': 0 }
        
        if isFit == 'true':
            years[year]['fit'] += 1
        else:
            years[year]['unfit'] += 1
        
    
    

print(f'Max Idade: {maxAge}')
print(f'Min Idade: {minAge}')

print(f'Males: {male}')
print(f'Females: {female}')

del categories['modalidade']
print(tabulate(categories.items(), headers=['Modalidade', 'Atletas'], tablefmt='fancy_grid'))

table_data = []
for year, values in years.items():
    table_data.append([year, values['fit'], values['unfit']])

print(tabulate(table_data, headers=['Ano', 'Aptos', 'Não Aptos'], tablefmt='fancy_grid'))