# About
This code represents a Python program for obtaining weather forecasts and displaying them in a pop-up window using the tkinter and tkcalendar libraries. Below is a step-by-step description of what happens in the program:

1. Importing necessary libraries:
- datetime and timedelta for date manipulation.
- requests for making HTTP requests to the API.
- tkinter and tkcalendar for creating the graphical user interface.
2. Initializing global variables:

- widthWindow sets the width of the pop-up window.
- todayDate and todayDay determine the current date and day, and set the range for requesting data.
- apiKey contains the API key for accessing the OpenWeatherMap weather service.
3. Function printResult:

- Retrieves and processes weather data for a given city and date.
- Formats the date for the request.
- Makes two requests to the OpenWeatherMap API: one for a 5-day forecast with 3-hour intervals, and another for the current weather.
- Compiles and displays information about the current weather and temperature on a graph in the pop-up window.
4. Function clearWindow:

- Clears the pop-up window of all widgets created using the grid and place methods.
5. Function chooseDate:

- Creates a calendar for the user to select a date.
- Adds a button to confirm the selected date.
- Checks if the selected date falls within the allowable range.
6. Function begin:

- Initializes the program, clears the window, and displays a welcome message.
- Adds an input field for the city name and a confirm button.
7. Function searchCity:

- Retrieves the city name entered by the user.
- Makes a request to the OpenWeatherMap API to search for the city by name.
- If the city is found, displays information about the found cities and allows the user to select the desired one.
- Once a city is selected, displays a calendar for selecting the forecast date.
8. Creating and launching the main window:

- The main window is created using Tk(), and its parameters are set.
- The begin function is called to start the program.
- The main event processing loop mainloop() is started.

The program provides a user-friendly interface for obtaining weather forecasts in the selected city and displays the results graphically.