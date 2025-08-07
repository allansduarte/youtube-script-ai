"""
Basic tests for YouTube Script AI functionality.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from storytelling.technique_database import TechniqueDatabase
from storytelling.hook_techniques import HookTechniques
from storytelling.narrative_structures import NarrativeStructures
from storytelling.engagement_patterns import EngagementPatterns


class TestStorytellingComponents:
    """Test storytelling components."""
    
    def test_hook_techniques_initialization(self):
        """Test that hook techniques initialize correctly."""
        hooks = HookTechniques()
        assert len(hooks.get_all_hooks()) > 0
        
        # Test specific hook retrieval
        curiosity_hook = hooks.get_hook("curiosity_gap")
        assert curiosity_hook is not None
        assert curiosity_hook.name == "Curiosity Gap"
    
    def test_narrative_structures_initialization(self):
        """Test that narrative structures initialize correctly."""
        structures = NarrativeStructures()
        assert len(structures.get_all_structures()) > 0
        
        # Test specific structure retrieval
        hero_journey = structures.get_structure("hero_journey")
        assert hero_journey is not None
        assert hero_journey.name == "Jornada do Herói"
    
    def test_engagement_patterns_initialization(self):
        """Test that engagement patterns initialize correctly."""
        patterns = EngagementPatterns()
        assert len(patterns.get_all_techniques()) > 0
        
        # Test specific pattern retrieval
        pattern_interrupt = patterns.get_technique("pattern_interrupt")
        assert pattern_interrupt is not None
        assert pattern_interrupt.name == "Pattern Interrupt"
    
    def test_technique_database_integration(self):
        """Test that technique database integrates all components."""
        db = TechniqueDatabase()
        
        # Test statistics
        stats = db.get_statistics()
        assert stats["total_hooks"] > 0
        assert stats["total_structures"] > 0
        assert stats["total_patterns"] > 0
        
        # Test script structure generation
        structure = db.generate_complete_script_structure(
            niche="tecnologia",
            hook_type="curiosity_gap",
            structure_type="problem_solution",
            video_length=10,
            topic="Como aprender Python"
        )
        
        assert structure is not None
        assert "metadata" in structure
        assert "hook" in structure
        assert "structure" in structure
        assert structure["metadata"]["topic"] == "Como aprender Python"
    
    def test_hook_generation_with_context(self):
        """Test hook generation with context."""
        hooks = HookTechniques()
        
        context = {
            "something shocking": "95% das pessoas aprendem Python errado",
            "contradicts expectation": "pensam que precisam decorar sintaxe"
        }
        
        generated_hook = hooks.generate_hook("curiosity_gap", context)
        assert "95% das pessoas aprendem Python errado" in generated_hook
        assert "pensam que precisam decorar sintaxe" in generated_hook
    
    def test_niche_filtering(self):
        """Test filtering techniques by niche."""
        db = TechniqueDatabase()
        
        tech_recommendations = db.get_recommendations_for_niche("tecnologia")
        assert "hooks" in tech_recommendations
        assert "structures" in tech_recommendations
        assert "patterns" in tech_recommendations
        
        # Check that we get relevant hooks for tech niche
        tech_hooks = tech_recommendations["hooks"]
        assert len(tech_hooks) > 0
    
    def test_search_functionality(self):
        """Test search across all techniques."""
        db = TechniqueDatabase()
        
        # Search for curiosity-related techniques
        results = db.search_techniques("curiosity")
        assert len(results["hooks"]) > 0 or len(results["patterns"]) > 0
        
        # Search for problem-related techniques
        results = db.search_techniques("problem")
        assert len(results["structures"]) > 0


if __name__ == "__main__":
    # Run basic tests if executed directly
    test_class = TestStorytellingComponents()
    
    print("Running basic functionality tests...")
    
    try:
        test_class.test_hook_techniques_initialization()
        print("✅ Hook techniques test passed")
        
        test_class.test_narrative_structures_initialization()
        print("✅ Narrative structures test passed")
        
        test_class.test_engagement_patterns_initialization()
        print("✅ Engagement patterns test passed")
        
        test_class.test_technique_database_integration()
        print("✅ Technique database test passed")
        
        test_class.test_hook_generation_with_context()
        print("✅ Hook generation test passed")
        
        test_class.test_niche_filtering()
        print("✅ Niche filtering test passed")
        
        test_class.test_search_functionality()
        print("✅ Search functionality test passed")
        
        print("\n🎉 All tests passed! System is working correctly.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)