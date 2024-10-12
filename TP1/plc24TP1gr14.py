# Problema 1 - Processador de Pessoas listadas nos Róis de Confessados

import re

# Abrir o ficheiro, 'processos.txt', e copiar as linhas
with open('processos.txt', 'r') as f:
    linhas = f.readlines()
    
# Abrir/criar o ficheiro, 'processos-filtrados.txt', escrever as linhas sem registos repetidos
with open('processos-filtrados.txt', 'w') as f:
    linhas_sem_repetidos = list(set(linhas))
    f.writelines(linhas_sem_repetidos)


# Alínea a)
def freq_processos_ano():
    anos = {} # Utilizamos um dicionário para armazenar os anos e a sua frequência
    
    for linha in linhas_sem_repetidos:
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
    
    for linha in linhas_sem_repetidos:
        # Extrair o ano e calcular o século
        processo_ano = re.search(r'(\d{4})(\-)', linha)
        if processo_ano:
            ano = int(processo_ano.group(1))
            seculo = (ano // 100) + 1
    
        # Inicializar o século no dicionário se ainda não estiver presente
        if seculo not in seculos:
            seculos[seculo] = {'nomes_proprios': {}, 'apelidos': {}}
    
        # Extrair os nomes do Confessado, pai e mãe
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

    for linha in linhas_sem_repetidos:
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

    for linha in linhas_sem_repetidos:
        # Partir a linha em partes
        partes = linha.split("::")
        if len(partes) > 4:
            pai = partes[3]  # Nome do pai
            mae = partes[4]  # Nome da mãe
            pais = (pai, mae)  # Combinação do pai e da mãe como chave

            # Incrementar a contagem de filhos confessados para o par de pais
            if pais in pais_frequencia:
                pais_frequencia[pais] += 1
            else:
                pais_frequencia[pais] = 1

    # Filtrar para encontrar os pais com mais do que 1 Filho Confessado
    pais_com_mais_de_um_filho = {pais: freq for pais, freq in pais_frequencia.items() if freq > 1}

    return pais_com_mais_de_um_filho


# Alínea e)
import json

def imprimir_primeiro_registo_json():
    # Extrair o primeiro registro
    primeiro_registo = linhas_sem_repetidos[0]
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
    with open('primeiro_registo.json', 'w') as f:
        json.dump(registo_dict, f, indent=4, ensure_ascii=False)
        
imprimir_primeiro_registo_json()

