import React from 'react';
import { pages } from '../../app-constants';
import '../../App.css';

export interface NavbarProps {
    changePage(newPage: number): void;
}
export const Navbar: React.FC<NavbarProps> = ({
    changePage,
}) => {
    
    const handlePageChange = (page: string) => {
        // Think about a better way to do that:
        switch(page) {
            case 'Amigos':
                changePage(0);
                break;
            case 'About':
                changePage(1);
                break;
            case 'FAQ':
                changePage(2);
                break;
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
            case 'Sign Out':
                changePage(7);
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