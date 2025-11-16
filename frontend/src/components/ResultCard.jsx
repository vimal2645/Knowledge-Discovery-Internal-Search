import React from 'react';

function ResultCard({ result }) {
  const handleDownload = () => {
    window.open(
      `http://localhost:5000/api/download/${result.filename}`,
      '_blank'
    );
  };

  const getCategoryEmoji = (category) => {
    const emojiMap = {
      'Reports': '📊',
      'Campaigns': '📢',
      'Presentations': '🎯',
      'Documentation': '📝',
      'General': '📄'
    };
    return emojiMap[category] || '📄';
  };

  return (
    <div className="result-card">
      <div className="result-header">
        <h4>{getCategoryEmoji(result.category)} {result.filename}</h4>
        <span className="category-badge">{result.category}</span>
      </div>
      
      <p className="preview">{result.preview}</p>
      
      <div className="result-footer">
        <span className="date">📅 {result.upload_date}</span>
        <button onClick={handleDownload} className="download-btn">
          ⬇️ Download
        </button>
      </div>
    </div>
  );
}

export default ResultCard;
