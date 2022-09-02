import React from 'react'
import { useState } from 'react'
import axiosInstance from '../apiUrl';

function SearchBar ({
    searchedWines, setSearchedWines, wineryWines, setWineryWines }) {
  const [query, setQuery] = useState('')

  return (
    <form className='flex justify-center' onSubmit={(e) => {
      axiosInstance.post('/wines/search', {'searched_text': query}).then(
      response => {
          setWineryWines([]);
          const searched_wines = response.data.wines;
          setSearchedWines(searched_wines)
      }).catch(error => {
        alert('Error: ' + error.message)
      });
      e.preventDefault();
    }}>   
        <div className="relative w-1/2 mt-48 mb-8">
            <div className="flex absolute inset-y-0 left-0 items-center pl-3
                pointer-events-none">
              <svg aria-hidden="true"
                  className="w-5 h-5 text-gray-500 dark:text-gray-400"
                  fill="none" stroke="currentColor"
                  viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path
                  strokeLinecap="round" strokeLinejoin="round"
                  strokeWidth="2"
                  d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z">
                </path>
              </svg>
            </div>
            <input
                type="text" 
                id="default-search"
                className="block p-4 pl-10 w-full text-sm text-gray-900
                bg-gray-50 rounded-lg border border-gray-300
                focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700
                dark:border-gray-600 dark:placeholder-gray-400
                dark:text-white dark:focus:ring-blue-500
                dark:focus:border-blue-500"
                placeholder="Search Name/Vineyard or Variety"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                required
            />
            <button
                type="submit"
                className="text-white absolute right-2.5 bottom-2.5 bg-blue-700
                hover:bg-blue-800 focus:ring-4 focus:outline-none
                focus:ring-black-300 font-medium text-sm px-4 py-2
                dark:bg-blue-600 dark:hover:bg-blue-700
                dark:focus:ring-blue-800"
            >
              Search
            </button>
        </div>
    </form>
  )
}

export default SearchBar;