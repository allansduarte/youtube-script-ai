# Guia de Uso - YouTube Script AI

## Visão Geral

O YouTube Script AI é um sistema completo para geração de scripts de YouTube utilizando técnicas avançadas de storytelling. Este guia cobre todas as funcionalidades principais do sistema.

## Modos de Operação

### 1. Interface Web (Recomendado)

```bash
python src/main.py --mode interface
```

Abre uma interface web amigável em `http://localhost:7860` (requer gradio instalado).

**Nova funcionalidade**: Agora inclui campo de descrição opcional em ambas as abas para fornecer contexto adicional ao LLM.

### 2. Interface CLI (Atualizada)

A interface de linha de comando agora inclui prompt para descrição opcional:

```bash
python app/simple_cli.py
```

Exemplo de uso com descrição:
```
Tópico do vídeo: Como criar um e-commerce
Descrição (opcional): tenho loja física e quero vender online
```

### 2. Geração de Scripts

#### Geração Rápida de Estrutura
```bash
python src/main.py --mode generate --niche tecnologia --topic "Como aprender Python"
```

#### Geração Completa de Script
```bash
python src/main.py --mode generate --topic "Como criar seu primeiro app"
```

### 3. Exemplos Interativos

```bash
python examples/quick_start.py
```

Executa exemplos completos demonstrando todas as funcionalidades.

## Interface Web Atualizada

A interface web agora inclui o campo de **descrição** em ambas as abas:

### Tab "Estrutura"
- Campo de descrição com placeholder e dicas
- Máximo de 500 caracteres
- Exemplos contextuais mostrados
- Descrição aparece nos metadados da estrutura gerada

### Tab "Script Completo"  
- Mesmo campo de descrição para consistência
- Descrição incorporada no script final
- Metadados incluem a descrição fornecida
- Melhor qualidade de script quando descrição é fornecida

### Exemplos de Uso na Interface Web

#### Exemplo Tecnologia:
- **Tópico**: "Como criar um app móvel"
- **Descrição**: "quero criar um app de delivery para competir com iFood"

#### Exemplo Negócios:
- **Tópico**: "Como começar dropshipping"  
- **Descrição**: "tenho R$ 2000 para investir e quero trabalhar de casa"

#### Exemplo Educação:
- **Tópico**: "Como passar no ENEM"
- **Descrição**: "estudo à noite depois do trabalho e tenho dificuldade em exatas"

## Uso Programático

### Geração Básica de Estrutura

```python
from src.storytelling.technique_database import TechniqueDatabase

# Inicializar o banco de técnicas
db = TechniqueDatabase()

# Gerar estrutura de script
structure = db.generate_complete_script_structure(
    niche="tecnologia",
    hook_type="curiosity_gap",
    structure_type="problem_solution", 
    video_length=10,
    topic="Como aprender programação do zero"
)

print(f"Hook: {structure['hook']['type']}")
print(f"Estrutura: {structure['structure']['name']}")
```

### Geração Completa de Script

```python
from src.generation.script_generator import ScriptGenerator, ScriptGenerationRequest

# Inicializar o gerador
generator = ScriptGenerator()

# Criar requisição de geração com descrição (novo campo opcional)
request = ScriptGenerationRequest(
    topic="Como começar no YouTube",
    description="tenho câmera simples e R$ 500 para investir",  # Novo campo opcional
    niche="entretenimento",
    hook_type="personal_story",
    structure_type="hero_journey",
    target_duration=12,
    tone="casual",
    target_audience="iniciantes",
    include_cta=True
)

# Gerar script
script = generator.generate_script(request)

print(f"Script gerado:")
print(f"Qualidade: {script.quality_score:.2f}")
print(f"Duração: {script.estimated_duration:.1f} min")
print(script.script_text)
```

### Exemplo sem Descrição (Compatibilidade com Versão Anterior)

```python
# A descrição é opcional - o código anterior continua funcionando
request = ScriptGenerationRequest(
    topic="Como aprender programação",
    niche="tecnologia",
    hook_type="curiosity_gap",
    structure_type="problem_solution",
    target_duration=10,
    tone="educational",
    target_audience="iniciantes",
    include_cta=True
    # description não especificado - script será gerado normalmente
)

script = generator.generate_script(request)
```

### Análise de Scripts Existentes

```python
from src.data_processing.script_analyzer import ScriptAnalyzer

# Inicializar analisador
analyzer = ScriptAnalyzer()

# Texto do script para análise
script_text = """
Galera, hoje vou ensinar como criar seu primeiro app...
[resto do script]
"""

# Analisar script
analysis = analyzer.analyze_script(script_text, "video_123")

print(f"Score de engajamento: {analysis.engagement_score:.2f}")
print(f"Hooks identificados: {analysis.identified_techniques['hooks']}")
print(f"Recomendações: {analysis.recommendations}")
```

## Técnicas de Storytelling Disponíveis

### Hooks (Aberturas)

#### 1. Curiosity Gap
- **Descrição**: Cria lacuna entre o que sabemos e queremos saber
- **Exemplo**: "Eu descobri que 90% das pessoas fazem isso errado..."
- **Melhor para**: Educação, Tecnologia, Negócios

#### 2. Controversy
- **Descrição**: Apresenta declaração controversa
- **Exemplo**: "A faculdade é perda de tempo..."
- **Melhor para**: Negócios, Educação, Lifestyle

#### 3. Personal Story
- **Descrição**: Inicia com história pessoal envolvente
- **Exemplo**: "Há 2 anos eu estava dormindo no sofá..."
- **Melhor para**: Lifestyle, Negócios, Desenvolvimento Pessoal

#### 4. Statistics Shock
- **Descrição**: Apresenta estatísticas surpreendentes
- **Exemplo**: "97% das pessoas falham no primeiro ano..."
- **Melhor para**: Negócios, Finanças, Saúde

#### 5. Direct Question
- **Descrição**: Faz pergunta direta ao viewer
- **Exemplo**: "Você já se perguntou por que..."
- **Melhor para**: Desenvolvimento Pessoal, Educação

### Estruturas Narrativas

#### 1. Hero's Journey (Jornada do Herói)
- **Seções**: Mundo Comum → Chamado → Jornada → Transformação → Retorno
- **Melhor para**: Desenvolvimento pessoal, Empreendedorismo
- **Duração**: 8-15 minutos

#### 2. Problem-Solution (Problema-Solução)
- **Seções**: Identificação → Amplificação → Solução → Explicação → CTA
- **Melhor para**: Educação, Tecnologia, Tutoriais
- **Duração**: 5-12 minutos

#### 3. List Format (Formato Lista)
- **Seções**: Introdução → Desenvolvimento dos Itens → Resumo
- **Melhor para**: Dicas, Reviews, Comparações
- **Duração**: 3-10 minutos

### Padrões de Engajamento

#### Pattern Interrupt
- **Uso**: Quebra padrão para reganhar atenção
- **Exemplo**: "Espera, acabei de falar bobagem..."
- **Timing**: 3-4 min, 7-8 min

#### Callback
- **Uso**: Referencia pontos anteriores
- **Exemplo**: "Lembra do que falei no início?"
- **Timing**: Meio do vídeo, conclusão

#### Social Proof
- **Uso**: Usa evidência social para credibilidade
- **Exemplo**: "Mais de 1000 pessoas já confirmaram..."
- **Timing**: Após afirmações importantes

## Campo Descrição (Novo)

### O que é a Descrição?
O campo de **descrição** é uma nova funcionalidade opcional que permite fornecer contexto adicional sobre:
- Sua situação específica
- Objetivo com o vídeo
- Público-alvo específico
- Limitações ou recursos disponíveis
- Resultados esperados

### Como Usar a Descrição

#### Bons Exemplos de Descrição:
- **Tecnologia**: "quero criar meu primeiro app para conseguir emprego como desenvolvedor"
- **Negócios**: "tenho R$ 1000 para investir e 3 horas por dia disponíveis"
- **Educação**: "trabalho 8h por dia e só tenho 2h para estudar concursos"
- **Lifestyle**: "sempre acordo cansado e sem energia para o dia"
- **YouTube**: "tenho câmera simples e quero gerar renda extra"

#### Dicas para Escrever uma Boa Descrição:
1. **Seja específico**: Mencione números, tempo, recursos
2. **Inclua contexto**: Sua situação atual ou limitações
3. **Defina objetivo**: O que você quer alcançar
4. **Mantenha conciso**: Máximo 500 caracteres
5. **Use linguagem natural**: Escreva como você falaria

### Impacto da Descrição na Qualidade
Quando você fornece uma descrição:
- **Hooks mais personalizados**: O script será mais relevante para sua situação
- **Exemplos mais precisos**: Referências diretas ao seu contexto
- **Conteúdo mais direcionado**: Foco no que você realmente precisa
- **Maior engajamento**: Audiência se identifica mais com situações reais

## Personalização por Nicho

### Tecnologia
- **Hooks recomendados**: Curiosity Gap, Statistics Shock
- **Estruturas**: Problem-Solution, List Format
- **Tom**: Professional, Educational

### Negócios
- **Hooks recomendados**: Controversy, Personal Story
- **Estruturas**: Hero's Journey, Problem-Solution
- **Tom**: Professional, Enthusiastic

### Educação
- **Hooks recomendados**: Curiosity Gap, Direct Question
- **Estruturas**: Problem-Solution, List Format
- **Tom**: Educational, Casual

### Lifestyle
- **Hooks recomendados**: Personal Story, Direct Question
- **Estruturas**: Hero's Journey, Before-After
- **Tom**: Casual, Enthusiastic

### Entretenimento
- **Hooks recomendados**: Controversy, Statistics Shock
- **Estruturas**: List Format, Chronological
- **Tom**: Enthusiastic, Casual

## Configuração de Tom

### Casual
- **Características**: Linguagem informal, conectores como "galera", "mano"
- **Uso**: Lifestyle, entretenimento, público jovem

### Professional
- **Características**: Linguagem formal, conectores como "é importante notar"
- **Uso**: Negócios, educação corporativa

### Enthusiastic
- **Características**: Muita energia, exclamações, ênfase
- **Uso**: Motivação, vendas, entretenimento

### Educational
- **Características**: Explicações claras, estrutura lógica
- **Uso**: Tutoriais, cursos, educação

## Adaptação de Audiência

### Iniciantes
- **Complexidade**: Baixa
- **Explicações**: Detalhadas
- **Vocabulário**: Simples
- **Exemplos**: Básicos

### Intermediários
- **Complexidade**: Média
- **Explicações**: Moderadas
- **Vocabulário**: Técnico
- **Exemplos**: Práticos

### Avançados
- **Complexidade**: Alta
- **Explicações**: Mínimas
- **Vocabulário**: Expert
- **Exemplos**: Avançados

### Geral
- **Complexidade**: Média
- **Explicações**: Quando necessário
- **Vocabulário**: Acessível
- **Exemplos**: Variados

## Métricas de Qualidade

### Engagement Score (0-1)
- **0.8-1.0**: Excelente - Script altamente envolvente
- **0.6-0.8**: Bom - Script com bom potencial
- **0.4-0.6**: Regular - Precisa melhorias
- **0.0-0.4**: Ruim - Requer revisão completa

### Componentes do Score
- **Hook Quality (25%)**: Eficácia da abertura
- **Engagement Elements (35%)**: Padrões de engajamento
- **Story Structure (25%)**: Elementos narrativos
- **Length Appropriateness (15%)**: Duração adequada

## Dicas de Otimização

### Para Melhor Engajamento
1. **Use múltiplos hooks**: Combine diferentes técnicas
2. **Adicione pattern interrupts**: A cada 3-4 minutos
3. **Inclua social proof**: Valide suas afirmações
4. **Faça perguntas**: Mantenha audiência ativa

### Para Melhor Retenção
1. **Hook forte**: Primeiros 15 segundos são críticos
2. **Preview do conteúdo**: Antecipe o que vem
3. **Callbacks**: Referencie pontos anteriores
4. **Transições claras**: Use conectores

### Para Melhor Conversão
1. **CTAs claros**: Like, subscribe, comment
2. **Próximos passos**: Dê direção específica
3. **Urgência**: Crie senso de ação imediata
4. **Valor primeiro**: Entregue antes de pedir

## Solução de Problemas

### Script muito repetitivo
- **Causa**: Geração automática limitada
- **Solução**: Use custom_context para variação

### Score de qualidade baixo
- **Causa**: Falta de elementos de engajamento
- **Solução**: Adicione mais técnicas, ajuste duração

### Hook não apropriado
- **Causa**: Incompatibilidade com nicho
- **Solução**: Use recomendações por nicho

### Estrutura confusa
- **Causa**: Muitas seções ou mal organizadas
- **Solução**: Simplifique, use menos seções