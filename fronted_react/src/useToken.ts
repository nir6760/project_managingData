import { useState } from 'react';

export default function useToken() {
  const getToken = () => {
    const tokenString = localStorage.getItem('token');
    //const tokenString = sessionStorage.getItem('token');
    const userToken = JSON.parse(tokenString!);
    return userToken
  };
  
  let [token, setToken] = useState(getToken());

  const saveToken = (userToken: any ) => {
    const userToken_string = JSON.stringify(userToken)
    localStorage.setItem('token', userToken_string);
    //sessionStorage.setItem('token', JSON.stringify(userToken));
    setToken(userToken_string);
    //console.log(`${userToken_string} token has been saved to session storage`);
  };
  //token = getToken();
  return {
    setToken: saveToken,
    token : getToken()
  }
}