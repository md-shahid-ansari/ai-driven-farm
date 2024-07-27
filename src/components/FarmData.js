import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Section, SectionTitle, DataItem, LocationInfo } from '../styles';

const FarmData = () => {
    const [weatherData, setWeatherData] = useState({});
    const [soilData, setSoilData] = useState({});
    const [nasaData, setNasaData] = useState({});
    const [agroData, setAgroData] = useState({});
    const [location, setLocation] = useState({ lat: null, lon: null });
    const [error, setError] = useState('');

    useEffect(() => {
        // Get user's current location
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                setLocation({ lat: latitude, lon: longitude });

                // Fetch data based on location
                axios.get(`/api/weather?lat=${latitude}&lon=${longitude}`)
                    .then(response => setWeatherData(response.data))
                    .catch(error => console.error('Error fetching weather data:', error));

                axios.get(`/api/soil?lat=${latitude}&lon=${longitude}`)
                    .then(response => setSoilData(response.data))
                    .catch(error => console.error('Error fetching soil data:', error));

                axios.get(`/api/nasa?lat=${latitude}&lon=${longitude}`)
                    .then(response => setNasaData(response.data))
                    .catch(error => console.error('Error fetching NASA data:', error));

                axios.get(`/api/agro?lat=${latitude}&lon=${longitude}`)
                    .then(response => setAgroData(response.data))
                    .catch(error => console.error('Error fetching agro data:', error));
            },
            (err) => {
                setError('Error retrieving location');
                console.error('Error retrieving location:', err);
            }
        );
    }, []);

    return (
        <Section>
            <SectionTitle>Farm Data</SectionTitle>
            {error ? <p>{error}</p> : (
                <>
                    <LocationInfo>
                        <h3>Current Location</h3>
                        <p>Latitude: {location.lat}</p>
                        <p>Longitude: {location.lon}</p>
                    </LocationInfo>
                    <DataItem>
                        <h3>Weather Data</h3>
                        <p>Temperature: {weatherData.temperature}°C</p>
                        <p>Humidity: {weatherData.humidity}%</p>
                        <p>Condition: {weatherData.weather}</p>
                    </DataItem>
                    <DataItem>
                        <h3>Soil Data</h3>
                        <p>Soil Moisture: {soilData.soil_moisture}</p>
                    </DataItem>
                    <DataItem>
                        <h3>NASA Data</h3>
                        <p>Temperature: {nasaData.temperature}°C</p>
                        <p>Humidity: {nasaData.humidity}%</p>
                    </DataItem>
                    <DataItem>
                        <h3>Agro Data</h3>
                        <p>Temperature: {agroData.temperature}°C</p>
                        <p>Humidity: {agroData.humidity}%</p>
                    </DataItem>
                </>
            )}
        </Section>
    );
};

export default FarmData;
