import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_file

from expensecalculator import ExpenseCalculator

# Load environment variables from .env file
load_dotenv()

# Ensure you have the huggingface_hub_api_token set in your .env file
huggingfacehub_api_token = os.getenv('HUGGINGFACEHUB_API_TOKEN')
# Initialize ExpenseCalculator instance
model_name = os.getenv('MODEL_NAME')
expense_calculator = ExpenseCalculator(model_name, huggingfacehub_api_token)

# Create Flask app
app = Flask(__name__)

@app.route('/calculate_expenses', methods=['POST'])
def calculate_expenses():
    """
    Endpoint to calculate adjusted expenses based on input CSV file, savings goal, and excluded categories.

    The endpoint expects a POST request with the following form data:
    - csv_file: The CSV file containing the initial expense data.
    - savings_goal: The percentage of total expenses the user wants to save (as an integer).
    - excluded_categories: The category to exclude from adjustment (as a string).

    Returns:
        Response: A CSV file with the adjusted expenses, or a JSON error message.
    """
    if 'csv_file' not in request.files:
        return jsonify({"error": "CSV file not provided"}), 400

    csv_file = request.files['csv_file']
    savings_goal = request.form.get('savings_goal', type=int)
    excluded_categories = request.form.get('excluded_categories')

    if savings_goal is None or not excluded_categories:
        return jsonify({"error": "Invalid input"}), 400

    try:
        csv_output = expense_calculator.extract_adjusted_expenses(csv_file, savings_goal, excluded_categories)
        return send_file(csv_output, mimetype='text/csv', download_name='adjusted_expenses.csv', as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)