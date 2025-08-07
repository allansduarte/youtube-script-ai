"""Main entry point for the YouTube Script AI application."""

import os
import sys
import argparse
import logging
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from storytelling.technique_database import TechniqueDatabase


def setup_logging():
    """Setup logging configuration."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('youtube_script_ai.log')
        ]
    )


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="YouTube Script AI - Hybrid LLM Training Pipeline")
    parser.add_argument("--mode", choices=["collect", "train", "generate", "interface"], 
                       default="interface", help="Operation mode")
    parser.add_argument("--config", default="config.yaml", help="Configuration file path")
    parser.add_argument("--niche", default="tecnologia", help="Content niche")
    parser.add_argument("--topic", default="", help="Specific topic for generation")
    
    args = parser.parse_args()
    
    setup_logging()
    logger = logging.getLogger(__name__)
    
    logger.info("Starting YouTube Script AI")
    logger.info(f"Mode: {args.mode}")
    
    if args.mode == "interface":
        # Add app directory to path
        sys.path.insert(0, str(Path(__file__).parent.parent / "app"))
        from web_interface import launch_interface
        launch_interface()
    
    elif args.mode == "collect":
        logger.info("Data collection mode not yet implemented")
        
    elif args.mode == "train":
        logger.info("Training mode not yet implemented")
        
    elif args.mode == "generate":
        # Script generation mode
        if args.topic:
            from generation.script_generator import ScriptGenerator, ScriptGenerationRequest
            
            generator = ScriptGenerator()
            request = ScriptGenerationRequest(
                topic=args.topic,
                niche=args.niche,
                hook_type="curiosity_gap",
                structure_type="problem_solution",
                target_duration=10,
                tone="casual",
                target_audience="geral",
                include_cta=True
            )
            
            script = generator.generate_script(request)
            
            print("\n=== SCRIPT COMPLETO GERADO ===\n")
            print(f"Tópico: {script.metadata['topic']}")
            print(f"Qualidade: {script.quality_score:.2f}/1.0")
            print(f"Duração estimada: {script.estimated_duration:.1f} minutos")
            print(f"Técnicas usadas: {len(script.techniques_used)}")
            print(f"\n--- SCRIPT ---\n")
            print(script.script_text)
            print(f"\n--- FIM DO SCRIPT ---\n")
        else:
            # Quick generation example
            db = TechniqueDatabase()
            structure = db.generate_complete_script_structure(
                niche=args.niche,
                hook_type="curiosity_gap",
                structure_type="problem_solution",
                video_length=10,
                topic=args.topic or "Como aprender programação"
            )
            
            print("\n=== ESTRUTURA DE SCRIPT GERADA ===\n")
            print(f"Tópico: {structure['metadata']['topic']}")
            print(f"Nicho: {structure['metadata']['niche']}")
            print(f"Duração estimada: {structure['metadata']['estimated_length']} minutos")
            print(f"\nHook ({structure['hook']['type']}):")
            print(f"Template: {structure['hook']['template']}")
            print(f"Exemplo: {structure['hook']['example']}")
            print(f"\nEstrutura ({structure['structure']['name']}):")
            for section in structure['structure']['sections']:
                print(f"- {section['name']}: {section['purpose']} ({section['estimated_duration']})")


if __name__ == "__main__":
    main()