import React, { useState } from 'react';
import '../styles/SearchBar.css';
import logo from '../img/podcast-search.png';

const SearchBar = ({ onSearch, isSearching }) => {
  const [query, setQuery] = useState('');
  const [isExpanded, setIsExpanded] = useState(true);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (query.trim()) {
      setIsExpanded(false);
      onSearch(query);
    }
  };

  // Add banner styles
  const bannerStyle = {
    width: '100%',
    height: '200px',
    marginBottom: '20px',
    position: 'relative',
    overflow: 'hidden'
  };

  const imageStyle = {
    width: '100%',
    height: '100%',
    objectFit: 'cover',
    objectPosition: 'center'
  };

  return (
    <div>
      <div style={bannerStyle}>
        <img 
          src= {logo} 
          alt="Podcast Search Banner"
          style={imageStyle}
        />
      </div>
      <div className={`search-container ${!isExpanded ? 'collapsed' : ''}`}>
        <form onSubmit={handleSubmit}>
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search for podcasts..."
            className="search-input"
            disabled={isSearching}
          />
          <button 
            type="submit" 
            className="search-button"
            disabled={isSearching}
          >
            Search
          </button>
        </form>
      </div>
    </div>
  );
};

export default SearchBar;