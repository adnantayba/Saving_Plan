# Expense Adjustment API

## Project Overview

The Expense Adjustment API is a Flask-based web application that provides an endpoint for calculating adjusted expenses based on a user's monthly expenses, savings goal, and excluded categories. The application leverages a fine-tuned Hugging Face model to process the input data and generate adjusted expenses. Users can upload their expenses in a CSV file format, specify their savings goal, and define categories to exclude from adjustment.

## Features

- **CSV Input Handling**: Users can upload their expense data in CSV format (expense categories as columns and expense values as rows).
- **Savings Goal Calculation**: Adjust expenses to meet a specified savings goal.
- **Category Exclusion**: Exclude specific expense categories from adjustment while calculating the savings.
- **CSV Output**: Download the adjusted expenses in CSV format.

## Technologies Used

- **Python**: The core programming language for the application.
- **Flask**: A lightweight WSGI web application framework used to build the API.
- **Pandas**: A data manipulation and analysis library used for handling CSV data.
- **Hugging Face**: A platform providing state-of-the-art natural language processing models.
- **LangChain**: A library for building language model applications, used for integrating Hugging Face models.
- **dotenv**: A library for loading environment variables from a `.env` file.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/expense-adjustment-api.git
    cd expense-adjustment-api
    ```

2. **Create and activate a virtual environment**:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install the required packages**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up environment variables**:
    Create a `.env` file in the project root directory and add your Hugging Face API token and the model name:
    ```plaintext
    HUGGINGFACEHUB_API_TOKEN=your_huggingfacehub_api_token
    MODEL_NAME=`meta-llama/Meta-Llama-3-8B-Instruct`
    ```

## Usage

1. **Run the Flask application**:
    ```bash
    python app.py
    ```

2. **API Endpoint**:
    - **URL**: `/calculate_expenses`
    - **Method**: `POST`
    - **Form Data**:
        - `csv_file`: The CSV file containing the initial expense data.
        - `savings_goal`: The percentage of total expenses the user wants to save (as an integer).
        - `excluded_categories`: The category to exclude from adjustment (as a string).

3. **Example Request**:
    Use `curl` or any API testing tool (e.g., Postman) to send a request:
    ```bash
    curl -X POST http://127.0.0.1:5000/calculate_expenses \
        -F "csv_file=@path/to/your/expenses.csv" \
        -F "savings_goal=20" \
        -F "excluded_categories=Entertainment"
    ```

4. **Response**:
    - On success, the response will be a CSV file download with the adjusted expenses.
    - On failure, the response will be a JSON error message.

## File Structure

```plaintext
.
├── app.py                  # Main Flask application file
├── expensecalculator.py    # ExpenseCalculator class definition
├── utils.py                # Utility functions for expense handling
├── requirements.txt        # Required Python packages
├── .envsample              # Environment variables sample file
├── README.md               # Project documentation
