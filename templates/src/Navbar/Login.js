import React from "react"
import { useAuth0 } from "@auth0/auth0-react";

const LoginButton = () => {
  const { loginWithRedirect } = useAuth0();

  return (
    <button
      className="px-3 text-lg hover:text-gray-800"
      onClick={() => loginWithRedirect()}>
      Sign In
    </button>
  )
};

export default LoginButton;