from config import DEFAULT_CONFIG

import os
import json
import logging
import time
import random
from typing import Any, Dict, List, Tuple
import openai

def load_file(file_path: str) -> str:
    """
    Load the contents of a file.

    Args:
        file_path (str): Path to the file to be loaded.

    Returns:
        str: Contents of the file.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If there's an error reading the file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        raise
    except IOError as e:
        logging.error(f"Error reading file {file_path}: {str(e)}")
        raise

def save_file(content: str, file_path: str) -> None:
    """
    Save content to a file.

    Args:
        content (str): Content to be saved.
        file_path (str): Path where the file should be saved.

    Raises:
        IOError: If there's an error writing to the file.
    """
    if os.path.exists(file_path):
        logging.info(f"Output already exists; preserving {file_path}")
        return
    try:
        with open(file_path, 'x', encoding='utf-8') as file:
            file.write(content)
        
        logging.info(f"File saved successfully: {file_path}")
    except FileExistsError:
        logging.info(f"Output already exists; preserving {file_path}")
    except IOError as e:
        logging.error(f"Error writing to file {file_path}: {str(e)}")
        raise

def setup_logging(log_file: str = 'fieldshift2.log', level: int = logging.INFO) -> logging.Logger:
    """
    Set up logging for the application.

    Args:
        log_file (str): Name of the log file. Defaults to 'fieldshift2.log'.
        level (int): Logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: Configured logger object.
    """
    logger = logging.getLogger('FieldSHIFT-2')
    logger.setLevel(level)

    file_handler = logging.FileHandler(log_file)
    console_handler = logging.StreamHandler()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger

def process_text(text: str) -> str:
    """
    Process text for analysis or manipulation.

    Args:
        text (str): Input text to be processed.

    Returns:
        str: Processed text.
    """
    # Implement text processing logic here
    # This could include tokenization, lowercasing, removing punctuation, etc.
    return text.lower()

def calculate_similarity(text1: str, text2: str) -> float:
    """
    Calculate similarity between two texts.

    Args:
        text1 (str): First text for comparison.
        text2 (str): Second text for comparison.

    Returns:
        float: Similarity score between 0 and 1.
    """
    # Implement similarity calculation logic here
    # This could use techniques like cosine similarity, Jaccard similarity, etc.
    return DEFAULT_CONFIG['analysis_params']['similarity_threshold']

def chunk_text(text: str, chunk_size: int) -> List[str]:
    """
    Split text into chunks of specified size.

    Args:
        text (str): Input text to be chunked.
        chunk_size (int): Maximum size of each chunk.

    Returns:
        List[str]: List of text chunks.
    """
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

def merge_dicts(dict1: Dict, dict2: Dict) -> Dict:
    """
    Merge two dictionaries.

    Args:
        dict1 (Dict): First dictionary.
        dict2 (Dict): Second dictionary.

    Returns:
        Dict: Merged dictionary.
    """
    return {**dict1, **dict2}

def setup_llm(llm_params: Dict[str, Any] = None) -> None:
    """
    Set up the LLM with the provided API key and parameters

    Args:
        llm_params (Dict[str, Any]): LLM parameters from config
    """
    if llm_params is None:
        llm_params = DEFAULT_CONFIG['llm_params']
    openai.api_key = llm_params.get('api_key')

def generate_llm_response(prompt: str, llm_params: Dict[str, Any] = DEFAULT_CONFIG['llm_params']) -> Tuple[str, float]:
    """
    Generate a response from the LLM.

    Args:
        prompt (str): The input prompt for the LLM.
        llm_params (Dict[str, Any]): LLM parameters from config

    Returns:
        Tuple[str, float]: The generated response from the LLM and the time taken in seconds.
    """
    start_time = time.time()
    try:
        response = openai.ChatCompletion.create(
            model=llm_params.get('model'),
            messages=[{"role": "user", "content": prompt}],
            max_tokens=llm_params.get('max_tokens'),
            temperature=llm_params.get('temperature'),
            top_p=llm_params.get('top_p'),
            frequency_penalty=llm_params.get('frequency_penalty'),
            presence_penalty=llm_params.get('presence_penalty'),
            n=llm_params.get('n'),
            stream=llm_params.get('stream'),
            stop=llm_params.get('stop')
        )
        generated_response = response.choices[0].message.content.strip()
    except Exception as e:
        logging.error(f"Error generating LLM response: {str(e)}")
        raise
    finally:
        end_time = time.time()
    
    time_taken = end_time - start_time
    return generated_response, time_taken

def process_pro_shifted_domains(input_dir: str, output_dir: str, llm_params: Dict[str, Any] = DEFAULT_CONFIG['llm_params']) -> None:
    """
    Process all files in the Pro-Shifted_Domain folder, send them to LLM, and save outputs in the Shifted_Domain folder.

    Args:
        input_dir (str): Path to the Pro-Shifted_Domain folder.
        output_dir (str): Path to the Shifted_Domain folder.
        llm_params (Dict[str, Any]): LLM parameters from config.
    """
    logger = logging.getLogger('FieldSHIFT-2')
    logger.info(f"Starting to process pro-shifted domains from {input_dir}")

    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            input_path = os.path.join(input_dir, filename)
            output_filename = f"shifted_{filename}"
            output_path = os.path.join(output_dir, output_filename)
            if os.path.exists(output_path):
                logger.info(f"Output already exists; preserving {output_path}")
                continue

            logger.info(f"Processing file: {filename}")
            
            try:
                with open(input_path, 'r', encoding='utf-8') as file:
                    content = file.read()

                prompt = f"Please shift the following pro-shifted domain:\n\n{content}"
                
                shifted_content, time_taken = generate_llm_response(prompt, llm_params)
                
                save_file(shifted_content, output_path)
                
                logger.info(f"Processed {filename} in {time_taken:.2f} seconds. Output saved as {output_filename}")
            
            except Exception as e:
                logger.error(f"Error processing {filename}: {str(e)}")

    logger.info("Finished processing all pro-shifted domains")

def batch_process_llm(prompts: List[str], llm_params: Dict[str, Any] = DEFAULT_CONFIG['llm_params']) -> List[Tuple[str, float]]:
    """
    Process a batch of prompts through the LLM.

    Args:
        prompts (List[str]): List of input prompts for the LLM.
        llm_params (Dict[str, Any]): LLM parameters from config

    Returns:
        List[Tuple[str, float]]: List of generated responses from the LLM and their respective processing times.
    """
    responses = []
    for prompt in prompts:
        response, time_taken = generate_llm_response(prompt, llm_params)
        responses.append((response, time_taken))
    return responses

def get_api_key() -> str:
    """Read the OpenAI API key from the LLM_keys.key file."""
    key_file_path = os.path.join(os.path.dirname(__file__), 'LLM_keys.key')
    try:
        with open(key_file_path, 'r') as key_file:
            for line in key_file:
                if line.startswith('OPENAI_API_KEY'):
                    return line.split('=')[1].strip()
    except FileNotFoundError:
        logging.error(f"API key file not found: {key_file_path}")
    except Exception as e:
        logging.error(f"Error reading API key: {str(e)}")
    
    raise ValueError("OPENAI_API_KEY not found in LLM_keys.key file")

# Add any other utility functions that might be needed across multiple modules

def generate_transition_matrix(size: int = 4) -> List[List[float]]:
    """Generate a random transition matrix with specific constraints."""
    matrix = [[0.0 for _ in range(size)] for _ in range(size)]
    
    # First state (empowered) always transitions to itself
    matrix[0][0] = 1.0
    
    # Generate transitions for states 2-4 (High/Medium/HomoSacer)
    for i in range(1, size):
        row = [random.random() for _ in range(1, size)]
        total = sum(row)
        for j in range(1, size):
            matrix[i][j] = row[j-1] / total
    
    return matrix

def generate_entity(name: str, entity_type: str) -> Dict[str, Any]:
    """Generate an entity with its properties."""
    entity = {
        "name": name,
        "type": entity_type,
        "baseline_transition_matrix": generate_transition_matrix(),
        "empowered_transition_matrix": generate_transition_matrix(),
        "subjected_transition_matrix": generate_transition_matrix(),
    }
    
    if entity_type == "narrative":
        entity["influence"] = random.uniform(0.1, 1.0)
    elif entity_type == "demos":
        entity["vulnerability"] = random.uniform(0.1, 1.0)
    
    return entity

def generate_entity_library() -> Dict[str, Any]:
    """Generate the complete entity library."""
    narratives = [
        "Narrative_1a",
        "Narrative_1b",
        "Narrative_2a",
        "Narrative_2b",
        "Narrative_3a",
        "Narrative_3b",
    ]
    
    demos = [
        "demo_1a",
        "demo_1b",
        "demo_2a",
        "demo_2b",
        "demo_3a",
        "demo_3b",
    ]
    
    library = {
        "entities": [
            generate_entity(narrative, "narrative") for narrative in narratives
        ] + [
            generate_entity(demo, "demos") for demo in demos
        ]
    }
    return library

def save_entity_library(library: Dict[str, Any], filename: str):
    """Save the entity library to a JSON file."""
    if os.path.exists(filename):
        logging.info(f"Output already exists; preserving {filename}")
        return
    parent = os.path.dirname(filename)
    if parent:
        os.makedirs(parent, exist_ok=True)
    try:
        with open(filename, 'x') as f:
            json.dump(library, f, indent=2)
    except FileExistsError:
        return
    logging.info(f"Entity library saved to {filename}")