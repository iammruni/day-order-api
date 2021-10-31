# Day Order REST API
## Context
My college, SRM-IST, has a system in place to decide the schedule of the courses. One key factor in that is the Day Order. Day Order is a number ranging from 1-5. The schedules for these day orders is pre decided and each day a day order number is displayed (ascending order) on the college website and the students follow the schedule for that particular day order. To check what day order it is today, one has to login to the website using credentials. I automated this process by using the browser automation framework, Selenium. For the sake of it, I decided that I should now create an API for the same. A HIGHLY inefficient method, but to get me started with Flask API, it's okay.

# How It Works
_Not an in depth explanation_
`flask_api.py` is the main file that needs to be run to start the app. It initializes the app, the endpoints and defines the get and post methods.
`api_key.py` is the backend to **generate**, **save** and **verify** the API Keys. It uses the `encrypt` function of the `sha256_crypt` class from `passlib` library.
## The API Keys
The API Key can be any string. It has a permissions integer associated with it. Permissions: 1 = GET; 2 = POST; 3 = GET and POST; 0 = BLACKLIST
The keys are hashed using SHA256 and stored.