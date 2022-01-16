import React, { useState } from 'react';
import { wrap64ForSend } from '../../../app-constants';
import { serverPath } from '../../../config';
import '../../../App.css';
import useToken from '../../../useToken';



export interface AdminListProps {
    changePage(newPage: number): void;
}

export const AdminList: React.FC<AdminListProps> = ({
    changePage,
}) => {
    localStorage.setItem('pageAuth', '9');
    const [fetchingData, setFetchingData] = React.useState(true);
    const { token, setToken } = useToken();
    // the value of the search field 
    const [name, setName] = useState('');

    // This holds a list of some fiction people
    // Some  have the same name but different age and id
    let USERS = [
        { name: 'No admin at the list' },
    ];
    interface Dict {
    }
    // the search result
    const [foundUsers, setFoundUsers] = useState(USERS);
    const [AllUsers, setAllUsers] = useState(USERS);

    const filter = (e: { target: { value: any; }; }) => {
        const keyword = e.target.value;

        if (keyword !== '') {
            const results = AllUsers.filter((user) => {
                return user.name.toLowerCase().startsWith(keyword.toLowerCase());
                // Use the toLowerCase() method to make it case-insensitive
            });
            setFoundUsers(results);
        } else {
            setFoundUsers(AllUsers);
            // If the text field is empty, show all users
        }

        setName(keyword);
    };
    const handleMouseEvent = (e: any) => {
        e.preventDefault();
        console.log('click');
        changePage(3);
        // Do something
    };

    React.useEffect(() => {
        const fetchAdminList = async (credentials: any) => {

            //Simple POST request with a JSON body using fetch
            var fetchedData;
            let connection: boolean = true;

            const requestOptions1 = {

                method: 'POST',
                body: JSON.stringify(credentials)
            };
            try {
                var response = await fetch(`${serverPath}/admins_name_list`, requestOptions1);
                var response_json = await response.json();

                if (response_json.hasOwnProperty('result_lst')) {
                    fetchedData = response_json['result_lst'];
                    console.log("inside fetchedData");
                    console.log(fetchedData);
                    setFetchingData(false);

                    setFoundUsers(fetchedData);
                    setAllUsers(fetchedData);

                    // setFetching is false here


                }
                else {
                    console.log(response_json['error']);
                }

            } catch (e) {
                connection = false;
                console.error('connection error ');
                alert('Connection Error - Please check your internet connection');
                //console.error(e);
            }
            if (connection === false) {
                return;
            }
        }
        fetchAdminList({
            token: wrap64ForSend(token)
        }).catch(console.error);
        setFetchingData(false)
    }, [])

    return (
        <div className="adminListcontainer">
            <input
                type="search"
                value={name}
                onChange={filter}
                className="input"
                placeholder="Serch for an admin name"
            />

            <div className="user-list">
                {foundUsers && foundUsers.length > 0 ? (
                    foundUsers.map((user) => (
                        <li key={user.name} className="user">
                            <span className="user-name">{user.name}</span>
                        </li>
                    ))
                ) : (
                    <h1>No results found!</h1>
                )}
            </div>
            <br />
            <br />
            <br />
            <button className='nav-button' onClick={handleMouseEvent}>Return to Home Page</button>
        </div>
    )
}

