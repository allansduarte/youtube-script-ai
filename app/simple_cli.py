"""
Simple CLI interface for testing when Gradio is not available.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from storytelling.technique_database import TechniqueDatabase


def simple_cli_interface():
    """Simple CLI interface for testing."""
    print("🎬 YouTube Script AI - CLI Interface")
    print("=" * 50)
    
    db = TechniqueDatabase()
    
    # Get available options
    hooks = list(db.hooks.get_all_hooks().keys())
    structures = list(db.structures.get_all_structures().keys())
    niches = ["tecnologia", "educacao", "negocios", "lifestyle", "entretenimento"]
    
    print(f"📊 Sistema carregado com:")
    print(f"   • {len(hooks)} tipos de hooks")
    print(f"   • {len(structures)} estruturas narrativas")
    print(f"   • {len(db.patterns.get_all_techniques())} padrões de engajamento")
    print()
    
    # Interactive input
    print("📝 Configure seu script:")
    topic = input("Tópico do vídeo: ") or "Como aprender programação do zero"
    
    print(f"\n🎯 Nichos disponíveis: {', '.join(niches)}")
    niche = input("Escolha o nicho (tecnologia): ") or "tecnologia"
    
    print(f"\n🎣 Hooks disponíveis: {', '.join(hooks[:3])}...")
    hook_type = input("Tipo de hook (curiosity_gap): ") or "curiosity_gap"
    
    print(f"\n📖 Estruturas disponíveis: {', '.join(structures[:3])}...")
    structure_type = input("Estrutura narrativa (problem_solution): ") or "problem_solution"
    
    video_length = input("Duração do vídeo em minutos (10): ") or "10"
    
    print("\n🚀 Gerando estrutura...")
    print("=" * 50)
    
    # Generate structure
    structure = db.generate_complete_script_structure(
        niche=niche,
        hook_type=hook_type,
        structure_type=structure_type,
        video_length=int(video_length),
        topic=topic
    )
    
    if structure:
        print(f"""
# 🎬 Estrutura de Script Gerada

## 📊 Metadados
- **Tópico**: {structure['metadata']['topic']}
- **Nicho**: {structure['metadata']['niche']}
- **Duração estimada**: {structure['metadata']['estimated_length']} minutos

## 🎣 Hook ({structure['hook']['type']})
**Template**: {structure['hook']['template']}
**Exemplo**: {structure['hook']['example']}

## 📖 Estrutura Narrativa ({structure['structure']['name']})
""")
        
        for i, section in enumerate(structure['structure']['sections'], 1):
            print(f"**{i}. {section['name']}** ({section['estimated_duration']})")
            print(f"   {section['purpose']}")
            print()
        
        print("✅ Estrutura gerada com sucesso!")
    else:
        print("❌ Erro ao gerar estrutura")
    
    print("\n🎉 Teste da interface CLI concluído!")


if __name__ == "__main__":
    simple_cli_interface()