from dotenv import load_dotenv
import pandas as pd
from tqdm import tqdm
import multiprocessing
import os
import requests

def env_load():
    load_dotenv()
    return os.environ['ACCESS_TOKEN']

def genius(search_term, access_token, per_page=15):
    try:
        genius_search_url = f"http://api.genius.com/search?q={search_term}&" + \
                            f"access_token={access_token}&per_page={per_page}"

        response = requests.get(genius_search_url)
        json_data = response.json()

    except Exception as e:
        print(e)
    return json_data['response']['hits']

def genius_to_df(search_term, access_token, n_results_per_term=10):
    try:
        print(f"Processing iteration for item: {search_term} in process {os.getpid()}")
        json_data = genius(search_term, access_token, per_page=n_results_per_term)
        hits = [hit['result'] for hit in json_data]
        df = pd.DataFrame(hits)

        # expand dictionary elements
        df_stats = df['stats'].apply(pd.Series)
        df_stats.rename(columns={c:'stat_' + c for c in df_stats.columns},
                        inplace=True)
        
        df_primary = df['primary_artist'].apply(pd.Series)
        df_primary.rename(columns={c:'primary_artist_' + c for c in df_primary.columns},
                        inplace=True)
        
        df = pd.concat((df, df_stats, df_primary), axis=1)
        return df
    except Exception as e:
        print(e)

def process_wrapper(queue, access_token, item):
    try:
        result = genius_to_df(item, access_token)
        queue.put(result)
    except Exception as e:
        print(f"Error in process {os.getpid()} for item {item}: {e}")

def save_to_csv(df_list):
    res_df = pd.concat(df_list)
    res_df.to_csv('genius_output.csv', index=False, header=True)
    return

# def process_iteration(iteration):
#     # Your iteration processing code goes here
#     print(f"Processing iteration {iteration} in process {os.getpid()}")

if __name__ == "__main__":

    dfs = []
    processes = []
    result_queue = multiprocessing.Queue()

    try:
        access_token = env_load()
        search_terms = ['Shadows of Intent', 'Cigarettes After Sex', 'The 1975', 'Slowdive', 'Deftones', 'Loathe', 'Joji', 'Invent Animate', 'Currents', 'Ne Obliviscaris']

        for item in tqdm(search_terms):
            process = multiprocessing.Process(target=process_wrapper, args=(result_queue, access_token, item))
            processes.append(process)
            process.start()

        for process in processes:
            print("process join")
            process.join(timeout=30)   

        df_list = []
        
        while not result_queue.empty():
            df_list.append(result_queue.get())

        
        save_to_csv(df_list)
         
    except Exception as e:
        print(e)