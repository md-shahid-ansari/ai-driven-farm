import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Section, SectionTitle, DataItem, LocationInfo, labelStyle, selectStyle, hoverEffect } from '../styles';
import CropList from './CropList';

// const URL = "http://localhost:5000";
const URL = "https://farm-ai-5w5g.onrender.com";

const FarmData = () => {
    const [crops, setCrops] = useState([]);
    const [location, setLocation] = useState({ lat: null, lon: null });
    const [soils, setSoils] = useState([]);
    const [currentSoil, setCurrentSoil] = useState('All');
    const [errorLoc, setErrorLoc] = useState('');
    const [zones, setZones] = useState([]);
    const [currentZone, setCurrentZone] = useState('');
    const [loading, setLoading] = useState(false);
    const [loadingZones, setLoadingZones] = useState(false);
    const [loadingSoils, setLoadingSoils] = useState(false);
    const [filteredCrops, setFilteredCrops] = useState([]);

    useEffect(() => {
        const fetchLocationAndData = async () => {
            setLoading(true);

            navigator.geolocation.getCurrentPosition(
                async (position) => {
                    const { latitude, longitude } = position.coords;
                    setLocation({ lat: latitude, lon: longitude });

                    try {
                        setLoadingZones(true);
                        const zonesResponse = await axios.get(`${URL}/zones`);
                        setZones(zonesResponse.data);
                    } catch (error) {
                        console.error('Error fetching zone data:', error);
                    } finally {
                        setLoadingZones(false);
                    }

                    try {
                        setLoadingSoils(true);
                        const soilsResponse = await axios.get(`${URL}/soils`);
                        setSoils(soilsResponse.data);
                    } catch (error) {
                        console.error('Error fetching soil data:', error);
                    } finally {
                        setLoadingSoils(false);
                    }

                    setLoading(false);
                },
                (err) => {
                    setErrorLoc('Error retrieving location');
                    console.error('Error retrieving location:', err);
                    setLoading(false);
                }
            );
        };

        fetchLocationAndData();
    }, []);

    useEffect(() => {
        const fetchCurrentZone = async () => {
            if (location.lat == null || location.lon == null) return;

            setLoading(true);
            try {
                const response = await axios.get(`${URL}/current_zone?lat=${location.lat}&lon=${location.lon}`);
                const zone = zones.find(zone => zone.Name === response.data);
                // setCurrentZone(zone ? zone.ZoneId : 6);
                //for now data is only available for zone 6
                setCurrentZone(zone ? 6 : 6);

            } catch (error) {
                console.error('Error fetching current zone:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchCurrentZone();
    }, [location, zones]);

    useEffect(() => {
        const fetchRecommendations = async (zoneId) => {
            if (!zoneId) return;

            setLoading(true);
            try {
                const response = await axios.get(`${URL}/crops?zone_id=${zoneId}`);
                setCrops(response.data);
                setFilteredCrops(response.data);
            } catch (error) {
                console.error('Error fetching recommendations:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchRecommendations(currentZone || 6);
    }, [currentZone]);

    const handleSoilTypeChange = (event) => {
        const selectedSoil = event.target.value;
        setCurrentSoil(selectedSoil);
        if (selectedSoil === "All"){
            setFilteredCrops(crops);
            return;
        }

        // Filter crops based on the selected soil type
        const filtered = crops.filter(crop => crop['Soil Type'] && crop['Soil Type'].includes(selectedSoil));
        setFilteredCrops(filtered);
    };

    const handleZoneChange = (event) => {
        alert("Setting current zone to Zone 6, because only Zone 6 is available.");
        setCurrentZone(6);
    };

    return (
        <Section>
            <SectionTitle>Farm Data</SectionTitle>
            <LocationInfo>
                <h3>Current Location</h3>
                {errorLoc ? (
                    <p>{errorLoc}</p>
                ) : (
                    <>
                        <p><strong>Latitude: {location.lat}</strong></p>
                        <p><strong>Longitude: {location.lon}</strong></p>
                    </>
                )}
                <br />
                <label htmlFor="zone" style={labelStyle}>
                    Current zone  
                </label>
                {loadingZones ? (
                    <p>Loading zones...</p>
                ) : (
                    <select
                        id="zone"
                        value={currentZone}
                        onChange={handleZoneChange}
                        style={selectStyle}
                        onMouseOver={(e) => e.target.style.borderColor = hoverEffect.borderColor}
                        onMouseOut={(e) => e.target.style.borderColor = '#ccc'}
                    >
                        {zones.map((element) => (
                            <option key={element.ZoneId} value={element.ZoneId}>
                                {element.Name}
                            </option>
                        ))}
                    </select>
                )}
                <br />
                <label htmlFor="soilType" style={labelStyle}>
                    Soil
                </label>
                {loadingSoils ? (
                    <p>Loading soils...</p>
                ) : (
                    <select
                        id="soilType"
                        value={currentSoil}
                        onChange={handleSoilTypeChange}
                        style={selectStyle}
                        onMouseOver={(e) => e.target.style.borderColor = hoverEffect.borderColor}
                        onMouseOut={(e) => e.target.style.borderColor = '#ccc'}
                    >
                        <option key={0} value="All">
                                All
                            </option>
                        {soils.map((element, index) => (
                            <option key={index + 1} value={element}>
                                {element}
                            </option>
                        ))}
                    </select>
                )}
            </LocationInfo>

            {loading ? (
                <p>Loading...</p>
            ) : (
                <DataItem>
                    <SectionTitle>Recommended Crops & Plants</SectionTitle>
                    <CropList crops={filteredCrops} />
                </DataItem>
            )}
        </Section>
    );
};

export default FarmData;
