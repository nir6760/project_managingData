import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import { styled } from '@mui/styles';
import React from 'react';
import {wrap64ForSend } from '../../../app-constants';
import { serverPath } from '../../../config';
import '../../../App.css';
import useToken from '../../../useToken';


async function signUpUser(credentials: any) {
  //Simple POST request with a JSON body using fetch
  let new_token: string = "no_token";
  let my_admin_name: string = "no_name";

  const requestOptions1 = {

    method: 'POST',
    body: JSON.stringify(credentials)
  };
  try {
    var response = await fetch(`${serverPath}/register_admin`, requestOptions1);
    var response_json = await response.json();
    //console.log(response_json);
    if (response_json.hasOwnProperty('token')) {
      new_token = response_json['token'];
      my_admin_name = response_json['admin_name'];
      //console.log(response_json['token']);
    }
    else {
      alert(response_json['error']);
      new_token = "error";
    }

  } catch (e) {
    new_token = "error";
    console.error('connection error ');
    alert('Connection Error - Please check your internet connection');
    //console.error(e);
  }
  return { new_token, my_admin_name }
}


const theme = createTheme();


const MyTextField = styled(TextField)({
  background: 'linear-gradient(45deg, #b3e5fc 10%, white 100%)',
});
export const AddAdmin = () => {
  localStorage.setItem('pageAuth', '6');
  const [search, setSearch] = React.useState('');
  const { token, setToken } = useToken();
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
    const { new_token, my_admin_name } = await signUpUser({
      admin_name: admin_name,
      password: wrap64ForSend(password !== null ? password.toString() : "no_pass"),
      token: wrap64ForSend(token)
    });

    if (new_token === "error") {
      return;
    }
    else {
      alert('Admin has been added to system');
      // localStorage.setItem('admin_name', my_admin_name);
      // setToken(token);

    }
  };

  // const handleSearch = (event: { target: { value: React.SetStateAction<string>; }; }) => {
  //   setSearch(event.target.value);
  // };

  // const data = {
  //   nodes: nodes.filter((item: { name: string | string[]; }) =>
  //     item.name.includes(search);
  //   ),
  // };

  return (
    <ThemeProvider theme={theme}>
      <h1> Register a new admin </h1>
      <Container component="main" maxWidth="xs">
        <Typography component="h1" variant="h6">
          Insert a unique username and a password for registration
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
              Sign him Up
            </Button>
          </Box>
        </Box>

        {/* <label htmlFor="search">
          Search by Task:
          <input id="search" type="text" onChange={handleSearch} />
        </label>

        <Table data={data}>
          ...
        </Table> */}

      </Container>
    </ThemeProvider>
  )
}