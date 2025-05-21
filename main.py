#!/usr/bin/env python3
"""
ImageCompressor - CLI para compressão eficiente de imagens

Esta ferramenta permite comprimir imagens individuais ou em lote,
oferecendo diferentes níveis de compressão e mantendo uma qualidade
visual aceitável mesmo com reduções significativas de tamanho.

Uso:
    python main.py caminho/para/imagem.jpg -m moderado
    python main.py caminho/para/diretorio -m agressivo -o pasta_saida
"""

import os
import sys
import argparse
import logging
from typing import List, Optional

from compressor import ImageCompressor
from utils import setup_logging, validate_path, get_image_files, ensure_output_dir

# Configuração de logging
logger = logging.getLogger("ImageCompressor")


def parse_arguments() -> argparse.Namespace:
    """Define e processa os argumentos da linha de comando."""
    parser = argparse.ArgumentParser(
        description="Comprime imagens individuais ou diretórios de imagens.",
        epilog="Exemplo: python main.py imagem.jpg -m agressivo"
    )
    
    parser.add_argument(
        "input",
        help="Caminho para a imagem ou diretório a ser comprimido"
    )
    
    parser.add_argument(
        "-m", "--mode",
        choices=["leve", "moderado", "agressivo"],
        default="moderado",
        help="Nível de compressão (padrão: moderado)"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Diretório de saída para as imagens comprimidas"
    )
    
    parser.add_argument(
        "-q", "--quality",
        type=int,
        help="Qualidade de compressão personalizada (0-100). Sobrepõe o modo."
    )
    
    parser.add_argument(
        "-s", "--scale",
        type=float,
        help="Fator de escala para redimensionamento (ex: 0.5 para reduzir pela metade)"
    )
    
    parser.add_argument(
        "--keep-metadata",
        action="store_true",
        help="Preserva os metadados da imagem (por padrão são removidos)"
    )
    
    parser.add_argument(
        "--format",
        choices=["auto", "jpg", "png", "webp"],
        default="auto",
        help="Força um formato específico de saída (auto seleciona automaticamente)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Mostra informações detalhadas durante o processamento"
    )
    
    return parser.parse_args()


def process_images(compressor: ImageCompressor, 
                   input_path: str, 
                   output_dir: Optional[str], 
                   is_batch: bool) -> List[tuple]:
    """
    Processa as imagens de entrada usando o compressor.
    
    Args:
        compressor: Instância do compressor de imagens
        input_path: Caminho para imagem ou diretório
        output_dir: Diretório de saída
        is_batch: Flag indicando se estamos processando em lote
        
    Returns:
        Lista de tuplas (nome_arquivo, tamanho_original, tamanho_final, taxa_compressão)
    """
    results = []
    
    if is_batch:
        # Compressão em lote (diretório)
        image_files = get_image_files(input_path)
        total_files = len(image_files)
        
        if total_files == 0:
            logger.warning(f"Nenhuma imagem encontrada em {input_path}")
            return results
            
        logger.info(f"Encontradas {total_files} imagens para processar")
        
        for idx, img_path in enumerate(image_files, 1):
            logger.info(f"Processando {idx}/{total_files}: {os.path.basename(img_path)}")
            try:
                result = compressor.compress_image(img_path, output_dir)
                results.append(result)
            except Exception as e:
                logger.error(f"Erro ao processar {img_path}: {str(e)}")
    else:
        # Compressão de arquivo único
        try:
            result = compressor.compress_image(input_path, output_dir)
            results.append(result)
        except Exception as e:
            logger.error(f"Erro ao processar {input_path}: {str(e)}")
            sys.exit(1)
    
    return results


def display_results(results: List[tuple]) -> None:
    """
    Exibe um relatório com os resultados da compressão.
    
    Args:
        results: Lista de tuplas (nome_arquivo, tamanho_original, tamanho_final, taxa_compressão)
    """
    if not results:
        logger.warning("Nenhum resultado de compressão para exibir.")
        return
        
    print("\n" + "=" * 80)
    print(f"{'ARQUIVO':<30} {'TAMANHO ORIGINAL':<15} {'TAMANHO FINAL':<15} {'REDUÇÃO':<10}")
    print("-" * 80)
    
    total_original = 0
    total_final = 0
    
    for filename, original_size, final_size, reduction in results:
        print(f"{os.path.basename(filename):<30} {original_size:<15} {final_size:<15} {reduction:<10.2f}%")
        total_original += original_size
        total_final += final_size
    
    print("-" * 80)
    
    # Calcular totais
    total_reduction = ((total_original - total_final) / total_original * 100) if total_original > 0 else 0
    print(f"{'TOTAL':<30} {total_original:<15} {total_final:<15} {total_reduction:<10.2f}%")
    print("=" * 80 + "\n")


def main():
    """Função principal do programa."""
    args = parse_arguments()
    
    # Configurar nível de logging
    log_level = logging.INFO if args.verbose else logging.WARNING
    setup_logging(log_level)
    
    # Validar caminho de entrada
    input_path = os.path.abspath(args.input)
    is_batch = os.path.isdir(input_path)
    
    if not validate_path(input_path):
        logger.error(f"Caminho de entrada inválido: {input_path}")
        sys.exit(1)
    
    # Determinar diretório de saída
    if args.output:
        output_dir = os.path.abspath(args.output)
    else:
        if is_batch:
            output_dir = os.path.join(os.path.dirname(input_path), "comprimidas")
        else:
            output_dir = os.path.dirname(input_path)
    
    # Garantir que o diretório de saída exista
    ensure_output_dir(output_dir)
    
    # Criar o compressor com as configurações apropriadas
    compressor = ImageCompressor(
        mode=args.mode,
        quality=args.quality,
        scale_factor=args.scale,
        keep_metadata=args.keep_metadata,
        output_format=args.format
    )
    
    # Processar as imagens
    logger.info(f"Iniciando compressão no modo: {args.mode}")
    results = process_images(compressor, input_path, output_dir, is_batch)
    
    # Exibir resultados
    if results:
        display_results(results)
        logger.info(f"Compressão concluída. Imagens salvas em: {output_dir}")
    else:
        logger.error("Nenhuma imagem foi processada com sucesso.")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nOperação cancelada pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        sys.exit(1)
