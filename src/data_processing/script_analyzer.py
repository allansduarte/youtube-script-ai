"""
Script analyzer for processing and analyzing YouTube video scripts.

This module analyzes scripts to identify storytelling techniques,
narrative structures, and engagement patterns used.
"""

import re
import logging
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import json


@dataclass
class AnalysisResult:
    """Result of script analysis."""
    video_id: str
    script_text: str
    identified_techniques: Dict[str, List[str]]
    structure_analysis: Dict[str, Any]
    engagement_score: float
    quality_metrics: Dict[str, float]
    recommendations: List[str]


class ScriptAnalyzer:
    """Analyzes scripts for storytelling techniques and patterns."""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.hook_patterns = self._initialize_hook_patterns()
        self.engagement_patterns = self._initialize_engagement_patterns()
        self.story_markers = self._initialize_story_markers()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the analyzer."""
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
    
    def _initialize_hook_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for identifying hook techniques."""
        return {
            "curiosity_gap": [
                r"eu descobri que",
                r"existe um segredo",
                r"o que vou.*mostrar",
                r"você não vai acreditar",
                r"descoberta.*surpreendente"
            ],
            "controversy": [
                r"vai contra tudo",
                r"é uma mentira",
                r"não é verdade",
                r"estão.*errado",
                r"a verdade é"
            ],
            "personal_story": [
                r"há.*anos.*atrás",
                r"eu estava",
                r"comigo aconteceu",
                r"minha história",
                r"quando eu.*tinha"
            ],
            "statistics_shock": [
                r"\d+%.*pessoas",
                r"\d+.*em cada",
                r"apenas \d+%",
                r"mais de \d+.*milhões",
                r"estatística.*chocante"
            ],
            "question_direct": [
                r"você já se perguntou",
                r"qual.*diferença",
                r"por que.*algumas pessoas",
                r"você sabia que",
                r"já aconteceu.*você"
            ]
        }
    
    def _initialize_engagement_patterns(self) -> Dict[str, List[str]]:
        """Initialize patterns for engagement techniques."""
        return {
            "pattern_interrupt": [
                r"espera",
                r"pare tudo",
                r"calma aí",
                r"ops",
                r"aliás"
            ],
            "callback": [
                r"lembra.*início",
                r"como.*falei",
                r"voltando.*aquela",
                r"aquela.*história",
                r"como.*mencionei"
            ],
            "social_proof": [
                r"não sou só eu",
                r"mais de.*pessoas",
                r"meus.*alunos",
                r"especialistas.*recomendam",
                r"estudos.*mostram"
            ],
            "interaction": [
                r"deixe.*comentários",
                r"escreva.*sim",
                r"dê.*like",
                r"se.*inscreva",
                r"compartilhe"
            ]
        }
    
    def _initialize_story_markers(self) -> Dict[str, List[str]]:
        """Initialize markers for story structure."""
        return {
            "beginning": [
                r"era uma vez",
                r"começou quando",
                r"tudo.*começou",
                r"primeira vez",
                r"no início"
            ],
            "conflict": [
                r"problema.*surgiu",
                r"dificuldade.*apareceu",
                r"desafio.*maior",
                r"obstáculo",
                r"erro.*cometi"
            ],
            "resolution": [
                r"solução.*encontrei",
                r"descobri.*como",
                r"finalmente.*consegui",
                r"resultado.*foi",
                r"aprendi.*que"
            ],
            "lesson": [
                r"lição.*importante",
                r"o.*que.*aprendi",
                r"moral.*história",
                r"takeaway",
                r"resumindo"
            ]
        }
    
    def analyze_script(self, script_text: str, video_id: str = None) -> AnalysisResult:
        """Perform complete analysis of a script."""
        script_text = script_text.lower()
        
        # Identify techniques
        identified_techniques = {
            "hooks": self._identify_hooks(script_text),
            "engagement": self._identify_engagement_patterns(script_text),
            "story_elements": self._identify_story_elements(script_text)
        }
        
        # Analyze structure
        structure_analysis = self._analyze_structure(script_text)
        
        # Calculate engagement score
        engagement_score = self._calculate_engagement_score(script_text, identified_techniques)
        
        # Calculate quality metrics
        quality_metrics = self._calculate_quality_metrics(script_text, identified_techniques)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(
            identified_techniques, structure_analysis, quality_metrics
        )
        
        return AnalysisResult(
            video_id=video_id or "unknown",
            script_text=script_text,
            identified_techniques=identified_techniques,
            structure_analysis=structure_analysis,
            engagement_score=engagement_score,
            quality_metrics=quality_metrics,
            recommendations=recommendations
        )
    
    def _identify_hooks(self, text: str) -> List[str]:
        """Identify hook techniques used in the script."""
        identified = []
        
        # Focus on first 200 words for hook analysis
        words = text.split()[:200]
        hook_text = " ".join(words)
        
        for hook_type, patterns in self.hook_patterns.items():
            for pattern in patterns:
                if re.search(pattern, hook_text):
                    identified.append(hook_type)
                    break
        
        return identified
    
    def _identify_engagement_patterns(self, text: str) -> List[str]:
        """Identify engagement patterns throughout the script."""
        identified = []
        
        for pattern_type, patterns in self.engagement_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    identified.append(pattern_type)
                    break
        
        return identified
    
    def _identify_story_elements(self, text: str) -> List[str]:
        """Identify story structure elements."""
        identified = []
        
        for element_type, patterns in self.story_markers.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    identified.append(element_type)
                    break
        
        return identified
    
    def _analyze_structure(self, text: str) -> Dict[str, Any]:
        """Analyze the overall structure of the script."""
        words = text.split()
        total_words = len(words)
        
        # Divide into sections for analysis
        section_size = total_words // 4
        sections = [
            " ".join(words[i:i+section_size]) 
            for i in range(0, total_words, section_size)
        ]
        
        structure = {
            "total_words": total_words,
            "estimated_duration_minutes": total_words / 150,  # ~150 words per minute
            "sections": len(sections),
            "hook_strength": self._assess_hook_strength(sections[0] if sections else ""),
            "conclusion_strength": self._assess_conclusion_strength(sections[-1] if sections else ""),
            "narrative_flow": self._assess_narrative_flow(sections)
        }
        
        return structure
    
    def _assess_hook_strength(self, hook_section: str) -> float:
        """Assess the strength of the hook (0-1)."""
        score = 0.0
        
        # Check for hook techniques
        hook_count = sum(1 for hook_type, patterns in self.hook_patterns.items()
                        for pattern in patterns if re.search(pattern, hook_section))
        
        score += min(hook_count * 0.3, 0.6)  # Up to 0.6 for multiple hooks
        
        # Check for emotional words
        emotional_words = ["incrível", "surpreendente", "chocante", "impressionante", "revolucionário"]
        emotion_count = sum(1 for word in emotional_words if word in hook_section)
        score += min(emotion_count * 0.1, 0.2)  # Up to 0.2 for emotional words
        
        # Check for specific promises
        promise_patterns = ["vou.*mostrar", "você.*vai.*aprender", "vai.*descobrir"]
        promise_count = sum(1 for pattern in promise_patterns if re.search(pattern, hook_section))
        score += min(promise_count * 0.1, 0.2)  # Up to 0.2 for promises
        
        return min(score, 1.0)
    
    def _assess_conclusion_strength(self, conclusion_section: str) -> float:
        """Assess the strength of the conclusion (0-1)."""
        score = 0.0
        
        # Check for call-to-action
        cta_patterns = ["se inscreva", "deixe.*like", "compartilhe", "comenta", "ative.*sino"]
        cta_count = sum(1 for pattern in cta_patterns if re.search(pattern, conclusion_section))
        score += min(cta_count * 0.3, 0.6)
        
        # Check for summary/recap
        summary_patterns = ["resumindo", "recapitulando", "em resumo", "principais.*pontos"]
        summary_count = sum(1 for pattern in summary_patterns if re.search(pattern, conclusion_section))
        score += min(summary_count * 0.2, 0.4)
        
        return min(score, 1.0)
    
    def _assess_narrative_flow(self, sections: List[str]) -> float:
        """Assess the narrative flow between sections (0-1)."""
        if len(sections) < 2:
            return 0.5
        
        # Check for transition words
        transition_patterns = ["agora", "depois", "então", "em seguida", "primeiro", "segundo"]
        transition_score = 0.0
        
        for section in sections[1:]:  # Skip first section
            section_transitions = sum(1 for pattern in transition_patterns 
                                    if re.search(pattern, section[:100]))  # First 100 chars
            transition_score += min(section_transitions * 0.2, 0.3)
        
        # Normalize by number of sections
        avg_transition_score = transition_score / (len(sections) - 1)
        
        return min(avg_transition_score, 1.0)
    
    def _calculate_engagement_score(self, text: str, techniques: Dict[str, List[str]]) -> float:
        """Calculate overall engagement score (0-1)."""
        score = 0.0
        
        # Hook score (25% of total)
        hook_score = len(techniques["hooks"]) * 0.05  # Up to 0.25 for 5 hooks
        score += min(hook_score, 0.25)
        
        # Engagement patterns score (35% of total)
        engagement_score = len(techniques["engagement"]) * 0.08  # Up to 0.35 for ~4 patterns
        score += min(engagement_score, 0.35)
        
        # Story elements score (25% of total)
        story_score = len(techniques["story_elements"]) * 0.06  # Up to 0.25 for 4 elements
        score += min(story_score, 0.25)
        
        # Length appropriateness (15% of total)
        words = len(text.split())
        if 300 <= words <= 2000:  # Good length range
            length_score = 0.15
        elif 200 <= words < 300 or 2000 < words <= 3000:
            length_score = 0.10
        else:
            length_score = 0.05
        
        score += length_score
        
        return min(score, 1.0)
    
    def _calculate_quality_metrics(self, text: str, techniques: Dict[str, List[str]]) -> Dict[str, float]:
        """Calculate various quality metrics."""
        words = text.split()
        sentences = text.split('.')
        
        return {
            "readability": self._calculate_readability(words, sentences),
            "technique_diversity": len(set(techniques["hooks"] + techniques["engagement"] + techniques["story_elements"])) / 12,
            "hook_quality": min(len(techniques["hooks"]) / 3, 1.0),
            "engagement_frequency": len(techniques["engagement"]) / max(len(words) / 200, 1),  # Engagements per 200 words
            "story_completeness": len(techniques["story_elements"]) / 4
        }
    
    def _calculate_readability(self, words: List[str], sentences: List[str]) -> float:
        """Calculate readability score (simplified)."""
        if not words or not sentences:
            return 0.0
        
        avg_sentence_length = len(words) / len(sentences)
        
        # Simple readability based on sentence length
        if 10 <= avg_sentence_length <= 20:
            return 1.0
        elif 8 <= avg_sentence_length < 10 or 20 < avg_sentence_length <= 25:
            return 0.8
        elif 6 <= avg_sentence_length < 8 or 25 < avg_sentence_length <= 30:
            return 0.6
        else:
            return 0.4
    
    def _generate_recommendations(self, 
                                techniques: Dict[str, List[str]], 
                                structure: Dict[str, Any], 
                                quality: Dict[str, float]) -> List[str]:
        """Generate recommendations for improvement."""
        recommendations = []
        
        # Hook recommendations
        if not techniques["hooks"]:
            recommendations.append("Adicione um hook forte no início do vídeo para capturar atenção")
        elif len(techniques["hooks"]) == 1:
            recommendations.append("Considere combinar múltiplas técnicas de hook para maior impacto")
        
        # Engagement recommendations
        if len(techniques["engagement"]) < 2:
            recommendations.append("Adicione mais elementos de engajamento ao longo do vídeo")
        
        # Structure recommendations
        if structure["hook_strength"] < 0.5:
            recommendations.append("Fortaleça o hook com mais curiosidade, controvérsia ou história pessoal")
        
        if structure["conclusion_strength"] < 0.5:
            recommendations.append("Melhore a conclusão com call-to-actions claros e resumo dos pontos principais")
        
        if structure["narrative_flow"] < 0.5:
            recommendations.append("Use mais palavras de transição para melhorar o fluxo narrativo")
        
        # Quality recommendations
        if quality["readability"] < 0.6:
            recommendations.append("Ajuste o tamanho das frases para melhorar a legibilidade")
        
        if quality["technique_diversity"] < 0.4:
            recommendations.append("Diversifique as técnicas de storytelling usadas")
        
        # Duration recommendations
        duration = structure["estimated_duration_minutes"]
        if duration < 3:
            recommendations.append("Considere expandir o conteúdo - vídeos muito curtos podem ter menor alcance")
        elif duration > 15:
            recommendations.append("Considere dividir em vídeos menores ou remover conteúdo menos essencial")
        
        return recommendations
    
    def analyze_multiple_scripts(self, scripts: List[Tuple[str, str]]) -> List[AnalysisResult]:
        """Analyze multiple scripts and return results."""
        results = []
        
        for video_id, script_text in scripts:
            try:
                result = self.analyze_script(script_text, video_id)
                results.append(result)
                self.logger.info(f"Analyzed script for video {video_id}")
            except Exception as e:
                self.logger.error(f"Error analyzing script for video {video_id}: {e}")
        
        return results
    
    def export_analysis(self, result: AnalysisResult, file_path: str) -> None:
        """Export analysis result to JSON file."""
        data = {
            "video_id": result.video_id,
            "script_text": result.script_text,
            "identified_techniques": result.identified_techniques,
            "structure_analysis": result.structure_analysis,
            "engagement_score": result.engagement_score,
            "quality_metrics": result.quality_metrics,
            "recommendations": result.recommendations
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        self.logger.info(f"Analysis exported to {file_path}")