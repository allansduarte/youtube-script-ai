# YouTube Script AI

Pipeline completo para treinar LLM especializado em scripts do YouTube com storytelling e hooks.

## 🎯 Objetivo

Este projeto implementa um sistema híbrido que combina técnicas de storytelling fundamentais com scripts reais de sucesso do YouTube para treinar um modelo Llama especializado em geração de scripts.

## ✨ Características Principais

- **🎣 Hook Techniques**: Biblioteca completa de técnicas de abertura comprovadas
- **📖 Narrative Structures**: Estruturas narrativas para diferentes tipos de conteúdo
- **🎯 Engagement Patterns**: Padrões para manter o engajamento ao longo do vídeo
- **🤖 Hybrid Training**: Pipeline de treinamento que combina teoria e prática
- **🌐 Web Interface**: Interface amigável para geração de scripts
- **📊 Performance Analysis**: Análise de correlação entre técnicas e performance

## 🚀 Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/allansduarte/youtube-script-ai.git
cd youtube-script-ai

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o arquivo .env com suas chaves de API

# Lance a interface web
python src/main.py --mode interface
```

## 📁 Estrutura do Projeto

```
youtube-script-ai/
├── src/                     # Código fonte principal
│   ├── storytelling/        # Técnicas de storytelling
│   ├── data_collection/     # Coleta de dados do YouTube
│   ├── data_processing/     # Processamento e análise
│   ├── training/            # Pipeline de treinamento
│   └── generation/          # Sistema de geração
├── data/                    # Datasets e dados processados
├── models/                  # Modelos treinados
├── app/                     # Interface web
└── docs/                    # Documentação
```

## 🎬 Exemplo de Uso

### Interface Web
```bash
python src/main.py --mode interface
```

### Geração via CLI
```bash
python src/main.py --mode generate --niche tecnologia --topic "Como aprender Python"
```

### Exemplo Programático
```python
from src.storytelling.technique_database import TechniqueDatabase

db = TechniqueDatabase()
structure = db.generate_complete_script_structure(
    niche="tecnologia",
    hook_type="curiosity_gap", 
    structure_type="problem_solution",
    video_length=10,
    topic="Como aprender programação do zero"
)

print(structure)
```

## 🎯 Técnicas de Storytelling Incluídas

### Hooks Disponíveis
- **Curiosity Gap**: Criar lacuna de curiosidade
- **Controversy**: Declarações controversas
- **Personal Story**: Histórias pessoais envolventes
- **Statistics Shock**: Estatísticas impactantes
- **Direct Question**: Perguntas diretas ao viewer

### Estruturas Narrativas
- **Hero's Journey**: Jornada do herói clássica
- **Problem-Solution**: Problema e solução
- **Before-After**: Antes e depois
- **List Format**: Formato de lista
- **Tutorial Step**: Passo a passo

### Padrões de Engajamento
- **Pattern Interrupt**: Quebra de padrão
- **Callback**: Referências anteriores
- **Suspense Builder**: Construção de suspense
- **Social Proof**: Prova social
- **Interaction Prompt**: Chamadas para interação

## 🔧 Configuração

### Variáveis de Ambiente Necessárias

```env
# YouTube Data API
YOUTUBE_API_KEY=your_youtube_api_key_here

# Hugging Face (para modelos)
HUGGINGFACE_TOKEN=your_huggingface_token_here

# Weights & Biases (tracking)
WANDB_API_KEY=your_wandb_api_key_here
```

### Configuração YAML

O arquivo `config.yaml` controla todos os aspectos do sistema:

```yaml
youtube:
  api_key: "YOUR_API_KEY"
  max_results: 50

model:
  base_model: "meta-llama/Llama-2-7b-hf"
  max_length: 2048
  temperature: 0.7

training:
  theory_weight: 0.4
  practice_weight: 0.6
  num_epochs: 3
```

## 🎓 Pipeline de Treinamento

### Fase 1: Fundação Teórica (40%)
- Técnicas de storytelling fundamentais
- Hooks e aberturas eficazes
- Estruturas narrativas comprovadas

### Fase 2: Realidade Prática (60%)
- Scripts reais de vídeos de sucesso
- Análise de performance
- Correlação técnicas vs resultados

### Fase 3: Hibridização
- Combinação teoria + prática
- Exemplos ponte conectando ambos
- Fine-tuning especializado

## 📊 Métricas e Análise

O sistema inclui métricas especializadas para:

- **Engagement Rate**: Taxa de engajamento
- **Retention Analysis**: Análise de retenção
- **Hook Effectiveness**: Eficácia dos hooks
- **Structure Performance**: Performance das estruturas
- **Technique Correlation**: Correlação técnicas vs resultados

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.

## 🔗 Links Úteis

- [Documentação Completa](docs/)
- [Guia de Instalação](docs/installation.md)
- [Tutorial de Uso](docs/usage_guide.md)
- [Referência de API](docs/api_reference.md)
- [Técnicas de Storytelling](docs/storytelling_techniques.md)

## 📧 Contato

Allan Duarte - [GitHub](https://github.com/allansduarte)

Link do Projeto: [https://github.com/allansduarte/youtube-script-ai](https://github.com/allansduarte/youtube-script-ai)

---

⭐ **Se este projeto foi útil para você, considere dar uma estrela!** ⭐
