"""
YouTube Script AI - Pipeline completo para treinar LLM especializado em scripts do YouTube

Este projeto implementa um sistema híbrido que combina técnicas de storytelling
fundamentais com scripts reais de sucesso do YouTube para treinar um modelo
Llama especializado em geração de scripts.
"""

__version__ = "0.1.0"
__author__ = "Allan Duarte"
__email__ = "contact@example.com"

from . import data_collection
from . import data_processing
from . import training
from . import generation
from . import storytelling

__all__ = [
    "data_collection",
    "data_processing", 
    "training",
    "generation",
    "storytelling",
]