import numpy as np
import pandas as pd
from ze_package.ingestion import (
    ingest_from_pokedex_api, 
    connect_to_supabase, 
    dataframe_to_bucket,
    get_client_clickhouse,
    create_pokemon_table,
    fetch_pokemon_data,
    insert_pokemon_data
)
import os
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('NEXT_PUBLIC_SUPABASE_URL')
key = os.getenv('NEXT_PUBLIC_SUPABASE_ANON_KEY')

try:
    supabase_client = connect_to_supabase(url, key)
    data = ingest_from_pokedex_api()
    df = pd.DataFrame(data['results'])
    randomint = np.random.randint(0, 10000)
    result = dataframe_to_bucket(supabase_client, "meubocketkkk", df, f"pokemons-{randomint}.csv")

except Exception as e:
    print(f"Erro durante a execução: {str(e)}")