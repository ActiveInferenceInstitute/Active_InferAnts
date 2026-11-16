import logging
import os
import time
from typing import Dict, Any, List
from utils import generate_llm_response, save_file, load_file
from config import DEFAULT_CONFIG
from dotenv import load_dotenv
import openai
import importlib.util

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger('FieldSHIFT-2')

def get_api_key():
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        key_file_path = os.path.join(os.path.dirname(__file__), 'LLM_keys.key')
        if os.path.exists(key_file_path):
            with open(key_file, 'r') as key_file:
                for line in key_file:
                    if line.startswith('OPENAI_API_KEY'):
                        api_key = line.split('=')[1].strip()
                        break
    
    if api_key:
        logger.info(f"API key found: {api_key[:5]}...{api_key[-5:]}")
    else:
        logger.error("No API key found")
    
    return api_key

def evaluate_dissertation(dissertation_content: str, grant_summary: str, llm_params: Dict[str, Any]) -> str:
    """
    Evaluate the dissertation content from the perspective of grant relevance.

    Args:
        dissertation_content (str): The content of the dissertation to be evaluated.
        grant_summary (str): The content of the grant summary file.
        llm_params (Dict[str, Any]): LLM parameters from config.

    Returns:
        str: The evaluated dissertation content.
    """
    logger.info("Evaluating dissertation for grant relevance...")

    # Define the prompt template
    prompt_template = """
    You are an expert grant reviewer tasked with evaluating a PhD dissertation for its relevance to a specific grant. Please provide a detailed, comprehensive evaluation of the dissertation's relevance to the grant. Use the following guidelines:

    1. Introduction (200-300 words):
       - Briefly summarize the dissertation's main topic and research questions.
       - State your overall impression of the work in the context of the grant's objectives.
       - Review the key overall mission of your organization & your clearest top-line summary for if/how/whether the dissertation aligns (including being honest if it is not relevant). 

    2. Relevance to Grant (500-700 words):
       - Assess the dissertation's relevance to the grant's focus areas and objectives.
       - Provide specific examples or quotes from the dissertation that align with the grant's goals.
       - Use quantitative measures such as funding/relevance percentiles to evaluate the alignment.

    3. Anticipatory Grant Reviewer Feedback (500-700 words):
       - Provide feedback from six perspectives ranging from strongly positive to strongly negative.
       - For each perspective, include specific examples or quotes from the dissertation.
       - Explain the rationale behind each perspective, considering the grant's criteria and objectives.

    4. Contribution to the Field (400-500 words):
       - Assess the overall contribution of the dissertation to the field, viewed through the lens of the grant's objectives.
       - Compare and contrast the dissertation's findings or approach with the grant's focus areas.
       - Use exact quotes from the dissertation and juxtapose them with relevant quotes from the grant summary.

    5. Methodology and Data Analysis (300-400 words):
       - Evaluate the appropriateness and rigor of the research methodology in the context of the grant's requirements.
       - Comment on the data analysis techniques used, their effectiveness, and any limitations.
       - Provide specific examples or quotes from the dissertation to illustrate your points.

    6. Writing and Structure (200-300 words):
       - Assess the overall quality of writing, clarity, and organization of the dissertation.
       - Comment on the use of citations, figures, and tables if applicable, relating to the grant's standards and practices.

    7. Recommendations for Improvement (300-400 words):
       - Provide specific, actionable recommendations for improving the dissertation to better align with the grant's objectives.
       - Explain how these improvements would enhance the overall quality and impact of the work.
       - Where possible, provide examples or quotes from the grant summary to support your recommendations.

    8. Conclusion (200-300 words):
       - Summarize your evaluation, reiterating the main strengths and areas for improvement.
       - Provide a final assessment of the dissertation's relevance to the grant and its potential impact.

    Throughout your evaluation, use exact quotations from the dissertation to support your points. Consistently juxtapose these with the grant's objectives and quotes from the grant summary. Ensure that your evaluation is balanced, constructive, and provides specific examples to support your assessment while clearly demonstrating the dissertation's relevance to the grant. Make it a comprehensive Markdown bulletpoint document with subsections for maximum clarity.

    Grant Summary:
    {grant_summary}

    Dissertation Content:
    {dissertation_content}

    Do it:
    """

    try:
        prompt = prompt_template.format(grant_summary=grant_summary, dissertation_content=dissertation_content)
        evaluation = generate_llm_response(prompt, llm_params)
        logger.info("Dissertation evaluated for grant relevance successfully.")
        return evaluation
    except Exception as e:
        logger.error(f"Error evaluating dissertation for grant relevance: {str(e)}")
        raise

def process_dissertation_evaluation(input_dir: str, output_base_dir: str, llm_params: Dict[str, Any]):
    """
    Process the evaluation of dissertations for all files in the input directory from multiple grant perspectives.

    Args:
        input_dir (str): Directory containing input files with existing dissertations.
        output_base_dir (str): Base directory to save the evaluated dissertations.
        llm_params (Dict[str, Any]): LLM parameters from config.
    """
    try:
        # Discover paths; read descriptions only for missing outputs.
        grant_paths = []
        grant_dir = os.path.join(os.path.dirname(__file__), '../Fonds/Summarized_Grants')
        for root, dirs, files in os.walk(grant_dir):
            for file in files:
                if file.endswith('.md'):
                    grant_path = os.path.join(root, file)
                    grant_name = os.path.splitext(file)[0]
                    grant_paths.append((grant_name, grant_path))
                    logger.info(f"Discovered grant summary: {file}")

        grant_contents = {}
        for input_file in os.listdir(input_dir):
            if input_file.endswith(".md"):
                input_file_path = os.path.join(input_dir, input_file)
                
                for grant_name, grant_path in grant_paths:
                    # Prepare the output directory and file name
                    output_dir = os.path.join(output_base_dir, f"Evaluated_for_{grant_name}")
                    os.makedirs(output_dir, exist_ok=True)
                    output_file_name = f"{os.path.splitext(input_file)[0]}_evaluated_for_{grant_name}.md"
                    output_file_path = os.path.join(output_dir, output_file_name)
                    
                    # Skip if the evaluated file already exists
                    if os.path.exists(output_file_path):
                        continue
                    
                    if grant_path not in grant_contents:
                        with open(grant_path, 'r') as source:
                            grant_contents[grant_path] = source.read()
                    description = grant_contents[grant_path]
                    # Load the existing dissertation content
                    dissertation_content = load_file(input_file_path)
                    
                    # Evaluate the dissertation
                    start_time = time.time()
                    evaluated_dissertation = evaluate_dissertation(dissertation_content, description, llm_params)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    logger.info(f"Dissertation evaluated for {grant_name} in {elapsed_time:.2f} seconds.")
                    
                    # Ensure evaluated dissertation is a string
                    if isinstance(evaluated_dissertation, tuple):
                        evaluated_dissertation = ' '.join(map(str, evaluated_dissertation))

                    # Save the evaluated dissertation to a Markdown file
                    with open(output_file_path, 'w') as f:
                        f.write(evaluated_dissertation)
                    
                    logger.info(f"Evaluated dissertation saved: {output_file_name}")

        logger.info("Dissertation evaluation process completed successfully.")
    except Exception as e:
        logger.error(f"Error in process_dissertation_evaluation: {str(e)}")
        raise

if __name__ == "__main__":
    logger.info("Starting script execution")
    
    # Define the input directory and output directory
    input_dir = "/home/tet/Documents/Github/Active_InferAnts/ActiveInferAnts/1_PREPARE/Methods/Research/FieldSHIFT-2/Inputs_and_Outputs/Shifted_Dissertations_Improved_Once"
    output_base_dir = "/home/tet/Documents/Github/Active_InferAnts/ActiveInferAnts/1_PREPARE/Methods/Research/FieldSHIFT-2/Inputs_and_Outputs/Dissertation_Grant_Evaluations"
    
    # Ensure the output base directory exists
    os.makedirs(output_base_dir, exist_ok=True)
    
    # Prepare LLM parameters
    api_key = get_api_key()
    if not api_key:
        raise ValueError("API key not found or invalid")
    
    # Set the API key explicitly in the OpenAI configuration
    openai.api_key = api_key
    
    llm_params = {**DEFAULT_CONFIG['llm_params'], 'api_key': api_key}
    
    try:
        # Process the dissertation evaluations
        process_dissertation_evaluation(input_dir, output_base_dir, llm_params)
    except Exception as e:
        logger.error(f"An error occurred during script execution: {str(e)}")
        raise
    
    logger.info("Script execution completed")