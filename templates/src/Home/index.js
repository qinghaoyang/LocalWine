import React from 'react'
import { useState } from 'react'
import SearchBar from '../SearchBar'
import Wines from '../Wines';

function Home() {
    const [searchedWines, setSearchedWines] = useState([])
    const [wineryWines, setWineryWines] = useState([])

    return (
      <div className={ (searchedWines.length > 0 || wineryWines.length > 0) ? 
        "min-h-screen bg-black/95" :
        "min-h-screen bg-[url('../public/background.webp')]" }>
        <div className="bg-[url('../public/background.webp')]">
          <SearchBar
            searchedWines={searchedWines} 
            setSearchedWines={setSearchedWines}
            wineryWines={wineryWines}
            setWineryWines={setWineryWines}
          />
        </div>
        <div className="">
          {wineryWines.length > 0 ?
              <Wines wines={wineryWines} wineryWines={wineryWines}
          setWineryWines={setWineryWines}/>
          : <Wines wines={searchedWines} wineryWines={wineryWines}
          setWineryWines={setWineryWines}/>}
        </div>
      </div>
    )
}

export default Home;