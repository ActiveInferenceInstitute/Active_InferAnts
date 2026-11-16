import logging
import os
import time
from dotenv import load_dotenv
import openai 
from utils import load_file, save_file, generate_llm_response
from config import USER_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def get_api_key():
    # Try to load from .env file
    load_dotenv()
    api_key = os.getenv('OPENAI_API_KEY')
    
    # If not found in .env, try to load from LLM_keys.key
    if not api_key:
        key_file_path = os.path.join(os.path.dirname(__file__), 'LLM_keys.key')
        if os.path.exists(key_file_path):
            with open(key_file_path, 'r') as key_file:
                for line in key_file:
                    if line.startswith('OPENAI_API_KEY'):
                        api_key = line.split('=')[1].strip()
                        break
    
    return api_key

def perform_domain_shift(input_file: str, output_dir: str, llm_params: dict) -> None:
    """
    Perform a domain shift on a single domain file, send it to LLM, and save the response.

    Args:
        input_file (str): Path to the input domain file.
        output_dir (str): Directory to save the shifted domain.
        llm_params (dict): Parameters for the language model.
    """
    try:
        output_file_name = os.path.basename(input_file).replace('concatenated_', 'shifted_')
        output_file_path = os.path.join(output_dir, output_file_name)
        if os.path.exists(output_file_path):
            logger.info(f"Output already exists; preserving {output_file_path}")
            return
        logger.info(f"Processing file: {input_file}")
        
        # Load domain content
        domain_content = load_file(input_file)
        
        # Set the OpenAI API key
        openai.api_key = llm_params['api_key']
        
        # Generate the shifted domain using LLM
        shifted_domain, _ = generate_llm_response(domain_content, llm_params)
        
        
        # Save the shifted domain
        save_file(shifted_domain, output_file_path)
        
        logger.info(f"Shifted domain saved: {output_file_name}")
    except Exception as e:
        logger.error(f"Error processing file {input_file}: {str(e)}")

def process_domain_shift(input_dir: str, output_dir: str, config: dict) -> None:
    """
    Process domain shifts on all domain files in the input directory using the provided configuration.

    Args:
        input_dir (str): Path to the input directory containing domain files.
        output_dir (str): Directory to save the shifted domains.
        config (dict): Configuration dictionary.
    """
    try:
        logger.info("Starting domain shift processing")
        
        llm_params = None
        
        # Iterate over all files in the input directory
        for input_file in os.listdir(input_dir):
            input_file_path = os.path.join(input_dir, input_file)
            
            # Prepare the output file name
            output_file_name = input_file.replace('concatenated_', 'shifted_')
            output_file_path = os.path.join(output_dir, output_file_name)
            
            # Check if the output file already exists
            if os.path.exists(output_file_path):
                logger.info(f"Output file already exists: {output_file_name}. Skipping LLM request.")
                print(f"Output file already exists: {output_file_name}. Skipping LLM request.")
            else:
                # Perform the domain shift
                if llm_params is None:
                    api_key = get_api_key()
                    if not api_key:
                        raise ValueError("API key not found in .env or LLM_keys.key file")
                    llm_params = {**USER_CONFIG['llm_params'], 'api_key': api_key}
                start_time = time.time()
                perform_domain_shift(input_file_path, output_dir, llm_params)
                elapsed_time = time.time() - start_time
                logger.info(f"Elapsed time for processing {input_file}: {elapsed_time:.2f} seconds")
        
        logger.info("Domain shift processing completed successfully.")
    except Exception as e:
        logger.error(f"Error in process_domain_shift: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting script execution")
    
    # Define the input directory and output directory
    input_dir = "/home/tet/Documents/Github/Active_InferAnts/ActiveInferAnts/1_PREPARE/Methods/Research/FieldSHIFT-2/Inputs_and_Outputs/Pro-Shifted_Domain"
    output_dir = "/home/tet/Documents/Github/Active_InferAnts/ActiveInferAnts/1_PREPARE/Methods/Research/FieldSHIFT-2/Inputs_and_Outputs/Shifted_Domain"
    
    # Define the base directory for configuration
    base_dir = "/home/tet/Documents/Github/Active_InferAnts/ActiveInferAnts/1_PREPARE/Methods/Research/FieldSHIFT-2"
    
    # Create a configuration dictionary
    config = {
        'base_dir': base_dir,
        'output_dirs': {
            'Shifted_Domain': output_dir
        }
    }
    
    # Process the domain shift
    process_domain_shift(input_dir, output_dir, config)
    
    logger.info("Script execution completed")