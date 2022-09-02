import { Route, Routes } from 'react-router-dom';
import Map from './Map';
import Navbar from './Navbar'
import Home from './Home'
import Profile from './Profile';


function App() {
	return (
    // <div className="min-h-screen bg-slate-100">
    <div>
      <Navbar />
      <Routes>
        <Route exact path="/" element={<Home />} />
        <Route exact path="/profile" element={<Profile />} />
        <Route exact path="/map" element={<Map />} />
        <Route path="/wineries/:wineryId/wines" ></Route>
      </Routes>
    </div>
  );
}

export default App;
