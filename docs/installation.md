# Guia de Instalação - YouTube Script AI

## Pré-requisitos

### Sistema Operacional
- Linux, macOS, ou Windows 10/11
- Python 3.9 ou superior
- 8GB RAM mínimo (16GB recomendado)
- 10GB espaço em disco

### Ferramentas Necessárias
- Git
- Python 3.9+
- pip (gerenciador de pacotes Python)

## Instalação Passo a Passo

### 1. Clone o Repositório

```bash
git clone https://github.com/allansduarte/youtube-script-ai.git
cd youtube-script-ai
```

### 2. Crie um Ambiente Virtual

```bash
# Usando venv
python -m venv venv

# Ative o ambiente virtual
# No Linux/macOS:
source venv/bin/activate

# No Windows:
venv\Scripts\activate
```

### 3. Instale as Dependências

```bash
# Dependências principais
pip install -r requirements.txt

# Dependências de desenvolvimento (opcional)
pip install -r requirements-dev.txt
```

### 4. Configure as Variáveis de Ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env
nano .env  # ou use seu editor preferido
```

Preencha as seguintes variáveis:

```env
# YouTube Data API (obrigatório para coleta de dados)
YOUTUBE_API_KEY=your_youtube_api_key_here

# Hugging Face Token (obrigatório para modelos)
HUGGINGFACE_TOKEN=your_huggingface_token_here

# Weights & Biases (opcional - para tracking)
WANDB_API_KEY=your_wandb_api_key_here
WANDB_PROJECT=youtube-script-ai
```

### 5. Configure o YouTube Data API

1. Acesse o [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto ou selecione um existente
3. Ative a YouTube Data API v3
4. Crie credenciais (API Key)
5. Copie a API Key para o arquivo `.env`

### 6. Configure o Hugging Face

1. Acesse [Hugging Face](https://huggingface.co/)
2. Crie uma conta gratuita
3. Vá em Settings > Access Tokens
4. Crie um novo token com permissões de leitura
5. Copie o token para o arquivo `.env`

### 7. Teste a Instalação

```bash
# Teste básico do sistema
python src/main.py --mode generate --topic "Como aprender Python"

# Teste da interface web
python src/main.py --mode interface
```

## Instalação com Docker (Alternativa)

### 1. Build da Imagem

```bash
docker build -t youtube-script-ai .
```

### 2. Execute o Container

```bash
docker run -p 7860:7860 \
  -e YOUTUBE_API_KEY=your_api_key \
  -e HUGGINGFACE_TOKEN=your_token \
  youtube-script-ai
```

## Verificação da Instalação

### Teste Rápido

```python
from src.storytelling.technique_database import TechniqueDatabase

# Instanciar o banco de técnicas
db = TechniqueDatabase()

# Verificar se tudo está funcionando
stats = db.get_statistics()
print(f"Hooks disponíveis: {stats['total_hooks']}")
print(f"Estruturas disponíveis: {stats['total_structures']}")
print(f"Padrões disponíveis: {stats['total_patterns']}")
```

### Teste da Interface Web

```bash
python src/main.py --mode interface
```

Abra seu navegador em `http://localhost:7860`

## Solução de Problemas

### Erro: "ModuleNotFoundError"

```bash
# Verifique se está no ambiente virtual correto
which python

# Reinstale as dependências
pip install -r requirements.txt
```

### Erro: "YouTube API Key Invalid"

1. Verifique se a API Key está correta no arquivo `.env`
2. Confirme que a YouTube Data API v3 está ativada
3. Verifique se há cotas disponíveis na API

### Erro: "CUDA not available"

O sistema funciona apenas com CPU por padrão. Para GPU:

```bash
# Para NVIDIA GPUs
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Verifique se CUDA está disponível
python -c "import torch; print(torch.cuda.is_available())"
```

### Performance Lenta

1. Verifique se tem RAM suficiente (16GB recomendado)
2. Para treinamento, use GPU quando possível
3. Ajuste `batch_size` no `config.yaml` se necessário

## Configuração de Desenvolvimento

### Ferramentas de Desenvolvimento

```bash
# Instale dependências de dev
pip install -r requirements-dev.txt

# Configure pre-commit hooks
pre-commit install

# Execute testes
pytest tests/

# Formatação de código
black src/ tests/
flake8 src/ tests/
```

### Estrutura de Desenvolvimento

```
youtube-script-ai/
├── src/                    # Código principal
├── tests/                  # Testes automatizados
├── docs/                   # Documentação
├── data/                   # Dados e datasets
├── models/                 # Modelos treinados
├── config.yaml            # Configuração principal
├── requirements.txt       # Dependências
└── .env                   # Variáveis de ambiente
```

## Próximos Passos

1. Leia o [Guia de Uso](usage_guide.md)
2. Explore os [Exemplos](../examples/)
3. Consulte a [Documentação de API](api_reference.md)
4. Entenda as [Técnicas de Storytelling](storytelling_techniques.md)

## Suporte

Para problemas de instalação:
1. Verifique os issues no GitHub
2. Consulte a documentação completa
3. Abra um novo issue se necessário