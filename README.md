Weather Tool
============

Command-line helper for checking current temperature and wind conditions from [OpenWeather](https://openweathermap.org/).

Requirements
------------
- Python 3.13 or newer
- OpenWeather API key
- [`uv`](https://docs.astral.sh/uv/) (optional, recommended)

Get an OpenWeather API Key
--------------------------
1. Sign in or create a free account at <https://home.openweathermap.org/users/sign_up>.
2. Generate an API key from <https://home.openweathermap.org/api_keys>.
3. Copy the key value.

Create a `.env` File
--------------------
Create a file named `.env` alongside `main.py` containing:

```
API_KEY=your-openweather-api-key
```

Run the Tool
------------
- Using `uv` (recommended):

  ```
  uv run main.py
  ```

- Using standard Python:

  ```
  python -m main
  ```

Follow the prompts to fetch weather data by city or ZIP code. Enter `n` when prompted to exit.
