import os
import json
import logging
from typing import List, Dict, Any
from textstat import textstat
from nltk.tokenize import word_tokenize
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from utils import load_file, save_file, process_text
from config import DEFAULT_CONFIG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def calculate_lexical_diversity(text: str) -> float:
    words = word_tokenize(text.lower())
    return len(set(words)) / len(words)

def calculate_sentiment(text: str) -> Dict[str, float]:
    analyzer = SentimentIntensityAnalyzer()
    return analyzer.polarity_scores(text)

def calculate_readability(text: str) -> Dict[str, float]:
    return {
        'flesch_reading_ease': textstat.flesch_reading_ease(text),
        'flesch_kincaid_grade': textstat.flesch_kincaid_grade(text),
        'gunning_fog': textstat.gunning_fog(text),
        'smog_index': textstat.smog_index(text),
        'automated_readability_index': textstat.automated_readability_index(text),
        'coleman_liau_index': textstat.coleman_liau_index(text),
        'linsear_write_formula': textstat.linsear_write_formula(text),
        'dale_chall_readability_score': textstat.dale_chall_readability_score(text)
    }

def perform_pca_analysis(features: List[float], output_dir: str, filename: str) -> None:
    pca_plot_path = os.path.join(output_dir, f'{filename}_pca.png')
    if os.path.exists(pca_plot_path):
        return
    logger.info(f"Performing PCA analysis for {filename}")
    pca = PCA(n_components=2)
    principal_components = pca.fit_transform(features)
    
    plt.figure()
    plt.scatter(principal_components[:, 0], principal_components[:, 1])
    plt.title(f'PCA of {filename}')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    
    plt.savefig(pca_plot_path)
    logger.info(f"PCA plot saved to {pca_plot_path}")

def analyze_text(text: str, analysis_params: Dict[str, Any]) -> Dict[str, Any]:
    logger.info("Analyzing text")
    processed_text = process_text(text)
    results = {}

    if 'lexical_diversity' in analysis_params['linguistic_features']:
        results['lexical_diversity'] = calculate_lexical_diversity(processed_text)
        logger.info("Calculated lexical diversity")

    if 'sentiment' in analysis_params['linguistic_features']:
        results['sentiment'] = calculate_sentiment(processed_text)
        logger.info("Calculated sentiment")

    if 'readability' in analysis_params['linguistic_features']:
        results['readability'] = calculate_readability(processed_text)
        logger.info("Calculated readability")

    return results

def perform_linguistic_analysis(input_dir: str, output_dir: str) -> None:
    analysis_path = os.path.join(output_dir, 'analysis.json')
    pca_path = os.path.join(output_dir, f'{os.path.basename(input_dir)}_pca.png')
    if os.path.exists(analysis_path) and os.path.exists(pca_path):
        return
    analysis_params = DEFAULT_CONFIG['analysis_params']
    results = {}
    all_features = []

    logger.info(f"Starting linguistic analysis for directory: {input_dir}")
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            file_path = os.path.join(input_dir, filename)
            logger.info(f"Processing file: {file_path}")
            text = load_file(file_path)
            analysis_result = analyze_text(text, analysis_params)
            results[filename] = analysis_result
            all_features.append(list(analysis_result.values()))

    os.makedirs(output_dir, exist_ok=True)
    if not os.path.exists(analysis_path):
        save_file(json.dumps(results, indent=2), analysis_path)
        logger.info(f"Analysis results saved to {analysis_path}")

    if not os.path.exists(pca_path) and all_features and all_features[0]:
        perform_pca_analysis(all_features, output_dir, os.path.basename(input_dir))

def perform_meta_analysis(base_dir: str) -> None:
    sub_folders = ['Shifted_Domain', 'Shifted_Domain_Dissertation_Outline']
    output_base_dir = os.path.dirname("1_PREPARE/Methods/Research/FieldSHIFT-2/Inputs_and_Outputs/Analyses/Where_The_Analysis_Should_be.md")

    logger.info(f"Starting meta analysis for base directory: {base_dir}")
    for sub_folder in sub_folders:
        input_dir = os.path.join(base_dir, sub_folder)
        output_dir = os.path.join(output_base_dir, sub_folder)
        if os.path.exists(input_dir):
            logger.info(f"Analyzing sub-folder: {sub_folder}")
            os.makedirs(output_dir, exist_ok=True)  # Ensure output sub-folder exists
            perform_linguistic_analysis(input_dir, output_dir)

if __name__ == "__main__":
    base_dir = "1_PREPARE/Methods/Research/FieldSHIFT-2/Inputs_and_Outputs"
    perform_meta_analysis(base_dir)