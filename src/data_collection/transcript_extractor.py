"""
Transcript extraction from YouTube videos.

This module handles the extraction and processing of YouTube video transcripts
using the youtube-transcript-api library.
"""

import logging
from typing import List, Dict, Optional, Any
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
import re


class TranscriptExtractor:
    """Extracts and processes YouTube video transcripts."""
    
    def __init__(self):
        self.logger = self._setup_logging()
        self.formatter = TextFormatter()
    
    def _setup_logging(self) -> logging.Logger:
        """Setup logging for the extractor."""
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
    
    def extract_transcript(self, video_id: str, languages: List[str] = None) -> Optional[Dict[str, Any]]:
        """Extract transcript from a YouTube video."""
        if languages is None:
            languages = ['pt', 'pt-BR', 'en', 'en-US']
        
        try:
            # Try to get transcript in preferred language order
            transcript_data = YouTubeTranscriptApi.get_transcript(
                video_id, 
                languages=languages
            )
            
            # Format transcript
            formatted_transcript = self.formatter.format_transcript(transcript_data)
            
            # Process transcript data
            processed_transcript = self._process_transcript(transcript_data, formatted_transcript)
            processed_transcript['video_id'] = video_id
            processed_transcript['languages_attempted'] = languages
            
            self.logger.info(f"Successfully extracted transcript for video {video_id}")
            return processed_transcript
            
        except Exception as e:
            self.logger.warning(f"Could not extract transcript for video {video_id}: {e}")
            return None
    
    def _process_transcript(self, transcript_data: List[Dict], formatted_text: str) -> Dict[str, Any]:
        """Process raw transcript data into structured format."""
        
        # Basic statistics
        total_duration = max([item['start'] + item['duration'] for item in transcript_data])
        word_count = len(formatted_text.split())
        
        # Extract timing information
        segments = []
        for item in transcript_data:
            segments.append({
                'start_time': item['start'],
                'end_time': item['start'] + item['duration'], 
                'duration': item['duration'],
                'text': item['text'].strip(),
                'word_count': len(item['text'].split())
            })
        
        # Identify potential hook (first 30 seconds)
        hook_segments = [seg for seg in segments if seg['start_time'] <= 30]
        hook_text = ' '.join([seg['text'] for seg in hook_segments])
        
        # Calculate speaking rate (words per minute)
        speaking_rate = (word_count / total_duration) * 60 if total_duration > 0 else 0
        
        # Identify pauses (segments with longer duration relative to word count)
        avg_words_per_second = word_count / total_duration if total_duration > 0 else 0
        pauses = []
        for seg in segments:
            expected_duration = seg['word_count'] / avg_words_per_second if avg_words_per_second > 0 else seg['duration']
            if seg['duration'] > expected_duration * 2 and seg['duration'] > 3:  # Pause longer than 3 seconds
                pauses.append({
                    'start_time': seg['start_time'],
                    'duration': seg['duration'],
                    'type': 'pause'
                })
        
        return {
            'full_text': formatted_text,
            'segments': segments,
            'hook_text': hook_text,
            'statistics': {
                'total_duration_seconds': total_duration,
                'total_duration_minutes': total_duration / 60,
                'word_count': word_count,
                'segment_count': len(segments),
                'speaking_rate_wpm': speaking_rate,
                'pause_count': len(pauses),
                'average_segment_duration': sum([seg['duration'] for seg in segments]) / len(segments)
            },
            'pauses': pauses,
            'language_detected': self._detect_language(formatted_text)
        }
    
    def _detect_language(self, text: str) -> str:
        """Simple language detection based on common words."""
        portuguese_indicators = ['que', 'não', 'com', 'uma', 'para', 'você', 'isso', 'como', 'mais', 'muito']
        english_indicators = ['the', 'and', 'that', 'have', 'for', 'not', 'with', 'you', 'this', 'but']
        
        text_lower = text.lower()
        pt_score = sum([text_lower.count(word) for word in portuguese_indicators])
        en_score = sum([text_lower.count(word) for word in english_indicators])
        
        return 'pt' if pt_score > en_score else 'en'
    
    def extract_multiple_transcripts(self, video_ids: List[str], languages: List[str] = None) -> Dict[str, Dict[str, Any]]:
        """Extract transcripts from multiple videos."""
        results = {}
        
        for video_id in video_ids:
            transcript = self.extract_transcript(video_id, languages)
            if transcript:
                results[video_id] = transcript
        
        self.logger.info(f"Successfully extracted {len(results)} transcripts out of {len(video_ids)} videos")
        return results
    
    def analyze_script_structure(self, transcript: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze the structure of a transcript for storytelling elements."""
        segments = transcript['segments']
        full_text = transcript['full_text']
        
        # Identify potential structure elements
        analysis = {
            'hook_analysis': self._analyze_hook(transcript['hook_text']),
            'engagement_elements': self._find_engagement_elements(full_text),
            'call_to_actions': self._find_call_to_actions(full_text),
            'story_markers': self._find_story_markers(full_text),
            'question_patterns': self._find_questions(full_text),
            'energy_changes': self._detect_energy_changes(segments)
        }
        
        return analysis
    
    def _analyze_hook(self, hook_text: str) -> Dict[str, Any]:
        """Analyze the hook for common techniques."""
        hook_indicators = {
            'question': r'\?',
            'numbers': r'\b\d+%|\b\d+\s*(pessoas|milhões|mil|anos)',
            'controversy': r'(nunca|ninguém|segredo|verdade|mentira|errado)',
            'personal': r'(eu|minha|meu|comigo|aconteceu)',
            'curiosity': r'(descobri|revelou|segredo|surpresa|incrível)',
            'urgency': r'(agora|hoje|importante|crucial|precisa)'
        }
        
        detected_techniques = {}
        for technique, pattern in hook_indicators.items():
            matches = re.findall(pattern, hook_text.lower())
            detected_techniques[technique] = len(matches)
        
        return {
            'text': hook_text,
            'word_count': len(hook_text.split()),
            'techniques_detected': detected_techniques,
            'dominant_technique': max(detected_techniques.keys(), key=lambda k: detected_techniques[k])
        }
    
    def _find_engagement_elements(self, text: str) -> List[Dict[str, Any]]:
        """Find engagement elements in the transcript."""
        patterns = {
            'direct_address': r'(você|vocês)',
            'questions': r'[^.!?]*\?',
            'exclamations': r'[^.!?]*!',
            'callbacks': r'(lembra|como falei|mencionei)',
            'previews': r'(vou mostrar|em breve|daqui a pouco)'
        }
        
        elements = []
        for element_type, pattern in patterns.items():
            matches = re.finditer(pattern, text.lower())
            for match in matches:
                elements.append({
                    'type': element_type,
                    'text': match.group(),
                    'position': match.start()
                })
        
        return elements
    
    def _find_call_to_actions(self, text: str) -> List[str]:
        """Find call-to-action phrases."""
        cta_patterns = [
            r'se inscreva',
            r'deixe.*like',
            r'comenta.*embaixo',
            r'compartilhe',
            r'ative.*sininho',
            r'clica.*link'
        ]
        
        ctas = []
        for pattern in cta_patterns:
            matches = re.findall(pattern, text.lower())
            ctas.extend(matches)
        
        return ctas
    
    def _find_story_markers(self, text: str) -> List[str]:
        """Find story structure markers."""
        story_patterns = [
            r'era uma vez',
            r'aconteceu que',
            r'primeiro',
            r'depois',
            r'finalmente',
            r'no final',
            r'resultado foi'
        ]
        
        markers = []
        for pattern in story_patterns:
            matches = re.findall(pattern, text.lower())
            markers.extend(matches)
        
        return markers
    
    def _find_questions(self, text: str) -> List[str]:
        """Extract all questions from the text."""
        questions = re.findall(r'[^.!?]*\?', text)
        return [q.strip() for q in questions if len(q.strip()) > 5]
    
    def _detect_energy_changes(self, segments: List[Dict]) -> List[Dict[str, Any]]:
        """Detect potential energy changes based on segment patterns."""
        changes = []
        
        for i in range(1, len(segments)):
            prev_seg = segments[i-1]
            curr_seg = segments[i]
            
            # Detect significant duration changes (possible energy shifts)
            duration_change = abs(curr_seg['duration'] - prev_seg['duration'])
            if duration_change > 2:  # More than 2 seconds difference
                changes.append({
                    'timestamp': curr_seg['start_time'],
                    'type': 'pace_change',
                    'description': f"Duration change from {prev_seg['duration']:.1f}s to {curr_seg['duration']:.1f}s"
                })
        
        return changes