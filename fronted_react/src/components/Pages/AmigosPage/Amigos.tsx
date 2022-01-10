import axios, { Axios, AxiosResponse } from 'axios';
import React from 'react';
import '../../../App.css';
import { Character } from '../../../types';
import { CharacterCard } from './CharacterCard';

export interface AmigosPageProps {
    characters: Character[];
    setCharacters: React.Dispatch<React.SetStateAction<Character[]>>;
}

export const AmigosPage: React.FC<AmigosPageProps> = ({
    characters,
    setCharacters,
}) => {

    const [currentInput, setCurrentInput] = React.useState<string>('');

    const addCharacter = () => {
        if (currentInput === '') {
            alert('יא שובב, לא הכנסת דמות!');
            return;
            // Can you think about other validations? duplications? security issues?
        }
        const newCharacter: Character = {
            name: currentInput,
        }
        // Check this out: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Destructuring_assignment
        const newCharactersList = [...characters, newCharacter];
        setCharacters(newCharactersList);
    }

    const addRandomCharacter = async () => {
        const randomNumber = Math.floor(Math.random() * 270);
        let newCharacterFromApi;
        try {
            newCharacterFromApi = await fetch(`https://rickandmortyapi.com/api/character/${randomNumber}`);
            newCharacterFromApi = await newCharacterFromApi.json();


        } catch (e) {
            console.error(e);
        }




        if (newCharacterFromApi && newCharacterFromApi?.name !== '') {
            const newCharacter: Character = {
                name: newCharacterFromApi.name,
                image: newCharacterFromApi.image,
            }
            const newCharactersList = [...characters, newCharacter];
            setCharacters(newCharactersList);
        }
    }
    function function_example(res: AxiosResponse<any, any>) {
        // What is the problem with this approach? Read about debouncing.
        console.log('exmple func');
        return null;
    }

    const examplePostRequest = async () => {
        var body = {
            chat_id: 'testName2',
            user_name: 'testLastName'
        };
        // axios.get('http://127.0.0.1:5000/')
        //     .then(function (response) {
        //         console.log(response);
        //     })
        //     .catch(function (error) {
        //         console.log('no respone - get');
        //         console.log(error);
        //     });

        axios.post('http://127.0.0.1:5000/register_user', body)
          .then(function (response) {
            console.log(response);
          })
          .catch(function (error) {
            console.log(error);
          });

        // Simple POST request with a JSON body using fetch
        // const requestOptions = {
            
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify(body)
        // };
        // fetch('http://127.0.0.1:5000/register_user', requestOptions)
        //     .then(response => console.log(response))
        //     .catch(response =>console.log('error in post'));
    
    }

    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        // What is the problem with this approach? Read about debouncing.
        e.preventDefault();
        setCurrentInput(e.target.value); // Hint <- this is the problem. think about state and re-rendering.
    }

    return (
        <>
            <h2> Amigos Page </h2>
            <div className='page-container'>
                <input onChange={handleInputChange} />
                <button className='add-remove-button' onClick={addCharacter}> + </button>
                <button className='add-remove-button' onClick={addRandomCharacter}> Random </button>
                <button className='add-remove-button' onClick={examplePostRequest}> register test </button>
            </div>
            <div className='cards-container'>
                {characters.length > 0 ?
                    characters.map(character =>
                        <CharacterCard key={Math.random()} character={character} />) :

                    <h2> Hi! No Character yet! </h2>
                }
            </div>
        </>
    );
}