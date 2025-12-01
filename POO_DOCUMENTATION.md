# 🎓 Documentação POO - AI ou Não?

## Conceitos de Programação Orientada a Objetos Implementados

Este projeto demonstra **todos os 5 conceitos fundamentais de POO** de forma prática e aplicada.

---

## 1️⃣ Classes e Objetos

### Definição
Classes são moldes/blueprints que definem estruturas de dados e comportamentos. Objetos são instâncias dessas classes.

### Implementação no Projeto

**`models.py`**
```python
class ImageData:
    """Representa dados de uma imagem"""
    def __init__(self, image: Image.Image, filename: str):
        self.__image = image
        self.__filename = filename

class AnalysisResult:
    """Representa o resultado de uma análise"""
    def __init__(self, probability: int, analysis_text: str):
        self.__probability = probability
        self.__analysis_text = analysis_text
```

**Uso no app.py**
```python
# Criar OBJETO do serviço de detecção
detection_service = AIDetectionService()

# Usar OBJETO para analisar
result = detection_service.analyze_image(image_file)  # result é um OBJETO AnalysisResult
```

---

## 2️⃣ Encapsulamento

### Definição
Encapsulamento esconde os detalhes internos de implementação e expõe apenas interfaces necessárias. Em Python, usa-se `_` (protegido) e `__` (privado) por convenção.

### Implementação no Projeto

**`models.py` - Atributos Privados com Properties**
```python
class ImageData:
    def __init__(self, image: Image.Image, filename: str):
        self.__image = image  # Atributo PRIVADO (__)
        self.__filename = filename  # Não pode ser acessado diretamente
    
    @property
    def image(self) -> Image.Image:
        """Getter - acesso controlado ao atributo privado"""
        return self.__image
    
    @property
    def filename(self) -> str:
        """Getter - acesso controlado"""
        return self.__filename
```

**`services.py` - Métodos Privados**
```python
class AIDetectionService:
    def __init__(self, api_key: str):
        self.__api_key = api_key  # PRIVADO - não acessível fora da classe
        self.__config = None  # PRIVADO
    
    def _validate_and_configure(self):  # Método PROTEGIDO (_)
        """Validação interna - não deve ser chamado externamente"""
        pass
    
    def analyze_image(self, image_file):  # Método PÚBLICO
        """Interface pública para análise"""
        pass
```

**Benefícios:**
- Dados internos não podem ser modificados acidentalmente
- Controle total sobre como os dados são acessados/modificados
- Facilita manutenção e mudanças internas

---

## 3️⃣ Herança

### Definição
Herança permite que uma classe (filha) herde atributos e métodos de outra classe (pai), promovendo reutilização de código.

### Implementação no Projeto

**`analyzers.py` - Hierarquia de Classes**

```python
# Classe PAI (base)
class BaseAnalyzer(ABC):
    def __init__(self, config: AIModelConfig):
        self._config = config  # Atributo herdado por todas as subclasses
    
    def _extract_probability(self, text: str) -> int:
        """Método COMUM herdado por todos os filhos"""
        pass

# Classe FILHA (herda de BaseAnalyzer)
class GeminiAIDetector(BaseAnalyzer):
    def __init__(self, config):
        super().__init__(config)  # Chama construtor do PAI
        # Herda _config e _extract_probability automaticamente

# Classe NETA (herança multinível)
class FastAIDetector(GeminiAIDetector):
    # Herda de GeminiAIDetector que herda de BaseAnalyzer
    pass
```

**`exceptions.py` - Hierarquia de Exceções**
```python
# Exceção BASE
class AIDetectionException(Exception):
    def __init__(self, message: str, error_code: str):
        self.message = message
        self.error_code = error_code

# Exceções FILHAS herdam o comportamento da base
class InvalidImageException(AIDetectionException):
    def __init__(self, message: str = "Imagem inválida"):
        super().__init__(message, "INVALID_IMAGE")

class NoImageProvidedException(AIDetectionException):
    def __init__(self, message: str = "Nenhuma imagem enviada"):
        super().__init__(message, "NO_IMAGE_PROVIDED")
```

**Benefícios:**
- Reutilização de código (não repete lógica comum)
- Extensibilidade (fácil adicionar novos tipos)
- Organização hierárquica clara

---

## 4️⃣ Polimorfismo

### Definição
Polimorfismo permite que objetos de diferentes classes sejam tratados através de uma interface comum, mas cada um se comporta de forma diferente.

### Implementação no Projeto

**`analyzers.py` - Métodos Abstratos Sobrescritos**

```python
# Classe base define INTERFACE comum
class BaseAnalyzer(ABC):
    @abstractmethod
    def analyze(self, image_data: ImageData) -> AnalysisResult:
        """Cada subclasse DEVE implementar de forma diferente"""
        pass

# Implementação 1: Análise padrão
class GeminiAIDetector(BaseAnalyzer):
    def analyze(self, image_data: ImageData) -> AnalysisResult:
        # Implementação completa e detalhada
        prompt = self._generate_prompt()
        response = self._model.generate_content([prompt, image_data.image])
        return AnalysisResult(...)

# Implementação 2: Análise rápida (POLIMORFISMO)
class FastAIDetector(GeminiAIDetector):
    def _generate_prompt(self) -> str:
        # SOBRESCREVE o método para ser mais rápido
        return "Análise rápida. É IA? Responda 0-100."
    
    def _generate_detailed_analysis(self, image_data, probability):
        # SOBRESCREVE para análise mais simples
        return f"Análise rápida: {probability}%"

# Implementação 3: Análise detalhada (POLIMORFISMO)
class DetailedAIDetector(GeminiAIDetector):
    def _generate_prompt(self) -> str:
        # SOBRESCREVE para ser mais detalhado
        return "Análise PROFUNDA... [prompt longo]"
```

**`services.py` - Uso Polimórfico**
```python
def _select_analyzer(self, analysis_type: str) -> BaseAnalyzer:
    """Retorna diferentes implementações, mas todas são BaseAnalyzer"""
    if analysis_type == "fast":
        return FastAIDetector(self.__config)  # Comportamento rápido
    elif analysis_type == "detailed":
        return DetailedAIDetector(self.__config)  # Comportamento detalhado
    else:
        return GeminiAIDetector(self.__config)  # Comportamento padrão

def analyze_image(self, image_file, analysis_type: str):
    analyzer = self._select_analyzer(analysis_type)  # Tipo: BaseAnalyzer
    result = analyzer.analyze(image_data)  # POLIMORFISMO - chama o método certo
```

**Duck Typing em Python**
```python
# Todos respondem a .analyze(), mas cada um faz diferente
analyzers = [
    GeminiAIDetector(config),
    FastAIDetector(config),
    DetailedAIDetector(config)
]

for analyzer in analyzers:
    result = analyzer.analyze(image_data)  # POLIMORFISMO!
    # Cada um executa analyze() de forma diferente
```

**Benefícios:**
- Código flexível e extensível
- Mesma interface, diferentes comportamentos
- Fácil trocar implementações sem mudar código cliente

---

## 5️⃣ Exceções

### Definição
Exceções são mecanismos para tratar erros de forma estruturada, permitindo separar lógica de negócio do tratamento de erros.

### Implementação no Projeto

**`exceptions.py` - Hierarquia de Exceções Customizadas**

```python
# Exceção BASE customizada
class AIDetectionException(Exception):
    def __init__(self, message: str, error_code: str):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)
    
    def to_dict(self):
        """Facilita retornar erro como JSON"""
        return {
            'error': self.message,
            'error_code': self.error_code,
            'success': False
        }

# Exceções ESPECÍFICAS
class InvalidImageException(AIDetectionException):
    """Imagem inválida ou corrompida"""
    pass

class NoImageProvidedException(AIDetectionException):
    """Nenhuma imagem fornecida"""
    pass

class AnalysisFailedException(AIDetectionException):
    """Falha na análise"""
    def __init__(self, message: str, original_error: Exception = None):
        self.original_error = original_error
        super().__init__(message, "ANALYSIS_FAILED")
```

**`services.py` - Lançando Exceções**
```python
class AIDetectionService:
    def _create_image_data(self, image_file) -> ImageData:
        if not image_file:
            raise NoImageProvidedException()  # LANÇA exceção customizada
        
        try:
            image = Image.open(BytesIO(image_bytes))
        except (IOError, OSError) as e:
            raise InvalidImageException(f"Erro ao abrir: {e}")  # LANÇA com contexto

class GeminiAIDetector(BaseAnalyzer):
    def analyze(self, image_data: ImageData) -> AnalysisResult:
        try:
            response = self._model.generate_content([prompt, image_data.image])
            return AnalysisResult(...)
        except Exception as e:
            raise AnalysisFailedException(
                message="Falha ao analisar imagem",
                original_error=e  # Preserva erro original
            )
```

**`app.py` - Tratando Exceções**
```python
@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    try:
        result = detection_service.analyze_image(image_file, analysis_type)
        return jsonify(result.to_dict())
    
    except AIDetectionException as e:
        # Trata TODAS as exceções customizadas
        print(f"Erro: {e.message} (Código: {e.error_code})")
        return jsonify(e.to_dict()), 400  # Usa método to_dict()
    
    except Exception as e:
        # Trata erros inesperados
        return jsonify({'error': str(e), 'success': False}), 500
```

**Benefícios:**
- Tratamento de erros estruturado e específico
- Mensagens de erro claras e úteis
- Separação entre lógica e tratamento de erro
- Facilita debug e manutenção

---

## 📊 Estrutura Completa do Projeto POO

```
backend/
├── app.py                 # Flask app - usa todas as classes
├── exceptions.py          # Exceções customizadas (EXCEÇÕES)
├── models.py              # Classes de dados (CLASSES, OBJETOS, ENCAPSULAMENTO)
├── analyzers.py           # Hierarquia de analisadores (HERANÇA, POLIMORFISMO)
├── services.py            # Serviço principal (COMPOSIÇÃO, ENCAPSULAMENTO)
└── requirements.txt
```

---

## 🎯 Resumo dos Conceitos

| Conceito | Arquivos | Exemplo Prático |
|----------|----------|-----------------|
| **Classes e Objetos** | `models.py`, todos | `ImageData`, `AnalysisResult`, `AIDetectionService` |
| **Encapsulamento** | `models.py`, `services.py` | Atributos `__privados`, `@property`, métodos `_protegidos` |
| **Herança** | `analyzers.py`, `exceptions.py` | `BaseAnalyzer` → `GeminiAIDetector` → `FastAIDetector` |
| **Polimorfismo** | `analyzers.py` | `.analyze()` diferente em cada subclasse |
| **Exceções** | `exceptions.py`, todos | `AIDetectionException` e subclasses customizadas |

---

## 🚀 Como Usar

O sistema mantém a **mesma funcionalidade** da versão anterior, mas agora com arquitetura POO:

```python
# Criar serviço (OBJETO)
service = AIDetectionService()

# Analisar imagem (POLIMORFISMO - usa diferentes analisadores)
result = service.analyze_image(image_file, analysis_type='standard')

# Acessar resultado (ENCAPSULAMENTO)
print(result.probability)      # Getter
print(result.classification)   # Getter
print(result.to_dict())        # Método público
```

---

## 💡 Vantagens da Refatoração POO

1. **Manutenibilidade**: Código organizado em módulos claros
2. **Extensibilidade**: Fácil adicionar novos tipos de análise
3. **Reutilização**: Lógica comum não é repetida
4. **Testabilidade**: Cada classe pode ser testada isoladamente
5. **Clareza**: Responsabilidades bem definidas
6. **Profissional**: Segue boas práticas da indústria

---

Desenvolvido para demonstrar conceitos de POO de forma prática e aplicada! 🎓
