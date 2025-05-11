import styled from 'styled-components';

export const Container = styled.div`
  font-family: 'Poppins', sans-serif;
  background: #000;
  color: #e0f2f1;
  padding: 30px;
  max-width: 100%;
  margin: 0 auto;

`;

export const HeaderContainer = styled.header`
  background: linear-gradient(135deg, #2e7d32, #1b5e20);
  padding: 15px;
  text-align: left;
  color: #fff;
  border-radius: 12px;
  margin-bottom: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: flex-start;

`;

export const Title = styled.h1`
  margin: 0;
  font-size: 3em;
  font-weight: 900;
  letter-spacing: 2px;
  color: #ffffff; /* changed */
  text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.2);

`;

export const Section = styled.section`
  background: #121212;
  padding: 25px 30px;
  margin-bottom: 25px;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0, 255, 0, 0.1);
  transition: all 0.3s ease;

  &:hover {
    transform: translateY(-4px);
  }

`;

export const SectionTitle = styled.h2`
  margin-top: 0;
  color: #ffffff; /* changed */
  font-size: 1.8em;
  font-weight: 600;
  text-shadow: 1px 1px 3px rgba(255, 255, 255, 0.15);

`;

export const DataItem = styled.div`
  margin-bottom: 12px;
  font-size: 1.05em;
  line-height: 1.6;
  color: #e0f2f1;

`;

export const ListItem = styled.li`
  list-style-type: none;
  padding: 12px 15px;
  background: #003300;
  margin-bottom: 8px;
  border-radius: 8px;
  font-weight: 500;
  transition: background-color 0.3s;
  color: #ffffff; /* changed */

  &:hover {
    background-color: #004d00;
  }
`;

export const LocationInfo = styled.div`
  margin-bottom: 30px;
  padding: 28px;
  background: #001a00;
  border-radius: 14px;
  border: 1px solid #2e7d32;
  box-shadow: 0 4px 12px rgba(0, 255, 0, 0.1);
  font-family: 'Poppins', sans-serif;

  h3 {
    margin: 0 0 14px 0;
    color: #ffffff; /* changed */
    font-size: 1.75em;
    font-weight: 700;
    letter-spacing: 0.5px;
    text-shadow: 1px 1px 2px rgba(255, 255, 255, 0.2);
  }

  p {
    margin: 8px 0;
    color: #d0fdd1;
    font-size: 1em;
    font-weight: 400;
    line-height: 1.1;
    letter-spacing: 0.3px;
  }

`;

export const labelStyle = {
  fontSize: '16px',
  fontWeight: '600',
  marginBottom: '6px',
  color: '#76ff03',
};

export const divStyle = {
  border: '1px solid #4caf50',
  borderRadius: '12px',
  padding: '25px',
  margin: '15px',
  width: '320px',
  boxShadow: '0px 6px 12px rgba(0, 255, 0, 0.1)',
  backgroundColor: '#000',
  color: '#e0f2f1',
  transition: 'transform 0.2s ease-in-out',
};

export const selectStyle = {
  padding: '10px 14px',
  fontSize: '16px',
  borderRadius: '6px',
  border: '1px solid #4caf50',
  backgroundColor: '#000',
  color: '#76ff03',
  cursor: 'pointer',
  outline: 'none',
  transition: 'border-color 0.3s ease',
  marginLeft: '10px',
};

export const hoverEffect = {
  borderColor: '#76ff03',
};                       




