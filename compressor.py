#!/usr/bin/env python3
"""
Módulo de compressão de imagens - Implementa a lógica central de compressão

Este módulo contém a classe principal ImageCompressor que gerencia
todo o processo de compressão de imagens, incluindo redimensionamento,
ajuste de qualidade e conversão de formato.
"""

import os
import logging
from typing import Tuple, Optional, Dict, Any
from PIL import Image, ImageOps

logger = logging.getLogger("ImageCompressor")

# Suporte a formatos de entrada
SUPPORTED_FORMATS = {'.jpg', '.jpeg', '.png', '.webp'}

# Configurações predefinidas para os modos de compressão
COMPRESSION_MODES = {
    "leve": {
        "quality": 85,
        "scale_factor": 1.0,
        "keep_metadata": True,
        "format_mapping": {"jpg": "jpg", "jpeg": "jpg", "png": "png", "webp": "webp"}
    },
    "moderado": {
        "quality": 70,
        "scale_factor": 0.8,
        "keep_metadata": False,
        "format_mapping": {"jpg": "jpg", "jpeg": "jpg", "png": "png", "webp": "webp"}
    },
    "agressivo": {
        "quality": 50,
        "scale_factor": 0.6,
        "keep_metadata": False,
        "format_mapping": {"jpg": "webp", "jpeg": "webp", "png": "webp", "webp": "webp"}
    }
}


class ImageCompressor:
    """
    Classe responsável pela compressão de imagens com diferentes configurações.
    """
    
    def __init__(
            self,
            mode: str = "moderado",
            quality: Optional[int] = None,
            scale_factor: Optional[float] = None,
            keep_metadata: Optional[bool] = None,
            output_format: str = "auto"
    ):
        """
        Inicializa o compressor com as configurações especificadas.
        
        Args:
            mode: Modo de compressão ('leve', 'moderado', 'agressivo')
            quality: Qualidade da imagem (0-100), sobrepõe o modo
            scale_factor: Fator de escala para redimensionamento
            keep_metadata: Se True, mantém os metadados da imagem
            output_format: Formato de saída ('auto', 'jpg', 'png', 'webp')
        """
        self.mode = mode
        self._load_mode_settings(mode)
        
        # Sobrescrever configurações padrão se especificadas
        if quality is not None:
            self.quality = max(1, min(100, quality))  # Garantir entre 1-100
        
        if scale_factor is not None:
            self.scale_factor = max(0.1, min(1.0, scale_factor))  # Garantir entre 0.1-1.0
            
        if keep_metadata is not None:
            self.keep_metadata = keep_metadata
            
        self.output_format = output_format
        
        logger.debug(f"Compressor inicializado: modo={mode}, qualidade={self.quality}, "
                    f"escala={self.scale_factor}, manter_metadados={self.keep_metadata}")

    def _load_mode_settings(self, mode: str) -> None:
        """
        Carrega as configurações predefinidas para o modo selecionado.
        
        Args:
            mode: Modo de compressão ('leve', 'moderado', 'agressivo')
        """
        if mode not in COMPRESSION_MODES:
            logger.warning(f"Modo '{mode}' não reconhecido. Usando 'moderado'.")
            mode = "moderado"
            
        settings = COMPRESSION_MODES[mode]
        self.quality = settings["quality"]
        self.scale_factor = settings["scale_factor"]
        self.keep_metadata = settings["keep_metadata"]
        self.format_mapping = settings["format_mapping"]

    def _get_output_format(self, input_format: str) -> str:
        """
        Determina o formato de saída com base no formato de entrada e nas configurações.
        
        Args:
            input_format: Formato da imagem de entrada (sem o ponto)
            
        Returns:
            Formato de saída a ser usado
        """
        input_format = input_format.lower()
        
        if self.output_format != "auto":
            return self.output_format
            
        if input_format in self.format_mapping:
            return self.format_mapping[input_format]
            
        # Fallback para JPG se o formato não for reconhecido
        return "jpg"

    def _calculate_new_dimensions(self, width: int, height: int) -> Tuple[int, int]:
        """
        Calcula as novas dimensões mantendo a proporção.
        
        Args:
            width: Largura original
            height: Altura original
            
        Returns:
            Tupla com as novas dimensões (largura, altura)
        """
        new_width = int(width * self.scale_factor)
        new_height = int(height * self.scale_factor)
        
        # Garantir dimensões mínimas
        new_width = max(new_width, 1)
        new_height = max(new_height, 1)
        
        return new_width, new_height

    def _get_saving_parameters(self, output_format: str) -> Dict[str, Any]:
        """
        Define os parâmetros de salvamento com base no formato de saída.
        
        Args:
            output_format: Formato de saída da imagem
            
        Returns:
            Dicionário com os parâmetros para Image.save()
        """
        params = {}
        
        if output_format.lower() == "jpg" or output_format.lower() == "jpeg":
            params = {
                "format": "JPEG",
                "quality": self.quality,
                "optimize": True,
                "progressive": True
            }
        elif output_format.lower() == "png":
            params = {
                "format": "PNG",
                "optimize": True,
                "compress_level": 9  # Maior compressão sem perda
            }
        elif output_format.lower() == "webp":
            params = {
                "format": "WEBP",
                "quality": self.quality,
                "method": 6  # Maior esforço de compressão
            }
        
        return params

    def _generate_output_filename(self, input_path: str, output_dir: str, output_format: str) -> str:
        """
        Gera o nome do arquivo de saída com base no modo e formato.
        
        Args:
            input_path: Caminho do arquivo de entrada
            output_dir: Diretório de saída
            output_format: Formato de saída
            
        Returns:
            Caminho completo para o arquivo de saída
        """
        base_name = os.path.basename(input_path)
        name_without_ext = os.path.splitext(base_name)[0]
        
        # Criar nome de arquivo com sufixo do modo de compressão
        output_filename = f"{name_without_ext}_{self.mode}.{output_format}"
        return os.path.join(output_dir, output_filename)

    def compress_image(self, input_path: str, output_dir: Optional[str] = None) -> Tuple[str, int, int, float]:
        """
        Comprime uma única imagem de acordo com as configurações.
        
        Args:
            input_path: Caminho para a imagem a ser comprimida
            output_dir: Diretório onde salvar a imagem comprimida
            
        Returns:
            Tupla (caminho_saída, tamanho_original, tamanho_final, porcentagem_redução)
            
        Raises:
            ValueError: Se o formato de entrada não for suportado
            IOError: Se ocorrer um erro ao ler ou salvar a imagem
        """
        # Validar formato de entrada
        _, ext = os.path.splitext(input_path)
        if ext.lower() not in SUPPORTED_FORMATS:
            raise ValueError(f"Formato não suportado: {ext}. Formatos suportados: {', '.join(SUPPORTED_FORMATS)}")
        
        # Configurar diretório de saída
        if output_dir is None:
            output_dir = os.path.dirname(input_path)
        
        # Obter tamanho original do arquivo em bytes
        original_size = os.path.getsize(input_path)
        
        # Carregar imagem
        try:
            with Image.open(input_path) as img:
                # Converter para RGB se for RGBA (importante para JPEG que não suporta alpha)
                if img.mode == 'RGBA' and (self._get_output_format(ext[1:]) in ['jpg', 'jpeg']):
                    logger.debug(f"Convertendo imagem {input_path} de RGBA para RGB")
                    img = img.convert('RGB')
                
                # Redimensionar se necessário
                if self.scale_factor < 1.0:
                    new_width, new_height = self._calculate_new_dimensions(img.width, img.height)
                    img = img.resize((new_width, new_height), Image.LANCZOS)
                    logger.debug(f"Imagem redimensionada de {img.width}x{img.height} para {new_width}x{new_height}")
                
                # Determinar formato de saída
                output_format = self._get_output_format(ext[1:])
                
                # Gerar nome do arquivo de saída
                output_path = self._generate_output_filename(input_path, output_dir, output_format)
                
                # Obter parâmetros de salvamento
                save_params = self._get_saving_parameters(output_format)
                
                # Remover metadados se necessário
                if not self.keep_metadata:
                    img = ImageOps.exif_transpose(img)  # Preservar orientação
                    data = list(img.getdata())
                    img_without_exif = Image.new(img.mode, img.size)
                    img_without_exif.putdata(data)
                    img = img_without_exif
                
                # Salvar imagem comprimida
                img.save(output_path, **save_params)
                
                # Obter tamanho final
                final_size = os.path.getsize(output_path)
                
                # Calcular porcentagem de redução
                reduction_percent = ((original_size - final_size) / original_size) * 100
                
                logger.info(f"Compressão concluída: {input_path} -> {output_path}")
                logger.info(f"Redução: {original_size} -> {final_size} bytes ({reduction_percent:.2f}%)")
                
                return output_path, original_size, final_size, reduction_percent
                
        except Exception as e:
            logger.error(f"Erro ao processar {input_path}: {str(e)}")
            raise
