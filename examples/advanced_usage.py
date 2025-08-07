"""
Advanced usage examples for YouTube Script AI.

This script demonstrates advanced features and use cases
for the YouTube Script AI system.
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from storytelling.technique_database import TechniqueDatabase
from generation.script_generator import ScriptGenerator, ScriptGenerationRequest
from data_processing.script_analyzer import ScriptAnalyzer


def example_niche_specific_optimization():
    """Example of optimizing scripts for specific niches."""
    print("🎯 Otimização por Nicho")
    print("=" * 50)
    
    db = TechniqueDatabase()
    generator = ScriptGenerator()
    
    # Different niches with optimized parameters
    niche_configs = {
        "tecnologia": {
            "hook_type": "curiosity_gap",
            "structure_type": "problem_solution",
            "tone": "educational",
            "audience": "intermediarios",
            "duration": 8
        },
        "negocios": {
            "hook_type": "controversy",
            "structure_type": "hero_journey",
            "tone": "professional",
            "audience": "geral",
            "duration": 12
        },
        "lifestyle": {
            "hook_type": "personal_story",
            "structure_type": "before_after",
            "tone": "casual",
            "audience": "geral",
            "duration": 6
        }
    }
    
    for niche, config in niche_configs.items():
        print(f"\n📊 Configuração para {niche.title()}:")
        print(f"   Hook: {config['hook_type']}")
        print(f"   Estrutura: {config['structure_type']}")
        print(f"   Tom: {config['tone']}")
        print(f"   Audiência: {config['audience']}")
        
        # Get recommendations for this niche
        recommendations = db.get_recommendations_for_niche(niche)
        print(f"   Hooks recomendados: {len(recommendations['hooks'])}")
        print(f"   Estruturas recomendadas: {len(recommendations['structures'])}")


def example_tone_comparison():
    """Example comparing different tones for the same topic."""
    print("\n🎭 Comparação de Tons")
    print("=" * 50)
    
    generator = ScriptGenerator()
    base_topic = "Como aumentar produtividade"
    
    tones = ["casual", "professional", "enthusiastic", "educational"]
    
    for tone in tones:
        request = ScriptGenerationRequest(
            topic=base_topic,
            niche="desenvolvimento_pessoal",
            hook_type="statistics_shock",
            structure_type="list_format",
            target_duration=5,
            tone=tone,
            target_audience="geral"
        )
        
        script = generator.generate_script(request)
        
        print(f"\n📝 Tom: {tone.title()}")
        print(f"   Qualidade: {script.quality_score:.2f}")
        print(f"   Duração: {script.estimated_duration:.1f} min")
        print(f"   Preview: {script.script_text[:100]}...")


def example_audience_adaptation():
    """Example of adapting content for different audiences."""
    print("\n👥 Adaptação de Audiência")
    print("=" * 50)
    
    generator = ScriptGenerator()
    topic = "Introdução ao Machine Learning"
    
    audiences = {
        "iniciantes": "Explicações detalhadas, vocabulário simples",
        "intermediarios": "Conceitos práticos, vocabulário técnico",
        "avancados": "Foco em aplicações, vocabulário expert",
        "geral": "Equilibrio entre acessibilidade e profundidade"
    }
    
    for audience, description in audiences.items():
        print(f"\n🎓 Audiência: {audience.title()}")
        print(f"   Estratégia: {description}")
        
        request = ScriptGenerationRequest(
            topic=topic,
            niche="tecnologia",
            hook_type="curiosity_gap",
            structure_type="problem_solution",
            target_duration=10,
            tone="educational",
            target_audience=audience
        )
        
        script = generator.generate_script(request)
        print(f"   Qualidade gerada: {script.quality_score:.2f}")
        print(f"   Técnicas usadas: {len(script.techniques_used)}")


def example_quality_optimization():
    """Example of optimizing script quality through iterations."""
    print("\n⚡ Otimização de Qualidade")
    print("=" * 50)
    
    generator = ScriptGenerator()
    analyzer = ScriptAnalyzer()
    
    # Generate initial script
    request = ScriptGenerationRequest(
        topic="5 erros comuns em programação",
        niche="tecnologia",
        hook_type="statistics_shock",
        structure_type="list_format",
        target_duration=8,
        tone="casual",
        target_audience="iniciantes"
    )
    
    print("🔄 Gerando e analisando script inicial...")
    script = generator.generate_script(request)
    analysis = analyzer.analyze_script(script.script_text, "optimization_test")
    
    print(f"📊 Análise inicial:")
    print(f"   Qualidade: {script.quality_score:.2f}")
    print(f"   Engajamento: {analysis.engagement_score:.2f}")
    print(f"   Hooks identificados: {len(analysis.identified_techniques['hooks'])}")
    print(f"   Padrões de engajamento: {len(analysis.identified_techniques['engagement'])}")
    
    print(f"\n💡 Recomendações de melhoria:")
    for i, rec in enumerate(analysis.recommendations[:3], 1):
        print(f"   {i}. {rec}")
    
    # Generate improved version with different parameters
    print(f"\n🔄 Gerando versão melhorada...")
    improved_request = ScriptGenerationRequest(
        topic=request.topic,
        niche=request.niche,
        hook_type="curiosity_gap",  # Changed from statistics_shock
        structure_type=request.structure_type,
        target_duration=request.target_duration,
        tone="enthusiastic",  # Changed from casual
        target_audience=request.target_audience,
        custom_context={
            "something shocking": "95% dos programadores cometem esses 5 erros básicos",
            "contradicts expectation": "mesmo tendo anos de experiência"
        }
    )
    
    improved_script = generator.generate_script(improved_request)
    improved_analysis = analyzer.analyze_script(improved_script.script_text, "optimization_improved")
    
    print(f"📊 Análise melhorada:")
    print(f"   Qualidade: {improved_script.quality_score:.2f} (+{improved_script.quality_score - script.quality_score:.2f})")
    print(f"   Engajamento: {improved_analysis.engagement_score:.2f} (+{improved_analysis.engagement_score - analysis.engagement_score:.2f})")
    
    return script, improved_script


def example_batch_generation():
    """Example of generating multiple scripts in batch."""
    print("\n📦 Geração em Lote")
    print("=" * 50)
    
    generator = ScriptGenerator()
    
    # Topics for tech channel
    topics = [
        "Como escolher sua primeira linguagem de programação",
        "5 ferramentas que todo desenvolvedor precisa conhecer",
        "Carreira em tech: por onde começar",
        "GitHub para iniciantes: guia completo",
        "Como se preparar para entrevistas de programação"
    ]
    
    print(f"🚀 Gerando {len(topics)} scripts para canal de tecnologia...")
    
    scripts = []
    total_quality = 0
    
    for i, topic in enumerate(topics, 1):
        request = ScriptGenerationRequest(
            topic=topic,
            niche="tecnologia",
            hook_type=["curiosity_gap", "statistics_shock", "question_direct"][i % 3],
            structure_type=["problem_solution", "list_format", "hero_journey"][i % 3],
            target_duration=8,
            tone="educational",
            target_audience="iniciantes"
        )
        
        script = generator.generate_script(request)
        scripts.append(script)
        total_quality += script.quality_score
        
        print(f"   {i}. {topic[:40]}... | Qualidade: {script.quality_score:.2f}")
    
    avg_quality = total_quality / len(scripts)
    print(f"\n📊 Resultados do lote:")
    print(f"   Scripts gerados: {len(scripts)}")
    print(f"   Qualidade média: {avg_quality:.2f}")
    print(f"   Duração total estimada: {sum(s.estimated_duration for s in scripts):.1f} min")
    
    return scripts


def example_technique_analysis():
    """Example of analyzing which techniques work best."""
    print("\n🔬 Análise de Técnicas")
    print("=" * 50)
    
    db = TechniqueDatabase()
    
    # Analyze technique effectiveness by niche
    niches = ["tecnologia", "negocios", "educacao", "lifestyle"]
    
    for niche in niches:
        print(f"\n📊 Análise para {niche.title()}:")
        
        recommendations = db.get_recommendations_for_niche(niche)
        
        # Get best hooks for this niche
        niche_hooks = [h for h in recommendations['hooks'] if niche in h.best_niches]
        if niche_hooks:
            best_hook = max(niche_hooks, key=lambda h: h.effectiveness_score)
            print(f"   Melhor hook: {best_hook.name} (score: {best_hook.effectiveness_score})")
        
        # Get best structures
        niche_structures = [s for s in recommendations['structures'] if niche in s.best_for]
        if niche_structures:
            best_structure = max(niche_structures, key=lambda s: s.engagement_score)
            print(f"   Melhor estrutura: {best_structure.name} (score: {best_structure.engagement_score})")
        
        # Validate combinations
        if niche_hooks and niche_structures:
            validation = db.validate_combination(
                best_hook.hook_type.value,
                best_structure.structure_type.value,
                niche
            )
            print(f"   Compatibilidade: {validation['compatibility_score']:.2f}")


def example_export_and_import():
    """Example of exporting and importing techniques."""
    print("\n💾 Export/Import de Técnicas")
    print("=" * 50)
    
    db = TechniqueDatabase()
    
    # Export techniques to JSON
    export_path = "/tmp/storytelling_techniques_export.json"
    print(f"📤 Exportando técnicas para {export_path}...")
    db.export_to_json(export_path)
    print("✅ Export concluído!")
    
    # Show statistics
    stats = db.get_statistics()
    print(f"\n📊 Estatísticas do sistema:")
    for key, value in stats.items():
        if isinstance(value, list):
            print(f"   {key}: {len(value)} itens")
        else:
            print(f"   {key}: {value}")


def main():
    """Run all advanced examples."""
    print("🎬 YouTube Script AI - Exemplos Avançados")
    print("=" * 60)
    
    try:
        example_niche_specific_optimization()
        example_tone_comparison()
        example_audience_adaptation()
        script, improved_script = example_quality_optimization()
        scripts = example_batch_generation()
        example_technique_analysis()
        example_export_and_import()
        
        print("\n" + "=" * 60)
        print("🎉 Todos os exemplos avançados executados com sucesso!")
        print("\n💡 Principais aprendizados:")
        print("   • Diferentes nichos requerem abordagens específicas")
        print("   • Tom pode impactar significativamente a qualidade")
        print("   • Adaptação de audiência melhora relevância")
        print("   • Iteração e análise melhoram resultados")
        print("   • Geração em lote otimiza produtividade")
        print("   • Análise de técnicas guia otimizações")
        
        return 0
        
    except Exception as e:
        print(f"❌ Erro durante execução avançada: {e}")
        return 1


if __name__ == "__main__":
    exit(main())