import React from 'react';
import './App.css';
import { Header } from './components/AppHeader/Header';
import { PageLayout } from './components/Pages/PageLayout';
import { Character } from './types';

function App() {

  const [characters, setCharacters] = React.useState<Character[]>([]);
  const [page, setPage] = React.useState<number>(3);

  const changePage = (newPage: number) => {
    setPage(newPage);
    // Think about validations...    
  }

   return (
     <div className="root">
        {page === 7 ? (
          <img src={require('./components/AppHeader/logo.png')} />
        ) : (
          <Header changePage={changePage}/>
        )}
        <PageLayout changePage={changePage} page={page} characters={characters} setCharacters={setCharacters} />
     </div>
   );
}

export default App;
