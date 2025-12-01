"""
Classes de modelo para representar dados do sistema.
Demonstra os conceitos de POO: CLASSES, OBJETOS e ENCAPSULAMENTO
"""

from PIL import Image
from typing import Optional
from dataclasses import dataclass
from io import BytesIO


class ImageData:
    """
    Classe que encapsula dados de uma imagem.
    Demonstra ENCAPSULAMENTO: atributos privados com getters/setters
    """
    
    def __init__(self, image: Image.Image, filename: str = "unknown"):
        self.__image = image  # Atributo privado (encapsulado)
        self.__filename = filename  # Atributo privado
        self.__size = image.size
        self.__format = image.format
    
    @property
    def image(self) -> Image.Image:
        """Getter para acessar a imagem (encapsulamento)"""
        return self.__image
    
    @property
    def filename(self) -> str:
        """Getter para acessar o nome do arquivo"""
        return self.__filename
    
    @property
    def size(self) -> tuple:
        """Getter para acessar o tamanho da imagem"""
        return self.__size
    
    @property
    def format(self) -> Optional[str]:
        """Getter para acessar o formato da imagem"""
        return self.__format
    
    @property
    def width(self) -> int:
        """Largura da imagem"""
        return self.__size[0]
    
    @property
    def height(self) -> int:
        """Altura da imagem"""
        return self.__size[1]
    
    def __str__(self):
        return f"ImageData(filename={self.filename}, size={self.size}, format={self.format})"
    
    def __repr__(self):
        return self.__str__()


class AnalysisResult:
    """
    Classe que encapsula o resultado de uma análise de imagem.
    Demonstra ENCAPSULAMENTO e CLASSES/OBJETOS
    """
    
    def __init__(self, probability: int, analysis_text: str):
        self.__probability = self.__validate_probability(probability)
        self.__analysis_text = analysis_text
        self.__classification = self.__determine_classification()
    
    @staticmethod
    def __validate_probability(probability: int) -> int:
        """Valida e normaliza a probabilidade para o intervalo 0-100"""
        return max(0, min(100, probability))
    
    def __determine_classification(self) -> str:
        """Determina a classificação baseada na probabilidade (método privado)"""
        if self.__probability >= 80:
            return "Muito provável IA"
        elif self.__probability >= 60:
            return "Provavelmente IA"
        elif self.__probability >= 40:
            return "Incerto"
        elif self.__probability >= 20:
            return "Provavelmente real"
        else:
            return "Muito provável real"
    
    @property
    def probability(self) -> int:
        """Getter para probabilidade"""
        return self.__probability
    
    @property
    def analysis_text(self) -> str:
        """Getter para texto de análise"""
        return self.__analysis_text
    
    @property
    def classification(self) -> str:
        """Getter para classificação"""
        return self.__classification
    
    @property
    def is_likely_ai(self) -> bool:
        """Retorna True se a imagem provavelmente foi gerada por IA"""
        return self.__probability >= 60
    
    @property
    def confidence_level(self) -> str:
        """Retorna o nível de confiança da análise"""
        if self.__probability >= 80 or self.__probability <= 20:
            return "Alta"
        elif self.__probability >= 60 or self.__probability <= 40:
            return "Média"
        else:
            return "Baixa"
    
    def to_dict(self) -> dict:
        """Converte o resultado para dicionário (útil para JSON)"""
        return {
            'probability': self.__probability,
            'classification': self.__classification,
            'analysis': self.__analysis_text,
            'is_likely_ai': self.is_likely_ai,
            'confidence_level': self.confidence_level,
            'success': True
        }
    
    def __str__(self):
        return f"AnalysisResult(probability={self.probability}%, classification='{self.classification}')"
    
    def __repr__(self):
        return self.__str__()


@dataclass
class AIModelConfig:
    """
    Configuração para modelos de IA.
    Demonstra uso de dataclasses (recurso moderno de POO em Python)
    """
    model_name: str
    api_key: str
    temperature: float = 0.4
    max_tokens: Optional[int] = None
    
    def __post_init__(self):
        """Valida a configuração após inicialização"""
        if not self.api_key:
            from exceptions import APIKeyMissingException
            raise APIKeyMissingException()
        
        if self.temperature < 0 or self.temperature > 1:
            raise ValueError("Temperature deve estar entre 0 e 1")
