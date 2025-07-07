import requests
import csv

def scrape_remoteok_jobs(keyword):
    url = "https://remoteok.com/api"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error al acceder a Remote OK. Código: {response.status_code}")
        return

    try:
        data = response.json()
    except Exception as e:
        print("Error al decodificar JSON:", e)
        return

    # Filtrar trabajos por palabra clave
    jobs = [
        job for job in data
        if isinstance(job, dict) and keyword.lower() in job.get('position', '').lower()
    ]

    print(f"{len(jobs)} trabajos encontrados que contienen '{keyword}'.")

    with open('remoteok_jobs.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Título', 'Empresa', 'Ubicación', 'URL'])

        for job in jobs:
            writer.writerow([
                job.get('position', 'Sin título'),
                job.get('company', 'Sin empresa'),
                job.get('location', 'Remoto'),
                f"https://remoteok.com{job.get('url', '')}"
            ])

    print("Archivo 'remoteok_jobs.csv' generado correctamente.")

if __name__ == "__main__":
    keyword = input("Buscar trabajos remotos de: ")
    scrape_remoteok_jobs(keyword)


