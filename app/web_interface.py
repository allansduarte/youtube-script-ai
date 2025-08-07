"""
Web interface for YouTube Script AI using Gradio.

This module provides a user-friendly web interface for generating
YouTube scripts with storytelling techniques.
"""

import os
import sys
import gradio as gr
import yaml
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from storytelling.technique_database import TechniqueDatabase


class ScriptGeneratorInterface:
    """Main interface for script generation."""
    
    def __init__(self):
        self.db = TechniqueDatabase()
        self.config = self._load_config()
    
    def _load_config(self):
        """Load configuration."""
        config_path = Path(__file__).parent.parent / "config.yaml"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {"interface": {"port": 7860, "share": False, "debug": False}}
    
    def generate_script_structure(self, topic, niche, hook_type, structure_type, video_length):
        """Generate script structure based on user inputs."""
        try:
            structure = self.db.generate_complete_script_structure(
                niche=niche,
                hook_type=hook_type,
                structure_type=structure_type,
                video_length=int(video_length),
                topic=topic
            )
            
            if not structure:
                return "❌ Erro ao gerar estrutura. Verifique os parâmetros."
            
            # Format output
            output = f"""
# 🎬 Estrutura de Script Gerada

## 📊 Metadados
- **Tópico**: {structure['metadata']['topic']}
- **Nicho**: {structure['metadata']['niche']}
- **Duração estimada**: {structure['metadata']['estimated_length']} minutos
- **Tipo de Hook**: {structure['metadata']['hook_type']}
- **Estrutura**: {structure['metadata']['structure_type']}

## 🎣 Hook ({structure['hook']['type']})
**Princípio Psicológico**: {structure['hook']['psychological_principle']}

**Template**: {structure['hook']['template']}

**Exemplo**: {structure['hook']['example']}

## 📖 Estrutura Narrativa ({structure['structure']['name']})
**Princípio Psicológico**: {structure['structure']['psychological_principle']}

"""
            
            for i, section in enumerate(structure['structure']['sections'], 1):
                output += f"""
### {i}. {section['name']} ({section['estimated_duration']})
**Propósito**: {section['purpose']}

**Elementos-chave**:
{chr(10).join([f"- {element}" for element in section['key_elements']])}

**Duração**: {section['duration_percentage']*100:.1f}% do vídeo
"""
            
            output += f"""
## 🎯 Plano de Engajamento
"""
            
            for timestamp, techniques in structure['engagement_plan'].items():
                output += f"- **{timestamp} min**: {', '.join(techniques)}\n"
            
            output += f"""
## 💡 Técnicas Recomendadas

**Pattern Interrupts**: {structure['recommended_techniques']['pattern_interrupts'][0]}

**Social Proof**: {structure['recommended_techniques']['social_proof'][0]}

**Interaction Prompts**: {structure['recommended_techniques']['interaction_prompts'][0]}
"""
            
            return output
            
        except Exception as e:
            return f"❌ Erro ao gerar estrutura: {str(e)}"
    
    def get_available_options(self):
        """Get available options for dropdowns."""
        hooks = list(self.db.hooks.get_all_hooks().keys())
        structures = list(self.db.structures.get_all_structures().keys())
        niches = self.config.get("data_collection", {}).get("niches", 
                                ["tecnologia", "educacao", "negocios", "lifestyle", "entretenimento"])
        
        return hooks, structures, niches
    
    def create_interface(self):
        """Create the Gradio interface."""
        hooks, structures, niches = self.get_available_options()
        
        with gr.Blocks(title="YouTube Script AI", theme=gr.themes.Soft()) as interface:
            gr.Markdown("""
            # 🎬 YouTube Script AI
            ## Pipeline Completo para Geração de Scripts com Storytelling
            
            Generate scripts profissionais para YouTube utilizando técnicas avançadas de storytelling
            e estruturas narrativas comprovadas.
            """)
            
            with gr.Row():
                with gr.Column():
                    topic_input = gr.Textbox(
                        label="📝 Tópico do Vídeo",
                        placeholder="Ex: Como aprender programação do zero",
                        value="Como aprender programação do zero"
                    )
                    
                    niche_dropdown = gr.Dropdown(
                        choices=niches,
                        label="🎯 Nicho",
                        value=niches[0]
                    )
                    
                    hook_dropdown = gr.Dropdown(
                        choices=hooks,
                        label="🎣 Tipo de Hook",
                        value=hooks[0]
                    )
                    
                    structure_dropdown = gr.Dropdown(
                        choices=structures,
                        label="📖 Estrutura Narrativa",
                        value=structures[0]
                    )
                    
                    length_slider = gr.Slider(
                        minimum=3,
                        maximum=20,
                        value=10,
                        step=1,
                        label="⏱️ Duração do Vídeo (minutos)"
                    )
                    
                    generate_btn = gr.Button("🚀 Gerar Estrutura", variant="primary")
                
                with gr.Column():
                    output_display = gr.Markdown(
                        label="📄 Estrutura Gerada",
                        value="👆 Preencha os campos ao lado e clique em 'Gerar Estrutura'"
                    )
            
            # Connect the button to the generation function
            generate_btn.click(
                fn=self.generate_script_structure,
                inputs=[topic_input, niche_dropdown, hook_dropdown, structure_dropdown, length_slider],
                outputs=[output_display]
            )
            
            # Add examples
            gr.Markdown("""
            ## 💡 Exemplos de Uso
            
            **Tecnologia**: "Os 5 melhores apps que você precisa conhecer em 2024"
            **Educação**: "Como estudar para concursos de forma eficiente"
            **Negócios**: "Como começar um negócio online do zero"
            **Lifestyle**: "Minha rotina matinal que mudou minha vida"
            **Entretenimento**: "Reagindo aos memes mais virais da semana"
            """)
        
        return interface


def launch_interface():
    """Launch the web interface."""
    generator = ScriptGeneratorInterface()
    interface = generator.create_interface()
    
    config = generator.config.get("interface", {})
    
    interface.launch(
        server_port=config.get("port", 7860),
        share=config.get("share", False),
        debug=config.get("debug", False),
        server_name="0.0.0.0"  # Allow external access
    )


if __name__ == "__main__":
    launch_interface()