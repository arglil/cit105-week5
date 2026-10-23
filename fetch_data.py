

import argparse
import requests

API_URL = "https://geocoding-api.open-meteo.com/v1/search"


def fetch_data(city, url=API_URL, timeout=5):
    """Retrieve city information and handle API failures."""
    try:
        response = requests.get(
            url,
            params={"name": city, "count": 1},
            timeout=timeout
        )

        # Check HTTP status before reading the response.
        if response.status_code == 404:
            return None, "The API endpoint was not found (404)."

        if 500 <= response.status_code <= 599:
            return None, "The weather service is unavailable. Try again later."

        if response.status_code != 200:
            return None, (
                f"The service returned HTTP {response.status_code}. "
                "Please try again."
            )

        try:
            data = response.json()
        except ValueError:
            return None, "The service returned invalid JSON data."

        if not isinstance(data, dict):
            return None, "The service returned an unexpected response."

        results = data.get("results")

        if not isinstance(results, list) or not results:
            return None, "No matching city was found."

        if not isinstance(results[0], dict):
            return None, "The city information was invalid."

        return results[0], None

    except requests.exceptions.Timeout:
        return None, "The service took too long to respond. Please try again."

    except requests.exceptions.ConnectionError:
        return None, (
            "Could not reach the service. "
            "Check your internet connection and try again."
        )

    except requests.exceptions.RequestException:
        return None, "A network request failed. Please try again."


def format_data(city):
    """Format city data without making any network requests."""
    fields = [
        ("City", city.get("name") or "Unknown"),
        ("State", city.get("admin1") or "Unknown"),
        ("Country", city.get("country") or "Unknown"),
        ("Population", (
            f"{city['population']:,}"
            if isinstance(city.get("population"), int)
            else "Unknown"
        )),
        ("Latitude", city.get("latitude")),
        ("Longitude", city.get("longitude")),
        ("Time Zone", city.get("timezone") or "Unknown"),
    ]

    lines = [
        "=" * 45,
        "CITY INFORMATION",
        "=" * 45
    ]

    for label, value in fields:
        if value is None:
            value = "Unknown"
        lines.append(f"{label:<15}: {value}")

    lines.append("=" * 45)
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", default=API_URL)
    parser.add_argument("--timeout", type=float, default=5)
    args = parser.parse_args()

    city = input("Enter a city name: ").strip()

    if not city:
        print("Please enter a city name.")
        return

    data, error = fetch_data(
        city,
        url=args.url,
        timeout=args.timeout
    )

    if error:
        print(error)
    else:
        print(format_data(data))


if __name__ == "__main__":
    main()
