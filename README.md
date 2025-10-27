Weather Tool
============

Interactive command-line helper for checking the current temperature and wind conditions using the [OpenWeather](https://openweathermap.org/) APIs.

Features
--------
- Prompts for a city name or ZIP/postal code and resolves the best match automatically.
- Retrieves current conditions from OpenWeather and shows temperature in Fahrenheit plus the reported wind status.
- Falls back to Zippopotam.us for postal-code lookups when a state or country name is supplied.
- Gracefully handles missing data and guides you through another lookup or exit.

Requirements
------------
- Python 3.13 or newer
- OpenWeather API key
- [`uv`](https://docs.astral.sh/uv/) (optional but recommended for dependency management)

Install Dependencies
--------------------
- Using `uv` (recommended):

  ```
  uv sync
  ```

- Using standard Python tooling:

  ```
  python -m venv .venv
  source .venv/bin/activate
  pip install .
  ```

Configure the API Key
---------------------
1. Sign in or create a free OpenWeather account at <https://home.openweathermap.org/users/sign_up>.
2. Generate an API key from <https://home.openweathermap.org/api_keys>.
3. Create a `.env` file in the project root (next to `main.py`) containing:

   ```
   API_KEY=your-openweather-api-key
   ```

   Alternatively, export `API_KEY` in your shell environment before running the tool.

Run the Tool
------------
- Using `uv` (runs inside the environment you synced with `uv sync`):

  ```
  uv run main.py
  ```

- Using standard Python:

  ```
  python -m main
  ```

Example Session
---------------
```
Would you like to get weather information? [y/n]: y
Great! Please enter city name like 'San Francisco' or zip code like '95014': 94040
The temperature in Mountain View (94040) is 65 degrees Fahrenheit.
The wind status in Mountain View (94040) is(are) light breeze.
Would you like to get weather information? [y/n]: n
Ok! Shutting Down...
```

Troubleshooting
---------------
- `Missing environment variable: API_KEY`: confirm the `.env` file exists or export `API_KEY` before running.
- `Unable to resolve city/ZIP`: verify your input is correct; for non-US cities include the country (e.g., `Paris,FR`).
- Network errors: re-run the command after verifying your internet connection.
