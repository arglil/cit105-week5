

\# CIT 105 Week 5 - Public API Consumption Exercise



\## Project Overview



This Python application uses the Open-Meteo Geocoding API to retrieve information about cities around the world.



Users enter a city name, and the program displays the city's location and population information in a formatted table.



\## API Information



\- API: Open-Meteo Geocoding API

\- Endpoint: https://geocoding-api.open-meteo.com/v1/search

\- HTTP Method: GET

\- Python Library: requests

\- Authentication: No API key required



The program extracts seven fields:



1\. City

2\. State or region

3\. Country

4\. Population

5\. Latitude

6\. Longitude

7\. Time zone



Missing fields are displayed as "Unknown".



\## Installation



Install the required packages:



&#x20;   python -m pip install -r requirements.txt



\## Running the Application



Run:



&#x20;   python fetch\_data.py



Enter a city name when prompted.



\## Successful API Test



Input:



&#x20;   miami



Actual output:



&#x20;   Enter a city name: miami

&#x20;   =============================================

&#x20;   CITY INFORMATION

&#x20;   =============================================

&#x20;   City           : Miami

&#x20;   State          : Florida

&#x20;   Country        : United States

&#x20;   Population     : 487,014

&#x20;   Latitude       : 25.77427

&#x20;   Longitude      : -80.19366

&#x20;   Time Zone      : America/New\_York

&#x20;   =============================================



\## Error Handling



The program handles:



\- HTTP 404 errors

\- HTTP 500-599 server errors

\- Other unexpected HTTP status codes

\- Request timeouts

\- Connection errors

\- Invalid JSON responses

\- Missing or incomplete API data



The fetch\_data() function handles API requests, while format\_data() formats results independently.



\## Failure Modes



\### Test 1: Invalid API Endpoint (404)



Command:



&#x20;   python fetch\_data.py --url "https://geocoding-api.open-meteo.com/invalid-endpoint"



Actual output:



&#x20;   Enter a city name: miami

&#x20;   The API endpoint was not found (404).



Result: Passed. The application handled the HTTP 404 error without crashing.



\### Test 2: Network Timeout



Command:



&#x20;   python fetch\_data.py --timeout 0.000001



Actual output:



&#x20;   Enter a city name: maimi

&#x20;   The service took too long to respond. Please try again.



Result: Passed. The application handled the timeout without crashing.



\### Test 3: Simulated Connection Failure



Command:



&#x20;   python fetch\_data.py --url "http://127.0.0.1:9"



Actual output:



&#x20;   Enter a city name: miami

&#x20;   Could not reach the service. Check your internet connection and try again.



Result: Passed. The application handled a connection failure without crashing.



This test simulated an unreachable service using a local address and closed port. It did not involve physically disconnecting the computer from the internet.



\## Automated Testing



The project includes two pytest tests that use saved sample data instead of making live API requests.



Run:



&#x20;   python -m pytest -v



Tests:



\- test\_format\_data\_displays\_city\_information

\- test\_format\_data\_handles\_missing\_fields



Actual result:



&#x20;   2 passed in 0.10s



\## AI Use Disclosure



ChatGPT was used to assist with selecting the API, developing and explaining the Python code, designing offline pytest tests, troubleshooting API compatibility, and organizing the project documentation.



The application and tests were executed locally, and the results documented above were captured from actual PowerShell runs.



\## Project Files



\- fetch\_data.py - Main Python application

\- test\_fetch\_data.py - Automated tests

\- sample\_response.json - Saved sample data for offline testing

\- requirements.txt - Python dependencies

\- .gitignore - Files excluded from Git tracking

\- README.md - Project documentation



