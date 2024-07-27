import React from 'react';
import Header from './components/Header';
import FarmData from './components/FarmData';
import Recommendations from './components/Recommendations';
import { Container } from './styles';

const App = () => {
    return (
        <Container>
            <Header />
            <FarmData />
            <Recommendations />
        </Container>
    );
};

export default App;
