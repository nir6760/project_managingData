export type FaqContent = {
    question: string;
    answer: string;
}

export const faqContent: FaqContent[] = [
    {
        question: 'Where to start?',
        answer: 'Go to New Poll page, add a poll and just send it, easy peasy.',
    },
    {
        question: 'What is the meaning of poll?',
        answer: 'On this site poll is a question with multiple answers.',
    },
    {
        question: 'Are there any restriction on poll?',
        answer: 'Yes, poll must be a question with at least 2 answers, and each answer should be uniqe.',
    },
    {
        question: 'Where I can view the poll results?',
        answer: 'Go to Polls Results page, select your poll and watch the results, note that you should send some poll first - q1',
    },
    {
        question: 'Can I view other admins polls results, and they can view mine!?',
        answer: 'No, due to privacy each admin can view and filter by only the polls he or she owns',
    },
    {
        question: 'But Who are on the mailing list?',
        answer: 'Every user that is register for PollsBot channel on Telegram is on your mailing list.',
    },
    {
        question: 'And if I want to filter my mailing list by previous answers on my polls?',
        answer: 'Great question, you can filter by that when you are creating the poll just before sending it.',
    },
    {
        question: `Are there any restrictions regarding registering other admins to this service?`,
        answer: 'Well only an admin can register an admin (so you can 🤓), each admin should have a uniqe name.',
    },
    {
        question: `What is Cors Policy and why Chrom might block requests from the server?`,
        answer: 'Honestly, we didn\'t fully understand and it seems like no one on the web did. You can try install some chrom extension - Allow CORS: Access-Control-Allow-Origin',
    },
    {
        question: `OK, Great Work I am having so much fun`,
        answer: 'Thanks, You welcome :)',
    }
]
    
