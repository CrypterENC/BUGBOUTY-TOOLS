import requests

def certificate_transparency(target, output_folder=None):
    """
    Perform certificate transparency enumeration using crt.sh.
    Returns a list of unique subdomains.
    """
    subs = set()
    try:
        url = f"https://crt.sh/?q=%25.{target}&output=json"
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            data = response.json()
            for item in data:
                name = item.get('name_value', '')
                name = name.replace('*.', '')
                if name and '.' in name:
                    subs.add(name)
        else:
            print(f"[-] crt.sh request failed with status {response.status_code}")
    except requests.RequestException as e:
        print(f"[-] Error fetching from crt.sh: {e}")
    return list(subs)
