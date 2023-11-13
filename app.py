import requests
import csv
import json
from bs4 import BeautifulSoup

def scrape_quotes(url, output_format='print'):
    try:
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('span', class_='text')

        if not quotes:
            print("No quotes found on the page.")
            return

        if output_format == 'print':
            for index, quote in enumerate(quotes, start=1):
                print(f"Quote #{index}: {quote.get_text(strip=True)}\n")
        elif output_format == 'csv':
            save_quotes_to_csv(quotes)
        elif output_format == 'json':
            save_quotes_to_json(quotes)
        else:
            print("Invalid output format. Supported formats: print, csv, json.")

    except requests.RequestException as e:
        print(f"Error during request: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def save_quotes_to_csv(quotes):
    with open('quotes.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Quote']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for quote in quotes:
            writer.writerow({'Quote': quote.get_text(strip=True)})

    print("Quotes saved to quotes.csv")

def save_quotes_to_json(quotes):
    quotes_list = [quote.get_text(strip=True) for quote in quotes]
    with open('quotes.json', 'w', encoding='utf-8') as jsonfile:
        json.dump({'Quotes': quotes_list}, jsonfile, ensure_ascii=False, indent=2)

    print("Quotes saved to quotes.json")

if __name__ == "__main__":
    scrape_quotes('http://quotes.toscrape.com', output_format='json')
