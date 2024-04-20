## SuperAngles FastAPI Project

This project is built with FastAPI to provide an API that interfaces with the Gemini model for natural language generation and executes SQL queries against a MySQL database. It's designed to handle incoming questions, generate responses using Gemini, and fetch relevant data from the database.

### Features

- **Gemini Integration**: Utilizes the Gemini model from Google's Generative AI to generate natural language responses based on prompts and questions.
- **SQL Query Execution**: Executes SQL queries against a MySQL database to fetch and return data based on the Gemini response.
- **CORS Middleware**: Handles CORS (Cross-Origin Resource Sharing) to allow requests from any origin.
- **Environment Variables**: Uses environment variables to store sensitive information and configurations.
- **Validation**: Validates incoming request data using Pydantic models.

### Setup and Installation

#### Prerequisites

- Python 3.8 or higher
- MySQL database
- Google API key for Gemini

#### Installation Steps

1. **Clone the repository**

    ```
    git clone https://github.com/yourusername/superangles-fastapi.git
    cd superangles-fastapi
    ```

2. **Install dependencies**

    ```
    pip install -r requirements.txt
    ```

3. **Environment Variables**

    Create a `.env` file in the root directory and add the following:

    ```
    GOOGLE_API_KEY=your_google_api_key
    ```

    Replace `your_google_api_key` with your actual Google API key.

4. **MySQL Configuration**

    Update the MySQL connection details in the `execute_sql_query` function:

    ```
    host="your_host_address",
    user="your_username",
    password="your_password",
    database="your_database_name"
    ```

### Running the Application

Run the following command to start the FastAPI application:

uvicorn main:app --reload

shell
Copy code

The application will be accessible at `http://127.0.0.1:8000`.

### API Endpoints

#### POST `/ask_question/`

- **Request Body**: 
{
"question": "Your question here"
}



- **Response**: 
{
"data": [
{
"0": "value1",
"1": "value2",
...
},
...
]
}



### Contributing

Contributions are welcome! Please follow the [Contributing Guidelines](CONTRIBUTING.md) for this project.

### License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) f