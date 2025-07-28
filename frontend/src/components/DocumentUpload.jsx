import React, { useState } from 'react';

const DocumentUpload = ({ onFileUpload }) => {
  const [isDragging, setIsDragging] = useState(false);
  
  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragging(true);
  };
  
  const handleDragLeave = () => {
    setIsDragging(false);
  };
  
  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragging(false);
    
    const files = Array.from(e.dataTransfer.files);
    const validFiles = files.filter(file => 
      file.type === 'application/pdf' || 
      file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
      file.type === 'message/rfc822'
    );
    
    if (validFiles.length > 0) {
      onFileUpload(validFiles);
    }
  };
  
  const handleFileInput = (e) => {
    const files = Array.from(e.target.files);
    const validFiles = files.filter(file => 
      file.type === 'application/pdf' || 
      file.type === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document' ||
      file.type === 'message/rfc822'
    );
    
    if (validFiles.length > 0) {
      onFileUpload(validFiles);
    }
  };
  
  return (
    <div className="document-upload">
      <h2>Upload Documents</h2>
      <div 
        className={`drop-area ${isDragging ? 'active' : ''}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <p>Drag & drop files here or</p>
        <label className="file-input-label">
          Browse Files
          <input 
            type="file" 
            multiple 
            accept=".pdf,.docx,.eml" 
            onChange={handleFileInput} 
            style={{ display: 'none' }} 
          />
        </label>
      </div>
      <div className="file-types">
        <p>Supported formats: PDF, DOCX, Email (.eml)</p>
      </div>
    </div>
  );
};

export default DocumentUpload;
