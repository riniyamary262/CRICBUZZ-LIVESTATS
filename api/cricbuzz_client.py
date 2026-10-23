import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from config import BASE_URL, get_api_key

def get_session():
    session = requests.Session()
    retry = Retry(total=3, backoff_factor=1, status_forcelist=[500,502,503,504])
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session

def fetch_live_matches():
    key = get_api_key()
    if not key:
        return {"error": "API key not set. Add RAPIDAPI_KEY to secrets.toml"}
    url = f"{BASE_URL}/matches/v1/live"
    headers = {"X-RapidAPI-Key": key, "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"}
    try:
        r = get_session().get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 403:
            return {
                "error": (
                    "RapidAPI denied access (403): this key is not subscribed to the "
                    "Cricbuzz Cricket API. Subscribe to the API in RapidAPI or use a "
                    "key that has an active subscription."
                )
            }
        return {"error": f"API request failed: {e}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}

def fetch_player_stats(player_id):
    key = get_api_key()
    if not key:
        return {"error": "API key not set"}
    url = f"{BASE_URL}/stats/v1/player/{player_id}/career"
    headers = {"X-RapidAPI-Key": key, "X-RapidAPI-Host": "cricbuzz-cricket.p.rapidapi.com"}
    try:
        r = get_session().get(url, headers=headers, timeout=10)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        if e.response is not None and e.response.status_code == 403:
            return {
                "error": (
                    "RapidAPI denied access (403): this key is not subscribed to the "
                    "Cricbuzz Cricket API. Subscribe to the API in RapidAPI or use a "
                    "key that has an active subscription."
                )
            }
        return {"error": f"API request failed: {e}"}
    except requests.exceptions.RequestException as e:
        return {"error": f"API request failed: {e}"}
