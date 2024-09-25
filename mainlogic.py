from typing import Iterable, Generator
import time
import requests
from itertools import chain

# Base URL for the API and protocol used for requests
BASE_URL = "api.the-odds-api.com/v4"
PROTOCOL = "https://"

# Custom exception for general API errors
class APIException(RuntimeError):
    def __str__(self):
        return f"('{self.args[0]}', '{self.args[1].json()['message']}')"

# Custom exception for authentication errors
class AuthenticationException(APIException):
    pass

# Custom exception for rate limiting errors
class RateLimitException(APIException):
    pass

# Function to handle and raise appropriate exceptions based on response status
def fix_faulty_response(response: requests.Response):
    if response.status_code == 401:
        raise AuthenticationException("Failed to authenticate with the API. is the API key valid?", response)
    elif response.status_code == 429:
        raise RateLimitException("Encountered API rate limit.", response)
    else:
        raise APIException("Unknown issue arose while trying to access the API.", response)
    
# Function to get available sports from the API
def get_sports(key: str) -> set[str]:
    # Construct URL and parameters for the API request
    url = f"{BASE_URL}/sports/"
    escaped_url = PROTOCOL + requests.utils.quote(url)
    querystring = {"apiKey": key}

    # Make the API request
    response = requests.get(escaped_url, params=querystring)
    if not response:
        fix_faulty_response(response)

    # Extract and return the keys of available sports
    return {item["key"] for item in response.json()}

# Function to get betting odds data for a specific sport and region
def get_data(key: str, sport: str, region: str = "eu"):
    # Construct URL and parameters for the API request
    url = f"{BASE_URL}/sports/{sport}/odds/"
    escaped_url = PROTOCOL + requests.utils.quote(url)
    querystring = {
        "apiKey": key,
        "regions": region,
        "oddsFormat": "decimal",
        "dateFormat": "unix"
    }

    # Make the API request
    response = requests.get(escaped_url, params=querystring)
    if not response:
        fix_faulty_response(response)

    # Return the JSON response
    return response.json()

# Function to process betting data and yield relevant information for arbitrage
def process_data(matches: Iterable, include_started_matches: bool = True) -> Generator[dict, None, None]:
    for match in matches:
        start_time = int(match["commence_time"])
        # Skip matches that have already started if not including started matches
        if not include_started_matches and start_time < time.time():
            continue
        
        best_odd_per_outcome = {}
        # Find the best odds for each outcome across all bookmakers
        for bookmaker in match["bookmakers"]:
            bookie_name = bookmaker["title"]
            for outcome in bookmaker["markets"][0]["outcomes"]:
                outcome_name = outcome["name"]
                odd = outcome["price"]
                if outcome_name not in best_odd_per_outcome.keys() or \
                        odd > best_odd_per_outcome[outcome_name][1]:
                    best_odd_per_outcome[outcome_name] = (bookie_name, odd)

        # Calculate the total implied odds to identify potential arbitrage opportunities
        total_implied_odds = sum(1/i[1] for i in best_odd_per_outcome.values())
        match_name = f"{match['home_team']} v. {match['away_team']}"
        time_to_start = (start_time - time.time()) / 3600
        league = match["sport_key"]

        # Yield a dictionary with relevant match information and betting odds
        yield {
            "match_name": match_name,
            "match_start_time": start_time,
            "hours_to_start": time_to_start,
            "league": league,
            "best_outcome_odds": best_odd_per_outcome,
            "total_implied_odds": total_implied_odds,
        }

# Function to find and return arbitrage opportunities based on the API data
def get_arbitrage_opportunities(key: str, region: str, cutoff: float):
    sports = get_sports(key)
    data = chain.from_iterable(get_data(key, sport, region=region) for sport in sports)
    data = filter(lambda x: x != "message", data)
    results = process_data(data)
    arbitrage_opportunities = list(filter(lambda x: 0 < x["total_implied_odds"] < 1-cutoff, results))
    return arbitrage_opportunities