import React from 'react';
import '../../App.css';
import { About } from './AboutPage/About';
import { AddAdmin } from './AddAdminPage/AddAdmin';
import { AdminList } from './AdminList/AdminList';
import { FAQ } from './FAQPage/FAQ';
import { Home } from './HomePage/Home';
import { NewPoll } from './NewPollPage/NewPoll';
import { PollsResults } from './PollsResultsPage/PollsResults';
import { SignIn } from './UnAuth/SignIn';



export interface PageLayoutProps {
    page: number;
    changePage(newPage: number): void;
}
export const PageLayout: React.FC<PageLayoutProps> = ({
    page,
    changePage,
}) => {

    switch(page) {   
        // case 1:
        //     return <About />
        // case 2:
        //     return <FAQ />
        case 3:
            return <Home changePage={changePage}/>
        case 4:
            return <NewPoll />
        case 5:
            return <PollsResults />
        case 6:
            return <AddAdmin/>
        case 7:
            return <FAQ/>
        case 8:
            return <About/>
        case 9:
            return <AdminList changePage={changePage}/>
        default:
            return <Home changePage={changePage}/>;            
    }
}



export interface PageLayoutUnAuthProps {
    pageUnAuth: number;
    setToken(newToken: string): void;
    changePage(newPage: number): void;
}
export const PageLayoutUnAuth: React.FC<PageLayoutUnAuthProps> = ({
    pageUnAuth,
    setToken,
    changePage,
}) => {
    switch(pageUnAuth) {
        case 0:
            return <SignIn setToken={setToken} changePage={changePage}/>           
        default:
            return <SignIn setToken={setToken} changePage={changePage}/>;            
    }
}