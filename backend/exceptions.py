class AIDetectionException(Exception):    
    def __init__(self, message: str, error_code: str = "UNKNOWN_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
    
    def to_dict(self):
        return {
            'error': self.message,
            'error_code': self.error_code,
            'success': False
        }


class InvalidImageException(AIDetectionException):
    def __init__(self, message: str = "Imagem inválida ou corrompida"):
        super().__init__(message, "INVALID_IMAGE")


class NoImageProvidedException(AIDetectionException):
    def __init__(self, message: str = "Nenhuma imagem foi enviada"):
        super().__init__(message, "NO_IMAGE_PROVIDED")


class APIKeyMissingException(AIDetectionException):
    def __init__(self, message: str = "Chave da API do Gemini não configurada"):
        super().__init__(message, "API_KEY_MISSING")


class AnalysisFailedException(AIDetectionException):
    def __init__(self, message: str = "Falha ao analisar imagem", original_error: Exception = None):
        self.original_error = original_error
        if original_error:
            message = f"{message}: {str(original_error)}"
        super().__init__(message, "ANALYSIS_FAILED")


class ModelNotAvailableException(AIDetectionException):
    def __init__(self, model_name: str):
        message = f"Modelo '{model_name}' não está disponível"
        super().__init__(message, "MODEL_NOT_AVAILABLE")
