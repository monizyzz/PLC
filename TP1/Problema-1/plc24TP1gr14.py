# Problema 1 - Processador de Pessoas listadas nos Róis de Confessados

import re
import json
from tabulate import tabulate

# Abrir o ficheiro, 'processos.txt', e copiar as linhas com registos repetidos
with open('processos.txt', 'r') as f:
    linhas_com_repetidos = f.readlines()
    
# Remover linhas com registos repetidos
linhas = list(set(linhas_com_repetidos))
    
# Abrir o ficheiro, 'processos.txt', e escrever as linhas sem registos repetidos
with open('processos.txt', 'w') as f:
    f.writelines(linhas)


# Alínea a)
def freq_processos_ano():
    anos = {} # Utilizamos um dicionário para armazenar os anos e a sua frequência
    
    for linha in linhas:
        processo_ano = re.search(r'(\d{4})(\-)', linha) # Procurar o ano no formato 'xxxx-'
    
        if processo_ano != None:
            ano = processo_ano.group(1) 
    
            if ano in anos: # Se o ano já existe no dicionário 
                anos[ano] += 1 # Incrementamos a frequência
            else:
                anos[ano] = 1 # Caso contrário, adicionamos o ano ao dicionário com a frequência 1
    
    return anos

    
# Alínea b)  
def freq_processos_nome():
    seculos = {}
    
    for linha in linhas:
        # Encontrar o ano e calcular o século
        processo_ano = re.search(r'(\d{4})(\-)', linha)
        if processo_ano:
            ano = int(processo_ano.group(1))
            seculo = (ano // 100) + 1
    
        # Inicializar o século no dicionário se ainda não estiver presente
        if seculo not in seculos:
            seculos[seculo] = {'nomes_proprios': {}, 'apelidos': {}}
    
        # Encontrar os nomes do Confessado, pai e mãe
        nomes_pessoas = re.findall(r':([A-Za-z ]+):', linha)
        
        for nome_completo in nomes_pessoas:
            nomes = re.split(r'\s+', nome_completo) # Remover espaços em branco e dividir o nome completo
            
            nome_proprio = nomes[0] # Nome Próprio (o primeiro em cada nome)
            apelido = nomes[-1] # Apelido (o último em cada nome)
            
            # Atualizar a frequência do nome próprio
            if nome_proprio in seculos[seculo]['nomes_proprios']:
                seculos[seculo]['nomes_proprios'][nome_proprio] += 1
            else:
                seculos[seculo]['nomes_proprios'][nome_proprio] = 1
            
            # Atualizar a frequência do apelido
            if apelido in seculos[seculo]['apelidos']:
                seculos[seculo]['apelidos'][apelido] += 1
            else:
                seculos[seculo]['apelidos'][apelido] = 1
    
    return seculos


# Alínea c)
def freq_processos_recomendados_por_tio():
    freq_tios = {}

    for linha in linhas:
        # Partir a linha em partes
        partes = linha.split("::")
        if len(partes) > 5:
            num_proc = partes[0] # Número do processo
            observacoes = partes[5] # Observações
            # Verificar se "Tio" ou "Tios" estão presentes nas observações
            if re.search(r'(\bTio\b|\bTios\b)', observacoes):
                if num_proc in freq_tios:
                    freq_tios[num_proc] += 1
                else:
                    freq_tios[num_proc] = 1

    return freq_tios


# Alínea d)
def pais_com_mais_de_um_filho():
    pais_frequencia = {}

    for linha in linhas:
        # Partir a linha em partes
        partes = linha.split("::")
        if len(partes) > 4:
            pai = partes[3]  # Nome do pai
            mae = partes[4]  # Nome da mãe
            
            # Verificar se os nomes do pai e da mãe não estão vazios
            if pai and mae:
                pais = (pai, mae)  # Combinação do pai e da mãe como chave

                # Incrementar a frequência de filhos confessados para o par de pais
                if pais in pais_frequencia:
                    pais_frequencia[pais] += 1
                else:
                    pais_frequencia[pais] = 1

    # Filtrar para encontrar os pais com mais do que 1 Filho Confessado
    pais_com_mais_de_um_filho = {pais: freq for pais, freq in pais_frequencia.items() if freq > 1}

    return pais_com_mais_de_um_filho


# Alínea e)
def imprimir_primeiro_registo_json():
    # Encontrar o primeiro registro
    primeiro_registo = linhas[0]
    partes = primeiro_registo.split("::")
    
    registo_dict = {
        "Processo": partes[0],
        "Data": partes[1],
        "Confessado": partes[2],
        "Pai": partes[3],
        "Mãe": partes[4],
        "Observações": partes[5] if partes[5] else "Não existem"
    }
    
    # Converter o dicionário para JSON e escrever no 'primeiro_registo.json'
    with open('primeiro-registo.json', 'w') as f:
        json.dump(registo_dict, f, indent=4, ensure_ascii=False)
        
imprimir_primeiro_registo_json()



def criar_pagina_html():
    # Chamar as funções para obter os resultados das alíneas
    resultado_a = freq_processos_ano()
    resultado_b = freq_processos_nome()
    resultado_c = freq_processos_recomendados_por_tio()
    resultado_d = pais_com_mais_de_um_filho()
    
    # Ler os dados do arquivo JSON criado
    with open('primeiro-registo.json', 'r') as f:
        resultado_e = json.load(f)
    
    
    # Criar a tabela a)
    anos = list(resultado_a.keys())
    frequencias = list(resultado_a.values())
    colunas = 10 
    
    tabela_a = "<table><tr>" + "".join(["<th>Ano</th><th>Frequência</th>"] * colunas) + "</tr>"
    
    for i in range(0, len(anos), colunas):
        tabela_a += "<tr>"
        for j in range(colunas):
            if i + j < len(anos):
                tabela_a += f"<td>{anos[i + j]}</td><td>{frequencias[i + j]}</td>"
            else:
                tabela_a += "<td></td><td></td>"
        tabela_a += "</tr>"
    tabela_a += "</table>"
    

    # Criar a tabela b)
    tabela_b = tabulate(resultado_b.items(), headers=["Séc.", "Frequência Dos Nomes Próprios e Apelidos"], tablefmt="html")
    
    
    # Criar a tabela c)
    processos = list(resultado_c.keys())
    frequencias_c = list(resultado_c.values())
    colunas = 8
    
    tabela_c = "<table><tr>" + "".join(["<th>Nº Processo</th><th>Frequência</th>"] * colunas) + "</tr>"
    
    for i in range(0, len(processos), colunas):
        tabela_c += "<tr>"
        for j in range(colunas):
            if i + j < len(processos):
                tabela_c += f"<td>{processos[i + j]}</td><td>{frequencias_c[i + j]}</td>"
            else:
                tabela_c += "<td></td><td></td>"
        tabela_c += "</tr>"
    tabela_c += "</table>"    
    
    
    # Criar a tabela d)
    pais = list(resultado_d.keys())
    num_filhos = list(resultado_d.values())
    colunas = 8

    tabela_d = "<table><tr>" + "".join(["<th>Pais</th><th>Nº Filhos</th>"] * colunas) + "</tr>"

    for i in range(0, len(pais), colunas):
        tabela_d += "<tr>"
        for j in range(colunas):
            if i + j < len(pais):
                tabela_d += f"<td style='font-size: smaller; width: 150px;'>{pais[i + j]}</td><td style='width: 50px;'>{num_filhos[i + j]}</td>"
            else:
                tabela_d += "<td style='font-size: smaller; width: 150px;'></td><td style='width: 50px;'></td>"
        tabela_d += "</tr>"
    tabela_d += "</table>"   
     
    # Estrutura do HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="pt">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Resultados do Processador</title>
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
        </style>
    </head>
    <body>
        <header>
            <h1>Output do Problema 1 do TP1 de PLC</h1>
        </header>
        <main>
            <h2>a) Frequência de Processos por ano</h2>
            {tabela_a}
            <h2>b) Frequência de Nomes Próprios e Apelidos por séculos, do Confessado, do seu pai e da sua mãe</h2>
            {tabela_b}
            <h2>c) Frequência de processos que são Recomendados por, pelo menos, um Tio</h2>
            {tabela_c}
            <h2>d) Todos os Pais que tenham mais do que 1 Filho Confessado</h2>
            {tabela_d}
            <h2>e) Primeiro Registo</h2>
            <ul>
                <li><strong>Processo:</strong> {resultado_e['Processo']}</li>
                <li><strong>Data:</strong> {resultado_e['Data']}</li>
                <li><strong>Confessado:</strong> {resultado_e['Confessado']}</li>
                <li><strong>Pai:</strong> {resultado_e['Pai']}</li>
                <li><strong>Mãe:</strong> {resultado_e['Mãe']}</li>
                <li><strong>Observações:</strong> {resultado_e['Observações']}</li>
            </ul>
        </main>
    </body>
    </html>
    """
    
    # Escrever o HTML no ficheiro 'index.html'
    with open('index.html', 'w') as f:
        f.write(html_content)

criar_pagina_html()