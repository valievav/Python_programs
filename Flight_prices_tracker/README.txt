FLIGHT PRICES TRACKER

PURPOSE: Return cheapest flight from the Skyskanner using custom parameters (city from/to, date etc.)

PREREQUISITES (for running on own machine):
1. Up and running MongoDB
2. Created separate db and collection for storing results (one of the parameters of the runner.py)

HOW TO RUN:
1. Open runner.py
2. Change parameters to custom if needed
3. Run main function

PROCESS FLOW:
1. Get airport city ids from city names (departure & destination)
2. Create Live Pricing Service Session (it should be created before requesting Live price data,
   more details at https://skyscanner.github.io/slate/#flights-live-prices)
3. Get results from Live API
4. Retry if process fails at any of the 3 points above
5. Record JSON from the response into MondoDB
6. Record JSON from the response into file if passed respective flag (for test purposes)
7. Repeat process for N days (pickle date in case process was interrupted, so it's possible to continue
   where it left off)
8. Find flights with price lower than threshold
