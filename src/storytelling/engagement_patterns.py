"""
Engagement patterns for YouTube content.

This module contains patterns and techniques to maintain viewer
engagement throughout the video.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class EngagementType(Enum):
    """Types of engagement techniques."""
    PATTERN_INTERRUPT = "pattern_interrupt"
    CALLBACK = "callback"
    SUSPENSE_BUILDER = "suspense_builder"
    INTERACTION_PROMPT = "interaction_prompt"
    VISUAL_TRANSITION = "visual_transition"
    ENERGY_SHIFT = "energy_shift"
    PREVIEW_HOOK = "preview_hook"
    SOCIAL_PROOF = "social_proof"


@dataclass
class EngagementTechnique:
    """Represents an engagement technique."""
    name: str
    technique_type: EngagementType
    description: str
    when_to_use: str
    template: str
    examples: List[str]
    effectiveness_score: float
    timing_recommendations: List[str]


class EngagementPatterns:
    """Manager class for engagement patterns."""
    
    def __init__(self):
        self.techniques = self._initialize_techniques()
    
    def _initialize_techniques(self) -> Dict[str, EngagementTechnique]:
        """Initialize all engagement techniques."""
        techniques = {}
        
        # Pattern Interrupt
        techniques["pattern_interrupt"] = EngagementTechnique(
            name="Pattern Interrupt",
            technique_type=EngagementType.PATTERN_INTERRUPT,
            description="Quebrar o padrão esperado para reganhar atenção",
            when_to_use="Quando a energia está baixando ou o conteúdo está ficando monótono",
            template="Espera, {unexpected statement}. Deixe-me explicar melhor...",
            examples=[
                "Espera, eu acabei de falar bobagem. Na verdade...",
                "Pare tudo! Esqueci de mencionar o mais importante...",
                "Ops, você percebeu esse erro que cometi?",
                "Aliás, você sabia que isso que acabei de falar pode estar errado?"
            ],
            effectiveness_score=0.80,
            timing_recommendations=["3-4 minutos", "7-8 minutos", "Quando notar queda de energia"]
        )
        
        # Callback
        techniques["callback"] = EngagementTechnique(
            name="Callback Reference",
            technique_type=EngagementType.CALLBACK,
            description="Referenciar algo mencionado anteriormente no vídeo",
            when_to_use="Para criar coesão e fazer a audiência se sentir 'por dentro'",
            template="Lembra do {previous_point} que mencionei no início? Agora faz sentido porque...",
            examples=[
                "Lembra da história que contei no início sobre meu fracasso? Agora você entende porque foi importante...",
                "Aquela estatística chocante do começo? Agora vou te mostrar como mudá-la...",
                "Voltando àquela pergunta que fiz no início..."
            ],
            effectiveness_score=0.75,
            timing_recommendations=["Meio do vídeo", "Conclusão", "Após explicações complexas"]
        )
        
        # Suspense Builder
        techniques["suspense_builder"] = EngagementTechnique(
            name="Suspense Builder",
            technique_type=EngagementType.SUSPENSE_BUILDER,
            description="Criar antecipação para o que vem a seguir",
            when_to_use="Antes de revelar informações importantes",
            template="Em {time}, vou revelar {important_information}. Mas primeiro...",
            examples=[
                "Em 2 minutos, vou te mostrar o segredo que mudou tudo. Mas primeiro, você precisa entender...",
                "Daqui a pouco vou revelar o erro que 90% das pessoas cometem. Mas antes...",
                "Aguenta aí que a parte mais importante vem agora...",
                "O que vou te contar em seguida vai te chocar, mas antes preciso contextualizar..."
            ],
            effectiveness_score=0.85,
            timing_recommendations=["Antes de pontos importantes", "Transições entre seções", "Meio do vídeo"]
        )
        
        # Interaction Prompt
        techniques["interaction_prompt"] = EngagementTechnique(
            name="Interaction Prompt",
            technique_type=EngagementType.INTERACTION_PROMPT,
            description="Pedir interação direta da audiência",
            when_to_use="Para aumentar engagement e manter atenção ativa",
            template="Deixe nos comentários: {specific_question}. Quero saber sua experiência com...",
            examples=[
                "Deixe nos comentários: qual foi seu maior erro ao começar? Quero ler todas as histórias...",
                "Escreva SIM nos comentários se você já passou por isso...",
                "Pausa o vídeo agora e responda honestamente: você realmente faz isso?",
                "Dê like se você concorda comigo até aqui..."
            ],
            effectiveness_score=0.70,
            timing_recommendations=["Meio do vídeo", "Após pontos importantes", "Final do vídeo"]
        )
        
        # Preview Hook
        techniques["preview_hook"] = EngagementTechnique(
            name="Preview Hook", 
            technique_type=EngagementType.PREVIEW_HOOK,
            description="Dar preview do que está por vir para manter interesse",
            when_to_use="Durante transições e para manter expectativa",
            template="Daqui a pouco você vai ver {preview_content}, mas primeiro...",
            examples=[
                "Daqui a pouco você vai ver exatamente como fazer isso, mas primeiro precisa entender a teoria...",
                "Em breve vou mostrar os resultados na tela, mas antes...",
                "Aguarde que vou te mostrar um exemplo real disso funcionando...",
                "Mais à frente você vai entender porque isso é tão importante..."
            ],
            effectiveness_score=0.75,
            timing_recommendations=["Início de novas seções", "Antes de exemplos práticos", "Transições"]
        )
        
        # Energy Shift
        techniques["energy_shift"] = EngagementTechnique(
            name="Energy Shift",
            technique_type=EngagementType.ENERGY_SHIFT,
            description="Mudar o nível de energia para reengajar a audiência",
            when_to_use="Quando a energia está baixa ou o ritmo está lento",
            template="Agora vou falar mais {energy_change} porque isso é {importance_level}...",
            examples=[
                "Agora vou falar mais devagar porque isso é fundamental...",
                "Prestem atenção agora porque isso é crucial!",
                "Vou repetir isso porque é importante: ...",
                "Okay, agora vamos acelerar porque eu quero te mostrar..."
            ],
            effectiveness_score=0.65,
            timing_recommendations=["Pontos cruciais", "Quando detectar perda de atenção", "Transições importantes"]
        )
        
        # Social Proof
        techniques["social_proof"] = EngagementTechnique(
            name="Social Proof",
            technique_type=EngagementType.SOCIAL_PROOF,
            description="Usar evidência social para aumentar credibilidade",
            when_to_use="Para validar pontos importantes e aumentar confiança",
            template="Não sou só eu dizendo isso. {social_proof_example}...",
            examples=[
                "Não sou só eu dizendo isso. Mais de 1000 pessoas já me mandaram mensagem confirmando...",
                "Olha só esses comentários de pessoas que aplicaram isso...",
                "Semana passada recebi 20 mensagens de pessoas que...",
                "Meus alunos sempre me perguntam sobre isso..."
            ],
            effectiveness_score=0.80,
            timing_recommendations=["Após fazer afirmações importantes", "Meio do vídeo", "Antes do call-to-action"]
        )
        
        return techniques
    
    def get_technique(self, technique_type: str) -> Optional[EngagementTechnique]:
        """Get a specific technique by type."""
        return self.techniques.get(technique_type)
    
    def get_techniques_by_timing(self, timing: str) -> List[EngagementTechnique]:
        """Get techniques suitable for specific timing."""
        return [
            technique for technique in self.techniques.values()
            if any(timing.lower() in rec.lower() for rec in technique.timing_recommendations)
        ]
    
    def get_best_techniques(self, min_score: float = 0.75) -> List[EngagementTechnique]:
        """Get techniques with effectiveness score above threshold."""
        return [technique for technique in self.techniques.values() if technique.effectiveness_score >= min_score]
    
    def suggest_techniques_for_timestamp(self, timestamp_minutes: int, video_length: int) -> List[EngagementTechnique]:
        """Suggest techniques based on video timestamp."""
        suggestions = []
        
        # Beginning (0-2 minutes)
        if timestamp_minutes <= 2:
            suggestions.extend(self.get_techniques_by_timing("início"))
        
        # Middle (2-8 minutes or middle 60% of video)
        elif timestamp_minutes <= video_length * 0.8:
            suggestions.extend(self.get_techniques_by_timing("meio"))
            # Add pattern interrupts for longer content
            if timestamp_minutes % 3 == 0:  # Every 3 minutes
                suggestions.append(self.get_technique("pattern_interrupt"))
        
        # End (last 20% of video)
        else:
            suggestions.extend(self.get_techniques_by_timing("final"))
        
        return suggestions
    
    def generate_engagement_plan(self, video_length: int) -> Dict[int, List[str]]:
        """Generate an engagement plan for a video of given length."""
        plan = {}
        
        # Add techniques at key timestamps
        timestamps = [
            int(video_length * 0.25),  # 25%
            int(video_length * 0.5),   # 50%
            int(video_length * 0.75),  # 75%
        ]
        
        for timestamp in timestamps:
            techniques = self.suggest_techniques_for_timestamp(timestamp, video_length)
            plan[timestamp] = [tech.name for tech in techniques[:2]]  # Top 2 suggestions
        
        return plan
    
    def get_all_techniques(self) -> Dict[str, EngagementTechnique]:
        """Get all available techniques."""
        return self.techniques