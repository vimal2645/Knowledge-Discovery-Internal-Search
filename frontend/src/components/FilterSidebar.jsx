import React from 'react';

function FilterSidebar({ categories, selectedCategory, onCategoryChange }) {
  return (
    <aside className="filter-sidebar">
      <h3>📁 Filter by Category</h3>
      <ul>
        {categories.map((category) => (
          <li
            key={category}
            className={selectedCategory === category ? 'active' : ''}
            onClick={() => onCategoryChange(category)}
          >
            {category}
          </li>
        ))}
      </ul>
    </aside>
  );
}

export default FilterSidebar;
