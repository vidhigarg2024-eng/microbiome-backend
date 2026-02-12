import pandas as pd
import numpy as np
from skbio.diversity.alpha import shannon
from skbio import DistanceMatrix
import json

# Mock taxonomy data (replace with real parsing later)
MOCK_TAXONOMY = {
    "Bacteria": 0.6, "Archaea": 0.1, "Fungi": 0.3
}

def mock_fastq_to_taxonomy(fastq_path):
    """Step 3: Taxonomic Classification (mock)"""
    return pd.DataFrame({
        "taxon": ["Bacteria", "Archaea", "Fungi"],
        "abundance": [0.6, 0.1, 0.3]
    })

def compute_diversity(tax_df):
    """Step 5: Diversity Analysis"""
    abundances = tax_df["abundance"].values
    alpha_shannon = shannon(abundances)
    
    # Mock beta (single sample = trivial)
    beta_matrix = np.array([[0.0]])
    
    return {"shannon": float(alpha_shannon), "beta_matrix": beta_matrix.tolist()}

def predict_risk(metrics):
    """Step 6: Stability & Risk Interpretation"""
    shannon = metrics["shannon"]
    if shannon > 5.0:
        return "LC"  # Least Concern
    elif shannon > 3.0:
        return "NT"  # Near Threatened
    else:
        return "VU"  # Vulnerable

def run_full_pipeline(fastq_path):
    """Steps 2-6: Complete workflow"""
    # Step 3: Taxonomy
    tax_df = mock_fastq_to_taxonomy(fastq_path)
    
    # Step 4: Functional (mock)
    functions = {"metabolism": 0.4, "immune": 0.3}
    
    # Step 5: Diversity
    diversity = compute_diversity(tax_df)
    
    # Step 6: Risk
    risk = predict_risk(diversity)
    
    return {
        "taxonomy": tax_df.to_dict("records"),
        "functions": functions,
        "diversity": diversity,
        "predicted_iucn": risk,
        "confidence": 0.85
    }
