import React, { useState } from 'react';
import DocumentUpload from './components/DocumentUpload';
import QueryForm from './components/QueryForm';
import ResultDisplay from './components/ResultDisplay';
import './styles.css';

function App() {
  const [uploadedFiles, setUploadedFiles] = useState([]);
  const [queryResult, setQueryResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleFileUpload = (files) => {
    setUploadedFiles(prev => [...prev, ...files]);
  };

  const handleQuerySubmit = async (query) => {
    if (!query.trim()) return;
    
    setIsLoading(true);
    try {
      const response = await fetch('http://localhost:5000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query }),
      });
      
      const data = await response.json();
      setQueryResult(data);
    } catch (error) {
      console.error('Error:', error);
      setQueryResult({ error: 'Failed to process query' });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>Document Query System</h1>
        <p>Upload documents and ask questions about their content</p>
      </header>
      
      <div className="main-content">
        <DocumentUpload onFileUpload={handleFileUpload} />
        
        <div className="query-section">
          <QueryForm onSubmit={handleQuerySubmit} />
          
          {isLoading && <div className="loading">Processing your query...</div>}
          
          {queryResult && <ResultDisplay result={queryResult} />}
        </div>
      </div>
      
      <footer className="app-footer">
        <p>Powered by Large Language Models</p>
      </footer>
    </div>
  );
}

export default App;
