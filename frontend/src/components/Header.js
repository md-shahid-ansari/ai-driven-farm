import React from 'react';
import { HeaderContainer, Title } from '../styles';
import { ReactComponent as Logo } from '../assets/logo.svg'; // adjust path as needed

const Header = () => {
    return (
        <HeaderContainer>
            <Logo style={{ width: '40px', height: '40px', marginRight: '10px' }} />
            <Title>Farm.ai</Title>
        </HeaderContainer>
    );
};

export default Header;











