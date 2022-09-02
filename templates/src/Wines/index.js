import React from 'react';
import { useState } from 'react';
import WineReviews from '../WineReviews';

import axiosInstance from '../apiUrl';

function Wines({ wines, wineryWines, setWineryWines }) {
    const [modal, setModal] = useState({isOpen: false, wine: {}});

    return (
      <div className='flex flex-wrap place-content-center'>
        {wines.map(wine => (
          <div className="w-64 mb-4 ml-2 mr-2 shadow-lg " >
            <div className="flex h-48 mx-auto">
              <img
                className="rounded h-full mx-auto "
                src={wine.photo_url}
                alt={wine.name}
              />
            </div>
            <div className="px-6 py-4">
              <button
                className="font-bold text-gray-200 text-xl mb-2"
                style={{ fontFamily: "coustard" }}
                onClick={() => {
                  setModal({isOpen: true, wine: wine});
                }}>
                  Vineyard: {wine.name}
              </button>
              <p
                className="text-gray-400 text-base"
                style={{ fontFamily: 'Gentium Basic' }}>
                  Variety: {wine.variety}
              </p>
              <p
                className="text-gray-400 text-base"
                style={{ fontFamily: 'Gentium Basic' }}>
                  Rating: {wine.avg_rating}/100
              </p>
              {/* <hr style={{ borderTop: "1px solid" }} /> */}
              <button
                className="italic text-gray-500 text-sm underline"
                style={{ fontFamily: 'Gentium Basic' }}
                onClick={() => {
                  axiosInstance.get('/wineries/' + wine.winery.id + '/wines').then(
                    response => {
                      console.log('response.data.wines: ', response.data.wines)
                      setWineryWines(response.data.wines)
                    }
                  )
                }}>
                Winery: {
                  wine.winery.name + ', ' + wine.winery.region + ', ' + wine.winery.state
                }
              </button>
              
            </div>
          </div>
        ))}
      <WineReviews modal={modal} setModal={setModal} className="rounded-lg mt-4 ml-32 mr-32" />
      </div>
    )
}

export default Wines;