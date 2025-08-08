"""
Simple CLI interface for testing when Gradio is not available.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from storytelling.technique_database import TechniqueDatabase
from generation.script_generator import ScriptGenerator, ScriptGenerationRequest


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
    
    print("\n📋 Descrição (opcional - pressione Enter para pular):")
    print("   Forneça contexto adicional sobre seu objetivo, situação ou necessidade específica")
    description = input("Descrição: ").strip()
    
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
- **Tópico**: {structure['metadata']['topic']}""")
        
        if description:
            print(f"- **Descrição**: {description}")
        
        print(f"""- **Nicho**: {structure['metadata']['niche']}
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
        
        # Ask if user wants to generate complete script
        print("\n🚀 Gerar script completo? (s/n):")
        generate_complete = input().lower().strip()
        
        if generate_complete in ['s', 'sim', 'y', 'yes']:
            print("\n📝 Configurações adicionais para o script:")
            tone = input("Tom (casual/professional/enthusiastic/educational): ") or "casual"
            audience = input("Audiência (iniciantes/intermediarios/avancados/geral): ") or "geral"
            include_cta = input("Incluir call-to-action? (s/n): ").lower().strip() not in ['n', 'nao', 'no']
            
            print("\n🎬 Gerando script completo...")
            print("=" * 50)
            
            try:
                generator = ScriptGenerator()
                request = ScriptGenerationRequest(
                    topic=topic,
                    niche=niche,
                    hook_type=hook_type,
                    structure_type=structure_type,
                    target_duration=int(video_length),
                    tone=tone,
                    target_audience=audience,
                    include_cta=include_cta,
                    description=description
                )
                
                script = generator.generate_script(request)
                
                print(f"""
# 🎬 Script Completo Gerado

## 📊 Metadados
- **Tópico**: {script.metadata['topic']}""")
                
                if script.metadata.get('description'):
                    print(f"- **Descrição**: {script.metadata['description']}")
                
                print(f"""- **Tom**: {script.metadata['tone']}
- **Audiência**: {script.metadata['target_audience']}
- **Duração estimada**: {script.estimated_duration:.1f} minutos
- **Score de qualidade**: {script.quality_score:.2f}/1.0

## 📝 Script Completo

{script.script_text}

✅ Script completo gerado com sucesso!
""")
            except Exception as e:
                print(f"❌ Erro ao gerar script completo: {e}")
    else:
        print("❌ Erro ao gerar estrutura")
    
    print("\n🎉 Teste da interface CLI concluído!")


if __name__ == "__main__":
    simple_cli_interface()