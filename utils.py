#!/usr/bin/env python3
"""
Módulo de utilitários para o ImageCompressor

Contém funções auxiliares para manipulação de arquivos, diretórios,
conversão de unidades e configuração de logging.
"""

import os
import sys
import glob
import logging
from typing import List, Optional

# Definição de constantes
SUPPORTED_EXTENSIONS = ('.jpg', '.jpeg', '.png', '.webp')


def setup_logging(level: int = logging.INFO) -> None:
    """
    Configura o sistema de logging para a aplicação.
    
    Args:
        level: Nível de logging (default: INFO)
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def validate_path(path: str) -> bool:
    """
    Verifica se um caminho existe e tem permissões adequadas.
    
    Args:
        path: Caminho a ser validado
        
    Returns:
        True se o caminho for válido, False caso contrário
    """
    if not os.path.exists(path):
        logging.error(f"Caminho não encontrado: {path}")
        return False
        
    if os.path.isfile(path):
        # Validar se é um formato de imagem suportado
        _, ext = os.path.splitext(path)
        if ext.lower() not in SUPPORTED_EXTENSIONS:
            logging.error(f"Formato de arquivo não suportado: {ext}")
            return False
            
        # Verificar se o arquivo pode ser lido
        if not os.access(path, os.R_OK):
            logging.error(f"Sem permissão para ler o arquivo: {path}")
            return False
    
    elif os.path.isdir(path):
        # Verificar se o diretório pode ser lido e navegado
        if not os.access(path, os.R_OK | os.X_OK):
            logging.error(f"Sem permissão para acessar o diretório: {path}")
            return False
    
    return True


def ensure_output_dir(directory: str) -> None:
    """
    Garante que o diretório de saída exista, criando-o se necessário.
    
    Args:
        directory: Caminho do diretório a ser criado
        
    Raises:
        OSError: Se não for possível criar o diretório
    """
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
            logging.info(f"Diretório de saída criado: {directory}")
        except OSError as e:
            logging.error(f"Erro ao criar diretório de saída: {e}")
            raise
    else:
        logging.debug(f"Diretório de saída existente: {directory}")


def get_image_files(directory: str) -> List[str]:
    """
    Retorna uma lista de caminhos para todas as imagens no diretório.
    
    Args:
        directory: Caminho do diretório a ser escaneado
        
    Returns:
        Lista de caminhos para arquivos de imagem
    """
    image_files = []
    
    # Criar padrões de busca para cada extensão suportada
    patterns = [os.path.join(directory, f"*{ext}") for ext in SUPPORTED_EXTENSIONS]
    patterns.extend([os.path.join(directory, f"*{ext.upper()}") for ext in SUPPORTED_EXTENSIONS])
    
    # Buscar arquivos correspondentes a cada padrão
    for pattern in patterns:
        image_files.extend(glob.glob(pattern))
    
    return sorted(image_files)


def format_file_size(size_bytes: int) -> str:
    """
    Formata um tamanho em bytes para uma representação legível (KB, MB, etc).
    
    Args:
        size_bytes: Tamanho em bytes
        
    Returns:
        String formatada com a unidade apropriada
    """
    # Definir unidades e seus respectivos divisores
    units = [("B", 0), ("KB", 10), ("MB", 20), ("GB", 30)]
    
    # Encontrar a unidade mais apropriada
    unit_index = 0
    for i, (unit, exp) in enumerate(units):
        if size_bytes < (1 << exp+10) or i == len(units) - 1:
            unit_index = i
            break
    
    # Calcular o valor na unidade escolhida
    unit, exp = units[unit_index]
    converted_size = size_bytes / (1 << exp) if exp > 0 else size_bytes
    
    # Formatar com duas casas decimais para KB, MB, GB
    if unit == "B":
        return f"{converted_size} {unit}"
    else:
        return f"{converted_size:.2f} {unit}"


def get_human_readable_mode(mode: str) -> str:
    """
    Retorna uma descrição legível para o modo de compressão.
    
    Args:
        mode: Modo de compressão ('leve', 'moderado', 'agressivo')
        
    Returns:
        Descrição legível do modo
    """
    descriptions = {
        "leve": "Compressão leve (alta qualidade)",
        "moderado": "Compressão moderada (equilíbrio)",
        "agressivo": "Compressão agressiva (menor tamanho)"
    }
    
    return descriptions.get(mode.lower(), f"Modo personalizado: {mode}")


def is_supported_image(filepath: str) -> bool:
    """
    Verifica se um arquivo é uma imagem suportada.
    
    Args:
        filepath: Caminho do arquivo
        
    Returns:
        True se for uma imagem suportada, False caso contrário
    """
    if not os.path.isfile(filepath):
        return False
        
    _, ext = os.path.splitext(filepath)
    return ext.lower() in SUPPORTED_EXTENSIONS
