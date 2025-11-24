from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os
from dotenv import load_dotenv
import base64
from PIL import Image
import io

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
CORS(app)  # Permitir requisições do frontend React

# Configurar API do Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

@app.route('/api/health', methods=['GET'])
def health():
    """Endpoint para verificar se o servidor está funcionando"""
    return jsonify({'status': 'ok', 'message': 'Backend está funcionando!'})

@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    """
    Endpoint para analisar se uma imagem foi gerada por IA
    Espera um arquivo de imagem no form-data
    """
    try:
        # Verificar se o arquivo foi enviado
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem foi enviada'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'Nenhuma imagem selecionada'}), 400
        
        # Ler a imagem
        image_bytes = file.read()
        image = Image.open(io.BytesIO(image_bytes))
        
        # Configurar o modelo Gemini
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Prompt otimizado para detecção de imagens geradas por IA
        prompt = """Analise cuidadosamente esta imagem e determine a probabilidade de ela ter sido gerada por uma inteligência artificial (especialmente modelos de geração de imagem como Imagen, DALL-E, Midjourney, Stable Diffusion, etc.).

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

        # Fazer a análise com o Gemini
        response = model.generate_content([prompt, image])
        
        # Extrair a probabilidade da resposta
        try:
            probability = int(response.text.strip())
            # Garantir que está no intervalo 0-100
            probability = max(0, min(100, probability))
        except ValueError:
            # Se não conseguir converter, tentar extrair número do texto
            import re
            numbers = re.findall(r'\d+', response.text)
            if numbers:
                probability = int(numbers[0])
                probability = max(0, min(100, probability))
            else:
                probability = 50  # Valor padrão em caso de erro
        
        # Gerar análise descritiva
        analysis_prompt = f"""Com base na probabilidade de {probability}% de esta imagem ter sido gerada por IA, forneça uma breve análise (2-3 frases) explicando os principais indicadores que levaram a essa conclusão."""
        
        analysis_response = model.generate_content([analysis_prompt, image])
        analysis_text = analysis_response.text.strip()
        
        # Determinar classificação
        if probability >= 80:
            classification = "Muito provável IA"
        elif probability >= 60:
            classification = "Provavelmente IA"
        elif probability >= 40:
            classification = "Incerto"
        elif probability >= 20:
            classification = "Provavelmente real"
        else:
            classification = "Muito provável real"
        
        return jsonify({
            'probability': probability,
            'classification': classification,
            'analysis': analysis_text,
            'success': True
        })
    
    except Exception as e:
        print(f"Erro ao processar imagem: {str(e)}")
        return jsonify({
            'error': f'Erro ao processar imagem: {str(e)}',
            'success': False
        }), 500

if __name__ == '__main__':
    # Verificar se a API key está configurada
    if not os.getenv('GEMINI_API_KEY'):
        print("⚠️  AVISO: GEMINI_API_KEY não está configurada!")
        print("Por favor, crie um arquivo .env com sua chave da API do Gemini")
    else:
        print("✅ API Key do Gemini configurada!")
    
    app.run(debug=True, port=5000)
