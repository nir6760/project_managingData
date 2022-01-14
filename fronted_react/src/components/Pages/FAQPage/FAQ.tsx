import React from 'react';
import '../../../App.css';
import { faqContent } from './faq-content';

export const FAQ = () => {
    localStorage.setItem('pageAuth', '7');

    return (
        <div className='about-page-container'>
            <h2 >  FAQ  </h2>
            { faqContent.map((faq, id) => 
                <details>
                    <summary>{faq.question}</summary>
                    {faq.answer}
                </details>
            )}                        
        </div>
    )
}