import React, { useState } from 'react';

const QueryForm = ({ onSubmit }) => {
  const [query, setQuery] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(query);
  };
  
  return (
    <div className="query-form">
      <h2>Ask a Question</h2>
      <form onSubmit={handleSubmit}>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Type your question about the uploaded documents..."
          rows={4}
          required
        />
        <button type="submit" className="submit-btn">
          Submit Query
        </button>
      </form>
    </div>
  );
};

export default QueryForm;
