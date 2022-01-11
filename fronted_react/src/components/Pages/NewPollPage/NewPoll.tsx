import React, { useState } from 'react';
import '../../../App.css';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import { createTheme, ThemeProvider } from '@mui/material/styles';
import MenuItem from '@mui/material/MenuItem';

const theme = createTheme();

export const NewPoll = () => {
    const [answersList, setAnswersList] = useState([{ answer: "" }]);

    const handleAnswersInputChange = (e: React.ChangeEvent<HTMLTextAreaElement | HTMLInputElement>, index: number) => {
        const { name, value } = e.target;
        const list = [...answersList];
        //list[index][name] = value;
        setAnswersList(list);
    };

    function handleAnswersRemoveClick(index: string) {
        const list = [...answersList];
        //list.splice(index, 1);
        setAnswersList(list);
    }

    const handleAnswersAddClick = () => {
        setAnswersList([...answersList, { answer: "" }]);
    };

    const [filterList, setFilterList] = useState([{ question: "", answer: ""}]);

    const questions = [
        {
            key: '',
            question: '',
        },
        {
            key: '0',
            question: 'How are you?',
        },
        {
            key: '1',
            question: 'How old are you?',
        },
      ];

    const [filterQuestion, setFillterQuestion] = React.useState('');

    const handleChange = (event: { target: { value: React.SetStateAction<string>; }; }) => {
        setFillterQuestion(event.target.value);
    };

    const handleFilterInputChange = (e: { target: { name: any; value: any; }; }, index: string | number) => {
        const { name, value } = e.target;
        const list = [...filterList];
        //list[index][name] = value;
        setFilterList(list);
    };

    function handleFilterRemoveClick(index: string) {
        const list = [...filterList];
        //list.splice(index, 1);
        setFilterList(list);
    }

    const handleFilterAddClick = () => {
        setFilterList([...filterList, { question: "", answer: ""}]);
    };

    const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const data = new FormData(event.currentTarget);
        // eslint-disable-next-line no-console
        console.log({
          Question: data.get('question'),
          Answer: answersList
        });
      };
    
      return (
        <ThemeProvider theme={theme}>
            <h1> New Poll </h1>
            <Container component="main" maxWidth="lg">
                <Box
                    sx={{
                        marginTop: 1,
                        marginBottom: 1,
                        display: 'flex',
                        flexDirection: 'column',
                        alignItems: 'center',
                    }}
                > 
                    <Box component="form" onSubmit={handleSubmit} noValidate sx={{ mt: 1 }}>
                        <Typography component="h5" variant="h6">
                            Add a question and possible answers
                        </Typography>
                        <TextField
                            margin="normal"
                            required
                            fullWidth
                            id="question"
                            label="Question"
                            name="question"
                            autoComplete="question"
                            autoFocus
                        />
                        {answersList.map((x, i) => {
                            return (
                            <div className="answers-box">
                                <TextField
                                    margin="normal"
                                    required
                                    fullWidth
                                    name='answer'
                                    label="Answer"
                                    type="answer"
                                    id="answer"
                                    autoComplete="current-answer"
                                    value={x.answer}
                                    onChange={e => handleAnswersInputChange(e, i)}
                                />
                                <div className="answers-box">
                                    {answersList.length !== 1 && <button className='add-remove-button' onClick={() => handleAnswersRemoveClick(i.toString())}>-</button>}
                                    {answersList.length - 1 === i && <button className='add-remove-button' onClick={handleAnswersAddClick}>+</button>}
                                </div>
                            </div>
                        );
                        })}
                        <Typography component="h5" variant="h6">
                        <br></br>
                            Filter relevant targets according to previous answers
                        </Typography>
                        {filterList.map((x, i) => {
                            return (
                            <div className="answers-box">
                                <TextField
                                    margin="normal"
                                    id="outlined-select-currency"
                                    select
                                    fullWidth
                                    label="Question"
                                    value={filterQuestion}
                                    onChange={handleChange}
                                >
                                {questions.map((option) => (
                                    <MenuItem key={option.key} value={option.key}>
                                        {option.question}
                                    </MenuItem>
                                ))}
                                </TextField>
                                <TextField
                                    margin="normal"
                                    id="outlined-select-currency"
                                    select
                                    fullWidth
                                    label="Answer"
                                    // value={filterQuestion}
                                    // onChange={handleChange}
                                />
                                <div className="answers-box">
                                    {filterList.length !== 1 && <button className='add-remove-button' onClick={() => handleFilterRemoveClick(i.toString())}>-</button>}
                                    {filterList.length - 1 === i && <button className='add-remove-button' onClick={handleFilterAddClick}>+</button>}
                                </div>
                            </div>
                        );
                        })}
                        <Button
                            type="submit"
                            fullWidth
                            variant="contained"
                            sx={{ mt: 4, mb: 2 }}
                        >
                            Submit
                        </Button>
                    </Box>
                </Box>
            </Container>
        </ThemeProvider>
    );
    }
