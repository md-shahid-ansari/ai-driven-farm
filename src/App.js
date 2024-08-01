import React from 'react';
import Header from './components/Header';
import FarmData from './components/FarmData';
import { Container } from './styles';

const App = () => {
    return (
        <Container>
            <Header />
            <FarmData />
        </Container>
    );
};

export default App;
