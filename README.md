# Drink API

A simple FastAPI application that interacts with a MongoDB database to provide drink-related data. It allows users to query drinks, ingredients, and glasses, either by name or dynamically.

## Features

- Fetch all drinks, ingredients, or glasses from the MongoDB database.
- Search for drinks, ingredients, or glasses by name.
- Get details about a specific drink, ingredient, or glass by name.

## Requirements

- Python 3.7 or higher
- MongoDB database

## Installation

1. Clone the repository:

   - `git clone <repo_url>`
   - `cd <repo_directory>`

2. Install dependencies:

   - `pip install -r requirements.txt`

3. Create a `.env` file to store your MongoDB URL:

   - `MONGODB_URL=<your_mongodb_connection_string>`

4. Run the application:

   - `uvicorn app:app --reload`

   The app will be available at `http://127.0.0.1:8000`.

## Endpoints

### **GET** `/drinks`

Fetches a list of all drinks in the database.

### **GET** `/drinks/{name}`

Fetches a specific drink by name.

### **GET** `/drinks?name={name}`

Search for drinks that contain the name string (case-insensitive).

### **GET** `/ingredients`

Fetches a list of all ingredients in the database.

### **GET** `/ingredients/{name}`

Fetches a specific ingredient by name.

### **GET** `/ingredients?name={name}`

Search for ingredients that contain the name string (case-insensitive).

### **GET** `/glasses`

Fetches a list of all glasses in the database.

### **GET** `/glasses/{name}`

Fetches a specific glass by name.

### **GET** `/glasses?name={name}`

Search for glasses that contain the name string (case-insensitive).

## Testing

To run the tests, use `pytest`:

- `pytest`

Make sure your `.env` file is configured with the MongoDB URL, and your database is running before testing.
