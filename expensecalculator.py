from langchain_huggingface import HuggingFaceEndpoint
from langchain.prompts import PromptTemplate
from utils import Utils

class ExpenseCalculator:
    """
    A class for calculating adjusted expenses based on a savings goal using Hugging Face models.
    """

    def __init__(self, model_name, huggingfacehub_api_token):
        """
        Initialize the ExpenseCalculator with a HuggingFace model and prompt template.

        Args:
            model_name (str): The Hugging Face model repository ID.
            huggingfacehub_api_token (str): The API token for accessing the Hugging Face model.

        Attributes:
            model_name (str): The Hugging Face model repository ID.
            huggingfacehub_api_token (str): The API token for accessing the Hugging Face model.
            hub_llm (HuggingFaceEndpoint): Endpoint for interacting with the Hugging Face model.
            prompt (PromptTemplate): Template for defining the prompt used to calculate expenses.
        """
        self.model_name = model_name
        self.huggingfacehub_api_token = huggingfacehub_api_token
        
        # Initialize the HuggingFace model endpoint
        self.hub_llm = HuggingFaceEndpoint(
            repo_id=self.model_name,
            huggingfacehub_api_token=self.huggingfacehub_api_token,
            max_new_tokens=100,
            temperature=0.5,
        )
        
        # Define the prompt template
        self.prompt = PromptTemplate(
            input_variables=['expenses', 'savings_goal', 'excluded_categories'],
            template="""
            Create a savings plan based on monthly expenses where the user wants to save a specified percentage of their total expenses, excluding {excluded_categories} from adjustment but including it in the total expense calculation.

            Given:

            Monthly expenses: {expenses}
            Savings goal: {savings_goal}%
            Calculate:

            The total amount the user should save per month.
            Adjust the expenses proportionally, excluding {excluded_categories}, to meet the savings goal.
            Provide the updated expenses in JSON format after adjustment.

            Example:
            If expenses are:
            {expenses}
            And the savings goal is {savings_goal}%, the adjusted expenses should reflect proportional reductions in the expenses categories while {excluded_categories} remain unchanged in the JSON format.

            The updated expenses as follows:
            """
        )

    def calculate_expenses(self, expenses, savings_goal, excluded_categories):
        """
        Calculate adjusted expenses based on input parameters using the HuggingFace model.

        Args:
            expenses (dict): A dictionary of monthly expenses with category names as keys and amounts as values.
            savings_goal (float): The percentage of total expenses the user wants to save.
            excluded_categories (str): A string specifying the category to exclude from adjustment.

        Returns:
            str: A JSON-like string representation of the adjusted expenses.
        """
        # Initialize the chain with prompt and HuggingFace model
        hub_chain = self.prompt | self.hub_llm
        
        # Invoke the chain with provided input
        response = hub_chain.invoke({
            "expenses": expenses,
            "savings_goal": savings_goal,
            "excluded_categories": excluded_categories
        })
        
        # Extract and return the expenses string
        return Utils.extract_expenses_string(response)
    
    def extract_adjusted_expenses(self, csv_file, savings_goal, excluded_categories):
        """
        Extracts and adjusts expenses based on a savings goal and excluded categories from a CSV file,
        then saves the adjusted expenses to a new CSV file.

        Args:
            csv_file (FileStorage): The CSV file containing the initial expense data.
            savings_goal (float): The percentage of total expenses the user wants to save.
            excluded_categories (str): A string specifying the category to exclude from adjustment.

        Returns:
            BytesIO: An in-memory CSV file with the adjusted expense data.

        Example:
            csv_file = open('expenses.csv', 'r')
            savings_goal = 20
            excluded_categories = "Entertainment"
            csv_output = extract_adjusted_expenses(csv_file, savings_goal, excluded_categories)
        """
        # Parse the CSV file to get the initial expenses as a dictionary
        expenses = Utils.parse_csv_to_expenses(csv_file)
        
        # Calculate the adjusted expenses based on the savings goal and excluded categories
        adjusted_expenses_str = self.calculate_expenses(expenses, savings_goal, excluded_categories)
        # Convert the adjusted expenses string to a dictionary
        adjusted_expenses_dict = eval(adjusted_expenses_str)
        
        # Save the adjusted expenses dictionary to a CSV file in memory
        csv_output = Utils.save_expenses_to_csv(adjusted_expenses_dict)
        
        return csv_output