from pathlib import Path

data_root = Path('dataset')
repos = data_root / 'repo.txt'
raw_pull_list = data_root / 'raw_pull_list'
pull_numbers = data_root / 'pull_numbers.json'
pull_detail = data_root / 'pull_detail'

suggestions_collect = data_root / 'suggestions.csv'
suggestions_labeled = data_root / 'suggestions_labeled.csv'
suggestions_processed = data_root / 'suggestions_processed.txt'

git_log = data_root / 'git_log'
historical = data_root / 'historical.csv'
stat_data = data_root / 'stat_data.csv'

participants = data_root / 'participants.json'
emails = data_root / 'emails.csv'
