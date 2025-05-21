![Icone da aplicação](logo.png)

# CLICompressor

Uma ferramenta CLI em Python para compressão eficiente de imagens, capaz de reduzir substancialmente o tamanho de arquivos de imagem mantendo uma qualidade visual aceitável.

⚠️ **Nota:** Esta aplicação foi idealizada e desenvolvida para suprir uma demanda real do ambiente de trabalho, proporcionando uma solução interna para compactação de imagens de forma rápida, eficiente e livre das limitações, anúncios e lentidão comuns em ferramentas online. CLICompressor é parte do ferramental próprio utilizado na empresa para otimizar processos recorrentes de compressão de imagens em lote.


## Características

- **Múltiplos perfis de compressão**: leve, moderado e agressivo
- **Redimensionamento proporcional** da resolução da imagem
- **Redução de qualidade** ajustável (1-100)
- **Conversão automática de formato** (ex: PNG para WebP em modo agressivo)
- **Remoção de metadados** (EXIF, etc.)
- **Suporte a múltiplos formatos**: JPG, JPEG, PNG, WebP
- **Processamento em lote** (diretórios inteiros)
- **Relatório de compressão** detalhado com comparação antes/depois
- **Código modular** pronto para integração em API/Frontend

## Requisitos

- Python 3.8+
- Pillow (PIL Fork)

## Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/Ambrosios13/CLICompressor
   cd CLICompressor
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### Compressão de arquivo único

```bash
python main.py caminho/para/imagem.jpg -m moderado
```

### Compressão de diretório (em lote)

```bash
python main.py caminho/para/diretorio -m agressivo -o ./pasta_saida
```

### Opções disponíveis

```
usage: main.py [-h] [-m {leve,moderado,agressivo}] [-o OUTPUT] [-q QUALITY]
               [-s SCALE] [--keep-metadata] [--format {auto,jpg,png,webp}] [-v]
               input

Comprime imagens individuais ou diretórios de imagens.

positional arguments:
  input                 Caminho para a imagem ou diretório a ser comprimido

optional arguments:
  -h, --help            Mostra esta mensagem de ajuda
  -m, --mode {leve,moderado,agressivo}
                        Nível de compressão (padrão: moderado)
  -o, --output OUTPUT   Diretório de saída para as imagens comprimidas
  -q, --quality QUALITY
                        Qualidade de compressão personalizada (0-100). Sobrepõe o modo.
  -s, --scale SCALE     Fator de escala para redimensionamento (ex: 0.5 para reduzir pela metade)
  --keep-metadata       Preserva os metadados da imagem (por padrão são removidos)
  --format {auto,jpg,png,webp}
                        Força um formato específico de saída (auto seleciona automaticamente)
  -v, --verbose         Mostra informações detalhadas durante o processamento
```

## Modos de compressão

| Modo      | Qualidade | Escala | Metadados | Conversão Automática          |
|-----------|-----------|--------|-----------|-------------------------------|
| Leve      | 85        | 1.0    | Mantém    | Mantém formato original       |
| Moderado  | 70        | 0.8    | Remove    | Mantém formato original       |
| Agressivo | 50        | 0.6    | Remove    | Converte para WebP (mais eficiente) |

## Estrutura do projeto

```
CLICompressor/
├── main.py         # Interface de linha de comando
├── compressor.py   # Lógica de compressão de imagens
├── utils.py        # Funções auxiliares
├── requirements.txt# Dependências do projeto
└── README.md       # Documentação
