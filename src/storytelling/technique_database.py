"""
Central database for all storytelling techniques.

This module provides a unified interface to access all storytelling
techniques, hooks, structures, and patterns.
"""

import json
from typing import Dict, List, Any, Optional
from .hook_techniques import HookTechniques, Hook
from .narrative_structures import NarrativeStructures, NarrativeStructure  
from .engagement_patterns import EngagementPatterns, EngagementTechnique


class TechniqueDatabase:
    """Central database for all storytelling techniques."""
    
    def __init__(self):
        self.hooks = HookTechniques()
        self.structures = NarrativeStructures()
        self.patterns = EngagementPatterns()
    
    def search_techniques(self, query: str, category: Optional[str] = None) -> Dict[str, List[Any]]:
        """Search for techniques across all categories."""
        results = {
            "hooks": [],
            "structures": [],
            "patterns": []
        }
        
        query_lower = query.lower()
        
        # Search hooks
        if not category or category == "hooks":
            for hook in self.hooks.get_all_hooks().values():
                if (query_lower in hook.name.lower() or 
                    query_lower in hook.description.lower() or
                    any(query_lower in niche.lower() for niche in hook.best_niches)):
                    results["hooks"].append(hook)
        
        # Search structures  
        if not category or category == "structures":
            for structure in self.structures.get_all_structures().values():
                if (query_lower in structure.name.lower() or
                    query_lower in structure.description.lower() or
                    any(query_lower in best_for.lower() for best_for in structure.best_for)):
                    results["structures"].append(structure)
        
        # Search patterns
        if not category or category == "patterns":
            for pattern in self.patterns.get_all_techniques().values():
                if (query_lower in pattern.name.lower() or
                    query_lower in pattern.description.lower() or
                    query_lower in pattern.when_to_use.lower()):
                    results["patterns"].append(pattern)
        
        return results
    
    def get_recommendations_for_niche(self, niche: str) -> Dict[str, List[Any]]:
        """Get technique recommendations for a specific niche."""
        return {
            "hooks": self.hooks.get_hooks_by_niche(niche),
            "structures": self.structures.get_structures_by_category(niche),
            "patterns": self.patterns.get_best_techniques()
        }
    
    def generate_complete_script_structure(self, 
                                         niche: str,
                                         hook_type: str,
                                         structure_type: str,
                                         video_length: int,
                                         topic: str) -> Dict[str, Any]:
        """Generate a complete script structure with all techniques."""
        
        # Get the specific techniques
        hook = self.hooks.get_hook(hook_type)
        structure = self.structures.get_structure(structure_type)
        engagement_plan = self.patterns.generate_engagement_plan(video_length)
        
        if not hook or not structure:
            return {}
        
        # Build complete structure
        script_structure = {
            "metadata": {
                "niche": niche,
                "topic": topic,
                "estimated_length": video_length,
                "hook_type": hook_type,
                "structure_type": structure_type
            },
            "hook": {
                "type": hook.name,
                "template": hook.template,
                "example": hook.examples[0] if hook.examples else "",
                "psychological_principle": hook.psychological_principle
            },
            "structure": {
                "name": structure.name,
                "sections": [
                    {
                        "name": section.name,
                        "purpose": section.purpose,
                        "duration_percentage": section.duration_percentage,
                        "key_elements": section.key_elements,
                        "estimated_duration": f"{section.duration_percentage * video_length:.1f} minutos"
                    }
                    for section in structure.sections
                ],
                "psychological_principle": structure.psychological_principle
            },
            "engagement_plan": engagement_plan,
            "recommended_techniques": {
                "pattern_interrupts": [
                    self.patterns.get_technique("pattern_interrupt").examples[0]
                ],
                "social_proof": [
                    self.patterns.get_technique("social_proof").examples[0]
                ],
                "interaction_prompts": [
                    self.patterns.get_technique("interaction_prompt").examples[0]
                ]
            }
        }
        
        return script_structure
    
    def export_to_json(self, file_path: str) -> None:
        """Export all techniques to JSON file."""
        data = {
            "hooks": {
                name: {
                    "name": hook.name,
                    "type": hook.hook_type.value,
                    "description": hook.description,
                    "template": hook.template,
                    "examples": hook.examples,
                    "effectiveness_score": hook.effectiveness_score,
                    "best_niches": hook.best_niches,
                    "psychological_principle": hook.psychological_principle
                }
                for name, hook in self.hooks.get_all_hooks().items()
            },
            "structures": {
                name: {
                    "name": structure.name,
                    "type": structure.structure_type.value,
                    "description": structure.description,
                    "sections": [
                        {
                            "name": section.name,
                            "purpose": section.purpose,
                            "duration_percentage": section.duration_percentage,
                            "key_elements": section.key_elements,
                            "examples": section.examples
                        }
                        for section in structure.sections
                    ],
                    "best_for": structure.best_for,
                    "engagement_score": structure.engagement_score,
                    "typical_duration": structure.typical_duration,
                    "psychological_principle": structure.psychological_principle
                }
                for name, structure in self.structures.get_all_structures().items()
            },
            "patterns": {
                name: {
                    "name": pattern.name,
                    "type": pattern.technique_type.value,
                    "description": pattern.description,
                    "when_to_use": pattern.when_to_use,
                    "template": pattern.template,
                    "examples": pattern.examples,
                    "effectiveness_score": pattern.effectiveness_score,
                    "timing_recommendations": pattern.timing_recommendations
                }
                for name, pattern in self.patterns.get_all_techniques().items()
            }
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get statistics about the technique database."""
        return {
            "total_hooks": len(self.hooks.get_all_hooks()),
            "total_structures": len(self.structures.get_all_structures()),
            "total_patterns": len(self.patterns.get_all_techniques()),
            "hook_types": list(set(hook.hook_type.value for hook in self.hooks.get_all_hooks().values())),
            "structure_types": list(set(structure.structure_type.value for structure in self.structures.get_all_structures().values())),
            "pattern_types": list(set(pattern.technique_type.value for pattern in self.patterns.get_all_techniques().values())),
            "supported_niches": list(set(
                niche for hook in self.hooks.get_all_hooks().values() 
                for niche in hook.best_niches
            ))
        }
    
    def validate_combination(self, hook_type: str, structure_type: str, niche: str) -> Dict[str, Any]:
        """Validate if a combination of techniques works well together."""
        hook = self.hooks.get_hook(hook_type)
        structure = self.structures.get_structure(structure_type)
        
        if not hook or not structure:
            return {"valid": False, "reason": "Hook ou estrutura não encontrada"}
        
        # Check if niche is compatible
        hook_compatible = niche in hook.best_niches
        structure_compatible = niche in structure.best_for
        
        score = (hook.effectiveness_score + structure.engagement_score) / 2
        
        return {
            "valid": True,
            "compatibility_score": score,
            "hook_compatible": hook_compatible,
            "structure_compatible": structure_compatible,
            "recommendations": [
                f"Hook effectiveness: {hook.effectiveness_score:.2f}",
                f"Structure engagement: {structure.engagement_score:.2f}",
                f"Combined score: {score:.2f}",
                f"Niche compatibility: Hook={hook_compatible}, Structure={structure_compatible}"
            ]
        }