import React from 'react';
import '../../../App.css';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { styled } from '@mui/styles';

const theme = createTheme();

const MyTextField = styled(TextField)({
  background: 'linear-gradient(45deg, #b3e5fc 10%, white 100%)',
});

export const AddAdmin = () => {
    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        console.log({
          Username: data.get('username'),
          Password: data.get('password')
        });
        //register
        //check if not exist
        //check valid input etc.
      };
    return (       
        <ThemeProvider theme={theme}>
            <h1> Add Admin </h1> 
            <Container component="main" maxWidth="xs">
                <Typography component="h1" variant="h6">
                    Insert the username and the password of the new admin
                </Typography>
                <Box
                    sx={{
                        marginTop: 1,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                >
                    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                        <MyTextField
                            margin="normal"
                            required
                            fullWidth
                            id="username"
                            label="Username"
                            name="username"
                            autoComplete="username"
                            autoFocus
                        />
                        <MyTextField
                            margin="normal"
                            required
                            fullWidth
                            name="password"
                            label="Password"
                            type="password"
                            id="password"
                            autoComplete="current-password"
                        />
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 3, mb: 2 }}
                        >
                            Add Admin
                        </Button>
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    )
}