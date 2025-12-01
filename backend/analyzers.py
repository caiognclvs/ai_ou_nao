from abc import ABC, abstractmethod
from typing import Optional
import google.generativeai as genai
import re

from models import ImageData, AnalysisResult, AIModelConfig
from exceptions import AnalysisFailedException, ModelNotAvailableException


class BaseAnalyzer(ABC):
    def __init__(self, config: AIModelConfig):
        self._config = config
        self._model = None
        self._initialize_model()
    
    @abstractmethod
    def _initialize_model(self):
        pass
    
    @abstractmethod
    def _generate_prompt(self) -> str:
        pass
    
    @abstractmethod
    def analyze(self, image_data: ImageData) -> AnalysisResult:
        pass
    
    def _extract_probability(self, response_text: str) -> int:
        try:
            probability = int(response_text.strip())
            return max(0, min(100, probability))
        except ValueError:
            numbers = re.findall(r'\d+', response_text)
            if numbers:
                probability = int(numbers[0])
                return max(0, min(100, probability))
            else:
                return 50
    
    def __str__(self):
        return f"{self.__class__.__name__}(model={self._config.model_name})"


class GeminiAIDetector(BaseAnalyzer):
    def _initialize_model(self):
        try:
            genai.configure(api_key=self._config.api_key)
            self._model = genai.GenerativeModel(self._config.model_name)
        except Exception as e:
            raise ModelNotAvailableException(self._config.model_name)
    
    def _generate_prompt(self) -> str:
        return """Analise cuidadosamente esta imagem e determine a probabilidade de ela ter sido gerada pelo GOOGLE GEMINI/IMAGEN (modelos de IA do Google).

FOCO ESPECIAL: Procure por SynthID - a marca d'água digital invisível do Google incorporada em imagens geradas por seus modelos de IA.

Indicadores-chave de imagens geradas pelo Google:
1. Presença de SynthID (marca d'água imperceptível do Google)
2. Padrões de ruído e artefatos específicos do Imagen/Gemini
3. Estilo visual característico dos modelos do Google (cores vibrantes, alto detalhamento)
4. Texturas e renderização típicas de difusão do Google
5. Assinaturas digitais ou metadados de geração do Google
6. Padrões de consistência/inconsistência específicos do Imagen

ATENÇÃO: Diferencie de outros geradores de IA (DALL-E, Midjourney, Stable Diffusion).

Responda APENAS com um número entre 0 e 100, onde:
- 0 = certeza de que NÃO foi gerada pelo Google Gemini/Imagen
- 100 = certeza de que FOI gerada pelo Google Gemini/Imagen
- Valores intermediários = nível de confiança

Forneça APENAS o número, sem explicações adicionais."""
    
    def analyze(self, image_data: ImageData) -> AnalysisResult:
        try:
            prompt = self._generate_prompt()
            response = self._model.generate_content([prompt, image_data.image])
            probability = self._extract_probability(response.text)
            
            analysis_text = self._generate_detailed_analysis(image_data, probability)
            
            return AnalysisResult(probability=probability, analysis_text=analysis_text)
            
        except Exception as e:
            raise AnalysisFailedException(
                message="Falha ao analisar imagem com Gemini AI",
                original_error=e
            )
    
    def _generate_detailed_analysis(self, image_data: ImageData, probability: int) -> str:
        try:
            analysis_prompt = f"""Com base na probabilidade de {probability}% de esta imagem ter sido gerada pelo Google Gemini/Imagen, forneça uma breve análise (2-3 frases) explicando:
1. Se detectou ou não a presença de SynthID (marca d'água do Google)
2. Outros indicadores específicos do Gemini/Imagen que levaram a essa conclusão
3. Como diferenciou (se aplicável) de outros geradores de IA"""
            
            analysis_response = self._model.generate_content([analysis_prompt, image_data.image])
            return analysis_response.text.strip()
        except Exception:
            return f"Análise indica {probability}% de probabilidade de ter sido gerada pelo Google Gemini/Imagen."


class FastAIDetector(GeminiAIDetector):    
    def _generate_prompt(self) -> str:
        return """Análise rápida: Esta imagem foi gerada pelo Google Gemini/Imagen?
Procure por SynthID (marca d'água do Google) e características visuais do Imagen.
Responda APENAS com um número de 0 (NÃO é do Google) a 100 (É do Google)."""
    
    def _generate_detailed_analysis(self, image_data: ImageData, probability: int) -> str:
        if probability >= 70:
            return f"Análise rápida detectou {probability}% de probabilidade de ser do Google Gemini/Imagen. Possível presença de SynthID ou características típicas do Imagen."
        elif probability >= 30:
            return f"Análise inconclusiva com {probability}% de probabilidade. Características ambíguas - pode ser outro gerador de IA ou foto real."
        else:
            return f"Análise rápida indica {probability}% de probabilidade de ser do Google. Provavelmente foto real ou de outro gerador de IA."


class DetailedAIDetector(GeminiAIDetector):
    def _generate_prompt(self) -> str:
        return """Realize uma análise PROFUNDA e ESPECIALIZADA para determinar se esta imagem foi gerada especificamente pelo GOOGLE GEMINI/IMAGEN.

PRIORIDADE MÁXIMA - Procure por:
1. **SynthID**: Marca d'água imperceptível do Google (padrões específicos nos pixels)
2. **Assinatura visual do Imagen**: Estilo de renderização característico do Google
3. **Padrões de difusão**: Específicos dos modelos do Google

Analise também:
4. Texturas e gradientes típicos do Imagen (suavidade característica)
5. Tratamento de iluminação e cores (paleta do Google)
6. Artefatos específicos do Gemini (diferentes de DALL-E/Midjourney/SD)
7. Metadados ou marcações digitais do Google
8. Estilo de composição e detalhamento típico do Imagen

DIFERENCIE de outros geradores:
- DALL-E (OpenAI): estilo mais pictórico
- Midjourney: estilo artístico dramático
- Stable Diffusion: características open-source específicas

Seja EXTREMAMENTE PRECISO. Responda com um número de 0 (NÃO é Google) a 100 (É Google)."""
    
    def analyze(self, image_data: ImageData) -> AnalysisResult:
        if image_data.width < 100 or image_data.height < 100:
            raise AnalysisFailedException("Imagem muito pequena para análise detalhada. Mínimo 100x100 pixels.")
        
        return super().analyze(image_data)
