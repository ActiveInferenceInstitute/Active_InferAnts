import logging
import os
from typing import List
from utils import load_file, save_file
from config import DEFAULT_CONFIG, SCRIPT_DIR
from itertools import product

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def generate_pro_shift_domains(domain_a: str, domain_b: str, prompt: str) -> str:
    """
    Generate a concatenated domain by combining two domains with a prompt.

    Args:
        domain_a (str): Content of the first domain.
        domain_b (str): Content of the second domain.
        prompt (str): Prompt template for generating concatenated domain.

    Returns:
        str: The concatenated domain content.
    """
    logger.info("Generating concatenated domain")
    concatenated_content = f"""
{prompt}

DOMAIN A:
{domain_a}

DOMAIN B:
{domain_b}

Now apply the Field Shift from Domain A to Domain B
"""
    return concatenated_content

def generate_concatenated_domains(domains: List[str], prompt: str, output_dir: str) -> None:
    """
    Generate concatenated domains for all combinations of two domains.

    Args:
        domains (List[str]): List of domain file paths.
        prompt (str): Prompt template for generating concatenated domains.
        output_dir (str): Directory to save the concatenated domains.
    """
    os.makedirs(output_dir, exist_ok=True)
    total_combinations = len(domains) ** 2
    completed_combinations = 0

    for domain_a, domain_b in product(domains, repeat=2):
        domain_a_name = os.path.splitext(os.path.basename(domain_a))[0]
        domain_b_name = os.path.splitext(os.path.basename(domain_b))[0]
        output_filename = f'concatenated_{domain_a_name}_to_{domain_b_name}.md'
        output_path = os.path.join(output_dir, output_filename)
        if os.path.exists(output_path):
            logger.info(f"Output already exists; preserving {output_path}")
            continue
        logger.info(f"Processing combination: {domain_a_name} and {domain_b_name}")
        
        domain_a_content = load_file(domain_a)
        domain_b_content = load_file(domain_b)
        
        concatenated_content = generate_pro_shift_domains(domain_a_content, domain_b_content, prompt)
        
        save_file(concatenated_content, output_path)
        
        logger.info(f"Concatenated domain saved as: {output_filename}")
        completed_combinations += 1
        logger.info(f"Completed {completed_combinations}/{total_combinations} combinations")

def process_domains(config: dict = DEFAULT_CONFIG) -> None:
    """
    Process domains using the provided configuration.

    Args:
        config (dict): Configuration dictionary.
    """
    try:
        logger.info("Starting domain processing")
        
        # Update the base directory for all input/output operations
        base_dir = os.path.join(SCRIPT_DIR, 'Inputs_and_Outputs')
        
        # Update input and output directories
        config['output_dirs'] = {
            'Domain': os.path.join(base_dir, 'Domain'),
            'Concatenated_Domain': os.path.join(base_dir, 'Pro-Shifted_Domain')  # Ensure correct output directory
        }
        
        input_domain_dir = config['output_dirs']['Domain']
        logger.info(f"Loading domains from: {input_domain_dir}")
        
        # Load domain contents
        domain_files = [os.path.join(input_domain_dir, f) for f in os.listdir(input_domain_dir) if f.endswith('.md')]

        logger.info("Domains loaded successfully")
        logger.info("Starting concatenation process")

        output_dir = config['output_dirs']['Concatenated_Domain']
        if any(
            not os.path.exists(os.path.join(
                output_dir,
                f"concatenated_{os.path.splitext(os.path.basename(a))[0]}_to_{os.path.splitext(os.path.basename(b))[0]}.md",
            ))
            for a, b in product(domain_files, repeat=2)
        ):
            prompt_path = os.path.join(base_dir, 'Prompts', 'FieldSHIFT-2-Domain_Shift.md')
            prompt = load_file(prompt_path)
            generate_concatenated_domains(domain_files, prompt, output_dir)

        logger.info("Concatenation process completed successfully.")
        print(f"\n{'='*50}\nConcatenation process summary:\n{'-'*50}")
        print(f"Total domains processed: {len(domain_files)}")
        print(f"Output directory: {config['output_dirs']['Concatenated_Domain']}")
        print(f"{'='*50}\n")
    except Exception as e:
        logger.error(f"Error in process_domains: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting script execution")
    process_domains()
    logger.info("Script execution completed")