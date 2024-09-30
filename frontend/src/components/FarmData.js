import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Section, SectionTitle, DataItem, LocationInfo, labelStyle, selectStyle, hoverEffect} from '../styles';
import CropList from './CropList';

// const URL = "https://aidrivenfarm.pythonanywhere.com";
const URL = "http://localhost:5000";

const FarmData = () => {
    const [recommended_crops, setRecommended_crops] = useState([]);
    const [seasonal_crops, setSeasonal_crops] = useState([]);
    const [location, setLocation] = useState({ lat: null, lon: null });
    const [soilType, setSoilType] = useState('');
    const [errorLoc, setErrorLoc] = useState('');
    const [zones, setZones] = useState([]);
    const [currentZone, setCurrentZone] = useState('');

    useEffect(() => {
        navigator.geolocation.getCurrentPosition(
            (position) => {
                const { latitude, longitude } = position.coords;
                setLocation({ lat: latitude, lon: longitude });
            },
            (err) => {
                setErrorLoc('Error retrieving location');
                console.error('Error retrieving location:', err);
            }
        );
        const fetchZones = () => {
            axios.get(`${URL}/zones`)
                .then(response => {
                    setZones(response.data);
                    // console.log(response.data);
                })
                .catch(error => console.error('Error fetching recommendation:', error));
        };

        const fetchCurrentZone = () => {
            axios.get(`${URL}/current_zone?lat=${location.lat}&lon=${location.lon}`)
                .then(response => {
                    setCurrentZone(response.data);
                    // console.log(response.data);
                })
                .catch(error => console.error('Error fetching recommendation:', error));
        };

        fetchZones();
        fetchCurrentZone();
    });

    const handleSoilTypeChange = (event) => {
        setSoilType(event.target.value);
        fetchSeasonalCrops(event.target.value)
        fetchRecommendations(event.target.value);
    };
    const handleZoneChange = (event) => {
        setCurrentZone(event.target.value);
    };

    const fetchRecommendations = (soil_type) => {
        axios.get(`${URL}/recommended_crops?soil_type=${soil_type}`)
            .then(response => {
                setRecommended_crops(response.data);
                // console.log(response.data);
            })
            .catch(error => console.error('Error fetching recommendation:', error));
    };

    const fetchSeasonalCrops = (soil_type) => {
        axios.get(`${URL}/seasonal_crops?soil_type=${soil_type}`)
            .then(response => {
                setSeasonal_crops(response.data);
                // console.log(response.data);
            })
            .catch(error => console.error('Error fetching recommendation:', error));
    };

    return (
        <Section>
            <SectionTitle>Farm Data</SectionTitle>
            <LocationInfo>
                <h3>Current Location</h3>
                {errorLoc ? <p>{errorLoc}</p> : (
                    <>
                        <p><strong>Latitude: {location.lat}</strong></p>
                        <p><strong>Longitude: {location.lon}</strong></p>
                    </>
                )}
                <br/>
                <>
                    <label htmlFor="zone" style={labelStyle}>
                        Current zone  
                    </label>
                    <select
                        id="zone"
                        value={currentZone}
                        onChange={handleZoneChange}
                        style={selectStyle}
                        onMouseOver={(e) => e.target.style.borderColor = hoverEffect.borderColor}
                        onMouseOut={(e) => e.target.style.borderColor = '#ccc'}
                    >
                        {zones.map((element, index) => (
                            <option key={index} value={element}>
                            {element}
                            </option>
                        ))}
                    </select>
                </>
                <br/>
                <>
                    <label htmlFor="soilType" style={labelStyle}>
                        Soil
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
                </>
            </LocationInfo>
            <DataItem>
                <SectionTitle>Recommended Crops & Plants</SectionTitle>
                <CropList recommended_crops={recommended_crops}/>
            </DataItem>
            <DataItem>
                <SectionTitle>Seasonal Crops & Plants</SectionTitle>
                <CropList recommended_crops={seasonal_crops}/>
            </DataItem>
        </Section>
    );
};

export default FarmData;