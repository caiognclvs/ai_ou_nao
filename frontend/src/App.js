import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(null);
  const [analyzing, setAnalyzing] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);
  const [dragActive, setDragActive] = useState(false);

  const handleFileSelect = (file) => {
    if (file && file.type.startsWith('image/')) {
      setSelectedFile(file);
      setPreviewUrl(URL.createObjectURL(file));
      setResult(null);
      setError(null);
    } else {
      setError('Por favor, selecione uma imagem válida');
    }
  };

  const handleDrag = (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileSelect(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      handleFileSelect(e.target.files[0]);
    }
  };

  const analyzeImage = async () => {
    if (!selectedFile) {
      setError('Por favor, selecione uma imagem primeiro');
      return;
    }

    setAnalyzing(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append('image', selectedFile);

    try {
      const response = await axios.post('http://localhost:5000/api/analyze', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setResult(response.data);
    } catch (err) {
      setError(err.response?.data?.error || 'Erro ao analisar imagem. Verifique se o backend está rodando.');
      console.error('Erro:', err);
    } finally {
      setAnalyzing(false);
    }
  };

  const resetAnalysis = () => {
    setSelectedFile(null);
    setPreviewUrl(null);
    setResult(null);
    setError(null);
  };

  const getProbabilityColor = (probability) => {
    if (probability >= 80) return '#e74c3c';
    if (probability >= 60) return '#e67e22';
    if (probability >= 40) return '#f39c12';
    if (probability >= 20) return '#3498db';
    return '#2ecc71';
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🤖 AI ou Não?</h1>
        <p className="subtitle">Detecte se uma imagem foi gerada por Inteligência Artificial</p>
      </header>

      <main className="App-main">
        {!previewUrl ? (
          <div 
            className={`upload-area ${dragActive ? 'drag-active' : ''}`}
            onDragEnter={handleDrag}
            onDragLeave={handleDrag}
            onDragOver={handleDrag}
            onDrop={handleDrop}
          >
            <div className="upload-content">
              <svg className="upload-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" />
              </svg>
              <h2>Arraste uma imagem aqui</h2>
              <p>ou</p>
              <label htmlFor="file-upload" className="file-upload-label">
                Escolher arquivo
              </label>
              <input
                id="file-upload"
                type="file"
                accept="image/*"
                onChange={handleChange}
                style={{ display: 'none' }}
              />
              <p className="upload-hint">Formatos suportados: JPG, PNG, GIF, WebP</p>
            </div>
          </div>
        ) : (
          <div className="analysis-container">
            <div className="image-preview">
              <img src={previewUrl} alt="Preview" />
            </div>

            {!result && (
              <button 
                onClick={analyzeImage} 
                disabled={analyzing}
                className="analyze-button"
              >
                {analyzing ? (
                  <>
                    <span className="spinner"></span>
                    Analisando...
                  </>
                ) : (
                  'Analisar Imagem'
                )}
              </button>
            )}

            {result && (
              <div className="result-container">
                <div 
                  className="probability-circle"
                  style={{ 
                    background: `conic-gradient(${getProbabilityColor(result.probability)} ${result.probability * 3.6}deg, #e0e0e0 0deg)` 
                  }}
                >
                  <div className="probability-inner">
                    <span className="probability-value">{result.probability}%</span>
                    <span className="probability-label">IA</span>
                  </div>
                </div>

                <div className="result-details">
                  <h3 className="classification" style={{ color: getProbabilityColor(result.probability) }}>
                    {result.classification}
                  </h3>
                  <p className="analysis-text">{result.analysis}</p>
                </div>
              </div>
            )}

            <button onClick={resetAnalysis} className="reset-button">
              Analisar outra imagem
            </button>
          </div>
        )}

        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}
      </main>

      <footer className="App-footer">
        <p>
          ⚠️ Esta ferramenta usa IA para análise e pode não ser 100% precisa. 
          Use como uma estimativa, não como certeza absoluta.
        </p>
      </footer>
    </div>
  );
}

export default App;
