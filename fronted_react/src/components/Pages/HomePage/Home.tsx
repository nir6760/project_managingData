import React, { Component }  from 'react';
import '../../../App.css';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import {getAdminName} from '../../AppHeader/Header';
import Button from '@mui/material/Button';

//const adminName = getAdminName();
const theme = createTheme();

export interface HomeProps {
    changePage(newPage: number): void;
}

export const Home: React.FC<HomeProps> = ({
    changePage,
}) => {
    localStorage.setItem('pageAuth', '3');

    const handleMouseEvent = (e: any) => {
        e.preventDefault();
        console.log('click');
        changePage(9);
        // Do something
      };
    return (  
        <ThemeProvider theme={theme}>
            <h1> Home </h1> 
                <Typography component="h1" variant="h6">
                    Hello, 
                    <br />
                    Welcome to the POLLSBOT Admins Interface!
                    <br />
                    Enjoy 😄
                    <br />
                    <br />
                    <button className='nav-button' onClick={handleMouseEvent}>View the Admin List</button>
                </Typography>
        </ThemeProvider>
    )
}