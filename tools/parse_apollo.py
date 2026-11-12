#!/usr/bin/env python3
"""Parse persisted Apollo search result JSON into the pool CSV.
Usage: parse_apollo.py <category> <json_file> [<json_file> ...]
Appends rows to people/pool/pool.csv, skipping apollo_ids already present."""
import csv, json, sys, os

POOL = os.path.join(os.path.dirname(__file__), '..', 'people', 'pool', 'pool.csv')

def rows_from(path):
    with open(path) as f:
        data = json.load(f)
    if isinstance(data, list):  # [{"type":"text","text":"{...}"}]
        payload = json.loads(data[0]['text'])
    else:
        payload = data
    return payload.get('people', [])

def main():
    category, files = sys.argv[1], sys.argv[2:]
    existing = set()
    with open(POOL) as f:
        for r in csv.DictReader(f):
            existing.add(r['apollo_id'])
    added = 0
    with open(POOL, 'a', newline='') as f:
        w = csv.writer(f)
        for path in files:
            for p in rows_from(path):
                pid = p.get('id', '')
                if not pid or pid in existing:
                    continue
                existing.add(pid)
                w.writerow([
                    category,
                    p.get('first_name', ''),
                    p.get('last_name_obfuscated', ''),
                    p.get('title', ''),
                    (p.get('organization') or {}).get('name', ''),
                    pid,
                ])
                added += 1
    print(f'{category}: +{added} rows (total ids seen: {len(existing)})')

if __name__ == '__main__':
    main()
