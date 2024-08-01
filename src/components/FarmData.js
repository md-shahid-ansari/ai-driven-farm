import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Section, SectionTitle, DataItem, LocationInfo, labelStyle, selectStyle, hoverEffect} from '../styles';
import CropList from './CropList';


const FarmData = () => {
    const [weatherData, setWeatherData] = useState({});
    const [recommended_crops, setRecommended_crops] = useState([]);
    const [seasonal_crops, setSeasonal_crops] = useState([]);
    const [location, setLocation] = useState({ lat: null, lon: null });
    const [soilType, setSoilType] = useState('');
    const [error, setError] = useState('');

    useEffect(() => {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                setLocation({ lat: latitude, lon: longitude });

                // Fetch weather data
                axios.get(`http://aidrivenfarm.pythonanywhere.com/weather?lat=${latitude}&lon=${longitude}`)
                    .then(response => setWeatherData(response.data))
                    .catch(error => {
                        setError('Error fetching weather data');
                        console.error('Error fetching weather data:', error);
                    });
            },
            (err) => {
                setError('Error retrieving location');
                console.error('Error retrieving location:', err);
            }
        );
    }, []);

    const handleSoilTypeChange = (event) => {
        setSoilType(event.target.value);
        fetchSeasonalCrops(event.target.value)
        fetchRecommendations(event.target.value);
    };

    const fetchRecommendations = (soil_type) => {
        axios.get(`http://aidrivenfarm.pythonanywhere.com/recommended_crops?temp=${weatherData.main?.temp}&humidity=${weatherData.main?.humidity}&soil_type=${soil_type}`)
            .then(response => {
                setRecommended_crops(response.data);
                // console.log(response.data);
            })
            .catch(error => console.error('Error fetching recommendation:', error));
    };

    const fetchSeasonalCrops = (soil_type) => {
        axios.get(`http://aidrivenfarm.pythonanywhere.com/seasonal_crops?lat=${location.lat}&lon=${location.lon}&soil_type=${soil_type}`)
            .then(response => {
                setSeasonal_crops(response.data);
                // console.log(response.data);
            })
            .catch(error => console.error('Error fetching recommendation:', error));
    };

    return (
        <Section>
            <SectionTitle>Farm Data</SectionTitle>
            {error ? <p>{error}</p> : (
                <>
                    <LocationInfo>
                        <h3>Current Location</h3>
                        <p><strong>Latitude: {location.lat}</strong></p>
                        <p><strong>Longitude: {location.lon}</strong></p>
                        <br></br>
                        <p><strong>Temperature: {weatherData.main?.temp}°C</strong></p>
                        <p><strong>Humidity: {weatherData.main?.humidity}%</strong></p>
                        <p><strong>Weather Condition: {weatherData.weather?.[0]?.description}</strong></p>
                    </LocationInfo>
                    <Section>
                        <label htmlFor="soilType" style={labelStyle}>
                            Select Soil Type 
                        </label>
                        <select
                            id="soilType"
                            value={soilType}
                            onChange={handleSoilTypeChange}
                            style={selectStyle}
                            onMouseOver={(e) => e.target.style.borderColor = hoverEffect.borderColor}
                            onMouseOut={(e) => e.target.style.borderColor = '#ccc'}
                        >
                            <option value="Clay">Clay</option>
                            <option value="Loamy">Loamy</option>
                            <option value="Alluvial">Alluvial</option>
                            <option value="Humus">Humus</option>
                            <option value="Mucky">Mucky</option>
                            <option value="Sandy Loam">Sandy Loam</option>
                        </select>
                    </Section>
                    <DataItem>
                        <SectionTitle>Recommended Crops & Plants</SectionTitle>
                        <CropList recommended_crops={recommended_crops}/>
                    </DataItem>
                    <DataItem>
                        <SectionTitle>Seasonal Crops & Plants</SectionTitle>
                        <CropList recommended_crops={seasonal_crops}/>
                    </DataItem>
                </>
            )}
        </Section>
    );
};

export default FarmData;