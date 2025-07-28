import React from 'react';

const ResultDisplay = ({ result }) => {
  if (!result) return null;
  
  if (result.error) {
    return (
      <div className="result-display error">
        <h2>Query Error</h2>
        <p>{result.error}</p>
      </div>
    );
  }
  
  return (
    <div className="result-display">
      <h2>Query Results</h2>
      
      <div className="result-section">
        <h3>Answer:</h3>
        <div className="answer-box">
          {result.answer}
        </div>
      </div>
      
      <div className="result-section">
        <h3>Explanation:</h3>
        <div className="explanation-box">
          {result.explanation}
        </div>
      </div>
      
      <div className="json-viewer">
        <h3>Raw JSON:</h3>
        <pre><code>{JSON.stringify(result, null, 2)}</code></pre>
      </div>
    </div>
  );
};

export default ResultDisplay;
