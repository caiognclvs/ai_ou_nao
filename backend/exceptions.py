"""
Exceções customizadas para o sistema de detecção de imagens IA.
Demonstra o conceito de POO: EXCEÇÕES
"""


class AIDetectionException(Exception):
    """Exceção base para erros do sistema de detecção de IA"""
    
    def __init__(self, message: str, error_code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
    
    def to_dict(self):
        """Converte a exceção para dicionário (útil para respostas JSON)"""
        return {
            'error': self.message,
            'error_code': self.error_code,
            'success': False
        }


class InvalidImageException(AIDetectionException):
    """Exceção lançada quando a imagem é inválida ou corrompida"""
    
    def __init__(self, message: str = "Imagem inválida ou corrompida"):
        super().__init__(message, "INVALID_IMAGE")


class NoImageProvidedException(AIDetectionException):
    """Exceção lançada quando nenhuma imagem é fornecida"""
    
    def __init__(self, message: str = "Nenhuma imagem foi enviada"):
        super().__init__(message, "NO_IMAGE_PROVIDED")


class APIKeyMissingException(AIDetectionException):
    """Exceção lançada quando a chave da API está ausente"""
    
    def __init__(self, message: str = "Chave da API do Gemini não configurada"):
        super().__init__(message, "API_KEY_MISSING")


class AnalysisFailedException(AIDetectionException):
    """Exceção lançada quando a análise falha"""
    
    def __init__(self, message: str = "Falha ao analisar imagem", original_error: Exception = None):
        self.original_error = original_error
        if original_error:
            message = f"{message}: {str(original_error)}"
        super().__init__(message, "ANALYSIS_FAILED")


class ModelNotAvailableException(AIDetectionException):
    """Exceção lançada quando o modelo da IA não está disponível"""
    
    def __init__(self, model_name: str):
        message = f"Modelo '{model_name}' não está disponível"
        super().__init__(message, "MODEL_NOT_AVAILABLE")
