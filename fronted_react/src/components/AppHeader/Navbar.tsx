import React from 'react';
import { pages, pagesUnAuth, wrap64ForSend } from '../../app-constants';
import '../../App.css';
import { serverPath } from '../../config';
import useToken from '../../useToken';


async function logoutUser(credentials: any) {

    let err_str: string = "no_err";
    let connection: boolean = true;
    let was_error: boolean = false;
    const requestOptions1 = {

        method: 'POST',
        body: JSON.stringify(credentials)
    };
    try {
        var response = await fetch(`${serverPath}/logout_admin`, requestOptions1);
        var response_json = await response.json();
        if (response_json.hasOwnProperty("message_back")) {
            return { connection, was_error }
        }
        err_str = response_json['error'];
    } catch (e) {
        console.log(e);
        connection = false;
        console.error('connection error ');
        alert('Connection Error - Please check your internet connection');
        //console.error(e);
    }

    return { connection, was_error }
}



export interface NavbarProps {
    changePage(newPage: number): void;
}
export const Navbar: React.FC<NavbarProps> = ({
    changePage,
}) => {
    const { token, setToken } = useToken();

    const handlePageChange = async (page: string) => {
        // Think about a better way to do that:
        switch (page) {
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
                //logout user
                const { connection, was_error } = await logoutUser({
                    token: wrap64ForSend(token),
                });
                if (connection === false) {
                    return;
                }
                
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
        switch (page) {
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