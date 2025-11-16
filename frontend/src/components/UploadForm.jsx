import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:5000/api';

function UploadForm({ onUploadSuccess }) {
  const [file, setFile] = useState(null);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState('');

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      setFile(selectedFile);
      console.log('File selected:', selectedFile.name);
    }
    setMessage('');
  };

  const handleUpload = async (e) => {
    e.preventDefault();
    
    if (!file) {
      setMessage('❌ Please select a file first');
      return;
    }

    // Check file type
    const allowedTypes = ['text/plain', 'application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
    if (!allowedTypes.includes(file.type)) {
      setMessage('❌ Only TXT, PDF, and DOCX files are allowed');
      return;
    }

    setUploading(true);
    setMessage('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      console.log('Uploading file:', file.name);
      const response = await axios.post(`${API_URL}/upload`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      });
      
      setMessage(`✅ ${response.data.message}`);
      setFile(null);
      
      // Reset file input
      const fileInput = document.getElementById('file-input');
      if (fileInput) fileInput.value = '';
      
      onUploadSuccess();
    } catch (error) {
      console.error('Upload error:', error);
      setMessage(`❌ ${error.response?.data?.error || 'Upload failed'}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="upload-form">
      <form onSubmit={handleUpload}>
        <input
          id="file-input"
          type="file"
          onChange={handleFileChange}
          accept=".txt,.pdf,.docx,.doc"
          disabled={uploading}
          required
        />
        <button type="submit" disabled={uploading || !file}>
          {uploading ? '⏳ Uploading...' : '📤 Upload Document'}
        </button>
      </form>
      {message && <p className="message">{message}</p>}
    </div>
  );
}

export default UploadForm;
