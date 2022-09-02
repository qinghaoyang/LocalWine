import React from "react"
import { useAuth0 } from "@auth0/auth0-react";

const LogoutButton = () => {
  const { logout } = useAuth0();

  return (
    <button
      className="px-3 text-lg hover:text-gray-800"
      onClick={() => logout({ returnTo: window.location.origin })}>
      Sign Out
    </button>
  );
};

export default LogoutButton;