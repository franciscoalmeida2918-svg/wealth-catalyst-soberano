import spacy
from fuzzywuzzy import fuzz
import requests
from datetime import datetime

# Carregar o modelo de linguagem do spaCy
nlp = spacy.load("pt_core_news_sm")

# Função para correção de erros de digitação usando fuzzywuzzy
def corrigir_erro(entrada, termos_possiveis):
    melhores_correspondencias = [(termo, fuzz.ratio(entrada, termo)) for termo in termos_possiveis]
    melhores_correspondencias = sorted(melhores_correspondencias, key=lambda x: x[1], reverse=True)
    termo_corrigido = melhores_correspondencias[0][0]
    return termo_corrigido

# Função para buscar a taxa SELIC atual da API do Banco Central
def buscar_taxa_selic():
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json&dataInicial=01/01/2023"
    resposta = requests.get(url)
    dados = resposta.json()
    taxa_selic_mais_recente = dados[-1]["valor"]
    return float(taxa_selic_mais_recente.replace(",", "."))

# Função para calcular o valor futuro de um investimento
def calcular_valor_futuro(valor_investido, taxa_juros, anos):
    taxa_juros_mensal = (taxa_juros / 100) / 12
    meses = anos * 12
    valor_futuro = valor_investido * ((1 + taxa_juros_mensal) ** meses)
    return valor_futuro

# Função para processar a pergunta
def processar_pergunta(pergunta):
    pergunta = pergunta.lower()

    # Definindo as palavras-chave e termos financeiros possíveis
    termos_investimento = ['tesouro direto', 'ações', 'fundos imobiliários', 'renda fixa', 'selic', 'inflação', 'aporte']
    termos_taxa = ['taxa de juros', 'selic', 'rentabilidade', 'rendimentos', 'inflacao']

    # Correção de erro de digitação se necessário
    termos_possiveis = termos_investimento + termos_taxa
    for termo in termos_possiveis:
        if fuzz.ratio(pergunta, termo) > 80:  # Se a correspondência for alta, sugerir correção
            pergunta = pergunta.replace(termo, corrigir_erro(pergunta, [termo]))
    
    # Usando spaCy para entender as intenções e entidades da pergunta
    doc = nlp(pergunta)
    intenções = []
    entidades = []
    
    for token in doc:
        if token.pos_ == "NOUN":  # Detectando possíveis entidades financeiras
            entidades.append(token.text)
        if token.pos_ == "VERB":  # Detectando possíveis intenções
            intenções.append(token.text)

    # Se a pergunta for sobre a SELIC
    if any('selic' in ent for ent in entidades):
        taxa_selic = buscar_taxa_selic()
        return f"A taxa SELIC atual é de {taxa_selic}% ao ano."

    # Se a pergunta for sobre cálculos de valor futuro de um investimento
    if any('investir' in intenções or 'aporte' in intenções for ent in entidades):
        try:
            valor_investido = float(input("Qual é o valor inicial do investimento? R$ "))
            taxa_juros = float(input("Qual é a taxa de juros anual? % "))
            anos = int(input("Por quantos anos você deseja investir? "))
            valor_futuro = calcular_valor_futuro(valor_investido, taxa_juros, anos)
            return f"O valor futuro do seu investimento de R$ {valor_investido} após {anos} anos será de R$ {valor_futuro:.2f}."
        except ValueError:
            return "Desculpe, houve um erro nos valores inseridos. Tente novamente."

    return "Desculpe, não consegui entender sua pergunta. Pode reformular?"

# Função principal para interação com o usuário
def interagir_com_ia():
    print("=== Consultoria de Investimentos Financeiros ===")
    while True:
        pergunta = input("\nFaça sua pergunta sobre investimentos (ou 'sair' para encerrar): ")
        if pergunta.lower() == "sair":
            print("Até logo!")
            break
        resposta = processar_pergunta(pergunta)
        print(resposta)

if __name__ == "__main__":
    interagir_com_ia()
