import json, requests, datetime
from tqdm import tqdm

adlist = json.loads(open('adlist.json', 'r').read())

domains = []
filterList = ['0.0.0.0 ', '|', '^', '\n', '(', ')', '\\', '127.0.0.1']
startFilter = ('#', '.', '!')

for id, ad in enumerate(tqdm(adlist)):
    address = ad['address']
    try:
        r = requests.get(address, timeout=10)
        if r.status_code == 200:
            for i in r.text.split('\n'):
                i = i.strip()
                if i.startswith(startFilter):
                    continue
                for filter in filterList:
                    i = i.replace(filter, '')
                domains.append(i)
    except Exception as e:
        print(f"Error: {e}")

with open('blocklist.txt', 'w+', encoding='utf-8') as adblock:
    adblock.write("# Generated by Pyenb\n")
    adblock.write("# Check out https://github.com/Pyenb\n")
    adblock.write(f"# Generated on {datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n")
    for domain in tqdm(set(domains)):
        adblock.write(f"{domain}\n")