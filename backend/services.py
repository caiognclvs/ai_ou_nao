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
    ANALYSIS_STANDARD = "standard"
    ANALYSIS_FAST = "fast"
    ANALYSIS_DETAILED = "detailed"
    
    def __init__(self, api_key: Optional[str] = None, model_name: str = "gemini-2.5-flash"):
        self.__api_key = api_key or os.getenv('GEMINI_API_KEY')
        self.__model_name = model_name
        self.__config = None
        self.__analyzer = None
        
        self._validate_and_configure()
    
    def _validate_and_configure(self):
        if not self.__api_key:
            raise APIKeyMissingException()
        
        self.__config = AIModelConfig(
            model_name=self.__model_name,
            api_key=self.__api_key
        )
        
        self.__analyzer = GeminiAIDetector(self.__config)
    
    def _create_image_data(self, image_file) -> ImageData:
        try:
            if not image_file or not hasattr(image_file, 'read'):
                raise NoImageProvidedException()
            
            image_bytes = image_file.read()
            if not image_bytes:
                raise InvalidImageException("Arquivo de imagem vazio")
            
            image = Image.open(BytesIO(image_bytes))
            
            filename = getattr(image_file, 'filename', 'unknown')
            
            return ImageData(image=image, filename=filename)
            
        except (IOError, OSError) as e:
            raise InvalidImageException(f"Não foi possível abrir a imagem: {str(e)}")
    
    def _select_analyzer(self, analysis_type: str) -> BaseAnalyzer:
        if analysis_type == self.ANALYSIS_FAST:
            return FastAIDetector(self.__config)
        elif analysis_type == self.ANALYSIS_DETAILED:
            return DetailedAIDetector(self.__config)
        else:
            return GeminiAIDetector(self.__config)
    
    def analyze_image(self, image_file, analysis_type: str = ANALYSIS_STANDARD) -> AnalysisResult:
        if not image_file:
            raise NoImageProvidedException()
        
        if hasattr(image_file, 'filename') and not image_file.filename:
            raise NoImageProvidedException("Nenhuma imagem selecionada")
        
        image_data = self._create_image_data(image_file)
        
        analyzer = self._select_analyzer(analysis_type)
        
        result = analyzer.analyze(image_data)
        
        return result
    
    def health_check(self) -> dict:
        return {
            'status': 'ok',
            'service': 'AI Detection Service',
            'model': self.__model_name,
            'api_configured': bool(self.__api_key),
            'analyzer': str(self.__analyzer)
        }
    
    @property
    def model_name(self) -> str:
        return self.__model_name
    
    @property
    def is_configured(self) -> bool:
        return self.__config is not None and self.__analyzer is not None
    
    def __str__(self):
        return f"AIDetectionService(model={self.__model_name}, configured={self.is_configured})"
    
    def __repr__(self):
        return self.__str__()
