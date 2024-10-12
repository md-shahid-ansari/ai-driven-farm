import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Section, SectionTitle, DataItem, LocationInfo, labelStyle, selectStyle, hoverEffect} from '../styles';
import CropList from './CropList';

// const URL = "https://aidrivenfarm.pythonanywhere.com";
const URL = "http://localhost:5000";

const FarmData = () => {
    const [crops, setCrops] = useState([]);
    const [location, setLocation] = useState({ lat: null, lon: null });
    const [soils, setSoils] = useState([]);
    const [currentSoil, setCurrentSoil] = useState('');
    const [errorLoc, setErrorLoc] = useState('');
    const [zones, setZones] = useState([]);
    const [currentZone, setCurrentZone] = useState('');
    const [loading , setLoading] = useState(false);

    useEffect(() => {
        setLoading(true)
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
                .catch(error => console.error('Error fetching zone:', error));
        };
        const fetchSoils = () => {
            axios.get(`${URL}/soils`)
                .then(response => {
                    setSoils(response.data);
                    // console.log(response.data);
                })
                .catch(error => console.error('Error fetching soil:', error));
        };

        fetchZones();
        fetchSoils();
        setLoading(false);
    },[]);

    useEffect(() => {
        setLoading(true);
        const lat = location.lat;
        const lon = location.lon;
        if( lat == null || lon == null){
            return;
        }
        const fetchCurrentZone = () => {
            axios.get(`${URL}/current_zone?lat=${location.lat}&lon=${location.lon}`)
                .then(response => {
                    const zone = zones.find(zone => zone.Name === response.data);
                    // setCurrentZone( zone ? zone.ZoneId : 6);
                    // bcoz it is only for zone 6
                    setCurrentZone(6);
                    // console.log(response.data);
                })
                .catch(error => console.error('Error fetching recommendation:', error));
        };

        fetchCurrentZone();
        setLoading(false);
    },[location.lat, location.lon, zones]);

    useEffect(() => {
        setLoading(true);
        const fetchRecommendations = (zoneId) => {
            axios.get(`${URL}/crops?zone_id=${zoneId}`)
                .then(response => {
                    setCrops(response.data);
                    // console.log(response.data);
                })
                .catch(error => console.error('Error fetching recommendation:', error));
        };

        fetchRecommendations(6);
        setLoading(false);
    },[]);

    const handleSoilTypeChange = (event) => {
        setCurrentSoil(event.target.value);
    };
    const handleZoneChange = (event) => {
        // setCurrentZone(event.target.value);
        // fetchRecommendations(currentZone);
        // bcoz it is only for zone 6
        alert("Setting current zone to Zone 6, Bcoz only Zone 6 is available.");  // Show an alert
        setCurrentZone(6);
    };

    const fetchRecommendations = (zoneId) => {
        setLoading(true);
        axios.get(`${URL}/crops?zone_id=${zoneId}`)
            .then(response => {
                setCrops(response.data);
                // console.log(response.data);
            })
            .catch(error => console.error('Error fetching recommendation:', error));
        setLoading(false);
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
                            <option key={index} value={element.ZoneId}>
                            {element.Name}
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
                        value={currentSoil}
                        onChange={handleSoilTypeChange}
                        style={selectStyle}
                        onMouseOver={(e) => e.target.style.borderColor = hoverEffect.borderColor}
                        onMouseOut={(e) => e.target.style.borderColor = '#ccc'}
                    >
                        {soils.map((element, index) => (
                            <option key={index} value={element}>
                            {element}
                            </option>
                        ))}
                    </select>
                </>
            </LocationInfo>
            
            {loading ? (
                <p style={labelStyle}>Loading...</p>  // Show loading message if data is being fetched
            ) : (
                <DataItem>
                    <SectionTitle>Recommended Crops & Plants</SectionTitle>
                    <CropList crops={crops}/>
                </DataItem>
            )}
        </Section>
    );
};

export default FarmData;