# Heritage Backend Project

## Overview
The Heritage Backend project is a Flask application designed to serve as the backend for the Heritage Horizon project. It connects to an existing frontend and provides a set of APIs to interact with the database, which is managed using SQLite.

## Project Structure
```
heritage-backend
├── src
│   ├── app.py                # Entry point of the Flask application
│   ├── config.py             # Configuration settings for the application
│   ├── api
│   │   ├── __init__.py       # Initializes the API module
│   │   └── routes.py         # Defines API endpoints
│   ├── models
│   │   ├── __init__.py       # Initializes the models module
│   │   ├── db.py             # Handles database connection and setup
│   │   └── models.py         # Defines database models
│   ├── schemas
│   │   └── schemas.py        # Defines data schemas for validation and serialization
│   └── services
│       └── auth.py           # Contains authentication-related services
├── instance
│   └── .gitkeep              # Keeps the instance directory tracked by Git
├── tests
│   └── test_api.py           # Unit tests for the API endpoints
├── requirements.txt           # Lists project dependencies
├── .env                       # Contains environment variables
├── .gitignore                 # Specifies files to ignore by Git
└── README.md                  # Documentation for the project
```

## Setup Instructions
1. **Clone the Repository**
   ```
   git clone <repository-url>
   cd heritage-backend
   ```

2. **Create a Virtual Environment**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory and set the necessary environment variables, such as database URLs and secret keys.

5. **Run the Application**
   ```
   python src/app.py
   ```

## Usage
The backend provides various API endpoints that can be accessed by the frontend. Refer to the `src/api/routes.py` file for a complete list of available endpoints and their functionalities.

## Testing
To run the unit tests for the API, execute the following command:
```
pytest tests/test_api.py
```

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.