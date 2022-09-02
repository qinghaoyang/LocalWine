import React from "react"
import { useState } from 'react'
import { useAuth0 } from "@auth0/auth0-react";
import LoginButton from "./Login";
import LogoutButton from "./Logout";

const Navbar = () => {
  const { user, isAuthenticated } = useAuth0();
  const [dropdown, setDropdown] = useState(false);

  return (
    <nav>
      <div className=" mx-auto px-6 flex justify-between items-center ">
        <a className="text-1xl py-2  rounded-md lg:text-3xl" href="/"
          style={{ fontFamily: "coustard" }}>
          <p className="ml-8 text-claret-800">LocalWines</p>
        </a>
        <div className="lg:block">
          <ul className="inline-flex mt-3">
            <li><a className="pl-3 pr-10 text-lg hover:text-gray-800 " href="/">Home</a></li>
            <li><a className="px-3 pr-10 text-lg hover:text-gray-800" href="/map">Map</a></li>
            <li>{isAuthenticated ?
              <div>
                <button onClick={() => setDropdown(!dropdown)}>
                  <img
                    className="h-9 rounded-full"
                    src={user.picture}
                    alt={user.name}
                    />
                </button>
                {dropdown ?
                <div className="origin-top-right absolute right-0 w-32 rounded-sm shadow-lg bg-white ">
                    <a href="/profile" className="px-3 pr-10 text-lg hover:text-gray-800">Profile</a>
                    <LogoutButton />
                </div>
                : <></>}
              </div>
              :<LoginButton />
              }</li>
          </ul>
        </div>
      </div>
    </nav>
  )
}
export default Navbar;