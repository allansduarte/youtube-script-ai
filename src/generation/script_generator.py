"""
Script generator for creating YouTube scripts using storytelling techniques.

This module generates complete scripts based on templates, structures,
and storytelling techniques.
"""

import random
import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from storytelling.technique_database import TechniqueDatabase


@dataclass
class ScriptGenerationRequest:
    """Request for script generation."""
    topic: str
    niche: str
    hook_type: str
    structure_type: str
    target_duration: int
    tone: str = "casual"
    target_audience: str = "geral"
    include_cta: bool = True
    description: str = ""
    custom_context: Dict[str, str] = None


@dataclass
class GeneratedScript:
    """Generated script with metadata."""
    script_text: str
    metadata: Dict[str, Any]
    techniques_used: List[str]
    structure_breakdown: Dict[str, str]
    estimated_duration: float
    quality_score: float


class ScriptGenerator:
    """Generates YouTube scripts using storytelling techniques."""
    
    def __init__(self):
        self.db = TechniqueDatabase()
        self.logger = self._setup_logging()
        self.tone_modifiers = self._initialize_tone_modifiers()
        self.audience_adapters = self._initialize_audience_adapters()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the generator."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger
    
    def _initialize_tone_modifiers(self) -> Dict[str, Dict[str, List[str]]]:
        """Initialize tone modifiers for different styles."""
        return {
            "casual": {
                "connectors": ["Olha", "Cara", "Mano", "Galera", "Pessoal"],
                "emphasis": ["super", "muito", "demais", "pra caramba"],
                "transitions": ["Agora", "Aí", "Então", "Daí", "Tipo assim"]
            },
            "professional": {
                "connectors": ["Vamos analisar", "É importante notar", "Considerando"],
                "emphasis": ["significativamente", "consideravelmente", "extremamente"],
                "transitions": ["Em seguida", "Posteriormente", "Ademais", "Além disso"]
            },
            "enthusiastic": {
                "connectors": ["Gente!", "Isso é incrível!", "Olha que incrível!"],
                "emphasis": ["MUITO", "extremamente", "incrivelmente", "fantasticamente"],
                "transitions": ["E agora", "E mais", "E tem mais", "Espera que tem mais"]
            },
            "educational": {
                "connectors": ["Vamos entender", "É fundamental", "Primeiro ponto"],
                "emphasis": ["claramente", "precisamente", "especificamente"],
                "transitions": ["Primeiro", "Segundo", "Em terceiro lugar", "Para concluir"]
            }
        }
    
    def _initialize_audience_adapters(self) -> Dict[str, Dict[str, Any]]:
        """Initialize adapters for different audiences."""
        return {
            "iniciantes": {
                "complexity": "low",
                "explanations": True,
                "examples": "basic",
                "vocabulary": "simple"
            },
            "intermediarios": {
                "complexity": "medium", 
                "explanations": False,
                "examples": "practical",
                "vocabulary": "technical"
            },
            "avancados": {
                "complexity": "high",
                "explanations": False,
                "examples": "advanced",
                "vocabulary": "expert"
            },
            "geral": {
                "complexity": "medium",
                "explanations": True,
                "examples": "varied",
                "vocabulary": "accessible"
            }
        }
    
    def generate_script(self, request: ScriptGenerationRequest) -> GeneratedScript:
        """Generate a complete script based on the request."""
        try:
            self.logger.info(f"Generating script for topic: {request.topic}")
            
            # Get the complete structure
            structure = self.db.generate_complete_script_structure(
                niche=request.niche,
                hook_type=request.hook_type,
                structure_type=request.structure_type,
                video_length=request.target_duration,
                topic=request.topic
            )
            
            if not structure:
                raise ValueError("Could not generate script structure")
            
            # Generate script content
            script_sections = self._generate_script_sections(structure, request)
            
            # Assemble final script
            script_text = self._assemble_script(script_sections, request)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(script_text, structure)
            
            # Extract techniques used
            techniques_used = self._extract_techniques_used(structure, request)
            
            # Create structure breakdown
            structure_breakdown = self._create_structure_breakdown(script_sections)
            
            # Estimate duration
            estimated_duration = len(script_text.split()) / 150  # ~150 words per minute
            
            result = GeneratedScript(
                script_text=script_text,
                metadata={
                    "topic": request.topic,
                    "description": request.description,
                    "niche": request.niche,
                    "hook_type": request.hook_type,
                    "structure_type": request.structure_type,
                    "tone": request.tone,
                    "target_audience": request.target_audience,
                    "target_duration": request.target_duration
                },
                techniques_used=techniques_used,
                structure_breakdown=structure_breakdown,
                estimated_duration=estimated_duration,
                quality_score=quality_score
            )
            
            self.logger.info(f"Script generated successfully. Quality score: {quality_score:.2f}")
            return result
            
        except Exception as e:
            self.logger.error(f"Error generating script: {e}")
            raise
    
    def _generate_script_sections(self, structure: Dict[str, Any], request: ScriptGenerationRequest) -> Dict[str, str]:
        """Generate content for each section of the script."""
        sections = {}
        
        # Generate hook section
        sections["hook"] = self._generate_hook_section(structure["hook"], request)
        
        # Generate main content sections
        for i, section in enumerate(structure["structure"]["sections"]):
            section_key = f"section_{i+1}_{section['name'].lower().replace(' ', '_')}"
            sections[section_key] = self._generate_content_section(section, request, i+1)
        
        # Generate conclusion if requested
        if request.include_cta:
            sections["conclusion"] = self._generate_conclusion_section(request)
        
        return sections
    
    def _generate_hook_section(self, hook_info: Dict[str, Any], request: ScriptGenerationRequest) -> str:
        """Generate the hook section."""
        # Get context for hook customization
        context = self._build_hook_context(request)
        
        # Get base hook template
        hook_template = hook_info["template"]
        
        # Replace placeholders with context
        hook_text = hook_template
        for key, value in context.items():
            hook_text = hook_text.replace(f"{{{key}}}", value)
        
        # Apply tone modifications
        hook_text = self._apply_tone_modifications(hook_text, request.tone)
        
        # Add opening connector based on tone
        connectors = self.tone_modifiers[request.tone]["connectors"]
        opener = random.choice(connectors)
        
        return f"{opener}, {hook_text}"
    
    def _build_hook_context(self, request: ScriptGenerationRequest) -> Dict[str, str]:
        """Build context dictionary for hook customization."""
        context = request.custom_context or {}
        
        # Incorporate user-provided description for better context
        if request.description:
            # Use description to enhance context
            description_lower = request.description.lower()
            context["user_description"] = request.description
            
            # Extract additional context hints from description
            if any(word in description_lower for word in ["problema", "dificuldade", "desafio"]):
                context["has_problem_focus"] = "true"
            if any(word in description_lower for word in ["solução", "resolver", "método"]):
                context["has_solution_focus"] = "true"
            if any(word in description_lower for word in ["experiência", "história", "aconteceu"]):
                context["has_personal_element"] = "true"
        
        # Add default context based on topic and niche
        topic_lower = request.topic.lower()
        
        if "python" in topic_lower or "programação" in topic_lower:
            if request.description:
                # Use description to customize the shocking statement
                context.update({
                    "something shocking": f"90% das pessoas que {request.description[:50].lower()}... fazem isso completamente errado",
                    "contradicts expectation": "pensam que precisam decorar sintaxe",
                    "topic": "programação",
                    "subject": "aprender código"
                })
            else:
                context.update({
                    "something shocking": "90% das pessoas aprendem programação de forma totalmente errada",
                    "contradicts expectation": "pensam que precisam decorar sintaxe",
                    "topic": "programação",
                    "subject": "aprender código"
                })
        elif "negócio" in topic_lower or "empreend" in topic_lower:
            if request.description:
                context.update({
                    "something shocking": f"95% das pessoas que tentam {request.description[:50].lower()}... falham nos primeiros 6 meses",
                    "contradicts expectation": "focam no produto errado",
                    "topic": "empreendedorismo", 
                    "subject": "construir um negócio"
                })
            else:
                context.update({
                    "something shocking": "95% dos negócios online falham nos primeiros 6 meses",
                    "contradicts expectation": "focam no produto errado",
                    "topic": "empreendedorismo",
                    "subject": "construir um negócio"
                })
        elif "youtube" in topic_lower:
            if request.description:
                context.update({
                    "something shocking": f"apenas 2% dos youtubers que {request.description[:50].lower()}... conseguem viver do canal",
                    "contradicts expectation": "fazem tudo pensando no algoritmo",
                    "topic": "YouTube",
                    "subject": "crescer no YouTube"
                })
            else:
                context.update({
                    "something shocking": "apenas 2% dos youtubers conseguem viver do canal",
                    "contradicts expectation": "fazem tudo pensando no algoritmo",
                    "topic": "YouTube",
                    "subject": "crescer no YouTube"
                })
        else:
            # Generic context enhanced with description
            if request.description:
                context.update({
                    "something shocking": f"a maioria das pessoas que {request.description[:50].lower()}... faz isso de forma completamente errada",
                    "contradicts expectation": "usam métodos desatualizados",
                    "topic": request.topic.lower(),
                    "subject": request.topic.lower()
                })
            else:
                context.update({
                    "something shocking": f"a maioria das pessoas não sabe como {request.topic.lower()}",
                    "contradicts expectation": "usam métodos desatualizados",
                    "topic": request.topic.lower(),
                    "subject": request.topic.lower()
                })
        
        return context
    
    def _generate_content_section(self, section_info: Dict[str, Any], request: ScriptGenerationRequest, section_num: int) -> str:
        """Generate content for a main section."""
        purpose = section_info["purpose"]
        key_elements = section_info["key_elements"]
        duration_percentage = section_info["duration_percentage"]
        
        # Calculate target word count for this section
        total_words = request.target_duration * 150  # 150 words per minute
        section_words = int(total_words * duration_percentage)
        
        # Generate content based on section purpose and elements
        content_parts = []
        
        # Add section transition
        transitions = self.tone_modifiers[request.tone]["transitions"]
        transition = random.choice(transitions)
        content_parts.append(f"{transition},")
        
        # Generate content for each key element
        words_per_element = section_words // len(key_elements)
        
        for element in key_elements:
            element_content = self._generate_element_content(
                element, purpose, request, words_per_element
            )
            content_parts.append(element_content)
        
        # Add engagement element if it's a middle section
        if 2 <= section_num <= 4:
            engagement = self._generate_engagement_element(request)
            content_parts.append(engagement)
        
        return " ".join(content_parts)
    
    def _generate_element_content(self, element: str, purpose: str, request: ScriptGenerationRequest, target_words: int) -> str:
        """Generate content for a specific element."""
        # This is a simplified content generation
        # In a real implementation, this could use templates or even AI models
        
        topic = request.topic.lower()
        audience_level = self.audience_adapters[request.target_audience]["complexity"]
        description_context = f" {request.description}" if request.description else ""
        
        if "problema" in element.lower():
            if "python" in topic:
                if request.description:
                    return f"O maior problema que vejo é que as pessoas tentam {request.description.lower()}, mas fazem isso decorando sintaxe. Isso não funciona porque programação não é sobre decorar, é sobre resolver problemas. Você passa horas tentando lembrar como escrever um loop, quando deveria estar focando em entender a lógica por trás."
                else:
                    return f"O maior problema que vejo é que as pessoas tentam aprender Python decorando sintaxe. Isso não funciona porque programação não é sobre decorar, é sobre resolver problemas. Você passa horas tentando lembrar como escrever um loop, quando deveria estar focando em entender a lógica por trás."
            else:
                base_problem = f"O principal problema com {topic}"
                if request.description:
                    return f"{base_problem} é que quando você {request.description.lower()}, a maioria das pessoas aborda de forma completamente errada. Elas focam nos detalhes técnicos sem entender os fundamentos."
                else:
                    return f"{base_problem} é que a maioria das pessoas aborda de forma completamente errada. Elas focam nos detalhes técnicos sem entender os fundamentos."
        
        elif "solução" in element.lower():
            if request.description:
                return f"A solução que descobri muda tudo. Em vez de {topic} da forma tradicional, especialmente quando você {request.description.lower()}, você precisa começar com uma abordagem diferente. Vou te mostrar exatamente como fazer isso."
            else:
                return f"A solução que descobri muda tudo. Em vez de {topic} da forma tradicional, você precisa começar com uma abordagem diferente. Vou te mostrar exatamente como fazer isso."
        
        elif "exemplo" in element.lower() or "demonstração" in element.lower():
            if request.description:
                return f"Deixe-me te mostrar um exemplo prático. Quando eu estava {request.description.lower()}, cometi esse mesmo erro. Mas depois que descobri essa técnica, tudo ficou mais claro."
            else:
                return f"Deixe-me te mostrar um exemplo prático. Quando eu estava aprendendo {topic}, cometi esse mesmo erro. Mas depois que descobri essa técnica, tudo ficou mais claro."
        
        elif "resultado" in element.lower():
            if request.description:
                return f"Os resultados foram impressionantes. Em apenas algumas semanas aplicando essa metodologia para {request.description.lower()}, consegui {topic} de forma muito mais eficiente."
            else:
                return f"Os resultados foram impressionantes. Em apenas algumas semanas aplicando essa metodologia, consegui {topic} de forma muito mais eficiente."
        
        else:
            # Generic content generation enhanced with description
            emphasis = random.choice(self.tone_modifiers[request.tone]["emphasis"])
            if request.description:
                return f"Isso é {emphasis} importante para {topic}, especialmente quando você {request.description.lower()}. A diferença está nos detalhes e na forma como você aborda cada etapa do processo."
            else:
                return f"Isso é {emphasis} importante para {topic}. A diferença está nos detalhes e na forma como você aborda cada etapa do processo."
    
    def _generate_engagement_element(self, request: ScriptGenerationRequest) -> str:
        """Generate an engagement element."""
        engagement_types = [
            "Deixe nos comentários: você já passou por isso? Quero saber sua experiência!",
            "Se você está gostando até aqui, dê aquele like para me ajudar!",
            "Pausa o vídeo agora e pensa: você realmente faz isso na prática?",
            "Lembra do que falei no início? Agora você está entendendo o porquê.",
            "Aguarda que vou te mostrar algo que vai te surpreender..."
        ]
        
        return random.choice(engagement_types)
    
    def _generate_conclusion_section(self, request: ScriptGenerationRequest) -> str:
        """Generate the conclusion section with CTA."""
        conclusion_parts = []
        
        # Summary
        conclusion_parts.append(f"Então, recapitulando: hoje você aprendeu sobre {request.topic}.")
        
        # Key takeaway
        conclusion_parts.append("O mais importante é que você comece a aplicar isso hoje mesmo.")
        
        # CTA elements
        cta_elements = [
            "Se esse vídeo foi útil para você, deixa aquele like.",
            "Se inscreve no canal se ainda não é inscrito.",
            "Ativa o sininho para não perder os próximos vídeos.",
            "E comenta embaixo: qual vai ser seu primeiro passo?"
        ]
        
        # Add 2-3 CTA elements
        selected_ctas = random.sample(cta_elements, k=random.randint(2, 3))
        conclusion_parts.extend(selected_ctas)
        
        # Closing
        conclusion_parts.append("Valeu pessoal, e até o próximo vídeo!")
        
        return " ".join(conclusion_parts)
    
    def _apply_tone_modifications(self, text: str, tone: str) -> str:
        """Apply tone-specific modifications to text."""
        if tone == "enthusiastic":
            # Add more exclamation marks
            text = text.replace(".", "!")
            # Add emphasis words
            text = text.replace(" muito ", " MUITO ")
        
        elif tone == "professional":
            # Ensure proper punctuation
            text = text.replace("!", ".")
            # Add professional connectors
            if not text.startswith(("É importante", "Devemos", "Precisamos")):
                text = "É importante notar que " + text.lower()
        
        return text
    
    def _assemble_script(self, sections: Dict[str, str], request: ScriptGenerationRequest) -> str:
        """Assemble the final script from sections."""
        script_parts = []
        
        # Add sections in order
        if "hook" in sections:
            script_parts.append(sections["hook"])
            script_parts.append("")  # Empty line for spacing
        
        # Add main content sections
        section_keys = [k for k in sections.keys() if k.startswith("section_")]
        section_keys.sort()  # Ensure proper order
        
        for key in section_keys:
            script_parts.append(sections[key])
            script_parts.append("")  # Empty line for spacing
        
        # Add conclusion
        if "conclusion" in sections:
            script_parts.append(sections["conclusion"])
        
        return "\n".join(script_parts)
    
    def _calculate_quality_score(self, script_text: str, structure: Dict[str, Any]) -> float:
        """Calculate a quality score for the generated script."""
        score = 0.0
        
        # Word count appropriateness (25%)
        words = len(script_text.split())
        target_words = structure["metadata"]["estimated_length"] * 150
        word_score = 1.0 - abs(words - target_words) / target_words
        score += max(word_score, 0) * 0.25
        
        # Structure completeness (25%)
        required_sections = len(structure["structure"]["sections"]) + 2  # +hook +conclusion
        script_sections = script_text.count("\n\n") + 1
        structure_score = min(script_sections / required_sections, 1.0)
        score += structure_score * 0.25
        
        # Engagement elements (25%)
        engagement_indicators = ["comentários", "like", "inscreva", "compartilhe"]
        engagement_count = sum(1 for indicator in engagement_indicators if indicator in script_text.lower())
        engagement_score = min(engagement_count / 4, 1.0)
        score += engagement_score * 0.25
        
        # Readability (25%)
        sentences = script_text.split('.')
        avg_words_per_sentence = words / len(sentences) if sentences else 0
        if 10 <= avg_words_per_sentence <= 20:
            readability_score = 1.0
        else:
            readability_score = max(0, 1.0 - abs(avg_words_per_sentence - 15) / 15)
        score += readability_score * 0.25
        
        return score
    
    def _extract_techniques_used(self, structure: Dict[str, Any], request: ScriptGenerationRequest) -> List[str]:
        """Extract list of techniques used in the script."""
        techniques = []
        
        # Add hook technique
        techniques.append(f"Hook: {structure['hook']['type']}")
        
        # Add structure technique
        techniques.append(f"Structure: {structure['structure']['name']}")
        
        # Add tone
        techniques.append(f"Tone: {request.tone}")
        
        # Add audience adaptation
        techniques.append(f"Audience: {request.target_audience}")
        
        return techniques
    
    def _create_structure_breakdown(self, sections: Dict[str, str]) -> Dict[str, str]:
        """Create a breakdown of the script structure."""
        breakdown = {}
        
        for key, content in sections.items():
            word_count = len(content.split())
            duration = word_count / 150  # minutes
            breakdown[key] = f"{word_count} palavras (~{duration:.1f} min)"
        
        return breakdown
    
    def generate_multiple_variations(self, request: ScriptGenerationRequest, count: int = 3) -> List[GeneratedScript]:
        """Generate multiple variations of a script."""
        variations = []
        
        for i in range(count):
            try:
                # Slightly modify the request for variation
                varied_request = ScriptGenerationRequest(
                    topic=request.topic,
                    niche=request.niche,
                    hook_type=request.hook_type,
                    structure_type=request.structure_type,
                    target_duration=request.target_duration,
                    tone=request.tone,
                    target_audience=request.target_audience,
                    include_cta=request.include_cta,
                    description=request.description,
                    custom_context=request.custom_context
                )
                
                script = self.generate_script(varied_request)
                variations.append(script)
                
            except Exception as e:
                self.logger.error(f"Error generating variation {i+1}: {e}")
        
        return variations