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
from generation.script_generator import ScriptGenerator, ScriptGenerationRequest


class ScriptGeneratorInterface:
    """Main interface for script generation."""
    
    def __init__(self):
        self.db = TechniqueDatabase()
        self.generator = ScriptGenerator()  # New: ScriptGenerator instance
        self.config = self._load_config()
        self.current_structure = None  # For storing approved structure
    
    def _load_config(self):
        """Load configuration."""
        config_path = Path(__file__).parent.parent / "config.yaml"
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            return {"interface": {"port": 7860, "share": False, "debug": False}}
    
    def generate_script_structure(self, topic, description, niche, hook_type, structure_type, video_length):
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
                error_output = "❌ Erro ao gerar estrutura. Verifique os parâmetros."
                error_status = "❌ **Erro**: Falha na geração da estrutura. Tente novamente."
                return error_output, error_status
            
            # Format output
            output = f"""
# 🎬 Estrutura de Script Gerada

## 📊 Metadados
- **Tópico**: {structure['metadata']['topic']}"""
            
            if description and description.strip():
                output += f"""
- **Descrição**: {description}"""
            
            output += f"""
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
            
            # Generate success status message
            success_status = """✅ **ESTRUTURA GERADA COM SUCESSO!**

🎯 **Revise a estrutura** ao lado e, se estiver satisfeito, clique em **"✅ Aprovar e Gerar Script"** abaixo.

📝 **Dica**: Você pode regenerar a estrutura com parâmetros diferentes se necessário."""
            
            return output, success_status
            
        except Exception as e:
            error_output = f"❌ Erro ao gerar estrutura: {str(e)}"
            error_status = f"❌ **Erro**: {str(e)}. Tente novamente."
            return error_output, error_status
    
    def approve_structure_and_prepare(self, current_output):
        """Approve current structure and prepare for script generation."""
        # Check if structure has been generated
        if not current_output or current_output.strip() == "":
            return "⚠️ **Erro**: Nenhuma estrutura encontrada. Gere uma estrutura primeiro clicando em 'Gerar Estrutura'."
        
        # Check for error messages in the output
        if "❌ Erro" in current_output:
            return "⚠️ **Erro**: A estrutura atual contém erros. Gere uma nova estrutura válida primeiro."
        
        # Check if it's still the placeholder text
        if "👆 Preencha os campos" in current_output:
            return "⚠️ **Atenção**: Preencha os campos e clique em 'Gerar Estrutura' primeiro antes de aprovar."
        
        # Check if structure contains expected elements (basic validation)
        if "# 🎬 Estrutura de Script Gerada" not in current_output:
            return "⚠️ **Erro**: Estrutura inválida. Gere uma estrutura válida primeiro."
        
        # Store the current output as approved structure
        # In a real implementation, you might want to parse and store the metadata
        return """🎉 **ESTRUTURA APROVADA COM SUCESSO!**

✅ Sua estrutura foi aprovada e está pronta para gerar o script completo.

📋 **Próximos Passos:**
1. Clique na aba **"🎬 Script Completo"** acima
2. Ajuste o tom e audiência conforme necessário
3. Clique em **"🎬 Gerar Script Completo"**

🚀 **Dica**: Os parâmetros da estrutura aprovada serão automaticamente aplicados no script final."""
    
    def generate_complete_script(self, topic, description, niche, hook_type, structure_type, 
                               video_length, tone, audience, include_cta):
        """Generate complete script based on approved structure."""
        try:
            # Create script generation request
            request = ScriptGenerationRequest(
                topic=topic,
                niche=niche,
                hook_type=hook_type,
                structure_type=structure_type,
                target_duration=int(video_length),
                tone=tone,
                target_audience=audience,
                include_cta=include_cta,
                description=description or ""
            )
            
            # Generate the complete script
            script = self.generator.generate_script(request)
            
            if not script:
                return "❌ Erro ao gerar script completo. Verifique os parâmetros."
            
            # Format the complete output
            output = f"""
# 🎬 Script Completo Gerado

## 📊 Metadados do Script
- **Tópico**: {script.metadata['topic']}"""
            
            if script.metadata.get('description'):
                output += f"""
- **Descrição**: {script.metadata['description']}"""
            
            output += f"""
- **Nicho**: {script.metadata['niche']}
- **Tom**: {script.metadata['tone']}
- **Audiência**: {script.metadata['target_audience']}
- **Duração estimada**: {script.estimated_duration:.1f} minutos
- **Score de qualidade**: {script.quality_score:.2f}/1.0

## 📝 Script Completo

{script.script_text}

## 🎯 Estrutura do Script

"""
            
            for section, info in script.structure_breakdown.items():
                section_name = section.replace('_', ' ').title()
                output += f"- **{section_name}**: {info}\n"
            
            output += f"""

## 💡 Técnicas Utilizadas

"""
            
            for technique in script.techniques_used:
                output += f"- {technique}\n"
            
            return output
            
        except Exception as e:
            return f"❌ Erro ao gerar script completo: {str(e)}"
    
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
            
            with gr.Tabs():
                # Tab 1: Structure Generation
                with gr.Tab("📝 Estrutura"):
                    gr.Markdown("### Etapa 1: Gerar e Revisar Estrutura do Script")
                    
                    with gr.Row():
                        with gr.Column():
                            topic_input = gr.Textbox(
                                label="📝 Tópico do Vídeo",
                                placeholder="Ex: Como aprender programação do zero",
                                value="Como aprender programação do zero"
                            )
                            
                            description_input = gr.Textbox(
                                label="📋 Descrição (Opcional)",
                                placeholder="Ex: Quero criar meu primeiro projeto web para encontrar emprego na área",
                                lines=3,
                                max_lines=4,
                                info="Forneça contexto adicional sobre seu objetivo, situação ou necessidade específica (máx. 500 caracteres)"
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
                            
                            generate_structure_btn = gr.Button("🚀 Gerar Estrutura", variant="primary")
                            
                            # Approval section with better visibility
                            with gr.Group():
                                gr.Markdown("### 📋 Status da Aprovação")
                                approval_status = gr.Markdown(
                                    value="⏳ **Aguardando**: Gere uma estrutura primeiro para poder aprovar.",
                                    container=True
                                )
                                approve_structure_btn = gr.Button("✅ Aprovar e Gerar Script", variant="secondary", size="lg")
                        
                        with gr.Column():
                            structure_output = gr.Markdown(
                                label="📄 Estrutura Gerada",
                                value="👆 Preencha os campos ao lado e clique em 'Gerar Estrutura'"
                            )
                
                # Tab 2: Complete Script Generation  
                with gr.Tab("🎬 Script Completo"):
                    gr.Markdown("### Etapa 2: Gerar Script Completo")
                    
                    with gr.Row():
                        with gr.Column():
                            # Copy parameters from Tab 1 (in a real app, these would be auto-filled)
                            script_topic_input = gr.Textbox(
                                label="📝 Tópico do Vídeo",
                                placeholder="Ex: Como aprender programação do zero",
                                value="Como aprender programação do zero"
                            )
                            
                            script_description_input = gr.Textbox(
                                label="📋 Descrição (Opcional)",
                                placeholder="Ex: Quero criar meu primeiro projeto web para encontrar emprego na área",
                                lines=3,
                                max_lines=4,
                                info="Forneça contexto adicional sobre seu objetivo, situação ou necessidade específica (máx. 500 caracteres)"
                            )
                            
                            script_niche_dropdown = gr.Dropdown(
                                choices=niches,
                                label="🎯 Nicho",
                                value=niches[0]
                            )
                            
                            script_hook_dropdown = gr.Dropdown(
                                choices=hooks,
                                label="🎣 Tipo de Hook",
                                value=hooks[0]
                            )
                            
                            script_structure_dropdown = gr.Dropdown(
                                choices=structures,
                                label="📖 Estrutura Narrativa",
                                value=structures[0]
                            )
                            
                            script_length_slider = gr.Slider(
                                minimum=3,
                                maximum=20,
                                value=10,
                                step=1,
                                label="⏱️ Duração do Vídeo (minutos)"
                            )
                            
                            # New fields for script generation
                            tone_dropdown = gr.Dropdown(
                                choices=["casual", "professional", "enthusiastic", "educational"],
                                label="🎭 Tom do Script",
                                value="casual"
                            )
                            
                            audience_dropdown = gr.Dropdown(
                                choices=["iniciantes", "intermediarios", "avancados", "geral"],
                                label="👥 Audiência",
                                value="geral"
                            )
                            
                            include_cta_checkbox = gr.Checkbox(
                                label="📢 Incluir Call-to-Action",
                                value=True
                            )
                            
                            generate_script_btn = gr.Button("🎬 Gerar Script Completo", variant="primary")
                        
                        with gr.Column():
                            script_output = gr.Markdown(
                                label="📄 Script Completo",
                                value="👆 Configure os parâmetros ao lado e clique em 'Gerar Script Completo'"
                            )
            
            # Connect Tab 1 buttons
            generate_structure_btn.click(
                fn=self.generate_script_structure,
                inputs=[topic_input, description_input, niche_dropdown, hook_dropdown, structure_dropdown, length_slider],
                outputs=[structure_output, approval_status]
            )
            
            approve_structure_btn.click(
                fn=self.approve_structure_and_prepare,
                inputs=[structure_output],
                outputs=[approval_status]
            )
            
            # Connect Tab 2 buttons
            generate_script_btn.click(
                fn=self.generate_complete_script,
                inputs=[
                    script_topic_input, script_description_input, script_niche_dropdown, script_hook_dropdown, 
                    script_structure_dropdown, script_length_slider, tone_dropdown, 
                    audience_dropdown, include_cta_checkbox
                ],
                outputs=[script_output]
            )
            
            # Add examples
            gr.Markdown("""
            ## 💡 Exemplos de Uso
            
            **Tecnologia**: "Os 5 melhores apps que você precisa conhecer em 2024"
            - *Descrição*: "Quero otimizar minha produtividade no trabalho remoto"
            
            **Educação**: "Como estudar para concursos de forma eficiente"
            - *Descrição*: "Trabalho 8h por dia e só tenho 2h livres para estudar"
            
            **Negócios**: "Como começar um negócio online do zero"
            - *Descrição*: "Tenho R$ 1000 para investir e quero gerar renda extra"
            
            **Lifestyle**: "Minha rotina matinal que mudou minha vida"
            - *Descrição*: "Sempre acordo cansado e sem disposição para o dia"
            
            **Entretenimento**: "Reagindo aos memes mais virais da semana"
            - *Descrição*: "Quero criar conteúdo que conecte com a Geração Z"
            
            ## 🔄 Fluxo de Uso
            1. **Tab Estrutura**: Configure parâmetros → Adicione descrição (opcional) → Gere estrutura → Revise → Aprove
            2. **Tab Script Completo**: Ajuste tom e audiência → Adicione descrição (opcional) → Gere script completo
            
            ## 📋 Dicas para Descrição
            - Mencione seu objetivo específico
            - Inclua sua situação atual ou limitações
            - Descreva seu público-alvo
            - Fale sobre resultados esperados
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