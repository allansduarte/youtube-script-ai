"""
Tests for web interface integration with ScriptGenerator.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from storytelling.technique_database import TechniqueDatabase
from generation.script_generator import ScriptGenerator, ScriptGenerationRequest


class TestWebIntegration:
    """Test integration between TechniqueDatabase and ScriptGenerator."""
    
    def test_structure_to_script_pipeline(self):
        """Test complete pipeline from structure generation to script generation."""
        # Initialize components
        db = TechniqueDatabase()
        generator = ScriptGenerator()
        
        # Generate structure first (current Tab 1 functionality)
        structure = db.generate_complete_script_structure(
            niche="tecnologia",
            hook_type="curiosity_gap",
            structure_type="problem_solution",
            video_length=10,
            topic="Como aprender Python do zero"
        )
        
        assert structure is not None
        assert "metadata" in structure
        assert structure["metadata"]["topic"] == "Como aprender Python do zero"
        
        # Create script generation request (new Tab 2 functionality)
        request = ScriptGenerationRequest(
            topic=structure["metadata"]["topic"],
            niche=structure["metadata"]["niche"],
            hook_type=structure["metadata"]["hook_type"],
            structure_type=structure["metadata"]["structure_type"],
            target_duration=structure["metadata"]["estimated_length"],
            tone="casual",
            target_audience="iniciantes",
            include_cta=True
        )
        
        # Generate complete script
        script = generator.generate_script(request)
        
        assert script is not None
        assert script.script_text is not None
        assert len(script.script_text) > 0
        assert script.quality_score > 0
        assert script.estimated_duration > 0
        assert len(script.techniques_used) > 0
        
        # Verify metadata consistency
        assert script.metadata["topic"] == request.topic
        assert script.metadata["niche"] == request.niche
        assert script.metadata["tone"] == request.tone
        assert script.metadata["target_audience"] == request.target_audience
        
        print(f"✅ Generated script with {len(script.script_text.split())} words")
        print(f"✅ Quality score: {script.quality_score:.2f}")
        print(f"✅ Estimated duration: {script.estimated_duration:.1f} minutes")
    
    def test_different_tones_and_audiences(self):
        """Test script generation with different tone and audience combinations."""
        generator = ScriptGenerator()
        
        test_cases = [
            ("casual", "iniciantes"),
            ("professional", "intermediarios"),
            ("enthusiastic", "geral"),
            ("educational", "avancados")
        ]
        
        for tone, audience in test_cases:
            request = ScriptGenerationRequest(
                topic="Como criar um canal no YouTube",
                niche="tecnologia",
                hook_type="curiosity_gap",
                structure_type="problem_solution",
                target_duration=8,
                tone=tone,
                target_audience=audience,
                include_cta=True
            )
            
            script = generator.generate_script(request)
            
            assert script is not None
            assert script.metadata["tone"] == tone
            assert script.metadata["target_audience"] == audience
            assert len(script.script_text) > 0
            
            print(f"✅ Generated script for tone='{tone}', audience='{audience}'")
    
    def test_script_structure_breakdown(self):
        """Test that generated script has proper structure breakdown."""
        generator = ScriptGenerator()
        
        request = ScriptGenerationRequest(
            topic="Melhores práticas de programação",
            niche="tecnologia",
            hook_type="statistics_shock",
            structure_type="hero_journey",
            target_duration=12,
            tone="educational",
            target_audience="intermediarios",
            include_cta=True
        )
        
        script = generator.generate_script(request)
        
        # Check structure breakdown
        assert len(script.structure_breakdown) > 0
        
        # Should have hook section
        hook_sections = [k for k in script.structure_breakdown.keys() if "hook" in k]
        assert len(hook_sections) > 0
        
        # Should have content sections  
        content_sections = [k for k in script.structure_breakdown.keys() if "section_" in k]
        assert len(content_sections) > 0
        
        # Should have conclusion if CTA is included
        conclusion_sections = [k for k in script.structure_breakdown.keys() if "conclusion" in k]
        assert len(conclusion_sections) > 0
        
        print(f"✅ Script has {len(script.structure_breakdown)} sections")
        for section, info in script.structure_breakdown.items():
            print(f"   - {section}: {info}")


if __name__ == "__main__":
    # Run integration tests if executed directly
    test_class = TestWebIntegration()
    
    print("Running web integration tests...")
    
    try:
        test_class.test_structure_to_script_pipeline()
        print("✅ Structure to script pipeline test passed")
        
        test_class.test_different_tones_and_audiences()
        print("✅ Different tones and audiences test passed")
        
        test_class.test_script_structure_breakdown()
        print("✅ Script structure breakdown test passed")
        
        print("\n🎉 All integration tests passed! Ready for web interface implementation.")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        sys.exit(1)