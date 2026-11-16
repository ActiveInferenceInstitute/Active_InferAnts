import os
import re
import nltk
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.transforms as transforms
from matplotlib.patches import Ellipse
import seaborn as sns
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.manifold import TSNE
from wordcloud import WordCloud
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import numpy as np
from scipy.stats import gaussian_kde
from scipy.stats import norm
import logging
import time
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import simpleSplit
import networkx as nx
from scipy.stats import spearmanr
import plotly.graph_objects as go
import plotly.express as px
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import matplotlib.cm as cm

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

plt.rcParams['font.family'] = 'DejaVu Sans'

class DissertationMetaAnalysis:
    def __init__(self, input_dir='Inputs_and_Outputs/Shifted_Dissertations/', output_dir='./Inputs_and_Outputs/Analyses/Dissertations/'):
        logging.info("Initializing DissertationMetaAnalysis")
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.files = self._get_files()
        self.texts = self._read_files()
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.update(['index', 'jsp', 'div', 'true', 'false', 'none', 'self', 'right', 'none', 'utf', '703', 'import', 'from', 'class', 'def', 'return', 'if', 'else', 'try', 'except', 'with', 'as', 'for', 'in', 'os', 'logging', 'open', 'read', 'write', 'join', 'path', 'exists', 'isdir', 'listdir', 'debug', 'info', 'warning', 'error', 'encoding', 'utf-8', 'and', 'of', 'the', 'to', 'a', 'active', 'in', 'as', 'true', 'for', 'with', 'def', 'will', 'may', 'um', 'uh', 'true', 'shall', 'nsf', "'d", "'ll", "'re", "'s", "'ve", 'could', 'might', 'must', "n't", 'need', 'sha', 'wo', 'would'])
        self._ensure_output_dir_exists()
        logging.info("Initialization complete")

    def _outputs_exist(self, paths):
        return all(os.path.exists(os.path.join(self.output_dir, path)) for path in paths)

    def _pca_outputs(self):
        return (
            'PCA_Analysis/Top_Terms_Per_Component.png',
            'PCA_Analysis/Term_Loadings.png',
            'PCA_Analysis/Documents_And_Terms_In_PCA_Space.png',
            'PCA_Analysis/Explained_Variance.png',
            'PCA_Analysis/3D_PCA_Plot.png',
        )

    def _cluster_outputs(self):
        return (
            'Clustering/KMeans_Clustering_PCA.png',
            'Clustering/KMeans_Clustering_tSNE.png',
            'Clustering/KMeans_Clustering_SVD.png',
            'Clustering/Hierarchical_Clustering_PCA.png',
            'Projections/PCA_Projection_By_Entity.png',
            'Projections/PCA_Projection_By_Domain.png',
            'PCA_Analysis/Top_Terms_Per_Component_20.png',
            'Interactive/Interactive_3D_Scatter.html',
            'Dendrograms/Hierarchical_Clustering_Dendrogram.png',
        ) + self._pca_outputs()

    def _tfidf_outputs(self):
        return (
            'TopTerms/Top_30_Terms_Bar_Chart.png',
            'Heatmaps/Term_Frequency_Heatmap.png',
            'Diversity/Shannon_Diversity_Indices.png',
            'Networks/Term_Network_Graph.png',
            'Heatmaps/Term_Correlation_Heatmap.png',
            'Heatmaps/Document_Similarity_Heatmap.png',
            'Heatmaps/Top_50_Terms_Document_Heatmap.png',
            'Heatmaps/Top_50_Terms_Cooccurrence_Heatmap.png',
        )

    def _analysis_outputs(self):
        return (
            self._cluster_outputs()
            + self._tfidf_outputs()
            + ('Heatmaps/Entity_Domain_Combination_Heatmap.png',)
            + tuple(f'WordClouds/{file}_wordcloud.png' for file in self.files)
        )

    def _get_files(self):
        logging.info("Getting files from input directory")
        files = [f for f in os.listdir(self.input_dir) if f.endswith('.md')]
        logging.info(f"Found {len(files)} files")
        return files

    def _read_files(self):
        logging.info("Reading files")
        texts = {}
        for file in self.files:
            logging.info(f"Reading file: {os.path.join(self.input_dir, file)}")
            with open(os.path.join(self.input_dir, file), 'r', encoding='utf-8') as f:
                texts[file] = f.read()
        logging.info("File reading complete")
        return texts

    def _ensure_output_dir_exists(self):
        logging.info("Ensuring output directories exist")
        directories = [
            self.output_dir,
            os.path.join(self.output_dir, 'WordClouds'),
            os.path.join(self.output_dir, 'Clustering'),
            os.path.join(self.output_dir, 'Heatmaps'),
            os.path.join(self.output_dir, 'Projections'),
            os.path.join(self.output_dir, 'PCA_Analysis'),
            os.path.join(self.output_dir, 'TopTerms'),
            os.path.join(self.output_dir, 'Diversity'),
            os.path.join(self.output_dir, 'Networks'),
            os.path.join(self.output_dir, 'Interactive'),
            os.path.join(self.output_dir, 'Dendrograms'),
            os.path.join(self.output_dir, 'WordClouds', 'Shaped'),
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
        logging.info("Output directories created")

    def _preprocess_text(self, text):
        logging.info("Preprocessing text")
        text = re.sub(r'[^\w\s]', '', text.lower())
        tokens = word_tokenize(text)
        return ' '.join([word for word in tokens if word not in self.stop_words])

    def perform_tfidf_analysis(self):
        logging.info("Performing TF-IDF analysis")
        vectorizer = TfidfVectorizer(stop_words=list(self.stop_words), lowercase=True, tokenizer=word_tokenize, token_pattern=None)
        tfidf_matrix = vectorizer.fit_transform([self._preprocess_text(text) for text in self.texts.values()])
        feature_names = vectorizer.get_feature_names_out()
        
        df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names, index=self.texts.keys())
        df = df[~df.index.duplicated(keep='first')]  # Remove duplicate index values
        top_terms = df.apply(lambda x: x.nlargest(10).index.tolist(), axis=1)
        
        logging.info("TF-IDF analysis complete")
        return top_terms, tfidf_matrix, vectorizer

    def cluster_documents(self, n_clusters=3):
        if self._outputs_exist(self._cluster_outputs()):
            return
        names = (
            'KMeans_Clustering_PCA.png',
            'KMeans_Clustering_tSNE.png',
            'KMeans_Clustering_SVD.png',
            'Hierarchical_Clustering_PCA.png',
        )
        missing = {
            name: not self._outputs_exist((os.path.join('Clustering', name),))
            for name in names
        }
        projections = (
            'Projections/PCA_Projection_By_Entity.png',
            'Projections/PCA_Projection_By_Domain.png',
        )
        need_projections = not self._outputs_exist(projections)
        need_interpretation = not self._outputs_exist(self._pca_outputs())
        need_terms = not self._outputs_exist(('PCA_Analysis/Top_Terms_Per_Component_20.png',))
        need_interactive = not self._outputs_exist(('Interactive/Interactive_3D_Scatter.html',))
        need_dendrogram = not self._outputs_exist(('Dendrograms/Hierarchical_Clustering_Dendrogram.png',))
        _, tfidf_matrix, vectorizer = self.perform_tfidf_analysis()
        kmeans_labels = None
        hierarchical_labels = None
        if any(missing[name] for name in names[:3]) or need_interactive:
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            kmeans_labels = kmeans.fit_predict(tfidf_matrix)
        if missing[names[3]]:
            hierarchical = AgglomerativeClustering(n_clusters=n_clusters)
            hierarchical_labels = hierarchical.fit_predict(tfidf_matrix.toarray())
        if missing[names[0]] or missing[names[3]] or need_projections or need_interpretation or need_terms or need_interactive:
            pca = PCA(n_components=50, random_state=42)
            pca_coordinates = pca.fit_transform(tfidf_matrix.toarray())
            pca_coords = pca_coordinates[:, :2]
        if missing[names[1]]:
            tsne = TSNE(n_components=2, random_state=42, perplexity=5)
            tsne_coords = tsne.fit_transform(tfidf_matrix.toarray())
        if missing[names[2]]:
            svd = TruncatedSVD(n_components=50, random_state=42)
            svd_coords = svd.fit_transform(tfidf_matrix)[:, :2]

        def plot_clusters(coords, labels, title, filename, method):
            if self._outputs_exist((os.path.join('Clustering', filename),)):
                return
            logging.info(f"Plotting {title}")
            plt.figure(figsize=(16, 12))
            scatter = plt.scatter(coords[:, 0], coords[:, 1], c=labels, cmap='viridis', s=100)
            plt.colorbar(scatter, label='Cluster')
            for label in set(labels):
                cluster_points = coords[labels == label]
                confidence_ellipse(cluster_points[:, 0], cluster_points[:, 1], plt.gca(), n_std=2.0,
                                   edgecolor=plt.cm.viridis(label / max(labels)))
            if method == 'PCA':
                for i, (comp, var) in enumerate(zip(pca.components_, pca.explained_variance_ratio_)):
                    plt.arrow(0, 0, comp[0]*var*20, comp[1]*var*20, color='r', alpha=0.5,
                              head_width=0.05, head_length=0.05)
                    plt.text(comp[0]*var*20, comp[1]*var*20, f'PC{i+1}\n({var:.2f})',
                             color='r', ha='center', va='center')
            for i, file in enumerate(self.texts.keys()):
                plt.annotate(file, (coords[i, 0], coords[i, 1]), fontsize=8, alpha=0.7)
            plt.title(title, fontsize=24, pad=20)
            plt.xlabel(f'{method} Component 1', fontsize=14)
            plt.ylabel(f'{method} Component 2', fontsize=14)
            plt.tight_layout(pad=3)
            plt.savefig(os.path.join(self.output_dir, 'Clustering', filename), dpi=300, bbox_inches='tight')
            plt.close()
            logging.info(f"Plot saved: {os.path.join(self.output_dir, 'Clustering', filename)}")

        if missing[names[0]]:
            plot_clusters(pca_coords, kmeans_labels, 'KMeans_Clustering_PCA', names[0], 'PCA')
        if missing[names[1]]:
            plot_clusters(tsne_coords, kmeans_labels, 'KMeans_Clustering_tSNE', names[1], 't-SNE')
        if missing[names[2]]:
            plot_clusters(svd_coords, kmeans_labels, 'KMeans_Clustering_SVD', names[2], 'SVD')
        if missing[names[3]]:
            plot_clusters(pca_coords, hierarchical_labels, 'Hierarchical_Clustering_PCA', names[3], 'PCA')
        if kmeans_labels is not None:
            logging.info("K-means Silhouette Score: %.4f", silhouette_score(tfidf_matrix, kmeans_labels))
        if hierarchical_labels is not None:
            logging.info("Hierarchical Clustering Silhouette Score: %.4f", silhouette_score(tfidf_matrix.toarray(), hierarchical_labels))
        if need_projections:
            self.visualize_projections(pca_coords, 'PCA')
        if need_interpretation:
            self.pca_interpretability(pca, vectorizer)
        if need_terms:
            self.plot_top_terms_per_component(pca, vectorizer.get_feature_names_out())
        if need_interactive:
            self.generate_interactive_3d_scatter(pca_coordinates[:, :3], kmeans_labels)
        if need_dendrogram:
            self.generate_dendrogram(tfidf_matrix.toarray())


    def generate_interactive_3d_scatter(self, pca_coords, labels):
        if self._outputs_exist(('Interactive/Interactive_3D_Scatter.html',)):
            return
        logging.info("Generating interactive 3D scatter plot")
        fig = go.Figure(data=[go.Scatter3d(
            x=pca_coords[:, 0],
            y=pca_coords[:, 1],
            z=pca_coords[:, 2],
            mode='markers',
            marker=dict(
                size=5,
                color=labels,
                colorscale='Viridis',
                opacity=0.8
            ),
            text=[f"Document: {doc}<br>Cluster: {label}" for doc, label in zip(self.texts.keys(), labels)],
            hoverinfo='text'
        )])

        fig.update_layout(
            title='Interactive 3D Scatter Plot of Documents',
            autosize=False,
            width=900,
            height=800,
            margin=dict(l=0, r=0, b=0, t=40)
        )

        fig.write_html(os.path.join(self.output_dir, 'Interactive', 'Interactive_3D_Scatter.html'))
        logging.info(f"Interactive 3D scatter plot saved: {os.path.join(self.output_dir, 'Interactive', 'Interactive_3D_Scatter.html')}")

    def generate_dendrogram(self, data):
        if self._outputs_exist(('Dendrograms/Hierarchical_Clustering_Dendrogram.png',)):
            return
        logging.info("Generating dendrogram")
        linked = linkage(data, 'ward')

        plt.figure(figsize=(20, 10))
        dendrogram(linked,
                   orientation='top',
                   labels=list(self.texts.keys()),
                   distance_sort='descending',
                   show_leaf_counts=True)
        plt.title('Hierarchical Clustering Dendrogram')
        plt.xlabel('Sample Index')
        plt.ylabel('Distance')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'Dendrograms', 'Hierarchical_Clustering_Dendrogram.png'), dpi=300, bbox_inches='tight')
        plt.close()
        logging.info(f"Dendrogram saved: {os.path.join(self.output_dir, 'Dendrograms', 'Hierarchical_Clustering_Dendrogram.png')}")

    def plot_top_terms_per_component(self, pca, feature_names, n_terms=20):
        if self._outputs_exist((f'PCA_Analysis/Top_Terms_Per_Component_{n_terms}.png',)):
            return
        logging.info("Plotting top terms per PCA component")
        fig, axes = plt.subplots(1, 2, figsize=(20, 10), sharey=True)
        
        for i, ax in enumerate(axes):
            component = pca.components_[i]
            indices = np.argsort(np.abs(component))[-n_terms:]
            terms = [feature_names[idx] for idx in indices]
            weights = component[indices]
            
            ax.barh(terms, weights, color='b')
            ax.set_title(f'PCA Component {i+1}')
            ax.set_xlabel('Weight')
            ax.set_ylabel('Term')
            self.add_value_labels(ax, weights, terms)
        
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'PCA_Analysis', f'Top_Terms_Per_Component_{n_terms}.png'), dpi=300, bbox_inches='tight')
        plt.close()
        logging.info(f"Top terms per component plot saved: {os.path.join(self.output_dir, 'PCA_Analysis', f'Top_Terms_Per_Component_{n_terms}.png')}")

    def add_value_labels(self, ax, values, labels):
        for i, (value, label) in enumerate(zip(values, labels)):
            ax.text(value, i, f'{value:.2f}', ha='center', va='center', color='white', fontsize=10, fontweight='bold', bbox=dict(facecolor='black', alpha=0.7))

    def visualize_projections(self, coords, method):
        if self._outputs_exist((
            f'Projections/{method}_Projection_By_Entity.png',
            f'Projections/{method}_Projection_By_Domain.png',
        )):
            return
        logging.info(f"Visualizing {method} projections")
        entities = [file.split('_')[0] for file in self.files]
        domains = [file.split('_')[1].split('.md')[0] if len(file.split('_')) > 1 else 'Unknown' for file in self.files]

        def plot_projection(color_by, title):
            filename = f"{method}_Projection_By_{title.split(' by ')[-1].replace(' ', '_')}.png"
            if self._outputs_exist((os.path.join('Projections', filename),)):
                return
            logging.info(f"Plotting {title}")
            plt.figure(figsize=(16, 12))
            unique_items = list(set(color_by))
            color_map = plt.cm.get_cmap('tab10')
            colors = [color_map(i/len(unique_items)) for i in range(len(unique_items))]
            color_dict = dict(zip(unique_items, colors))
            
            for i, item in enumerate(color_by):
                plt.scatter(coords[i, 0], coords[i, 1], c=[color_dict[item]], s=100, label=item if item not in plt.gca().get_legend_handles_labels()[1] else "")
                plt.annotate(self.files[i], (coords[i, 0], coords[i, 1]), fontsize=8, alpha=0.7)
            
            # Add confidence intervals
            for item in unique_items:
                item_coords = coords[np.array(color_by) == item]
                if len(item_coords) > 1:  # Only add confidence ellipse if there's more than one point
                    confidence_ellipse(item_coords[:, 0], item_coords[:, 1], plt.gca(), n_std=2.0, 
                                       edgecolor=color_dict[item], label=f'{item} (95% CI)')
            
            # Add gradient zones
            xx, yy = np.mgrid[coords[:, 0].min():coords[:, 0].max():100j, 
                              coords[:, 1].min():coords[:, 1].max():100j]
            positions = np.vstack([xx.ravel(), yy.ravel()]).T
            for item in unique_items:
                item_coords = coords[np.array(color_by) == item]
                if len(item_coords) > 1:  # Only add kernel density estimate if there's more than one point
                    try:
                        kernel = gaussian_kde(item_coords[:, :2].T)
                        f = np.reshape(kernel(positions.T).T, xx.shape)
                        plt.contourf(xx, yy, f, cmap='Blues', alpha=0.2)
                    except np.linalg.LinAlgError:
                        logging.warning(f"Could not compute kernel density estimate for {item}")
            
            plt.legend(title=title.split(' by ')[1], loc='center left', bbox_to_anchor=(1, 0.5))
            plt.title(title, fontsize=24, pad=20)
            plt.xlabel(f'{method} Component 1', fontsize=14)
            plt.ylabel(f'{method} Component 2', fontsize=14)
            plt.tight_layout(pad=3)
            
            plt.savefig(os.path.join(self.output_dir, 'Projections', filename), dpi=300, bbox_inches='tight')
            plt.close()

        plot_projection(entities, f'{method} Projection by Entity')
        plot_projection(domains, f'{method} Projection by Domain')

    def pca_interpretability(self, pca, vectorizer):
        paths = self._pca_outputs()
        missing = [not self._outputs_exist((path,)) for path in paths]
        if not any(missing):
            return
        if any(missing[:3]):
            feature_names = vectorizer.get_feature_names_out()

        def print_top_terms(component, feature_names, n=10):
            top_indices = np.argsort(component)[::-1][:n]
            return [(feature_names[i], component[i]) for i in top_indices]

        if missing[0]:
            n_components = 20
            n_top_terms = 40
            plt.figure(figsize=(20, 4 * n_components), dpi=300)
            for i, component in enumerate(pca.components_[:n_components]):
                top_terms = print_top_terms(component, feature_names, n_top_terms)
                terms = [term for term, _ in top_terms]
                loadings = [loading for _, loading in top_terms]
                sorted_indices = np.argsort(np.abs(loadings))[::-1]
                terms = [terms[i] for i in sorted_indices]
                loadings = [loadings[i] for i in sorted_indices]
                ax = plt.subplot(n_components, 1, i + 1)
                colors = sns.color_palette("husl", n_colors=n_top_terms)
                bars = plt.barh(range(n_top_terms), loadings, align='center', color=colors)
                plt.yticks(range(n_top_terms), terms, fontsize=12)
                plt.xlabel('Loading', fontsize=14)
                plt.title(f'Top Terms for PC{i+1}', fontsize=16)
                for bar in bars:
                    width = bar.get_width()
                    plt.text(width, bar.get_y() + bar.get_height()/2,
                             f'{width:.2f}', va='center', fontsize=10)
                sns.despine(left=True, bottom=True)
                plt.grid(axis='x', linestyle='--', alpha=0.7)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, paths[0]), dpi=300, bbox_inches='tight')
            plt.close()
            for i, component in enumerate(pca.components_):
                logging.info(f"Top terms for PC{i+1}:")
                logging.info(print_top_terms(component, feature_names))

        if missing[1]:
            logging.info("Visualizing term loadings on principal components")
            plt.figure(figsize=(20, 10))
            terms = feature_names
            x = pca.components_[0]
            y = pca.components_[1]
            plt.scatter(x, y)
            plt.xlabel("PC1")
            plt.ylabel("PC2")
            for i, term in enumerate(terms):
                plt.annotate(term, (x[i], y[i]))
            plt.title("Term_Loadings_On_Principal_Components")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, paths[1]), dpi=300, bbox_inches='tight')
            plt.close()

        if missing[2]:
            logging.info("Visualizing documents in PCA space with term vectors")
            pca_coords = pca.transform(vectorizer.transform(self.texts.values()).toarray())[:, :2]
            plt.figure(figsize=(20, 10))
            plt.scatter(pca_coords[:, 0], pca_coords[:, 1])
            for i, file in enumerate(self.texts.keys()):
                plt.annotate(file, (pca_coords[i, 0], pca_coords[i, 1]), fontsize=8)
            n_terms = 20
            terms = feature_names
            x = pca.components_[0]
            y = pca.components_[1]
            indices = np.argsort(np.sqrt(x**2 + y**2))[-n_terms:]
            for i in indices:
                plt.arrow(0, 0, x[i]*5, y[i]*5, color='r', alpha=0.5, head_width=0.05, head_length=0.05)
                plt.text(x[i]*5.2, y[i]*5.2, terms[i], color='r', ha='center', va='center')
            plt.xlabel("PC1")
            plt.ylabel("PC2")
            plt.title("Documents_And_Terms_In_PCA_Space")
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, paths[2]), dpi=300, bbox_inches='tight')
            plt.close()

        if missing[3]:
            logging.info("Plotting variance explained by each principal component")
            plt.figure(figsize=(10, 6))
            plt.plot(np.cumsum(pca.explained_variance_ratio_), marker='o', linestyle='--')
            plt.xlabel('Number of Components')
            plt.ylabel('Cumulative Explained Variance')
            plt.title('Explained_Variance_By_Number_Of_Principal_Components')
            plt.grid(True)
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, paths[3]), dpi=300, bbox_inches='tight')
            plt.close()

        if missing[4]:
            logging.info("Creating 3D PCA plot")
            from mpl_toolkits.mplot3d import Axes3D
            fig = plt.figure(figsize=(12, 8))
            ax = fig.add_subplot(111, projection='3d')
            pca_coords_3d = pca.transform(vectorizer.transform(self.texts.values()).toarray())[:, :3]
            ax.scatter(pca_coords_3d[:, 0], pca_coords_3d[:, 1], pca_coords_3d[:, 2], c='b', marker='o')
            for i, file in enumerate(self.texts.keys()):
                ax.text(pca_coords_3d[i, 0], pca_coords_3d[i, 1], pca_coords_3d[i, 2], file, fontsize=8)
            ax.set_xlabel('PC1')
            ax.set_ylabel('PC2')
            ax.set_zlabel('PC3')
            ax.set_title('3D_PCA_Plot')
            plt.tight_layout()
            plt.savefig(os.path.join(self.output_dir, paths[4]), dpi=300, bbox_inches='tight')
            plt.close()


    def entity_domain_analysis(self):
        if self._outputs_exist(('Heatmaps/Entity_Domain_Combination_Heatmap.png',)):
            return
        logging.info("Analyzing entity-domain combinations")
        entities = set()
        from_domains = set()
        to_domains = set()
        
        for file in self.files:
            parts = file.split('_')
            if len(parts) >= 2:
                entities.add(parts[0])
                to_domains.add(parts[-1].split('.md')[0])
                if len(parts) >= 3:
                    from_domains.add(parts[-2])
        
        print(f"Entities: {entities}")
        print(f"From Domains: {from_domains}")
        print(f"To Domains: {to_domains}")
        
        # Create a heatmap of entity-domain combinations
        matrix = pd.DataFrame(index=entities, columns=to_domains, data=0)
        for file in self.files:
            parts = file.split('_')
            if len(parts) >= 2:
                entity = parts[0]
                to_domain = parts[-1].split('.md')[0]
                if entity in matrix.index and to_domain in matrix.columns:
                    matrix.loc[entity, to_domain] += 1
                else:
                    logging.warning(f"Skipping file {file}: entity or domain not found in matrix")
        
        plt.figure(figsize=(20, 16))
        sns.heatmap(matrix, annot=True, cmap='YlOrRd', fmt='d', cbar_kws={'label': 'Number of Combinations'})
        plt.title('Entity_Domain_Combination_Heatmap', fontsize=24, pad=20)
        plt.xlabel('To Domains', fontsize=18)
        plt.ylabel('Entities', fontsize=18)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(rotation=0, fontsize=10)
        plt.tight_layout(pad=3)
        plt.savefig(os.path.join(self.output_dir, 'Heatmaps', 'Entity_Domain_Combination_Heatmap.png'), dpi=300, bbox_inches='tight')
        plt.close()

    def generate_word_clouds(self):
        logging.info("Generating word clouds")
        for file, text in self.texts.items():
            if self._outputs_exist((f'WordClouds/{file}_wordcloud.png',)):
                continue
            wordcloud = WordCloud(stopwords=self.stop_words, background_color='white', width=800, height=400).generate(text)
            plt.figure(figsize=(10, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis('off')
            plt.title(f'Word Cloud for {file}', fontsize=16)
            plt.tight_layout(pad=0)
            plt.savefig(os.path.join(self.output_dir, 'WordClouds', f'{file}_wordcloud.png'), dpi=300)
            plt.close()
            logging.info(f"Word cloud saved: {os.path.join(self.output_dir, 'WordClouds', f'{file}_wordcloud.png')}")

    def plot_top_terms_bar_chart(self, top_terms, num_terms=30):
        if self._outputs_exist((f'TopTerms/Top_{num_terms}_Terms_Bar_Chart.png',)):
            return
        logging.info(f"Plotting top {num_terms} terms bar chart")
        
        # Convert Series to list and flatten
        all_top_terms = [term for terms in top_terms.tolist() for term in terms]
        
        # Count term frequencies
        term_counts = Counter(all_top_terms)
        
        # Get the top N terms
        top_n_terms = sorted(term_counts.items(), key=lambda x: x[1], reverse=True)[:num_terms]
        
        # Create lists for plotting
        terms, counts = zip(*top_n_terms)
        
        # Create the bar plot
        plt.figure(figsize=(15, 10))
        plt.bar(terms, counts)
        plt.xticks(rotation=90)
        plt.xlabel('Terms')
        plt.ylabel('Frequency')
        plt.title(f'Top {num_terms} Terms Across All Documents')
        plt.tight_layout()
        
        # Save the plot
        plt.savefig(os.path.join(self.output_dir, 'TopTerms', f'Top_{num_terms}_Terms_Bar_Chart.png'), dpi=300, bbox_inches='tight')
        plt.close()
        
        logging.info(f"Top {num_terms} terms bar chart saved: {os.path.join(self.output_dir, 'TopTerms', f'Top_{num_terms}_Terms_Bar_Chart.png')}")

    def plot_term_frequency_heatmap(self, tfidf_matrix, feature_names):
        if self._outputs_exist(('Heatmaps/Term_Frequency_Heatmap.png',)):
            return
        logging.info("Plotting term frequency heatmap")
        df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names, index=self.texts.keys())
        plt.figure(figsize=(20, 10))
        sns.heatmap(df.T, cmap='YlGnBu', cbar_kws={'label': 'TF-IDF Score'})
        plt.title('Term Frequency Heatmap')
        plt.xlabel('Documents')
        plt.ylabel('Terms')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'Heatmaps', 'Term_Frequency_Heatmap.png'), dpi=300)
        plt.close()
        logging.info(f"Term frequency heatmap saved: {os.path.join(self.output_dir, 'Heatmaps', 'Term_Frequency_Heatmap.png')}")

    def calculate_diversity_indices(self, tfidf_matrix):
        if self._outputs_exist(('Diversity/Shannon_Diversity_Indices.png',)):
            return
        logging.info("Calculating diversity indices")
        df = pd.DataFrame(tfidf_matrix.toarray(), index=self.texts.keys())
        
        # Calculate Shannon diversity indices
        shannon_indices = df.apply(lambda x: -np.sum(x * np.log(x + 1e-10)), axis=1)
        
        # Sort indices from lowest to highest diversity
        shannon_indices = shannon_indices.sort_values()
        
        # Plotting
        plt.figure(figsize=(16, 10))  # Increase figure size for better readability
        ax = shannon_indices.plot(kind='bar', color='skyblue')
        plt.xlabel('Documents', fontsize=14, labelpad=10)  # Add more spacing for the x-axis label
        plt.ylabel('Shannon Diversity Index', fontsize=14, labelpad=10)  # Add more spacing for the y-axis label
        plt.title('Diversity Indices of Documents', fontsize=16, pad=20)  # Add more spacing for the title
        plt.xticks(rotation=90, ha='center')  # Rotate x-axis labels for better readability
        
        # Adjust layout to add more padding at the bottom
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.4)  # Increase bottom padding
        
        # Adjust x-axis labels
        ax.set_xticklabels(ax.get_xticklabels(), fontsize=8)
        
        plt.savefig(os.path.join(self.output_dir, 'Diversity', 'Shannon_Diversity_Indices.png'), dpi=300, bbox_inches='tight')
        plt.close()
        logging.info(f"Diversity indices plot saved: {os.path.join(self.output_dir, 'Diversity', 'Shannon_Diversity_Indices.png')}")

    def plot_term_network(self, tfidf_matrix, feature_names):
        if self._outputs_exist(('Networks/Term_Network_Graph.png',)):
            return
        logging.info("Plotting term network graph")
        df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names, index=self.texts.keys())
        G = nx.Graph()
        for term in feature_names:
            G.add_node(term)
        for doc in df.index:
            terms = df.loc[doc][df.loc[doc] > 0].index
            for i, term1 in enumerate(terms):
                for term2 in terms[i+1:]:
                    if G.has_edge(term1, term2):
                        G[term1][term2]['weight'] += 1
                    else:
                        G.add_edge(term1, term2, weight=1)
        pos = nx.spring_layout(G, k=0.1)
        plt.figure(figsize=(20, 20))
        nx.draw_networkx_nodes(G, pos, node_size=50)
        nx.draw_networkx_edges(G, pos, width=[G[u][v]['weight'] for u, v in G.edges()])
        nx.draw_networkx_labels(G, pos, font_size=8)
        plt.title('Term Network Graph')
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'Networks', 'Term_Network_Graph.png'), dpi=300)
        plt.close()
        logging.info(f"Term network graph saved: {os.path.join(self.output_dir, 'Networks', 'Term_Network_Graph.png')}")

    def plot_term_correlation_heatmap(self, tfidf_matrix, feature_names):
        if self._outputs_exist(('Heatmaps/Term_Correlation_Heatmap.png',)):
            return
        logging.info("Plotting term correlation heatmap")
        df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names, index=self.texts.keys())
        
        # Calculate Spearman correlation
        corr_matrix = df.T.corr(method='spearman')
        
        plt.figure(figsize=(20, 16))
        sns.heatmap(corr_matrix, cmap='coolwarm', center=0, vmin=-1, vmax=1, 
                    square=True, linewidths=0.5, cbar_kws={"shrink": .5})
        plt.title('Term Correlation Heatmap', fontsize=16)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'Heatmaps', 'Term_Correlation_Heatmap.png'), dpi=300, bbox_inches='tight')
        plt.close()
        logging.info(f"Term correlation heatmap saved: {os.path.join(self.output_dir, 'Heatmaps', 'Term_Correlation_Heatmap.png')}")

    def plot_document_similarity_heatmap(self, tfidf_matrix):
        if self._outputs_exist(('Heatmaps/Document_Similarity_Heatmap.png',)):
            return
        logging.info("Plotting document similarity heatmap")
        similarity_matrix = (tfidf_matrix * tfidf_matrix.T).toarray()
        
        plt.figure(figsize=(16, 14))
        sns.heatmap(similarity_matrix, cmap='YlGnBu', annot=True, fmt='.2f', 
                    xticklabels=self.texts.keys(), yticklabels=self.texts.keys())
        plt.title('Document Similarity Heatmap', fontsize=16)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'Heatmaps', 'Document_Similarity_Heatmap.png'), dpi=300, bbox_inches='tight')
        plt.close()
        logging.info(f"Document similarity heatmap saved: {os.path.join(self.output_dir, 'Heatmaps', 'Document_Similarity_Heatmap.png')}")

    def plot_term_document_heatmap(self, tfidf_matrix, feature_names, top_n=50):
        if self._outputs_exist((f'Heatmaps/Top_{top_n}_Terms_Document_Heatmap.png',)):
            return
        logging.info(f"Plotting top {top_n} terms-document heatmap")
        df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names, index=self.texts.keys())
        
        # Select top N terms based on mean TF-IDF score
        top_terms = df.mean().nlargest(top_n).index
        df_top = df[top_terms]
        
        plt.figure(figsize=(20, 16))
        sns.heatmap(df_top.T, cmap='YlOrRd', annot=False, 
                    xticklabels=True, yticklabels=True)
        plt.title(f'Top {top_n} Terms-Document Heatmap', fontsize=16)
        plt.xlabel('Documents', fontsize=12)
        plt.ylabel('Terms', fontsize=12)
        plt.xticks(rotation=90)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'Heatmaps', f'Top_{top_n}_Terms_Document_Heatmap.png'), dpi=300, bbox_inches='tight')
        plt.close()
        logging.info(f"Top {top_n} terms-document heatmap saved: {os.path.join(self.output_dir, 'Heatmaps', f'Top_{top_n}_Terms_Document_Heatmap.png')}")

    def plot_term_cooccurrence_heatmap(self, tfidf_matrix, feature_names, top_n=50):
        if self._outputs_exist((f'Heatmaps/Top_{top_n}_Terms_Cooccurrence_Heatmap.png',)):
            return
        logging.info(f"Plotting top {top_n} terms co-occurrence heatmap")
        df = pd.DataFrame(tfidf_matrix.toarray(), columns=feature_names, index=self.texts.keys())
        
        # Select top N terms based on mean TF-IDF score
        top_terms = df.mean().nlargest(top_n).index
        df_top = df[top_terms]
        
        # Calculate co-occurrence matrix
        cooccurrence = df_top.T.dot(df_top)
        
        plt.figure(figsize=(20, 16))
        sns.heatmap(cooccurrence, cmap='viridis', annot=False, 
                    xticklabels=True, yticklabels=True, square=True)
        plt.title(f'Top {top_n} Terms Co-occurrence Heatmap', fontsize=16)
        plt.xticks(rotation=90)
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, 'Heatmaps', f'Top_{top_n}_Terms_Cooccurrence_Heatmap.png'), dpi=300, bbox_inches='tight')
        plt.close()
        logging.info(f"Top {top_n} terms co-occurrence heatmap saved: {os.path.join(self.output_dir, 'Heatmaps', f'Top_{top_n}_Terms_Cooccurrence_Heatmap.png')}")

    def run_analysis(self):
        if self._outputs_exist(self._analysis_outputs()):
            return
        if not self._outputs_exist(self._tfidf_outputs()):
            top_terms, tfidf_matrix, vectorizer = self.perform_tfidf_analysis()
            if not self._outputs_exist(('TopTerms/Top_30_Terms_Bar_Chart.png',)):
                self.plot_top_terms_bar_chart(top_terms, num_terms=30)
            if not self._outputs_exist(('Heatmaps/Term_Frequency_Heatmap.png',)):
                self.plot_term_frequency_heatmap(tfidf_matrix, vectorizer.get_feature_names_out())
            if not self._outputs_exist(('Diversity/Shannon_Diversity_Indices.png',)):
                self.calculate_diversity_indices(tfidf_matrix)
            if not self._outputs_exist(('Networks/Term_Network_Graph.png',)):
                self.plot_term_network(tfidf_matrix, vectorizer.get_feature_names_out())
            if not self._outputs_exist(('Heatmaps/Term_Correlation_Heatmap.png',)):
                self.plot_term_correlation_heatmap(tfidf_matrix, vectorizer.get_feature_names_out())
            if not self._outputs_exist(('Heatmaps/Document_Similarity_Heatmap.png',)):
                self.plot_document_similarity_heatmap(tfidf_matrix)
            if not self._outputs_exist(('Heatmaps/Top_50_Terms_Document_Heatmap.png',)):
                self.plot_term_document_heatmap(tfidf_matrix, vectorizer.get_feature_names_out())
            if not self._outputs_exist(('Heatmaps/Top_50_Terms_Cooccurrence_Heatmap.png',)):
                self.plot_term_cooccurrence_heatmap(tfidf_matrix, vectorizer.get_feature_names_out())
        if not self._outputs_exist(self._cluster_outputs()):
            self.cluster_documents()
        if not self._outputs_exist(('Heatmaps/Entity_Domain_Combination_Heatmap.png',)):
            self.entity_domain_analysis()
        if not self._outputs_exist(tuple(f'WordClouds/{file}_wordcloud.png' for file in self.files)):
            self.generate_word_clouds()

def confidence_ellipse(x, y, ax, n_std=3.0, facecolor='none', **kwargs):
    """
    Create a plot of the covariance confidence ellipse of *x* and *y*.
    """
    if x.size != y.size:
        raise ValueError("x and y must be the same size")

    cov = np.cov(x, y)
    pearson = cov[0, 1]/np.sqrt(cov[0, 0] * cov[1, 1])
    
    ell_radius_x = np.sqrt(1 + pearson)
    ell_radius_y = np.sqrt(1 - pearson)
    ellipse = Ellipse((0, 0), width=ell_radius_x * 2, height=ell_radius_y * 2,
                      facecolor=facecolor, **kwargs)

    scale_x = np.sqrt(cov[0, 0]) * n_std
    mean_x = np.mean(x)

    scale_y = np.sqrt(cov[1, 1]) * n_std
    mean_y = np.mean(y)

    transf = transforms.Affine2D() \
        .rotate_deg(45) \
        .scale(scale_x, scale_y) \
        .translate(mean_x, mean_y)

    ellipse.set_transform(transf + ax.transData)
    return ax.add_patch(ellipse)

if __name__ == "__main__":
    analyzer = DissertationMetaAnalysis()
    analyzer.run_analysis()