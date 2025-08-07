"""
Hook techniques for YouTube video openings.

This module contains comprehensive hook techniques proven to capture
viewer attention in the first few seconds of YouTube videos.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class HookType(Enum):
    """Types of hooks for video openings."""
    CURIOSITY_GAP = "curiosity_gap"
    CONTROVERSY = "controversy"
    PERSONAL_STORY = "personal_story"
    STATISTICS_SHOCK = "statistics_shock"
    QUESTION_DIRECT = "question_direct"
    PROMISE_BENEFIT = "promise_benefit"
    PATTERN_INTERRUPT = "pattern_interrupt"
    PREVIEW_TEASER = "preview_teaser"
    EMOTIONAL_TRIGGER = "emotional_trigger"
    AUTHORITY_STATEMENT = "authority_statement"


@dataclass
class Hook:
    """Represents a hook technique."""
    name: str
    hook_type: HookType
    description: str
    template: str
    examples: List[str]
    effectiveness_score: float
    best_niches: List[str]
    psychological_principle: str


class HookTechniques:
    """Manager class for hook techniques."""
    
    def __init__(self):
        self.hooks = self._initialize_hooks()
    
    def _initialize_hooks(self) -> Dict[str, Hook]:
        """Initialize all hook techniques."""
        hooks = {}
        
        # Curiosity Gap
        hooks["curiosity_gap"] = Hook(
            name="Curiosity Gap",
            hook_type=HookType.CURIOSITY_GAP,
            description="Create a gap between what the viewer knows and wants to know",
            template="Eu descobri {something shocking} que {contradicts expectation}... mas antes de revelar, deixe-me contar como cheguei até aqui.",
            examples=[
                "Eu descobri que 90% das pessoas estão fazendo isso errado... mas antes de revelar o que é, deixe-me contar como descobri isso.",
                "Existe um segredo que apenas 1% das pessoas conhecem sobre {topic}... e hoje vou compartilhar com você.",
                "O que vou te mostrar nos próximos minutos pode mudar completamente sua forma de pensar sobre {subject}."
            ],
            effectiveness_score=0.85,
            best_niches=["educacao", "tecnologia", "negocios"],
            psychological_principle="Information Gap Theory - O cérebro humano tem necessidade compulsiva de preencher lacunas de informação"
        )
        
        # Controversy
        hooks["controversy"] = Hook(
            name="Controversy Hook",
            hook_type=HookType.CONTROVERSY,
            description="Present a controversial statement or opinion",
            template="{Controversial statement about popular belief}. Eu sei que isso vai contra tudo que você acredita, mas...",
            examples=[
                "A faculdade é uma perda de tempo e dinheiro. Eu sei que isso vai contra tudo que seus pais te ensinaram, mas...",
                "Trabalhar duro NÃO te fará rico. Na verdade, pode até te deixar mais pobre...",
                "95% dos cursos online são golpe. E vou provar isso para você nos próximos minutos."
            ],
            effectiveness_score=0.75,
            best_niches=["negocios", "educacao", "lifestyle"],
            psychological_principle="Cognitive Dissonance - Desconforto mental quando apresentado com informações que contradizem crenças existentes"
        )
        
        # Personal Story
        hooks["personal_story"] = Hook(
            name="Personal Story Hook",
            hook_type=HookType.PERSONAL_STORY,
            description="Start with a personal, relatable story",
            template="Há {time period} atrás, eu estava {negative situation}. Hoje, {positive outcome}. Deixe-me contar como isso mudou.",
            examples=[
                "Há 2 anos atrás, eu estava dormindo no sofá da casa da minha mãe. Hoje, tenho uma empresa de 7 dígitos. Deixe-me contar como tudo mudou.",
                "Eu já perdi mais de R$ 50.000 tentando aprender marketing digital. Mas esse erro me ensinou a estratégia que uso hoje para...",
                "Na escola, eu era o nerd que ninguém levava a sério. Hoje, ensino empreendedorismo para mais de 100.000 pessoas."
            ],
            effectiveness_score=0.80,
            best_niches=["lifestyle", "negocios", "desenvolvimento_pessoal"],
            psychological_principle="Narrative Transportation - Pessoas se conectam emocionalmente através de histórias pessoais"
        )
        
        # Statistics Shock
        hooks["statistics_shock"] = Hook(
            name="Statistics Shock",
            hook_type=HookType.STATISTICS_SHOCK,
            description="Present shocking or surprising statistics",
            template="{Shocking percentage} das pessoas {negative behavior/outcome}. Se você não quer fazer parte dessa estatística...",
            examples=[
                "97% das pessoas que começam um negócio online falham no primeiro ano. Se você não quer fazer parte dessa estatística...",
                "A pessoa média gasta 7 anos da sua vida no trabalho e morre com apenas R$ 1.000 na conta. Mas existe uma forma diferente...",
                "Apenas 2% das pessoas conseguem se aposentar confortavelmente. O resto depende da família ou do governo."
            ],
            effectiveness_score=0.70,
            best_niches=["negocios", "financas", "saude"],
            psychological_principle="Loss Aversion - Medo de perder ou ficar para trás motiva mais que o desejo de ganhar"
        )
        
        # Direct Question
        hooks["question_direct"] = Hook(
            name="Direct Question",
            hook_type=HookType.QUESTION_DIRECT,
            description="Ask a direct, engaging question to the viewer",
            template="Você já se perguntou {relatable question}? A resposta pode te surpreender...",
            examples=[
                "Você já se perguntou por que algumas pessoas conseguem tudo que querem enquanto outras lutam a vida inteira?",
                "Qual é a diferença entre pessoas que ganham R$ 5.000 e pessoas que ganham R$ 50.000 por mês?",
                "Se você pudesse mudar uma coisa na sua vida hoje, o que seria? E se eu te dissesse que é possível?"
            ],
            effectiveness_score=0.65,
            best_niches=["desenvolvimento_pessoal", "educacao", "lifestyle"],
            psychological_principle="Self-Reference Effect - Pessoas prestam mais atenção quando se sentem diretamente incluídas"
        )
        
        return hooks
    
    def get_hook(self, hook_type: str) -> Optional[Hook]:
        """Get a specific hook by type."""
        return self.hooks.get(hook_type)
    
    def get_hooks_by_niche(self, niche: str) -> List[Hook]:
        """Get all hooks suitable for a specific niche."""
        return [hook for hook in self.hooks.values() if niche in hook.best_niches]
    
    def get_best_hooks(self, min_score: float = 0.75) -> List[Hook]:
        """Get hooks with effectiveness score above threshold."""
        return [hook for hook in self.hooks.values() if hook.effectiveness_score >= min_score]
    
    def generate_hook(self, hook_type: str, context: Dict[str, str]) -> str:
        """Generate a hook using template and context."""
        hook = self.get_hook(hook_type)
        if not hook:
            return ""
        
        template = hook.template
        for key, value in context.items():
            template = template.replace(f"{{{key}}}", value)
        
        return template
    
    def get_all_hooks(self) -> Dict[str, Hook]:
        """Get all available hooks."""
        return self.hooks