"""
Hierarquia de analisadores de imagem usando classe abstrata.
Demonstra os conceitos de POO: HERANÇA, POLIMORFISMO e CLASSES ABSTRATAS
"""

from abc import ABC, abstractmethod
from typing import Optional
import google.generativeai as genai
import re

from models import ImageData, AnalysisResult, AIModelConfig
from exceptions import AnalysisFailedException, ModelNotAvailableException


class BaseAnalyzer(ABC):
    """
    Classe abstrata base para todos os analisadores.
    Demonstra HERANÇA: classes filhas herdarão métodos e atributos
    Demonstra POLIMORFISMO: classes filhas implementarão métodos abstratos de forma diferente
    """
    
    def __init__(self, config: AIModelConfig):
        self._config = config  # Atributo protegido (convenção Python com _)
        self._model = None
        self._initialize_model()
    
    @abstractmethod
    def _initialize_model(self):
        """Método abstrato: cada analisador implementa sua própria inicialização"""
        pass
    
    @abstractmethod
    def _generate_prompt(self) -> str:
        """Método abstrato: cada analisador tem seu próprio prompt"""
        pass
    
    @abstractmethod
    def analyze(self, image_data: ImageData) -> AnalysisResult:
        """
        Método abstrato principal: analisa uma imagem.
        POLIMORFISMO: cada subclasse implementará de forma diferente
        """
        pass
    
    def _extract_probability(self, response_text: str) -> int:
        """
        Método comum (não abstrato) herdado por todas as subclasses.
        Extrai probabilidade da resposta do modelo
        """
        try:
            probability = int(response_text.strip())
            return max(0, min(100, probability))
        except ValueError:
            # Tentar extrair número do texto
            numbers = re.findall(r'\d+', response_text)
            if numbers:
                probability = int(numbers[0])
                return max(0, min(100, probability))
            else:
                return 50  # Valor padrão
    
    def __str__(self):
        return f"{self.__class__.__name__}(model={self._config.model_name})"


class GeminiAIDetector(BaseAnalyzer):
    """
    Analisador específico usando Gemini AI.
    Demonstra HERANÇA: herda de BaseAnalyzer
    Demonstra POLIMORFISMO: implementa métodos abstratos da classe pai
    """
    
    def _initialize_model(self):
        """Implementação específica da inicialização (POLIMORFISMO)"""
        try:
            genai.configure(api_key=self._config.api_key)
            self._model = genai.GenerativeModel(self._config.model_name)
        except Exception as e:
            raise ModelNotAvailableException(self._config.model_name)
    
    def _generate_prompt(self) -> str:
        """Implementação específica do prompt (POLIMORFISMO)"""
        return """Analise cuidadosamente esta imagem e determine a probabilidade de ela ter sido gerada por uma inteligência artificial (especialmente modelos de geração de imagem como Imagen, DALL-E, Midjourney, Stable Diffusion, etc.).

Considere os seguintes aspectos:
1. Artefatos visuais típicos de IA (dedos extras, texto distorcido, inconsistências físicas)
2. Padrões de textura artificiais ou muito perfeitos
3. Iluminação e sombras inconsistentes
4. Elementos que desafiam a física ou anatomia
5. Qualidade e estilo típicos de imagens geradas por IA
6. Presença de "AI watermarks" ou padrões específicos

Responda APENAS com um número entre 0 e 100, onde:
- 0 significa certeza de que é uma foto real
- 100 significa certeza de que foi gerada por IA
- Valores intermediários representam o nível de confiança

Forneça APENAS o número, sem explicações adicionais."""
    
    def analyze(self, image_data: ImageData) -> AnalysisResult:
        """
        Implementação específica da análise (POLIMORFISMO).
        Este método sobrescreve o método abstrato da classe pai
        """
        try:
            # Análise de probabilidade
            prompt = self._generate_prompt()
            response = self._model.generate_content([prompt, image_data.image])
            probability = self._extract_probability(response.text)
            
            # Gerar análise descritiva
            analysis_text = self._generate_detailed_analysis(image_data, probability)
            
            return AnalysisResult(probability=probability, analysis_text=analysis_text)
            
        except Exception as e:
            raise AnalysisFailedException(
                message="Falha ao analisar imagem com Gemini AI",
                original_error=e
            )
    
    def _generate_detailed_analysis(self, image_data: ImageData, probability: int) -> str:
        """Gera análise textual detalhada (método auxiliar específico desta classe)"""
        try:
            analysis_prompt = f"""Com base na probabilidade de {probability}% de esta imagem ter sido gerada por IA, forneça uma breve análise (2-3 frases) explicando os principais indicadores que levaram a essa conclusão."""
            
            analysis_response = self._model.generate_content([analysis_prompt, image_data.image])
            return analysis_response.text.strip()
        except Exception:
            # Fallback para mensagem padrão se a análise descritiva falhar
            return f"Análise indica {probability}% de probabilidade de geração por IA."


class FastAIDetector(GeminiAIDetector):
    """
    Detector otimizado para análise rápida.
    Demonstra HERANÇA MULTINÍVEL: herda de GeminiAIDetector que herda de BaseAnalyzer
    Demonstra POLIMORFISMO: sobrescreve métodos para comportamento diferente
    """
    
    def _generate_prompt(self) -> str:
        """
        POLIMORFISMO: Sobrescreve o prompt para ser mais direto e rápido
        """
        return """Analise esta imagem rapidamente. É uma imagem gerada por IA ou uma foto real?
Responda APENAS com um número de 0 (certeza de real) a 100 (certeza de IA)."""
    
    def _generate_detailed_analysis(self, image_data: ImageData, probability: int) -> str:
        """
        POLIMORFISMO: Sobrescreve para gerar análise mais simples e rápida
        """
        if probability >= 70:
            return f"Análise rápida detectou {probability}% de probabilidade de ser IA. Características típicas de geração artificial identificadas."
        elif probability >= 30:
            return f"Análise inconclusiva com {probability}% de probabilidade. Características mistas detectadas."
        else:
            return f"Análise rápida indica {probability}% de probabilidade de IA. Características predominantemente naturais."


class DetailedAIDetector(GeminiAIDetector):
    """
    Detector com análise mais detalhada e precisa.
    Demonstra HERANÇA e POLIMORFISMO com foco em análise profunda
    """
    
    def _generate_prompt(self) -> str:
        """POLIMORFISMO: Prompt mais detalhado e específico"""
        return """Realize uma análise DETALHADA e PROFUNDA desta imagem para determinar se foi gerada por IA.

Analise CUIDADOSAMENTE:
1. Anatomia e proporções (especialmente mãos, dedos, rostos)
2. Física e iluminação (sombras, reflexos, perspectiva)
3. Texturas e padrões (repetições, artefatos, distorções)
4. Texto e caracteres (legibilidade, coerência)
5. Coerência global da cena
6. Detalhes finos e bordas
7. Metadados visuais e marcas d'água

Seja CRÍTICO e PRECISO. Responda com um número de 0 a 100."""
    
    def analyze(self, image_data: ImageData) -> AnalysisResult:
        """
        POLIMORFISMO: Adiciona validações extras antes da análise
        """
        # Validação adicional para análise detalhada
        if image_data.width < 100 or image_data.height < 100:
            raise AnalysisFailedException("Imagem muito pequena para análise detalhada. Mínimo 100x100 pixels.")
        
        # Chama o método da classe pai
        return super().analyze(image_data)
