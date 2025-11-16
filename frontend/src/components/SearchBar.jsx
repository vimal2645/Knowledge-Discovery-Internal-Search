import React, { useState } from 'react';

function SearchBar({ onSearch, loading }) {
  const [query, setQuery] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSearch(query);
  };

  return (
    <form onSubmit={handleSubmit} className="search-bar">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Search documents... (e.g., 'marketing campaign 2024')"
        disabled={loading}
      />
      <button type="submit" disabled={loading || !query.trim()}>
        🔍 Search
      </button>
    </form>
  );
}

export default SearchBar;
