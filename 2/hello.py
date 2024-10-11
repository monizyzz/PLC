import csv
import re

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



# 1) Calcular as Idades extremas dos registos no dataset
patternOne = r'\d+,'
maxAge = 0
minAge = 100


# 2) Calcular a distribuição por Género no total;
patternTwo = r'(M|F),'
male = 0
female = 0


for line in csv_string:
    
    # 1) Calcular as Idades extremas dos registos no dataset    
    matchAge = re.findall(patternOne, line)
    if matchAge:
        idade = int(matchAge[-1].replace(',', ''))
        maxAge = max(maxAge, idade)
        minAge = min(minAge, idade)
    
    # 2) Calcular a distribuição por Género no total;
    matchGender = re.findall(patternTwo, line)
    if matchGender:
        if matchGender[-1] == 'M':
            male += 1
        elif matchGender[-1] == 'F':
            female += 1

print(f'Max Idade: {maxAge}')
print(f'Min Idade: {minAge}')

print(f'Males: {male}')
print(f'Females: {female}')
    