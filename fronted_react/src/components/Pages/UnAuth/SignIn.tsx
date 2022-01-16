import LockOutlinedIcon from '@mui/icons-material/LockOutlined';
import Avatar from '@mui/material/Avatar';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import * as React from 'react';
import { extract64ForRecive, wrap64ForSend } from '../../../app-constants';
import { serverPath } from '../../../config';

async function loginUser(credentials: any) {
  //   try {
  //     axios.post(`${serverPath}/register_admin`, credentials)
  //       .then(function (response) {
  //         console.log(response);
  //       })
  //       .catch(function (error) {
  //         console.log("what is");
  //         console.log(error);
  //       });
  //   }
  //   catch (e) {
  //     console.log(e);
  //   }

  //Simple POST request with a JSON body using fetch
  let token: string = "no_token";
  let my_admin_name: string = "no_name";
  let connection: boolean = true;

  const requestOptions1 = {

    method: 'POST',
    body: JSON.stringify(credentials)
  };
  try {
    var response = await fetch(`${serverPath}/login_admin`, requestOptions1);
    var response_json = await response.json();
    if (!response_json.hasOwnProperty("token")) {
      return { connection, token, my_admin_name }
    }
    token = response_json['token'];
    token = extract64ForRecive(token)
    my_admin_name = extract64ForRecive(response_json['admin_name']);
  } catch (e) {
    console.log(e);
    connection = false;
    console.error('connection error ');
    alert('Connection Error - Please check your internet connection');
    //console.error(e);
  }

  return { connection, token, my_admin_name }
}

const theme = createTheme();

export interface SignInProps {
  setToken(newToken: string): void;
}

export const SignIn: React.FC<SignInProps> = ({
  setToken,
}) => {

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    let admin_name: FormDataEntryValue | null = data.get('admin_name');
    let password: FormDataEntryValue | null = data.get('password');
    if (admin_name === "" || password === "") {
      alert('credintials can\'t be empty');
      return;
    }
    //login user
    const { connection, token, my_admin_name } = await loginUser({
      admin_name: admin_name,
      password: wrap64ForSend(password !== null ? password.toString() : "no_pass")
    });
    if (connection === false) {
      return;
    }

    if (token && token !== "no_token") {
      localStorage.setItem('admin_name', my_admin_name);
      localStorage.setItem('pageAuth', '3');
      //console.log(token);
      setToken(token);
    }
    else {
      alert('The username or password are incorrect');
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <Box
          sx={{
            marginTop: 1,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Avatar sx={{ m: 1, bgcolor: 'primary.main' }}>
            <LockOutlinedIcon />
          </Avatar>
          <Typography component="h1" variant="h5">
            Sign In
          </Typography>
          <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="admin_name"
              label="user name"
              name="admin_name"
              autoComplete="admin_name"
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
              Sign In
            </Button>
          </Box>

        </Box>
      </Container>
    </ThemeProvider>
  );
}