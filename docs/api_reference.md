# API Reference - YouTube Script AI

## Core Classes

### TechniqueDatabase

Central database for all storytelling techniques.

```python
from src.storytelling.technique_database import TechniqueDatabase

db = TechniqueDatabase()
```

#### Methods

##### `generate_complete_script_structure(niche, hook_type, structure_type, video_length, topic)`

Generates a complete script structure with all components.

**Parameters:**
- `niche` (str): Content niche (tecnologia, educacao, negocios, lifestyle, entretenimento)
- `hook_type` (str): Type of hook (curiosity_gap, controversy, personal_story, statistics_shock, question_direct)
- `structure_type` (str): Narrative structure (hero_journey, problem_solution, list_format)
- `video_length` (int): Target duration in minutes
- `topic` (str): Specific topic for the video

**Returns:** `Dict[str, Any]` - Complete script structure

##### `search_techniques(query, category=None)`

Search for techniques across all categories.

**Parameters:**
- `query` (str): Search query
- `category` (str, optional): Specific category to search (hooks, structures, patterns)

**Returns:** `Dict[str, List[Any]]` - Search results by category

##### `get_recommendations_for_niche(niche)`

Get technique recommendations for a specific niche.

**Parameters:**
- `niche` (str): Content niche

**Returns:** `Dict[str, List[Any]]` - Recommended techniques by category

---

### ScriptGenerator

Generates complete YouTube scripts using storytelling techniques.

```python
from src.generation.script_generator import ScriptGenerator, ScriptGenerationRequest

generator = ScriptGenerator()
```

#### ScriptGenerationRequest

Data class for script generation parameters.

```python
request = ScriptGenerationRequest(
    topic="Como aprender Python",
    niche="tecnologia",
    hook_type="curiosity_gap",
    structure_type="problem_solution",
    target_duration=10,
    tone="casual",  # casual, professional, enthusiastic, educational
    target_audience="iniciantes",  # iniciantes, intermediarios, avancados, geral
    include_cta=True,
    custom_context={"key": "value"}  # Optional custom context
)
```

#### Methods

##### `generate_script(request)`

Generate a complete script based on the request.

**Parameters:**
- `request` (ScriptGenerationRequest): Generation parameters

**Returns:** `GeneratedScript` - Complete generated script with metadata

##### `generate_multiple_variations(request, count=3)`

Generate multiple variations of a script.

**Parameters:**
- `request` (ScriptGenerationRequest): Generation parameters
- `count` (int): Number of variations to generate

**Returns:** `List[GeneratedScript]` - List of script variations

---

### ScriptAnalyzer

Analyzes scripts for storytelling techniques and quality.

```python
from src.data_processing.script_analyzer import ScriptAnalyzer

analyzer = ScriptAnalyzer()
```

#### Methods

##### `analyze_script(script_text, video_id=None)`

Perform complete analysis of a script.

**Parameters:**
- `script_text` (str): The script text to analyze
- `video_id` (str, optional): Video identifier

**Returns:** `AnalysisResult` - Complete analysis results

##### `analyze_multiple_scripts(scripts)`

Analyze multiple scripts.

**Parameters:**
- `scripts` (List[Tuple[str, str]]): List of (video_id, script_text) tuples

**Returns:** `List[AnalysisResult]` - Analysis results for all scripts

---

### YouTubeCollector

Collects data from YouTube using the official API.

```python
from src.data_collection.youtube_collector import YouTubeCollector

collector = YouTubeCollector(api_key="your_api_key")
```

#### Methods

##### `search_videos(query, max_results=50, published_after=None, order="relevance")`

Search for videos based on query.

**Parameters:**
- `query` (str): Search query
- `max_results` (int): Maximum number of results
- `published_after` (datetime, optional): Filter by publication date
- `order` (str): Sort order (relevance, date, rating, viewCount)

**Returns:** `List[Dict[str, Any]]` - List of video data

##### `get_video_details(video_ids)`

Get detailed information for multiple videos.

**Parameters:**
- `video_ids` (List[str]): List of video IDs

**Returns:** `List[Dict[str, Any]]` - Detailed video information

##### `collect_trending_videos(region_code="BR", category_id=None, max_results=50)`

Collect trending videos from specified region.

**Parameters:**
- `region_code` (str): Region code (BR, US, etc.)
- `category_id` (str, optional): Specific category
- `max_results` (int): Maximum results

**Returns:** `List[Dict[str, Any]]` - Trending videos data

---

### TranscriptExtractor

Extracts and processes YouTube video transcripts.

```python
from src.data_collection.transcript_extractor import TranscriptExtractor

extractor = TranscriptExtractor()
```

#### Methods

##### `extract_transcript(video_id, languages=None)`

Extract transcript from a YouTube video.

**Parameters:**
- `video_id` (str): YouTube video ID
- `languages` (List[str], optional): Preferred languages

**Returns:** `Optional[Dict[str, Any]]` - Transcript data or None if failed

##### `analyze_script_structure(transcript)`

Analyze the structure of a transcript for storytelling elements.

**Parameters:**
- `transcript` (Dict[str, Any]): Transcript data

**Returns:** `Dict[str, Any]` - Structure analysis

---

## Data Structures

### Hook

```python
@dataclass
class Hook:
    name: str
    hook_type: HookType
    description: str
    template: str
    examples: List[str]
    effectiveness_score: float
    best_niches: List[str]
    psychological_principle: str
```

### NarrativeStructure

```python
@dataclass
class NarrativeStructure:
    name: str
    structure_type: StructureType
    description: str
    sections: List[NarrativeSection]
    best_for: List[str]
    engagement_score: float
    typical_duration: str
    psychological_principle: str
```

### EngagementTechnique

```python
@dataclass
class EngagementTechnique:
    name: str
    technique_type: EngagementType
    description: str
    when_to_use: str
    template: str
    examples: List[str]
    effectiveness_score: float
    timing_recommendations: List[str]
```

### GeneratedScript

```python
@dataclass
class GeneratedScript:
    script_text: str
    metadata: Dict[str, Any]
    techniques_used: List[str]
    structure_breakdown: Dict[str, str]
    estimated_duration: float
    quality_score: float
```

### AnalysisResult

```python
@dataclass
class AnalysisResult:
    video_id: str
    script_text: str
    identified_techniques: Dict[str, List[str]]
    structure_analysis: Dict[str, Any]
    engagement_score: float
    quality_metrics: Dict[str, float]
    recommendations: List[str]
```

## Constants and Enums

### HookType

```python
class HookType(Enum):
    CURIOSITY_GAP = "curiosity_gap"
    CONTROVERSY = "controversy"
    PERSONAL_STORY = "personal_story"
    STATISTICS_SHOCK = "statistics_shock"
    QUESTION_DIRECT = "question_direct"
    PATTERN_INTERRUPT = "pattern_interrupt"
    PREVIEW_TEASER = "preview_teaser"
    EMOTIONAL_TRIGGER = "emotional_trigger"
    AUTHORITY_STATEMENT = "authority_statement"
```

### StructureType

```python
class StructureType(Enum):
    HERO_JOURNEY = "hero_journey"
    PROBLEM_SOLUTION = "problem_solution"
    BEFORE_AFTER = "before_after"
    LIST_FORMAT = "list_format"
    TUTORIAL_STEP = "tutorial_step"
    STORY_LESSON = "story_lesson"
    COMPARE_CONTRAST = "compare_contrast"
    CHRONOLOGICAL = "chronological"
```

### EngagementType

```python
class EngagementType(Enum):
    PATTERN_INTERRUPT = "pattern_interrupt"
    CALLBACK = "callback"
    SUSPENSE_BUILDER = "suspense_builder"
    INTERACTION_PROMPT = "interaction_prompt"
    VISUAL_TRANSITION = "visual_transition"
    ENERGY_SHIFT = "energy_shift"
    PREVIEW_HOOK = "preview_hook"
    SOCIAL_PROOF = "social_proof"
```

## Configuration

### config.yaml Structure

```yaml
youtube:
  api_key: "YOUR_API_KEY"
  max_results: 50
  quality_threshold: 0.7

model:
  base_model: "meta-llama/Llama-2-7b-hf"
  max_length: 2048
  temperature: 0.7
  top_p: 0.9

training:
  theory_weight: 0.4
  practice_weight: 0.6
  validation_split: 0.2

data_collection:
  min_views: 10000
  min_engagement_rate: 0.02
  max_duration_minutes: 30
  languages: ["pt", "en"]
  niches: ["tecnologia", "educacao", "entretenimento", "lifestyle", "negocios"]

storytelling:
  hook_types: ["curiosity_gap", "controversy", "personal_story"]
  narrative_structures: ["hero_journey", "problem_solution", "list_format"]

generation:
  max_script_length: 1500
  min_script_length: 300
  include_analysis: true
  output_formats: ["markdown", "json", "txt"]

interface:
  port: 7860
  share: false
  debug: false
```

## Error Handling

All methods include appropriate error handling and logging. Common exceptions:

- `ValueError`: Invalid parameters or configuration
- `FileNotFoundError`: Missing configuration or data files
- `HttpError`: YouTube API errors
- `Exception`: General errors with detailed logging

## Examples

See `examples/quick_start.py` for comprehensive usage examples of all API components.