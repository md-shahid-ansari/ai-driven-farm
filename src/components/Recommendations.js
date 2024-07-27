import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Section, SectionTitle, ListItem } from '../styles';

const Recommendations = () => {
    const [recommendations, setRecommendations] = useState([]);

    useEffect(() => {
        axios.get('/api/recommendations')
            .then(response => setRecommendations(response.data.recommendations))
            .catch(error => console.error('Error fetching recommendations:', error));
    }, []);

    return (
        <Section>
            <SectionTitle>Recommendations</SectionTitle>
            <ul>
                {recommendations.map((rec, index) => (
                    <ListItem key={index}>{rec}</ListItem>
                ))}
            </ul>
        </Section>
    );
};

export default Recommendations;
