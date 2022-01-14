import React from 'react';
import './App.css';
import { Header, HeaderUnAuth } from './components/AppHeader/Header';
import { PageLayout, PageLayoutUnAuth } from './components/Pages/PageLayout';
import { Character } from './types';
import useToken from './useToken';


function App() {
  const pageUnAuthLocal_string = localStorage.getItem('pageUnAuth');
  var pageUnAuthInt = 0;
    if(pageUnAuthLocal_string !== null){
      pageUnAuthInt = Number(pageUnAuthLocal_string);
    }
    const pageAuthLocal_string = localStorage.getItem('pageAuth');
    var pageAuthInt = 3;
      if(pageAuthLocal_string !== null){
        pageAuthInt = Number(pageAuthLocal_string);
        console.log(`pageAuth is ${pageAuthInt}`);
      }

  const [characters, setCharacters] = React.useState<Character[]>([]);
  const [page, setPage] = React.useState<number>(pageAuthInt);
  const [pageUnAuth] = React.useState<number>(pageUnAuthInt);
  const { token, setToken } = useToken();

  const changePage = (newPage: number) => {
    setPage(newPage);
    // Think about validations...    
  }
  // const changePageUnAuth = (newPage: number) => {
  //   setPageUnAuth(newPage);
      
  
  //   localStorage.setItem('pageUnAuth', `${newPage}`);
  //   // Think about validations...    
  // }
  
  if(!token || token === "no_token") {
    return (
      
      <div className="root">
         <HeaderUnAuth/>
         <PageLayoutUnAuth pageUnAuth={pageUnAuth} setToken={setToken}/>
      </div>
    );
  }
   return (
      
     <div className="root">
        <Header setToken={setToken} changePage={changePage}/>
        <PageLayout  page={page} characters={characters} setCharacters={setCharacters} />
     </div>
   );
}

export default App;
