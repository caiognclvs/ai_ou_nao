"""
Serviço principal de detecção de IA em imagens.
Orquestra o uso de todas as classes POO do sistema.
"""

from typing import Optional
from PIL import Image
from io import BytesIO
import os

from models import ImageData, AnalysisResult, AIModelConfig
from analyzers import BaseAnalyzer, GeminiAIDetector, FastAIDetector, DetailedAIDetector
from exceptions import (
    InvalidImageException,
    NoImageProvidedException,
    APIKeyMissingException,
    AnalysisFailedException
)


class AIDetectionService:
    """
    Serviço principal que orquestra a detecção de imagens geradas por IA.
    Demonstra COMPOSIÇÃO: usa outras classes (has-a relationship)
    Demonstra ENCAPSULAMENTO: esconde detalhes de implementação
    """
    
    # Tipos de análise disponíveis (constantes de classe)
    ANALYSIS_STANDARD = "standard"
    ANALYSIS_FAST = "fast"
    ANALYSIS_DETAILED = "detailed"
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        """
        Inicializa o serviço de detecção.
        
        Args:
            api_key: Chave da API do Gemini (se None, busca de variável de ambiente)
            model_name: Nome do modelo a ser usado
        """
        self.__api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.__model_name = model_name
        self.__config = None
        self.__analyzer = None
        
        self._validate_and_configure()
    
    def _validate_and_configure(self):
        """Valida configurações e inicializa o analisador (método privado)"""
        if not self.__api_key:
            raise APIKeyMissingException()
        
        # Criar configuração
        self.__config = AIModelConfig(
            model_name=self.__model_name,
            api_key=self.__api_key
        )
        
        # Inicializar analisador padrão
        self.__analyzer = GeminiAIDetector(self.__config)
    
    def _create_image_data(self, image_file) -> ImageData:
        """
        Cria um objeto ImageData a partir de um arquivo.
        Método privado que encapsula a lógica de criação
        """
        try:
            if not image_file or not hasattr(image_file, 'read'):
                raise NoImageProvidedException()
            
            # Ler bytes da imagem
            image_bytes = image_file.read()
            if not image_bytes:
                raise InvalidImageException("Arquivo de imagem vazio")
            
            # Abrir imagem com PIL
            image = Image.open(BytesIO(image_bytes))
            
            # Obter nome do arquivo
            filename = getattr(image_file, 'filename', 'unknown')
            
            return ImageData(image=image, filename=filename)
            
        except (IOError, OSError) as e:
            raise InvalidImageException(f"Não foi possível abrir a imagem: {str(e)}")
    
    def _select_analyzer(self, analysis_type: str) -> BaseAnalyzer:
        """
        Seleciona o analisador apropriado baseado no tipo de análise.
        Demonstra POLIMORFISMO: retorna diferentes implementações de BaseAnalyzer
        """
        if analysis_type == self.ANALYSIS_FAST:
            return FastAIDetector(self.__config)
        elif analysis_type == self.ANALYSIS_DETAILED:
            return DetailedAIDetector(self.__config)
        else:  # standard
            return GeminiAIDetector(self.__config)
    
    def analyze_image(self, image_file, analysis_type: str = ANALYSIS_STANDARD) -> AnalysisResult:
        """
        Analisa uma imagem para detectar se foi gerada por IA.
        Método público principal do serviço.
        
        Args:
            image_file: Arquivo de imagem (Flask FileStorage ou similar)
            analysis_type: Tipo de análise ('standard', 'fast', 'detailed')
        
        Returns:
            AnalysisResult com a probabilidade e análise
        
        Raises:
            NoImageProvidedException: Se nenhuma imagem for fornecida
            InvalidImageException: Se a imagem for inválida
            AnalysisFailedException: Se a análise falhar
        """
        # Validar entrada
        if not image_file:
            raise NoImageProvidedException()
        
        if hasattr(image_file, 'filename') and not image_file.filename:
            raise NoImageProvidedException("Nenhuma imagem selecionada")
        
        # Criar objeto de dados da imagem
        image_data = self._create_image_data(image_file)
        
        # Selecionar analisador apropriado (POLIMORFISMO)
        analyzer = self._select_analyzer(analysis_type)
        
        # Realizar análise
        result = analyzer.analyze(image_data)
        
        return result
    
    def health_check(self) -> dict:
        """
        Verifica se o serviço está funcionando corretamente.
        
        Returns:
            Dicionário com status do serviço
        """
        return {
            'status': 'ok',
            'service': 'AI Detection Service',
            'model': self.__model_name,
            'api_configured': bool(self.__api_key),
            'analyzer': str(self.__analyzer)
        }
    
    @property
    def model_name(self) -> str:
        """Getter para o nome do modelo (ENCAPSULAMENTO)"""
        return self.__model_name
    
    @property
    def is_configured(self) -> bool:
        """Verifica se o serviço está configurado corretamente"""
        return self.__config is not None and self.__analyzer is not None
    
    def __str__(self):
        return f"AIDetectionService(model={self.__model_name}, configured={self.is_configured})"
    
    def __repr__(self):
        return self.__str__()
