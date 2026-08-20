from src.services.ingestion.engine import process_all_files

def run(event=None): return process_all_files((event or {}).get('source_folder','.github/artifacts'))
