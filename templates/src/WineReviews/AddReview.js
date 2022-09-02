import React from 'react';
import { useState } from 'react';
import axiosInstance from '../apiUrl';
import { useAuth0 } from "@auth0/auth0-react";

function AddReview( {modal, setModal} ) {
  const { user, isAuthenticated } = useAuth0();
  const wine = modal.wine;
  const [rating, setRating] = useState(null);
  const [text, setText] = useState('');
  return (
    <div className="w-full mt-4 ml-4 mr-4">
      {isAuthenticated ? 
      <form className="relative"
        onSubmit={(e) => {
        axiosInstance.post('/wines/' + wine.id + '/reviews', {
          taster: user.name,
          rating: rating,
          text: text
        }).then(
          axiosInstance.get('/wines/' + wine.id).then(
            (response) => {
              console.log('wine: ', response.data.wine)
              setModal({isOpen: true, wine: response.data.wine});
            })
        ).catch(error => {
          alert('Error: ' + error.message)
        });
        e.preventDefault();
      }}>
        <div>
          <h4 className="block text-gray-700 text-lg font-bold">
            Add Review:
          </h4>
          <input
            type="integer" 
            className="border"
            placeholder="Rating /100"
            value={rating}
            onChange={(e) => setRating(e.target.value)}
            required
          />
        </div>
        <div>
          <input
            type="text"
            className="border w-full h-36"
            value={text}
            onChange={(e) => setText(e.target.value)}
            required
          />
        </div>
        <button
          type="submit"
          className="text-white absolute right-0 bg-blue-700 border-2 border-blue-700
          hover:bg-blue-800 font-medium text-sm px-4 py-2
          dark:bg-blue-600 dark:hover:bg-blue-700
          dark:focus:ring-blue-800"
        >
          Submit
        </button>
      </form> : <></>}
      <button
          className="border-2 border-blue-500 absolute right-32
          font-medium text-sm px-4 py-2"
          onClick={() => {setModal({isOpen: false, wine: {}})}}>
            Cancel
        </button>
    </div>
  )
}

export default AddReview;
