import React from 'react';
import '../styles/SearchResults.css';

const SearchResults = ({ results }) => {
  console.log("results", results)
  if (!results.length) {
    console.log("iam here")
    return null;
  }
  
  return (
    <div className="search-results">
      <div>
        <h2>Search Results</h2>
        <p className="result-count">{results.length} results found</p>
      </div>
      {results.map((podcast, index) => (
        <div key={index} className="podcast-card">
          <div className="podcast-image">
            <img src={podcast.content_1__url || podcast.thumbnail__url || podcast.image__href} alt={podcast.summary__itunes} />
            <button className="play-button" onClick={() => window.open(podcast.content_0_player_url || podcast.enclosure__url)}>
              ▶
            </button>
          </div>
          <div className="podcast-info">
            <h3>{podcast.title}</h3>
            <p className="podcast-author">{podcast.author}</p>
            <p className="podcast-description">{podcast.description}</p>
            <em>{podcast.keywords__itunes}</em>
          </div>
        </div>
      ))}
    </div>
  );
};

export default SearchResults;