import styled from 'styled-components';

export const Container = styled.div`
    font-family: 'Arial', sans-serif;
    background: #f4f4f9;
    color: #333;
    padding: 20px;
    max-width: 100%;
    margin: 0 auto;

    @media (max-width: 768px) {
        padding: 10px;
    }
`;

export const HeaderContainer = styled.header`
    background: #4CAF50;
    padding: 20px;
    text-align: center;
    color: white;
    border-radius: 8px;
    margin-bottom: 20px;

    @media (max-width: 768px) {
        padding: 10px;
    }
`;

export const Title = styled.h1`
    margin: 0;

    @media (max-width: 768px) {
        font-size: 1.5em;
    }
`;

export const Section = styled.section`
    background: white;
    padding: 20px;
    margin-bottom: 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);

    @media (max-width: 768px) {
        padding: 10px;
    }
`;

export const SectionTitle = styled.h2`
    margin-top: 0;
    color: #4CAF50;

    @media (max-width: 768px) {
        font-size: 1.2em;
    }
`;

export const DataItem = styled.div`
    margin-bottom: 10px;

    @media (max-width: 768px) {
        font-size: 0.9em;
    }
`;

export const ListItem = styled.li`
    list-style-type: none;
    padding: 10px;
    background: #e3f2fd;
    margin-bottom: 5px;
    border-radius: 5px;

    @media (max-width: 768px) {
        padding: 5px;
    }
`;

export const LocationInfo = styled.div`
    margin-bottom: 20px;
    padding: 15px;
    background: #e8f5e9;
    border-radius: 8px;
    border: 1px solid #c8e6c9;

    h3 {
        margin: 0;
        color: #388e3c;
    }

    p {
        margin: 5px 0;
    }
`;

export const labelStyle = {
    fontSize: '16px',
    fontWeight: 'bold',
    marginBottom: '5px',
    color: '#333',
};

export const divStyle = {
    border: '1px solid #ccc', 
    borderRadius: '10px',
    padding: '20px', 
    margin: '10px', 
    width: '300px', 
    boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
    backgroundColor: '#f9f9f9',
    transition: 'transform 0.05s',
};

export const selectStyle = {
    padding: '8px 12px',
    fontSize: '17px',
    borderRadius: '4px',
    border: '1px solid #ccc',
    backgroundColor: '#f9f9f9',
    color: '#333',
    cursor: 'pointer',
    outline: 'none',
    transition: 'border-color 0.3s ease',
    marginLeft: '10px'
};

export const hoverEffect = {
    borderColor: '#007bff',
};
