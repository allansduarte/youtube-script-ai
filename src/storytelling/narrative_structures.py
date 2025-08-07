"""
Narrative structures for YouTube scripts.

This module contains proven narrative structures that work well
for different types of YouTube content.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class StructureType(Enum):
    """Types of narrative structures."""
    HERO_JOURNEY = "hero_journey"
    PROBLEM_SOLUTION = "problem_solution" 
    BEFORE_AFTER = "before_after"
    LIST_FORMAT = "list_format"
    TUTORIAL_STEP = "tutorial_step"
    STORY_LESSON = "story_lesson"
    COMPARE_CONTRAST = "compare_contrast"
    CHRONOLOGICAL = "chronological"


@dataclass
class NarrativeSection:
    """Represents a section of a narrative structure."""
    name: str
    purpose: str
    duration_percentage: float
    key_elements: List[str]
    examples: List[str]


@dataclass
class NarrativeStructure:
    """Represents a complete narrative structure."""
    name: str
    structure_type: StructureType
    description: str
    sections: List[NarrativeSection]
    best_for: List[str]
    engagement_score: float
    typical_duration: str
    psychological_principle: str


class NarrativeStructures:
    """Manager class for narrative structures."""
    
    def __init__(self):
        self.structures = self._initialize_structures()
    
    def _initialize_structures(self) -> Dict[str, NarrativeStructure]:
        """Initialize all narrative structures."""
        structures = {}
        
        # Hero's Journey
        hero_sections = [
            NarrativeSection(
                name="Ordinary World",
                purpose="Estabelecer o status quo e criar identificação",
                duration_percentage=0.10,
                key_elements=["Situação inicial", "Vida comum", "Identificação com audiência"],
                examples=["Eu era apenas mais um funcionário comum...", "Como qualquer pessoa da minha idade..."]
            ),
            NarrativeSection(
                name="Call to Adventure",
                purpose="Apresentar o desafio ou oportunidade",
                duration_percentage=0.15,
                key_elements=["Momento de mudança", "Oportunidade", "Desafio"],
                examples=["Até que um dia...", "Foi quando descobri...", "Tudo mudou quando..."]
            ),
            NarrativeSection(
                name="Journey & Challenges",
                purpose="Mostrar a jornada e os obstáculos",
                duration_percentage=0.50,
                key_elements=["Obstáculos", "Aprendizados", "Progressão"],
                examples=["O primeiro desafio foi...", "Cada erro me ensinou...", "Depois de muito tentar..."]
            ),
            NarrativeSection(
                name="Transformation",
                purpose="Revelar a mudança e o resultado",
                duration_percentage=0.20,
                key_elements=["Resultado", "Transformação", "Novo estado"],
                examples=["Hoje posso dizer que...", "A diferença é clara...", "Agora eu entendo..."]
            ),
            NarrativeSection(
                name="Return with Gift",
                purpose="Compartilhar o aprendizado com a audiência",
                duration_percentage=0.05,
                key_elements=["Lição", "Aplicação", "Call to action"],
                examples=["O que aprendi foi...", "Você também pode...", "Agora é sua vez..."]
            )
        ]
        
        structures["hero_journey"] = NarrativeStructure(
            name="Jornada do Herói",
            structure_type=StructureType.HERO_JOURNEY,
            description="Estrutura clássica que segue uma jornada de transformação pessoal",
            sections=hero_sections,
            best_for=["desenvolvimento_pessoal", "empreendedorismo", "lifestyle"],
            engagement_score=0.90,
            typical_duration="8-15 minutos",
            psychological_principle="Monomyth - Estrutura narrativa universal que ressoa profundamente com humanos"
        )
        
        # Problem-Solution
        problem_solution_sections = [
            NarrativeSection(
                name="Problem Identification",
                purpose="Identificar e amplificar o problema",
                duration_percentage=0.25,
                key_elements=["Problema comum", "Dor", "Frustração"],
                examples=["Você já passou por isso?", "O problema que todo mundo tem...", "A frustração de..."]
            ),
            NarrativeSection(
                name="Problem Amplification",
                purpose="Mostrar as consequências do problema",
                duration_percentage=0.20,
                key_elements=["Consequências", "Custos", "Impacto"],
                examples=["Se isso continuar...", "O custo de não resolver...", "As pessoas não percebem que..."]
            ),
            NarrativeSection(
                name="Solution Introduction",
                purpose="Apresentar a solução",
                duration_percentage=0.15,
                key_elements=["Solução", "Método", "Abordagem"],
                examples=["A solução é simples...", "Existe uma forma melhor...", "O método que funciona é..."]
            ),
            NarrativeSection(
                name="Solution Explanation",
                purpose="Explicar como a solução funciona",
                duration_percentage=0.30,
                key_elements=["Passo a passo", "Exemplos", "Evidências"],
                examples=["Primeiro você...", "Veja como funciona...", "O processo é..."]
            ),
            NarrativeSection(
                name="Call to Action",
                purpose="Motivar a implementação",
                duration_percentage=0.10,
                key_elements=["Próximos passos", "Motivação", "Urgência"],
                examples=["Agora é com você...", "Comece hoje mesmo...", "Não espere mais..."]
            )
        ]
        
        structures["problem_solution"] = NarrativeStructure(
            name="Problema-Solução",
            structure_type=StructureType.PROBLEM_SOLUTION,
            description="Estrutura focada em identificar problemas e apresentar soluções práticas",
            sections=problem_solution_sections,
            best_for=["educacao", "tecnologia", "negocios", "tutoriais"],
            engagement_score=0.85,
            typical_duration="5-12 minutos",
            psychological_principle="Problem-Solution Fit - Criar tensão através do problema e alívio através da solução"
        )
        
        # List Format
        list_sections = [
            NarrativeSection(
                name="Introduction & Promise",
                purpose="Prometer valor e estabelecer expectativas",
                duration_percentage=0.15,
                key_elements=["Promessa", "Benefícios", "Preview"],
                examples=["5 estratégias que vão...", "Os segredos que mudaram...", "Tudo que você precisa saber sobre..."]
            ),
            NarrativeSection(
                name="Item Development",
                purpose="Desenvolver cada item da lista",
                duration_percentage=0.70,
                key_elements=["Itens numerados", "Explicações", "Exemplos"],
                examples=["Primeiro...", "Segundo ponto...", "A terceira estratégia é..."]
            ),
            NarrativeSection(
                name="Summary & Next Steps",
                purpose="Resumir e dar próximos passos",
                duration_percentage=0.15,
                key_elements=["Resumo", "Recapitulação", "Ação"],
                examples=["Recapitulando...", "Em resumo...", "Agora que você sabe..."]
            )
        ]
        
        structures["list_format"] = NarrativeStructure(
            name="Formato Lista",
            structure_type=StructureType.LIST_FORMAT,
            description="Estrutura baseada em listas numeradas ou com bullet points",
            sections=list_sections,
            best_for=["educacao", "dicas", "reviews", "comparacoes"],
            engagement_score=0.75,
            typical_duration="3-10 minutos",
            psychological_principle="Cognitive Ease - Listas são fáceis de processar e lembrar"
        )
        
        return structures
    
    def get_structure(self, structure_type: str) -> Optional[NarrativeStructure]:
        """Get a specific structure by type."""
        return self.structures.get(structure_type)
    
    def get_structures_by_category(self, category: str) -> List[NarrativeStructure]:
        """Get all structures suitable for a specific category."""
        return [structure for structure in self.structures.values() if category in structure.best_for]
    
    def get_best_structures(self, min_score: float = 0.80) -> List[NarrativeStructure]:
        """Get structures with engagement score above threshold."""
        return [structure for structure in self.structures.values() if structure.engagement_score >= min_score]
    
    def generate_outline(self, structure_type: str, topic: str) -> List[str]:
        """Generate a script outline using a specific structure."""
        structure = self.get_structure(structure_type)
        if not structure:
            return []
        
        outline = []
        for section in structure.sections:
            outline.append(f"{section.name}: {section.purpose}")
            outline.extend([f"  - {element}" for element in section.key_elements])
        
        return outline
    
    def get_all_structures(self) -> Dict[str, NarrativeStructure]:
        """Get all available structures."""
        return self.structures