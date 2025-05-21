# Exemplos de Uso do CLICompresssor

Este documento apresenta exemplos práticos de como utilizar o CLICompressor para diversas necessidades de compressão de imagens.

## Casos de uso comuns

### 1. Compactar uma única foto para envio por e-mail

```bash
python main.py foto_grande.jpg -m moderado
```

Resultado: Uma imagem com sufixo `_moderado.jpg` com tamanho reduzido, ideal para compartilhamento.

### 2. Preparar imagens para um site web (máxima compressão)

```bash
python main.py pasta_imagens/ -m agressivo -o imagens_web/
```

Resultado: Todas as imagens são convertidas para WebP com alta compressão e resolução reduzida, otimizadas para web.

### 3. Leve redução mantendo alta qualidade

```bash
python main.py imagem_alta_resolucao.png -m leve -o saida/
```

Resultado: A imagem é levemente comprimida, mantendo metadados e formato original.

### 4. Utilizando configurações personalizadas

```bash
python main.py imagem.jpg -q 60 -s 0.7 --format webp -o personalizada/
```

Resultado: Compressão com qualidade 60%, redimensionada para 70% do tamanho original e convertida para WebP.

### 5. Processamento de um diretório mantendo metadados EXIF

```bash
python main.py fotos_viagem/ -m moderado --keep-metadata -o fotos_comprimidas/
```

Resultado: Imagens comprimidas mantendo informações EXIF como data, câmera, GPS, etc.

### 6. Conversão em lote para um formato específico

```bash
python main.py diversos_formatos/ --format jpg -o convertidas_jpg/
```

Resultado: Todas as imagens são convertidas para JPG com configurações de compressão padrão.

## Dicas para melhor desempenho

1. **Escolha do formato**:
   - Use JPG para fotografias
   - Use PNG para imagens com transparência e capturas de tela
   - Use WebP para melhor compressão geral (mas com menor compatibilidade)

2. **Encontrando o equilíbrio**:
   - Experimente começar com modo `moderado` e ajustar conforme necessário
   - Use a opção `-v` (verbose) para ver detalhes da compressão

3. **Lote vs Individual**:
   - Para poucos arquivos, comprima individualmente com configurações personalizadas
   - Para muitos arquivos similares, use o processamento em lote
