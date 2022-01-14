import React from 'react';
import { pages, pagesUnAuth } from '../../app-constants';
import '../../App.css';

export interface NavbarProps {
    setToken(newToken: string): void;
    changePage(newPage: number): void;
}
export const Navbar: React.FC<NavbarProps> = ({
    setToken,
    changePage,
}) => {
    
    const handlePageChange = (page: string) => {
        // Think about a better way to do that:
        switch(page) {
            case 'Home':
                changePage(3);
                break;
            case 'New Poll':
                changePage(4);
                break;
            case 'Polls Results':
                changePage(5);
                break;
            case 'Add Admin':
                changePage(6);
                break;
            case 'FAQ':
                changePage(7);
                break;
            case 'About':
                changePage(8);
                break;
            case 'Sign Out':
                setToken("no_token");
                changePage(3);
                break;
            default:
                break;
        }    
    }

    return (
        <div className='nav-tab'>
            {pages.map(page => 
                <button key={page} className='nav-button' onClick={() => handlePageChange(page)}>
                    {page}
                </button>)}
            <button key={'Sign Out'} className='nav-sign-out-button' onClick={() => handlePageChange('Sign Out')}>
                {'Sign Out'}
            </button>
        </div>
    )
}


export interface NavbarUnAuthProps {
    setToken(newToken: string): void;
    changePageUnAuth(newPage: number): void;
}
export const NavbarUnAuth: React.FC<NavbarUnAuthProps> = ({
    setToken,
    changePageUnAuth,
}) => {
    
    const handlePageChange = (page: string) => {
        // Think about a better way to do that:
        console.log(page);
        switch(page) {
            case 'Sign In':
                changePageUnAuth(0);
                break;
            // case 'Sign Up':
            //     console.log('sign up pressed');
            //     changePageUnAuth(1);
            //     break;
            default:
                break;
        }    
    }

    return (
        <div className='nav-tab'>
            {pagesUnAuth.map(page => 
                <button key={page} className='nav-button' onClick={() => handlePageChange(page)}>
                    {page}
                </button>)}
        </div>
    )
}