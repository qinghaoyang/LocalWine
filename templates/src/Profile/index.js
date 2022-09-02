import React from 'react';
import { useAuth0 } from '@auth0/auth0-react';

const Profile = () => {
  const { user } = useAuth0();
  const { name, picture, email } = user;

  return (
    <div>
      <div className="row align-items-center profile-header">
        <img className="mx-auto" src={picture} alt="Profile" />
        <div className="col-md text-center text-md-left">
          <h2>Name: {name}</h2>
          <p className="lead text-muted">Email: {email}</p>
        </div>
      </div>
    </div>
  );
};

export default Profile;