import requests

def request_links_in_json_from_substack(domain = "astralcodexten", link_path = "canonical_url"):
    HEADERS = {
        'Content-Type': 'application/json',
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0"
    }
    url = f"https://{domain}.substack.com/api/v1/archive"
    offset = 0
    limit = 12
    flag = True
    
    link_list = []
    while flag or response.ok:
        flag = False # Poor man's Do While
        params = {
            'sort': 'new',
            'search': '',
            'offset': str(offset),
            'limit': str(limit)
        }

        response = requests.get(url, headers=HEADERS, params=params)
        r = response.json()
        if len(r) < 1:
            break
        links = [r[i][link_path] for i in range(len(r))]
        link_list = *link_list, *links
        offset += limit
    return link_list