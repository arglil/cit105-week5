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

### Network Timeout and Connection Errors

**Test 1: Network Timeout**

The request timeout was set to a very small value.

```text
Enter a city name: maimi
The service took too long to respond. Please try again.
```

**Test 2: No Network (Wi-Fi Disconnected)**

Wi-Fi was disconnected before running the application.

```text
Enter a city name: miami
Could not reach the service. Check your internet connection and try again.
```



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



\## Assignment 2 – Structured Prompt Script


### Project Purpose

The Structured Prompt Script extracts invoice line items from unstructured text and converts them into a Python list of dictionaries. It is designed as a backend component for the Unified Business Hub capstone.

### Required JSON Schema

The AI response must be a JSON array. Every item must contain exactly these four fields:

| Field | Type | Validation |
|---|---|---|
| `item_name` | String | Non-empty |
| `quantity` | Number | Greater than 0 |
| `unit` | String | `each`, `box`, `case`, `pack`, `kg`, `lb`, or `liter` |
| `unit_price` | Number | Greater than or equal to 0 |

Example valid response:

```json
[
  {
    "item_name": "Bottled Water",
    "quantity": 3,
    "unit": "case",
    "unit_price": 12.50
  }
]
```

### Full Structured Prompt

The following is the current prompt used in `extract.py`:

```text
Extract invoice line items from the text provided.

Return a JSON array of objects. Every object must have exactly
these four keys:

- item_name: non-empty string
- quantity: positive number greater than zero
- unit: one of "each", "box", "case", "pack", "kg", "lb", "liter"
- unit_price: number greater than or equal to zero

Use the singular unit name. Do not invent missing prices,
quantities, or items. If an item cannot be represented with
all four required fields, omit it.

Return [] if there are no valid invoice items.

Do not include a preamble, explanation, markdown code fence,
comments, or any text outside the JSON array.
```

The prompt and validation rules should be reviewed and revised by the student before final submission, as required by the assignment.

### Environment Configuration

The application reads three environment variables:

- `AI_API_KEY` — API authentication key
- `AI_API_URL` — OpenAI-compatible chat completions endpoint
- `AI_MODEL` — Model identifier

The `.env.example` file documents these names without containing credentials. Actual secrets must not be committed to GitHub.

In PowerShell, once valid course credentials are available, the variables can be configured for the current session:

```powershell
$env:AI_API_KEY = "YOUR_COURSE_API_KEY"
$env:AI_API_URL = "YOUR_COURSE_API_ENDPOINT"
$env:AI_MODEL = "YOUR_COURSE_MODEL"
```

The values above are placeholders, not functioning credentials. The application reads operating-system environment variables directly; it does not automatically load a `.env` file.

### Offline Parser Testing

Run:

```powershell
python -m pytest test_extract.py -v
```

Seven parser tests passed during local testing, as reported by the student. The tests cover clean JSON, Markdown fences, introductory text, missing JSON, truncated JSON, invalid units, and missing fields.

The live API integration was not tested because course credentials and provider information were unavailable.


\### API Access and Testing Limitation



The `extract.py` application was developed to convert unstructured invoice text into structured JSON data for the Unified Business Hub capstone project.



The application includes environment-variable configuration, structured prompting, JSON extraction, schema validation, HTTP error handling, timeout handling, and token-usage reporting.



\*\*Live API testing was not performed\*\* because the course API credentials, provider information, and model configuration were not provided.



Instead, the parser was tested locally using saved AI response strings. These tests do not require an API connection or consume tokens.



Seven parser tests passed, as observed during local testing. The live API integration remains unverified.



\### Model Output Observations



The test cases demonstrate that AI-generated responses may contain Markdown code fences, introductory text, incomplete JSON, or values that violate the required schema. The parser is designed to handle these cases without crashing.



These are simulated response scenarios, not observations from a live AI model.



\### AI Assistance Disclosure



ChatGPT assisted with the Python implementation, parser design, test examples, debugging guidance, and documentation. The invoice extraction schema was reviewed and approved by the student. The prompt wording should be independently reviewed and revised by the student before submission.

