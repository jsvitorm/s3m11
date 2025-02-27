import os
import time
from supabase import create_client, Client
from prometheus_client import start_http_server, Gauge, Counter

# Definição das métricas
BUCKET_SIZE = Gauge('supabase_bucket_size_bytes', 'Tamanho total do bucket em bytes', ['bucket_name'])
BUCKET_FILE_COUNT = Gauge('supabase_bucket_file_count', 'Número de arquivos no bucket', ['bucket_name'])
BUCKET_ERRORS = Counter('supabase_bucket_errors_total', 'Número de erros ao coletar métricas', ['bucket_name', 'error_type'])

SUPABASE_URL = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY_BOLADONA')
BUCKET_NAME = os.getenv('BUCKET_NAME')

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def get_bucket_metrics():
    try:
        files = supabase.storage.from_(BUCKET_NAME).list()
        
        if not files or not isinstance(files, list):
            print("Erro: Resposta inválida ao listar arquivos")
            BUCKET_ERRORS.labels(bucket_name=BUCKET_NAME, error_type='invalid_response').inc()
            return
        
        print(files)

        total_size = sum(file['metadata'].get('size', 0) for file in files if 'metadata' in file)

        print(f"Tamanho total: {total_size} bytes, Número de arquivos: {len(files)}")

        BUCKET_SIZE.labels(bucket_name=BUCKET_NAME).set(total_size)
        BUCKET_FILE_COUNT.labels(bucket_name=BUCKET_NAME).set(len(files))

    except Exception as e:
        print(f"Erro ao coletar métricas: {str(e)}")
        BUCKET_ERRORS.labels(bucket_name=BUCKET_NAME, error_type='exception').inc()

def main():
    start_http_server(8000)  
    while True:
        get_bucket_metrics()
        time.sleep(5) 

if __name__ == "__main__":
    main()