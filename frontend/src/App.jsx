import React, { useState, useEffect } from 'react';
import axios from 'axios';
import SearchBar from './components/SearchBar';
import UploadForm from './components/UploadForm';
import ResultCard from './components/ResultCard';
import FilterSidebar from './components/FilterSidebar';

const API_URL = 'https://knowledge-discovery-internal-search-d87d.onrender.com/api';

function App() {
  const [results, setResults] = useState([]);
  const [categories, setCategories] = useState(['All']);
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [loading, setLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  // Fetch categories on load
  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await axios.get(`${API_URL}/categories`);
      setCategories(response.data.categories);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const handleSearch = async (query) => {
    if (!query.trim()) {
      setResults([]);
      return;
    }

    setLoading(true);
    setSearchQuery(query);

    try {
      const response = await axios.get(`${API_URL}/search`, {
        params: { q: query, category: selectedCategory }
      });
      setResults(response.data.results);
    } catch (error) {
      console.error('Error searching:', error);
      alert('Search failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleUploadSuccess = () => {
    fetchCategories();
    if (searchQuery) {
      handleSearch(searchQuery);
    }
  };

  const handleCategoryChange = (category) => {
    setSelectedCategory(category);
    if (searchQuery) {
      handleSearch(searchQuery);
    }
  };

  return (
    <div className="app">
      <header className="header">
        <h1>📚 Knowledge Discovery</h1>
        <p>Find any document instantly</p>
      </header>

      <div className="container">
        <div className="main-content">
          <UploadForm onUploadSuccess={handleUploadSuccess} />
          <SearchBar onSearch={handleSearch} loading={loading} />

          {loading && <div className="loading">Searching...</div>}

          {!loading && results.length > 0 && (
            <div className="results-section">
              <h3>Found {results.length} results for "{searchQuery}"</h3>
              <div className="results-grid">
                {results.map((result, index) => (
                  <ResultCard key={index} result={result} />
                ))}
              </div>
            </div>
          )}

          {!loading && searchQuery && results.length === 0 && (
            <div className="no-results">
              <p>No documents found for "{searchQuery}"</p>
              <p>Try different keywords or upload more documents</p>
            </div>
          )}
        </div>

        <FilterSidebar
          categories={categories}
          selectedCategory={selectedCategory}
          onCategoryChange={handleCategoryChange}
        />
      </div>
    </div>
  );
}

export default App;
