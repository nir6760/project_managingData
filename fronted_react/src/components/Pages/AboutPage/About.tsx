import React from 'react';
import '../../../App.css';


export const About = () => {
    localStorage.setItem('pageAuth', '8');

    return (
        <div className='about-page-container'>
            {/* {aboutRandomCharacter && !fetchingData ? <CharacterCard character={aboutRandomCharacter}/> : 'Loading...'} */}
            <h1> Final project at </h1>
            <h2>Managing Data On The WWW Course - 236369</h2>
            <h2>  Thechnion Institute </h2>
            <h4> You can check the FAQ for some details about the service</h4>
            <a href='https://github.com/nir6760/project_managingData'> GitHub repo </a>
            <br>
            </br>
            <br>
            </br>
        </div>

    )
}