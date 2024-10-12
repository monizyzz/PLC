import csv
import re
from tabulate import tabulate
import json
import os

csv_file = 'emd.csv'
csv_string = ''

with open(csv_file, mode='r', encoding="utf-8") as file:
    csv_string = file.read().split('\n')
    
fullTableData = [row.split(",") for row in csv_string]
headers = fullTableData[0]
rowsData = fullTableData[1:]

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


# e) Ajudar a normalizar as colunas do Nome, visto que o ficheiro original está inconsistente:
patternNames = r'^[^,]*,[^,]*,[^,]*,([^,]*),([^,]*)'

names = []


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
        gender = matchGender[-1]
        
        if gender == 'M':
            male += 1

            # e) Ajudar a normalizar as colunas do Nome, visto que o ficheiro original está inconsistente:
            matchNames = re.search(patternNames, line)
            if matchNames:
                names.append(matchNames.groups())

        
        elif gender == 'F':
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


# e) Ajudar a normalizar as colunas do Nome, visto que o ficheiro original está inconsistente:
jsonData = []

for name in names:
    jsonData.append({ 'firstName': name[0], 'lastName': name[1] })
    

outputFolderName = 'output'
os.makedirs(outputFolderName, exist_ok=True)

with open("./output/output.json", "w") as json_file:
    json.dump(jsonData, json_file, indent=4)  # indent=4 for pretty printing
    
    
    
htmlContent = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Output HTML File</title>
    <style>
         body {{
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        header {{
            background-color: #807e7c;
            color: white;
            padding: 20px;
            text-align: center;
            margin-bottom: 20px;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        h1 {{
            margin: 0;
            font-size: 24px;
        }}
        main {{
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            width: auto;
            margin: auto;
        }}
        p {{
            font-size: 18px;
            margin: 10px 0;
        }}
        table {{
            border-collapse: collapse;
            width: auto;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }}
        th {{
            background-color: #f2f2f2;
            font-size: 16px;
            color: #333;
        }}
        td {{
            font-size: 16px;
            color: #555;
        }}
        tr:hover {{
            background-color: #f5f5f5;
        }}
        div.table-wrapper {{
            display: flex;
            gap: 40px;
            justify-content: start;
            align-items: start;
            margin-top: 20px;
        }}
        .table-wrapper div {{
            flex: none;
            width: auto;
        }}

        .visible {{
            display: flex;
            justify-content: start;
            align-items: start;
            gap: 20px;
        }}
        
        .visiblePs {{
            display: flex;
            flex-direction: column;
            justify-content: start;
            align-items: start;
        }}
        
        .invisible {{
            display: none;
        }}
        
        button {{
            margin-bottom: 10px;
        }}

    </style>
</head>
<body>
    <header>
        <h1>Output da questão 2 do trabalho de PLC</h1>
    </header>
    <button><a href="./output.json" download>Download JSON</a></button>
    <button id="toggleBtn" >Show csv file</button>
    <main>
        <div class="visiblePs" id="wrapperPs">
            <p>Pessoa mais velha nos exames médicos: {maxAge} anos</p>
            <p>Pessoa mais nova nos exames médicos: {minAge} anos</p>
            <p>Número de homens nos exames médicos: {male}</p>
            <p>Número de mulheres nos exames médicos: {female}</p>
        </div>
        
        <div class="visible" id="output">
            {tabulate(categories.items(), headers=['Modalidade', 'Atletas'], tablefmt='html')}
            {tabulate(table_data, headers=['Ano', 'Aptos', 'Não Aptos'], tablefmt='html')}
        </div>
        
        <div class="invisible" id="input"> 
            {tabulate(rowsData, headers=headers, tablefmt='html')}
        </div>
    </main>
    <script>
        const toggleBtn = document.getElementById('toggleBtn')
        const inputTable = document.getElementById('input')
        const outputTable = document.getElementById('output')
        const wrapperPs = document.getElementById('wrapperPs')
        
        toggleBtn.addEventListener('click', () => {{
            inputTable.classList.toggle('visible')
            inputTable.classList.toggle('invisible')
            outputTable.classList.toggle('visible')
            outputTable.classList.toggle('invisible')
            wrapperPs.classList.toggle('visiblePs')
            wrapperPs.classList.toggle('invisible')

            if (outputTable.classList.contains('visible')) {{
                toggleBtn.textContent = 'Show csv file'
            }} else {{
                toggleBtn.textContent = 'Show output'
            }}

        }})
    </script>
</body>
</html>'''


with open("./output/index.html", "w") as html_file:
    html_file.write(htmlContent)