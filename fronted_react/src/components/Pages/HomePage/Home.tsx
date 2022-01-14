import React, { Component }  from 'react';
import '../../../App.css';
import Typography from '@mui/material/Typography';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import {getAdminName} from '../../AppHeader/Header';

//const adminName = getAdminName();
const theme = createTheme();

export const Home = () => {
    localStorage.setItem('pageAuth', '3');
    return (  
        <ThemeProvider theme={theme}>
            <h1> Home </h1> 
                <Typography component="h1" variant="h6">
                    Hello, 
                    <br />
                    Welcome to the POLLSBOT Admins Interface!
                    <br />
                    Enjoy 😄
                </Typography>
        </ThemeProvider>
    )
}