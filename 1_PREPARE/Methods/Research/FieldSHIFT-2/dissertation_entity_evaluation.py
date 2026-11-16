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

def evaluate_dissertation(dissertation_content: str, evaluator_name: str, entity_content: str, llm_params: Dict[str, Any]) -> str:
    """
    Evaluate the dissertation content from the perspective of the given evaluator.

    Args:
        dissertation_content (str): The content of the dissertation to be evaluated.
        evaluator_name (str): The name of the evaluator.
        entity_content (str): The content of the Entity.py file.
        llm_params (Dict[str, Any]): LLM parameters from config.

    Returns:
        str: The evaluated dissertation content.
    """
    logger.info(f"Evaluating dissertation from the perspective of {evaluator_name}...")

    # Replace {evaluator_name} with the content of Entity.py
    dissertation_content = dissertation_content.replace("{evaluator_name}", entity_content)

    # Define the prompt template
    prompt_template = """
    You are an expert in your field with a unique cognitive model, set of stances, and worldview. Please provide a detailed, comprehensive evaluation of the following PhD dissertation. Your evaluation should be long, coherent, relevant, and structured. Importantly, incorporate your specific perspective and expertise throughout the evaluation. Use the following guidelines:

    1. Introduction (200-300 words):
       - Briefly summarize the dissertation's main topic and research questions.
       - State your overall impression of the work, drawing on your specific expertise and worldview.

    2. Strengths (500-700 words):
       - Identify at least 5 major strengths of the dissertation.
       - For each strength, provide a specific example or quote from the dissertation, using exact quotations.
       - Explain why each strength is significant in the context of the field, relating it to your own cognitive model and stances.
       - Where relevant, juxtapose the dissertation's strengths with your own perspective or quotes from your own work or other literature in the field.

    3. Weaknesses (500-700 words):
       - Identify at least 5 areas for improvement or weaknesses in the dissertation.
       - For each weakness, provide a specific example or quote from the dissertation, using exact quotations.
       - Explain why each weakness is a concern from your unique perspective and how it could be addressed.
       - Where appropriate, contrast the dissertation's weaknesses with alternative approaches or viewpoints from your own work or expertise.

    4. Contribution to the Field (400-500 words):
       - Assess the overall contribution of this dissertation to the field, viewed through the lens of your specific expertise and worldview.
       - Compare and contrast the dissertation's findings or approach with existing literature, your own perspective, and your cognitive model.
       - Use exact quotes from the dissertation and juxtapose them with relevant quotes from your own work or other sources that align with your expertise.

    5. Methodology and Data Analysis (300-400 words):
       - Evaluate the appropriateness and rigor of the research methodology, drawing on your specific methodological expertise.
       - Comment on the data analysis techniques used, their effectiveness, and any limitations, relating to your own preferred approaches or critiques.
       - Provide specific examples or quotes from the dissertation to illustrate your points.

    6. Writing and Structure (200-300 words):
       - Assess the overall quality of writing, clarity, and organization of the dissertation.
       - Comment on the use of citations, figures, and tables if applicable, relating to your own standards and practices in academic writing.

    7. Recommendations for Improvement (300-400 words):
       - Provide specific, actionable recommendations for improving the dissertation, based on your unique perspective and expertise.
       - Explain how these improvements would enhance the overall quality and impact of the work, drawing on your cognitive model and worldview.
       - Where possible, provide examples or quotes from your own work or relevant literature to support your recommendations.

    8. Conclusion (200-300 words):
       - Summarize your evaluation, reiterating the main strengths and areas for improvement.
       - Provide a final assessment of the dissertation's contribution to the field and its potential impact, viewed through the lens of your specific expertise and worldview.

    9. Collaboration Opportunities Between Us (200-300 words):
       - Identify potential areas for collaboration between you and the author of the dissertation.
       - Explain how your unique expertise and perspective could complement the author's work.
       - Provide specific examples or ideas for collaborative projects or research.

    10. Other Collaboration Opportunities for You (200-300 words):
       - Suggest other potential collaborators or research groups that could benefit from the author's work.
       - Explain how these collaborations could enhance the impact and reach of the dissertation.
       - Provide specific examples or ideas for collaborative projects or research with these other entities.

    Throughout your evaluation, use exact quotations from the dissertation to support your points. Consistently juxtapose these with your own perspective, cognitive model, and quotes from your own work or relevant literature in the field. Ensure that your evaluation is balanced, constructive, and provides specific examples to support your assessment while clearly demonstrating your unique stance and expertise. Make it a comprehensive Markdown bulletpoint document with subsections for maximum clarity.

    Here is your worldview and cognitive model:
    {evaluator_name},

    Dissertation Content:
    {dissertation_content}

    Do it:
    """

    try:
        prompt = prompt_template.format(evaluator_name=evaluator_name, dissertation_content=dissertation_content)
        evaluation = generate_llm_response(prompt, llm_params)
        logger.info(f"Dissertation evaluated from the perspective of {evaluator_name} successfully.")
        return evaluation
    except Exception as e:
        logger.error(f"Error evaluating dissertation from the perspective of {evaluator_name}: {str(e)}")
        raise

def process_dissertation_evaluation(input_dir: str, output_base_dir: str, llm_params: Dict[str, Any]):
    """
    Process the evaluation of dissertations for all files in the input directory from multiple evaluators.

    Args:
        input_dir (str): Directory containing input files with existing dissertations.
        output_base_dir (str): Base directory to save the evaluated dissertations.
        llm_params (Dict[str, Any]): LLM parameters from config.
    """
    try:
        # Discover paths; read descriptions only for missing outputs.
        evaluator_paths = []
        entity_dir = os.path.join(os.path.dirname(__file__), '../Fonds/Entity')
        for root, dirs, files in os.walk(entity_dir):
            for file in files:
                if file.endswith('.py'):
                    module_path = os.path.join(root, file)
                    evaluator_name = os.path.splitext(file)[0]
                    evaluator_paths.append((evaluator_name, module_path))
                    logger.info(f"Discovered evaluator module: {file}")

        evaluator_contents = {}
        for input_file in os.listdir(input_dir):
            if input_file.endswith(".md"):
                input_file_path = os.path.join(input_dir, input_file)
                
                for evaluator_name, evaluator_path in evaluator_paths:
                    # Prepare the output directory and file name
                    output_dir = os.path.join(output_base_dir, f"Evaluated_by_{evaluator_name}")
                    os.makedirs(output_dir, exist_ok=True)
                    output_file_name = f"{os.path.splitext(input_file)[0]}_evaluated_by_{evaluator_name}.md"
                    output_file_path = os.path.join(output_dir, output_file_name)
                    
                    # Skip if the evaluated file already exists
                    if os.path.exists(output_file_path):
                        continue
                    
                    if evaluator_path not in evaluator_contents:
                        with open(evaluator_path, 'r') as source:
                            evaluator_contents[evaluator_path] = source.read()
                    description = evaluator_contents[evaluator_path]
                    # Load the existing dissertation content
                    dissertation_content = load_file(input_file_path)
                    
                    # Evaluate the dissertation
                    start_time = time.time()
                    evaluated_dissertation = evaluate_dissertation(dissertation_content, evaluator_name, description, llm_params)
                    end_time = time.time()
                    elapsed_time = end_time - start_time
                    logger.info(f"Dissertation evaluated by {evaluator_name} in {elapsed_time:.2f} seconds.")
                    
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
    output_base_dir = "/home/tet/Documents/Github/Active_InferAnts/ActiveInferAnts/1_PREPARE/Methods/Research/FieldSHIFT-2/Inputs_and_Outputs/Evaluated_Dissertations"
    
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