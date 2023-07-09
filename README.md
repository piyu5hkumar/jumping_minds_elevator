# Jumping Minds Elevator

This is a Django-based elevator system that provides functionality for managing elevators and user requests.

## Table of Contents

- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Features

- Create and manage elevators
- Create and manage user requests
- Track elevator movements and user requests in real-time using Redis
- Retrieve elevator and user request information through REST APIs

## Requirements

- Python 3.11.4
- Django 4.2.3
- Django REST Framework 3.14.0
- PostgreSQL 15.3
- Redis

## Installation

1. Clone the repository:

   ``` bash
   git clone https://github.com/piyu5hkumar/jumping_minds_elevator.git
   ```

2. Create a Python virtual environment and activate it:

   - On macOS and Linux:

     ``` bash
     python3 -m venv env
     source env/bin/activate
     ```

   - On Windows:

     ``` bash
     python -m venv env
     .\env\Scripts\activate
     ```

3. Install the dependencies using pip:

    ``` bash
    pip install -r requirements.txt
    ```

4. Configure the Django settings:
   - Create a .env file in the root directory of the project.
   - Set the required environment variables in the .env file, such as database credentials and Redis connection details.
5. Migrate the database:

    ``` bash
    python manage.py migrate
    ```

6. Run Django server

    ``` bash
    python manage.py runserver
    ```

7. Import collection
   [Postman Collection URL](https://api.postman.com/collections/23144646-6826697b-c291-4cd2-8b3a-174911dd6f5c?access_key=PMAT-01H4XXA1X59RPTV80NMQEPV0H0)

## Usage

To use the Elevator System, follow these steps:

1. Create elevators:

    - Send a POST request to /api/elevators/ with the desired number of elevators to initialize the system.

2. Create user requests:

    - Send a POST request to /api/user-requests/ with the required information, such as the elevator number and requested floor.

3. View elevator information:

    - Send a GET request to /api/elevators/ to retrieve a list of all elevators and their details.

4. View user request information:

    - Send a GET request to /api/user-requests/ to retrieve a list of all user requests and their details.

5. Move an elevator:
   - Send a POST request to /api/elevators/<elevator_number>/move_elevator/

## Contributing

Contributions to the Elevator System are welcome! If you find any issues or have suggestions for improvements, please feel free to open an issue or submit a pull request.

When contributing to this repository, please first discuss the changes you wish to make by opening an issue. This will help in coordinating efforts and ensuring that your work aligns with the project's goals.
