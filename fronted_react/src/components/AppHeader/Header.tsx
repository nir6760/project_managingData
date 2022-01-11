import React from 'react';
import '../../App.css';
import { Navbar, NavbarUnAuth } from './Navbar';

const getAdminName = () => {
    const adminNameString = localStorage.getItem('admin_name');
    //const tokenString = sessionStorage.getItem('admin_name');
    return adminNameString
    };
export interface HeaderProps {
    setToken(newToken: string): void;
    changePage(newPage: number): void;
}
export const Header: React.FC<HeaderProps> = ({
    changePage,
    setToken,
}) => {
const adminName = getAdminName();
    return (
        <>
        <div className='welcome-container'><h2>Hello {adminName}</h2></div>
        <div className='header-container'>
            <img src={require('./logo.png')} alt="logo" />
            
            <Navbar setToken={setToken} changePage={changePage} />
            
        </div>
        </>
    )
}



export interface HeaderUnAuthProps {
    setToken(newToken: string): void;
    changePageUnAuth(newPage: number): void;
}
export const HeaderUnAuth: React.FC<HeaderUnAuthProps> = ({
    setToken,
    changePageUnAuth,

}) => {
const adminName = getAdminName();
    return (
        <>
        <div className='header-container'>
            <img src={require('./logo.png')} alt="logo" />
            <NavbarUnAuth setToken={setToken} changePageUnAuth={changePageUnAuth} />
            
        </div>
        </>
    )
}