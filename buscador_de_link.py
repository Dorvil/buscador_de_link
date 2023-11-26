import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urlparse

# Função para extrair os links de uma página web
def extract_links(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    # Obtém os links da página, excluindo aqueles com 'javascript:void(0)'
    links = [a['href'] for a in soup.find_all('a', href=True) if 'javascript:void(0)' not in a['href']]
    return links

def save_to_file(links, nome_arquivo):
    with open(nome_arquivo, 'w') as file:
        for link in links:
            file.write(link + '\n')

def main():
    url = input("Digite o site ou IP para iniciar o crawling: ")
    
    # Adiciona 'https://' se não estiver presente na URL
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url

    print(f"Crawling {url}")

    start_time = time.time()  # Registra o tempo de início

    links = extract_links(url)

    end_time = time.time()  # Registra o tempo de término
    elapsed_time = end_time - start_time

    if not links:
        print("Nenhum link encontrado.")
        return

    print(f"\nLinks encontrados ({len(links)} no total):")
    for link in links:
        print(link)

    # Usa o nome do site (sem "https://") para criar o nome do arquivo
    nome_site = urlparse(url).netloc.replace('www.', '').replace('.', '_')
    nome_arquivo = f"{nome_site}.txt"

    salvar_arquivo = input("\nDeseja salvar os resultados em um arquivo? (s/n): ").lower()

    if salvar_arquivo == 's':
        # Salva os links no arquivo
        save_to_file(links, nome_arquivo)
        print(f"Resultados salvos em {nome_arquivo}")

    print(f"\nQuantidade de links encontrados: {len(links)}")
    print(f"Tempo total: {elapsed_time:.2f} segundos")

if __name__ == "__main__":
    main()
