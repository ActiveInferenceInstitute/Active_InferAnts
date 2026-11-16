"""Every existing meta-analysis artifact is protected before computation.

Controlled render/model interfaces avoid optional imports, downloads, large
research plots and scientific fitting. Marker files test preservation policy,
not scientific image quality or a qualified FieldSHIFT research runtime.
"""

import json
from pathlib import Path
from types import SimpleNamespace

import numpy as np
import pytest
from source_contract_helpers import FIELD, ForbiddenWork, load_definitions, seed_output

SOURCES = [
    ("Meta_Analysis_Shifted_Dissertation.py", "DissertationMetaAnalysis"),
    ("Meta_Analysis_Shifted_Dissertation_Outline.py", "DissertationOutlineMetaAnalysis"),
]
PCA_PATHS = (
    "PCA_Analysis/Top_Terms_Per_Component.png",
    "PCA_Analysis/Term_Loadings.png",
    "PCA_Analysis/Documents_And_Terms_In_PCA_Space.png",
    "PCA_Analysis/Explained_Variance.png",
    "PCA_Analysis/3D_PCA_Plot.png",
)
CLUSTER_PATHS = (
    "Clustering/KMeans_Clustering_PCA.png", "Clustering/KMeans_Clustering_tSNE.png",
    "Clustering/KMeans_Clustering_SVD.png", "Clustering/Hierarchical_Clustering_PCA.png",
    "Projections/PCA_Projection_By_Entity.png", "Projections/PCA_Projection_By_Domain.png",
    "PCA_Analysis/Top_Terms_Per_Component_20.png", *PCA_PATHS,
)
OTHER_PATHS = (
    "TopTerms/Top_30_Terms_Bar_Chart.png", "Heatmaps/Term_Frequency_Heatmap.png",
    "Diversity/Shannon_Diversity_Indices.png", "Heatmaps/Entity_Domain_Combination_Heatmap.png",
    "Networks/Term_Network_Graph.png", "Heatmaps/Term_Correlation_Heatmap.png",
    "Heatmaps/Document_Similarity_Heatmap.png", "Heatmaps/Top_50_Terms_Document_Heatmap.png",
    "Heatmaps/Top_50_Terms_Cooccurrence_Heatmap.png",
)
EXTRA_PATHS = ("Interactive/Interactive_3D_Scatter.html", "Dendrograms/Hierarchical_Clustering_Dendrogram.png")


class RenderFixture:
    def __init__(self):
        self.saved = []
        self.cm = self

    def savefig(self, filename, **kwargs):
        path = Path(filename)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"controlled rendering fixture")
        self.saved.append(path)

    def figure(self, **kwargs):
        return self

    def add_subplot(self, *args, **kwargs):
        return self

    def subplot(self, *args, **kwargs):
        return self

    def subplots(self, *args, **kwargs):
        return self, [self, self]

    def gca(self):
        return self

    def get_legend_handles_labels(self):
        return [], []

    def get_cmap(self, *args):
        return lambda value: (value, 0.0, 0.0, 1.0)

    def barh(self, *args, **kwargs):
        return []

    def __getattr__(self, name):
        return lambda *args, **kwargs: None


class MatrixFixture:
    def __init__(self, values=None):
        self.values = np.zeros((2, 40)) if values is None else values

    def toarray(self):
        return self.values


class VectorizerFixture:
    def get_feature_names_out(self):
        return np.array([f"term-{index}" for index in range(40)])

    def transform(self, texts):
        return MatrixFixture(np.zeros((len(list(texts)), 40)))


class PCAFixture:
    components_ = np.arange(120.0).reshape(3, 40)
    explained_variance_ratio_ = np.array([0.2, 0.3, 0.5])

    def fit_transform(self, values):
        return np.arange(len(values) * 50.0).reshape(len(values), 50)

    def transform(self, values):
        return np.arange(len(values) * 3.0).reshape(len(values), 3)


def instance(source, root, **values):
    rendering = RenderFixture()
    namespace = load_definitions(
        FIELD / source[0], plt=rendering,
        sns=SimpleNamespace(color_palette=lambda name, n_colors: ["blue"] * n_colors, despine=lambda **kwargs: None),
        **values,
    )
    analyzer = object.__new__(namespace[source[1]])
    analyzer.output_dir = str(root)
    analyzer.files = ["alice_one.md", "bob_two.md"]
    analyzer.texts = {"alice_one.md": "first fixture", "bob_two.md": "second fixture"}
    analyzer.stop_words = set()
    return analyzer, namespace, rendering


def expected_paths(source, files):
    extras = EXTRA_PATHS if source == SOURCES[0] else ()
    return (*CLUSTER_PATHS, *extras, *OTHER_PATHS, *(f"WordClouds/{file}_wordcloud.png" for file in files))


SINGLE = [
    ("plot_top_terms_per_component", ("data", "data"), {"n_terms": 7}, "PCA_Analysis/Top_Terms_Per_Component_7.png"),
    ("entity_domain_analysis", (), {}, "Heatmaps/Entity_Domain_Combination_Heatmap.png"),
    ("plot_top_terms_bar_chart", ("data",), {"num_terms": 11}, "TopTerms/Top_11_Terms_Bar_Chart.png"),
    ("plot_term_frequency_heatmap", ("data", "data"), {}, "Heatmaps/Term_Frequency_Heatmap.png"),
    ("calculate_diversity_indices", ("data",), {}, "Diversity/Shannon_Diversity_Indices.png"),
    ("plot_term_network", ("data", "data"), {}, "Networks/Term_Network_Graph.png"),
    ("plot_term_correlation_heatmap", ("data", "data"), {}, "Heatmaps/Term_Correlation_Heatmap.png"),
    ("plot_document_similarity_heatmap", ("data",), {}, "Heatmaps/Document_Similarity_Heatmap.png"),
    ("plot_term_document_heatmap", ("data", "data"), {"top_n": 7}, "Heatmaps/Top_7_Terms_Document_Heatmap.png"),
    ("plot_term_cooccurrence_heatmap", ("data", "data"), {"top_n": 9}, "Heatmaps/Top_9_Terms_Cooccurrence_Heatmap.png"),
]


@pytest.mark.parametrize("source", SOURCES)
@pytest.mark.parametrize("method,args,kwargs,target", SINGLE)
@pytest.mark.parametrize("historical", [b"", b"historical\x00\xff\r\n"])
def test_each_single_output_entrypoint_skips_before_data_or_rendering(tmp_path, source, method, args, kwargs, target, historical):
    analyzer, namespace, rendering = instance(source, tmp_path)
    poison = ForbiddenWork()
    namespace["plt"] = poison
    path = seed_output(tmp_path, target, historical)
    before = path.stat().st_mtime_ns
    getattr(analyzer, method)(*(poison for _ in args), **kwargs)
    assert path.read_bytes() == historical and path.stat().st_mtime_ns == before
    assert poison.calls == [] and rendering.saved == []


@pytest.mark.parametrize("method,target,args", [
    ("generate_interactive_3d_scatter", EXTRA_PATHS[0], 2),
    ("generate_dendrogram", EXTRA_PATHS[1], 1),
])
def test_dissertation_html_and_dendrogram_skip_before_construction(tmp_path, method, target, args):
    poison = ForbiddenWork()
    analyzer, _, rendering = instance(SOURCES[0], tmp_path, go=poison, linkage=poison)
    path = seed_output(tmp_path, target)
    getattr(analyzer, method)(*(poison for _ in range(args)))
    assert path.read_bytes() == b"historical\x00\xff\r\n"
    assert poison.calls == [] and rendering.saved == []


@pytest.mark.parametrize("source", SOURCES)
def test_complete_groups_and_orchestrator_do_not_read_or_fit(tmp_path, source):
    analyzer, _, rendering = instance(source, tmp_path)
    paths = [seed_output(tmp_path, path) for path in expected_paths(source, analyzer.files)]
    poison = ForbiddenWork()
    analyzer.perform_tfidf_analysis = poison
    analyzer.run_analysis()
    analyzer.cluster_documents()
    analyzer.pca_interpretability(poison, poison)
    analyzer.visualize_projections(poison, "PCA")
    assert poison.calls == [] and rendering.saved == []
    assert all(path.read_bytes() == b"historical\x00\xff\r\n" for path in paths)


@pytest.mark.parametrize("source", SOURCES)
@pytest.mark.parametrize("missing", PCA_PATHS)
def test_each_missing_pca_companion_is_created_without_rewriting_four_others(tmp_path, source, missing):
    analyzer, _, rendering = instance(source, tmp_path)
    preserved = [seed_output(tmp_path, path) for path in PCA_PATHS if path != missing]
    analyzer.pca_interpretability(PCAFixture(), VectorizerFixture())
    assert rendering.saved == [tmp_path / missing]
    assert (tmp_path / missing).read_bytes() == b"controlled rendering fixture"
    assert all(path.read_bytes() == b"historical\x00\xff\r\n" for path in preserved)


@pytest.mark.parametrize("source", SOURCES)
@pytest.mark.parametrize("present", ["Entity", "Domain"])
def test_projection_partial_pair_preserves_existing_companion(tmp_path, source, present):
    analyzer, _, rendering = instance(source, tmp_path)
    preserved = seed_output(tmp_path, f"Projections/Custom_Projection_By_{present}.png")
    other = "Domain" if present == "Entity" else "Entity"
    analyzer.visualize_projections(np.array([[0.0, 1.0], [2.0, 3.0]]), "Custom")
    assert rendering.saved == [tmp_path / f"Projections/Custom_Projection_By_{other}.png"]
    assert preserved.read_bytes() == b"historical\x00\xff\r\n"


@pytest.mark.parametrize("source", SOURCES)
def test_missing_interpretation_is_not_hidden_by_existing_cluster_plots(tmp_path, source):
    poison = ForbiddenWork()
    analyzer, namespace, rendering = instance(source, tmp_path, PCA=lambda **kwargs: PCAFixture(), KMeans=poison, AgglomerativeClustering=poison, TSNE=poison, TruncatedSVD=poison)
    missing = "PCA_Analysis/Explained_Variance.png"
    paths = [seed_output(tmp_path, path) for path in expected_paths(source, analyzer.files) if path != missing]
    analyzer.perform_tfidf_analysis = lambda: (None, MatrixFixture(), VectorizerFixture())
    analyzer.cluster_documents()
    assert rendering.saved == [tmp_path / missing]
    assert poison.calls == []
    assert all(path.read_bytes() == b"historical\x00\xff\r\n" for path in paths)


@pytest.mark.parametrize("source", SOURCES)
def test_missing_wordcloud_remains_eligible_without_unneeded_tfidf(tmp_path, source):
    generated = []

    class WordCloudFixture:
        def __init__(self, **kwargs):
            pass

        def generate(self, text):
            generated.append(text)
            return np.zeros((2, 2, 3))

    analyzer, _, rendering = instance(source, tmp_path, WordCloud=WordCloudFixture)
    missing = "WordClouds/bob_two.md_wordcloud.png"
    paths = [seed_output(tmp_path, path) for path in expected_paths(source, analyzer.files) if path != missing]
    poison = ForbiddenWork()
    analyzer.perform_tfidf_analysis = poison
    analyzer.run_analysis()
    assert rendering.saved == [tmp_path / missing]
    assert generated == ["second fixture"]
    assert poison.calls == []
    assert all(path.read_bytes() == b"historical\x00\xff\r\n" for path in paths)


def test_interactive_caller_passes_the_existing_third_pca_coordinate(tmp_path):
    class Figure:
        def __init__(self, data):
            self.data = data

        def update_layout(self, **kwargs):
            pass

        def write_html(self, filename):
            Path(filename).parent.mkdir(parents=True, exist_ok=True)
            Path(filename).write_text(json.dumps({"z": self.data[0]["z"].tolist()}))

    class KMeansFixture:
        def __init__(self, **kwargs):
            pass

        def fit_predict(self, matrix):
            return np.array([0, 1])

    analyzer, _, rendering = instance(
        SOURCES[0], tmp_path, PCA=lambda **kwargs: PCAFixture(), KMeans=KMeansFixture,
        silhouette_score=lambda *args: 0.5,
        go=SimpleNamespace(Figure=Figure, Scatter3d=lambda **kwargs: kwargs),
    )
    missing = EXTRA_PATHS[0]
    paths = [seed_output(tmp_path, path) for path in expected_paths(SOURCES[0], analyzer.files) if path != missing]
    analyzer.perform_tfidf_analysis = lambda: (None, MatrixFixture(), VectorizerFixture())
    analyzer.cluster_documents()
    assert json.loads((tmp_path / missing).read_text()) == {"z": [2.0, 52.0]}
    assert rendering.saved == []
    assert all(path.read_bytes() == b"historical\x00\xff\r\n" for path in paths)
