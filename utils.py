import pandas as pd
import csv
import io

class Utils:
    """
    A utility class for handling expense-related operations such as extracting expense strings,
    parsing CSV files to expenses, and saving expenses to CSV files.
    """

    @staticmethod
    def extract_expenses_string(s):
        """
        Extracts the first JSON-like expense string from a given input string.

        Args:
            s (str): The input string containing the expense data.

        Returns:
            str: The extracted expense string in JSON format.
        """
        # Find the start index of the first '{'
        start_index = s.find('{')
        # Find the end index of the first '}'
        end_index = s.find('}', start_index) + 1
        # Extract the expense string using the identified indices
        expenses_str = s[start_index:end_index]
        return expenses_str


    @staticmethod
    def parse_csv_to_expenses(csv_file):
        """
        Parses a CSV file to sum up expenses by category.

        Args:
            csv_file (FileStorage): The CSV file containing expense data.

        Returns:
            dict: A dictionary with expense categories as keys and the sum of expenses as values.
        """
        # Read the CSV file into a DataFrame
        df = pd.read_csv(csv_file)
        # Sum the expenses for each category and convert to dictionary
        expenses = df.sum(axis=0).to_dict()
        return expenses

    @staticmethod
    def save_expenses_to_csv(expenses_dict):
        """
        Saves a dictionary of expenses to a CSV file in memory.

        Args:
            expenses_dict (dict): A dictionary with expense categories as keys and expense amounts as values.

        Returns:
            BytesIO: An in-memory CSV file with the expense data.
        """
        # Create a CSV file in memory
        output = io.StringIO()
        # Initialize CSV writer
        writer = csv.writer(output)
        
        # Write header to the CSV file
        writer.writerow(['Category', 'Amount'])
        
        # Write data to the CSV file
        for category, amount in expenses_dict.items():
            writer.writerow([category, amount])
        
        # Get the CSV data as a string
        csv_data = output.getvalue()
        
        # Convert the CSV data to bytes
        output_bytes = io.BytesIO(csv_data.encode('utf-8'))
        
        # Seek to the beginning of the BytesIO object to prepare for reading
        output_bytes.seek(0)
        
        return output_bytes