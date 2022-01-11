import React from 'react';
import '../../../App.css';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { serverPath } from '../../../app-constants';

async function sigUpUser(credentials: any) {
    //Simple POST request with a JSON body using fetch
    let token:string = "no_token";
    let my_admin_name:string = "no_name";
  
    const requestOptions1 = {
  
      method: 'POST',
      body: JSON.stringify(credentials)
    };
      try {
        var response = await fetch(`${serverPath}/register_admin`,requestOptions1);
        var response_json = await response.json();
        console.log(response_json);
        if (response_json.hasOwnProperty('token')) {
          token = response_json['token'];
          my_admin_name = response_json['admin_name'];
          console.log(response_json['token']);
      }
      else {
          alert(response_json['error']);
          token="error";
      }
        
    } catch (e) {
        token="error";
      console.log('error connection');
      alert('Connection Error - Please check your internet connection');
        //console.error(e);
    }
    return {token, my_admin_name}
  }


const theme = createTheme();

export interface AddAdminProps {
    setToken(newToken: string): void;
  }
  
  export const AddAdmin: React.FC<AddAdminProps> = ({
    setToken,
  }) => {   
    localStorage.setItem('pageUnAuth', '1');
    const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        let admin_name: FormDataEntryValue | null = data.get('username');
        let password: FormDataEntryValue | null = data.get('password');
        if (admin_name === "" || password === "") {
          alert('credintials can\'t be empty');
          return;
        }
        //reister user
        const {token, my_admin_name} = await sigUpUser({
          admin_name: admin_name,
          password: password
        });
        
        if(token==="error"){
            return;
        }
        else {
            alert('You have been registered, redirect to Home');
            localStorage.setItem('admin_name', my_admin_name);
            setToken(token);
            
        }
      };
    return (       
        <ThemeProvider theme={theme}>
            <h1> Sign Up </h1> 
            <Container component="main" maxWidth="xs">
                <Typography component="h1" variant="h6">
                    Insert a uniqe username and a password for registration
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
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="username"
                            label="Username"
                            name="username"
                            autoComplete="username"
                            autoFocus
                        />
                        <TextField
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
                            Sign Up
                        </Button>
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    )
}