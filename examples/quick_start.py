"""
Example usage of the YouTube Script AI system.

This script demonstrates how to use the various components
of the system to generate and analyze YouTube scripts.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from storytelling.technique_database import TechniqueDatabase
from generation.script_generator import ScriptGenerator, ScriptGenerationRequest
from data_processing.script_analyzer import ScriptAnalyzer


def example_basic_usage():
    """Example of basic system usage."""
    print("🎬 YouTube Script AI - Exemplo Básico")
    print("=" * 50)
    
    # 1. Initialize the technique database
    db = TechniqueDatabase()
    
    # 2. Get system statistics
    stats = db.get_statistics()
    print(f"📊 Sistema carregado:")
    print(f"   • {stats['total_hooks']} tipos de hooks")
    print(f"   • {stats['total_structures']} estruturas narrativas")
    print(f"   • {stats['total_patterns']} padrões de engajamento")
    print()
    
    # 3. Generate a script structure
    print("🏗️ Gerando estrutura de script...")
    structure = db.generate_complete_script_structure(
        niche="tecnologia",
        hook_type="curiosity_gap",
        structure_type="problem_solution",
        video_length=8,
        topic="Como aprender Python de forma eficiente"
    )
    
    print(f"✅ Estrutura gerada para: {structure['metadata']['topic']}")
    print(f"   Hook: {structure['hook']['type']}")
    print(f"   Estrutura: {structure['structure']['name']}")
    print(f"   Duração: {structure['metadata']['estimated_length']} minutos")
    print()


def example_script_generation():
    """Example of complete script generation."""
    print("📝 Geração Completa de Script")
    print("=" * 50)
    
    # Initialize generator
    generator = ScriptGenerator()
    
    # Create generation request
    request = ScriptGenerationRequest(
        topic="Como aprender Python do zero em 30 dias",
        niche="tecnologia",
        hook_type="curiosity_gap",
        structure_type="problem_solution",
        target_duration=10,
        tone="casual",
        target_audience="iniciantes",
        include_cta=True,
        custom_context={
            "something shocking": "90% das pessoas desistem de Python na primeira semana",
            "contradicts expectation": "tentam aprender tudo ao mesmo tempo"
        }
    )
    
    # Generate script
    print("🚀 Gerando script completo...")
    script = generator.generate_script(request)
    
    print(f"✅ Script gerado!")
    print(f"   Qualidade: {script.quality_score:.2f}/1.0")
    print(f"   Duração estimada: {script.estimated_duration:.1f} minutos")
    print(f"   Técnicas usadas: {len(script.techniques_used)}")
    print()
    
    print("📄 Script gerado:")
    print("-" * 30)
    print(script.script_text)
    print("-" * 30)
    print()
    
    return script


def example_script_analysis():
    """Example of script analysis."""
    print("🔍 Análise de Script")
    print("=" * 50)
    
    # Sample script for analysis
    sample_script = """
    Galera, eu descobri que 90% das pessoas aprendem Python de forma totalmente errada. 
    E isso me fez perder meses tentando entender conceitos básicos.
    
    O problema é que todo mundo foca na sintaxe. Você passa horas decorando como escrever 
    um loop, mas não entende quando usar. Isso é como tentar dirigir decorando todas as 
    peças do carro.
    
    A solução que mudou tudo para mim foi começar com projetos reais. Em vez de fazer 
    exercícios chatos, comecei construindo um site simples. E sabe o que aconteceu? 
    Aprendi mais em uma semana do que em meses estudando teoria.
    
    Primeiro, escolha um projeto que te empolga. Pode ser um site, um jogo simples, 
    ou até um bot para WhatsApp. Depois, aprenda apenas o que precisa para esse projeto. 
    Isso te força a entender o propósito de cada linha de código.
    
    O resultado? Em 30 dias eu já estava criando meus próprios programas. E você também pode.
    
    Se esse vídeo foi útil, deixa aquele like. Se inscreve no canal e ativa o sininho. 
    E comenta embaixo: qual projeto você quer criar com Python?
    """
    
    # Initialize analyzer
    analyzer = ScriptAnalyzer()
    
    # Analyze script
    print("🔍 Analisando script...")
    analysis = analyzer.analyze_script(sample_script, "example_video")
    
    print(f"✅ Análise concluída!")
    print(f"   Score de engajamento: {analysis.engagement_score:.2f}/1.0")
    print(f"   Hooks identificados: {analysis.identified_techniques['hooks']}")
    print(f"   Padrões de engajamento: {analysis.identified_techniques['engagement']}")
    print(f"   Elementos de história: {analysis.identified_techniques['story_elements']}")
    print()
    
    print("💡 Recomendações:")
    for i, rec in enumerate(analysis.recommendations, 1):
        print(f"   {i}. {rec}")
    print()
    
    return analysis


def example_technique_search():
    """Example of searching for specific techniques."""
    print("🔍 Busca por Técnicas")
    print("=" * 50)
    
    db = TechniqueDatabase()
    
    # Search for curiosity-related techniques
    print("🎣 Buscando técnicas relacionadas a 'curiosidade':")
    results = db.search_techniques("curiosidade")
    
    for category, techniques in results.items():
        if techniques:
            print(f"   {category.title()}: {len(techniques)} encontradas")
            for technique in techniques[:2]:  # Show first 2
                if hasattr(technique, 'name'):
                    print(f"     - {technique.name}")
    print()
    
    # Get recommendations for a specific niche
    print("🎯 Recomendações para nicho 'tecnologia':")
    recommendations = db.get_recommendations_for_niche("tecnologia")
    
    print(f"   Hooks recomendados: {len(recommendations['hooks'])}")
    for hook in recommendations['hooks'][:2]:
        print(f"     - {hook.name} (score: {hook.effectiveness_score})")
    print()


def example_multiple_variations():
    """Example of generating multiple script variations."""
    print("🎭 Múltiplas Variações")
    print("=" * 50)
    
    generator = ScriptGenerator()
    
    request = ScriptGenerationRequest(
        topic="5 dicas para programar melhor",
        niche="tecnologia", 
        hook_type="statistics_shock",
        structure_type="list_format",
        target_duration=6,
        tone="enthusiastic",
        target_audience="intermediarios"
    )
    
    print("🚀 Gerando 3 variações do mesmo script...")
    variations = generator.generate_multiple_variations(request, count=3)
    
    for i, script in enumerate(variations, 1):
        print(f"   Variação {i}: {script.quality_score:.2f} qualidade, "
              f"{script.estimated_duration:.1f} min")
    
    print(f"✅ {len(variations)} variações geradas!")
    print()


def main():
    """Run all examples."""
    print("🎬 YouTube Script AI - Exemplos Completos")
    print("=" * 60)
    print()
    
    try:
        # Run examples
        example_basic_usage()
        script = example_script_generation()
        analysis = example_script_analysis()
        example_technique_search()
        example_multiple_variations()
        
        print("🎉 Todos os exemplos executados com sucesso!")
        print()
        print("💡 Próximos passos:")
        print("   1. Explore a interface web: python src/main.py --mode interface")
        print("   2. Gere seus próprios scripts: python src/main.py --mode generate")
        print("   3. Consulte a documentação em docs/")
        
    except Exception as e:
        print(f"❌ Erro durante execução: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())