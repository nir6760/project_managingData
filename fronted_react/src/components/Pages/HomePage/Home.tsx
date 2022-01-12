import React from 'react';
import '../../../App.css';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme();

export const Home = () => {
    return (  
        <ThemeProvider theme={theme}>
            <h1> Home </h1> 
                <Typography component="h1" variant="h6">
                    Hello, <b>*ADMIN's NAME*</b>,
                    <br />
                    Welcome to the POLLSBOT Admins Interface!
                    <br />
                    Enjoy 😄
                </Typography>
        </ThemeProvider>
    )
}