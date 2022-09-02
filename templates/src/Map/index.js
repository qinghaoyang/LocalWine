import React from 'react';
import { useState, useEffect } from 'react';
import { GoogleMap, useJsApiLoader, Marker, InfoWindow } from '@react-google-maps/api';

import axiosInstance from '../apiUrl';
import Wines from '../Wines';

const containerStyle = {
  width: '100%',
  height: '100%',
};

const center = {
    lat: 36.7783,
    lng: -119.4179
};

function MyComponent() {
  var { isLoaded: mapIsloaded } = useJsApiLoader({
    id: 'google-map-script',
    googleMapsApiKey: "AIzaSyCbPsdzuHr8hBGu1askRbWAjMGsDPiWdVo"
  })
  const [wineries, setWineries] = useState({items: [], isLoaded: false})

  const [wines, setWines] = useState([])
  
  const [map, setMap] = useState(null)
  
  const [icon, setIcon] = useState(null);
  
  const [infoWindow, setInfoWindow] = useState(null)
  
  const iconChange = (data) => {
    if (icon && data.id === icon.id) {
      return "https://storage.googleapis.com/support-kms-prod/SNP_2752129_en_v0"
    } else {
      return "https://storage.googleapis.com/support-kms-prod/SNP_2752125_en_v0"
    }
  }
    
  const onLoad = React.useCallback(function callback(map) {
    // const bounds = new window.google.maps.LatLngBounds(center);
    // map.fitBounds(bounds);
    // map.setZoom(6);
    setMap(map)
  }, [])
  
  const onUnmount = React.useCallback(function callback(map) {
    setMap(null)
  }, [])
  
  useEffect(() => {
    // console.log(instance.get('http://127.0.0.1:5000'))
    axiosInstance.get('/wineries/US').then(
      response => {
        const wineries = response.data.wineries;
        for (let i = 0; i < wineries.length; i++) {
          if (wineries[i].latitude < 0) {
            wineries[i].latitude = 360 + wineries[i].latitude;
          }
          if (wineries[i].longitude < 0) {
            wineries[i].longitude = 360 + wineries[i].longitude;
          }
        }
        setWineries({items: wineries, isLoaded: true})
      });
    }, []);

  // console.log(mapIsloaded)
  // console.log(wineries)
  return (mapIsloaded && wineries.isLoaded) ? (
    <div>
      <div className="h-screen bg-black/90 flex">
        <div className="w-1/2 mb-4 ml-2 mr-2 shadow-lg " >
          <div style={{ width: "100%", height: "100vh" }} >
            <GoogleMap
              mapContainerStyle={containerStyle}
              center={center}
              styles="hide"
              zoom={6}
              onLoad={onLoad}
              onUnmount={onUnmount}
            >
              {wineries.items.map(winery => (
                <Marker
                key={winery.id}
                icon={{
                  url: iconChange(winery),
                  scaleSize: new window.google.maps.Size(25, 25)
                }}
                onMouseOver={() => {
                  setIcon(winery)
                  setInfoWindow(winery)
                  setWines([])
                }}
                position={{
                  lat: winery.latitude,
                  lng: winery.longitude
                }}
                />
                )
                )}
              {infoWindow ?
                <InfoWindow
                key={infoWindow.id}
                position={{
                  lat: infoWindow.latitude + 0.01,
                  lng: infoWindow.longitude
                }}
                onCloseClick={() => {
                  setWines([])
                  setInfoWindow(null)}}
                >
                  <div>
                    <img 
                      className="w-15 h-12 mb-2"
                      src={infoWindow.photo_url}
                      style={{ width: '100px', height: '100px' }}
                      alt="winery"
                    />
                    <button
                      className="text-sm mb-3 underline"
                      style={{ fontFamily: "coustard" }}
                      onClick={() => {
                        axiosInstance.get(
                          '/wineries/' + infoWindow.id + '/wines'
                        ).then(
                          response => {
                            setWines(response.data.wines)
                          }
                        )
                      }}
                    >{infoWindow.name}</button>
                    <p
                      className="text-sm"
                      style={{ fontFamily: 'Gentium Basic' }}
                    >{infoWindow.region}</p>
                  </div>
                </InfoWindow>
                : null}
            </GoogleMap>
          </div>
        </div>
        {wines.length > 0 ?
          <div className='w-1/2 flex-1 overflow-y-scroll' >
            <Wines wines={wines} />
          </div>
        : null}
      </div>
    </div>
  ) : <></>
}

export default React.memo(MyComponent)