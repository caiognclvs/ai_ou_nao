from PIL import Image
from typing import Optional
from dataclasses import dataclass
from io import BytesIO


class ImageData:
    def __init__(self, image: Image.Image, filename: str = "unknown"):
        self.__image = image 
        self.__filename = filename
        self.__size = image.size
        self.__format = image.format
    
    @property
    def image(self) -> Image.Image:
        return self.__image
    
    @property
    def filename(self) -> str:
        return self.__filename
    
    @property
    def size(self) -> tuple:
        return self.__size
    
    @property
    def format(self) -> Optional[str]:
        return self.__format
    
    @property
    def width(self) -> int:
        return self.__size[0]
    
    @property
    def height(self) -> int:
        return self.__size[1]
    
    def __str__(self):
        return f"ImageData(filename={self.filename}, size={self.size}, format={self.format})"
    
    def __repr__(self):
        return self.__str__()


class AnalysisResult:
    def __init__(self, probability: int, analysis_text: str):
        self.__probability = self.__validate_probability(probability)
        self.__analysis_text = analysis_text
        self.__classification = self.__determine_classification()
    
    @staticmethod
    def __validate_probability(probability: int) -> int:
        return max(0, min(100, probability))
    
    def __determine_classification(self) -> str:
        if self.__probability >= 80:
            return "Muito provável do Google Gemini"
        elif self.__probability >= 60:
            return "Provavelmente do Google Gemini"
        elif self.__probability >= 40:
            return "Incerto"
        elif self.__probability >= 20:
            return "Provavelmente não é do Google"
        else:
            return "Muito provável que não é do Google"
    
    @property
    def probability(self) -> int:
        return self.__probability
    
    @property
    def analysis_text(self) -> str:
        return self.__analysis_text
    
    @property
    def classification(self) -> str:
        return self.__classification
    
    @property
    def is_likely_ai(self) -> bool:
        return self.__probability >= 60
    
    @property
    def confidence_level(self) -> str:
        if self.__probability >= 80 or self.__probability <= 20:
            return "Alta"
        elif self.__probability >= 60 or self.__probability <= 40:
            return "Média"
        else:
            return "Baixa"
    
    def to_dict(self) -> dict:
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
    model_name: str
    api_key: str
    temperature: float = 0.4
    max_tokens: Optional[int] = None
    
    def __post_init__(self):
        if not self.api_key:
            from exceptions import APIKeyMissingException
            raise APIKeyMissingException()
        
        if self.temperature < 0 or self.temperature > 1:
            raise ValueError("Temperature deve estar entre 0 e 1")
