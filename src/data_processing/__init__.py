"""Data processing module for analyzing and processing YouTube scripts."""

from .script_analyzer import ScriptAnalyzer
from .technique_identifier import TechniqueIdentifier, StructureExtractor, PerformanceCorrelator

__all__ = [
    "ScriptAnalyzer",
    "TechniqueIdentifier",
    "StructureExtractor",
    "PerformanceCorrelator",
]