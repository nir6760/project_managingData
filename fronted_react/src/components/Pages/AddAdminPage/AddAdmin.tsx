import React from 'react';
import '../../../App.css';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import { serverPath, base64, utf8} from '../../../app-constants';
import useToken from '../../../useToken';



async function sigUpUser(credentials: any) {
    //Simple POST request with a JSON body using fetch
    let new_token:string = "no_token";
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
          new_token = response_json['token'];
          my_admin_name = response_json['admin_name'];
          console.log(response_json['token']);
      }
      else {
          alert(response_json['error']);
          new_token="error";
      }
        
    } catch (e) {
      new_token="error";
      console.log('error connection');
      alert('Connection Error - Please check your internet connection');
        //console.error(e);
    }
    return {new_token, my_admin_name}
  }


const theme = createTheme();


  
  export const AddAdmin  = () => {   
    const { token, setToken } = useToken();
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
        const {new_token, my_admin_name} = await sigUpUser({
          admin_name: admin_name,
          password: base64.encode(utf8.encode(password)),
          token: base64.encode(utf8.encode(token))
        });
        
        if(new_token==="error"){
            return;
        }
        else {
            alert('Admin has been added to system');
            // localStorage.setItem('admin_name', my_admin_name);
            // setToken(token);
            
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