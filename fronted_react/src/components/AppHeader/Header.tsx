import React from 'react';
import '../../App.css';
import { Navbar } from './Navbar';

export const getAdminName = () => {
    const adminNameString = localStorage.getItem('admin_name');
    //const tokenString = sessionStorage.getItem('admin_name');
    return adminNameString
    };
export interface HeaderProps {
    changePage(newPage: number): void;
}
export const Header: React.FC<HeaderProps> = ({
    changePage,
}) => {
const adminName = getAdminName();
    return (
        <>
        <div className='welcome-container'><h2>Welcome {adminName}</h2></div>
        <div className='header-container'>
            <img src={require('./logo.png')} alt="logo" />
            
            <Navbar changePage={changePage} />
            
        </div>
        </>
    )
}



export const HeaderUnAuth = () => {
    return (
        <>
        <div className='header-container'>
            <img src={require('./logo.png')} alt="logo" />
        </div>
        </>
    )
}