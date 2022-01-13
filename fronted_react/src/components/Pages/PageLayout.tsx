import React from 'react';
import '../../App.css';
import { Character } from '../../types';
import { About } from './AboutPage/About';
import { AmigosPage } from './AmigosPage/Amigos';
import { FAQ } from './FAQPage/FAQ';
import { Home } from './HomePage/Home';
import { NewPoll } from './NewPollPage/NewPoll';
import { PollsResults } from './PollsResultsPage/PollsResults';
import { AddAdmin } from './AddAdminPage/AddAdmin';
import { SignIn } from './UnAuth/SignIn';

export interface PageLayoutProps {
    page: number;
    characters: Character[];
    setCharacters: React.Dispatch<React.SetStateAction<Character[]>>;
}
export const PageLayout: React.FC<PageLayoutProps> = ({
    page,
    characters,
    setCharacters,
}) => {

    switch(page) {
        case 0:
            return <AmigosPage characters={characters} setCharacters={setCharacters} />            
        case 1:
            return <About />
        case 2:
            return <FAQ />
        case 3:
            return <Home />
        case 4:
            return <NewPoll />
        case 5:
            return <PollsResults />
        case 6:
            return <AddAdmin/>
        default:
            return <Home />;            
    }
}



export interface PageLayoutUnAuthProps {
    pageUnAuth: number;
    setToken(newToken: string): void;
}
export const PageLayoutUnAuth: React.FC<PageLayoutUnAuthProps> = ({
    pageUnAuth,
    setToken,
}) => {
    switch(pageUnAuth) {
        case 0:
            return <SignIn setToken={setToken}/>           
        default:
            return <SignIn setToken={setToken}/>;            
    }
}