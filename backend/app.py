from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv

from services import AIDetectionService
from exceptions import AIDetectionException, APIKeyMissingException

load_dotenv()

app = Flask(__name__)
CORS(app)

try:
    detection_service = AIDetectionService()
    print(f"✅ Serviço inicializado: {detection_service}")
except APIKeyMissingException as e:
    print(f"⚠️  AVISO: {e.message}")
    print("Por favor, crie um arquivo .env com sua chave da API do Gemini")
    detection_service = None


@app.route('/api/health', methods=['GET'])
def health():
    if detection_service and detection_service.is_configured:
        return jsonify(detection_service.health_check())
    else:
        return jsonify({
            'status': 'error',
            'message': 'Serviço não configurado corretamente',
            'api_configured': False
        }), 503


@app.route('/api/analyze', methods=['POST'])
def analyze_image():
    if not detection_service or not detection_service.is_configured:
        return jsonify({
            'error': 'Serviço de detecção não está configurado',
            'success': False
        }), 503
    
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nenhuma imagem foi enviada', 'success': False}), 400
        
        image_file = request.files['image']
        
        analysis_type = request.form.get('type', 'standard')
        
        valid_types = ['standard', 'fast', 'detailed']
        if analysis_type not in valid_types:
            analysis_type = 'standard'
        
        result = detection_service.analyze_image(image_file, analysis_type)
        
        return jsonify(result.to_dict())
    
    except AIDetectionException as e:
        print(f"Erro de detecção: {e.message} (Código: {e.error_code})")
        return jsonify(e.to_dict()), 400
    
    except Exception as e:
        print(f"Erro inesperado: {str(e)}")
        return jsonify({
            'error': f'Erro ao processar imagem: {str(e)}',
            'success': False
        }), 500


@app.route('/api/analysis-types', methods=['GET'])
def get_analysis_types():
    return jsonify({
        'types': [
            {
                'id': AIDetectionService.ANALYSIS_STANDARD,
                'name': 'Análise Padrão',
                'description': 'Análise balanceada entre velocidade e precisão'
            },
            {
                'id': AIDetectionService.ANALYSIS_FAST,
                'name': 'Análise Rápida',
                'description': 'Análise mais rápida com menor precisão'
            },
            {
                'id': AIDetectionService.ANALYSIS_DETAILED,
                'name': 'Análise Detalhada',
                'description': 'Análise mais profunda e precisa (mais lenta)'
            }
        ]
    })


if __name__ == '__main__':
    print("\n" + "="*60)
    print("🤖 AI Detection Service - Backend POO")
    print("="*60)
    
    if detection_service and detection_service.is_configured:
        print(f"✅ Modelo: {detection_service.model_name}")
        print("✅ Serviço pronto para uso!")
    else:
        print("⚠️  Serviço não configurado - verifique a API key")
    
    print("="*60 + "\n")
    
    app.run(debug=True, port=5000)
