import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {
    Section,
    SectionTitle,
    DataItem,
    LocationInfo,
    labelStyle,
    selectStyle,
    hoverEffect,
} from '../styles';
import CropList from './CropList';

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
                    setErrorLoc('⚠️ Unable to retrieve your location.');
                    console.error('Location error:', err);
                    setLoading(false);
                }
            );
        };

        fetchLocationAndData();
    }, []);

    useEffect(() => {
        const fetchCurrentZone = async () => {
            if (!location.lat || !location.lon) return;
            setLoading(true);

            try {
                const response = await axios.get(`${URL}/current_zone?lat=${location.lat}&lon=${location.lon}`);
                // Only Zone 6 is supported in this version
                setCurrentZone(6);
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
                console.error('Error fetching crops:', error);
            } finally {
                setLoading(false);
            }
        };

        fetchRecommendations(currentZone || 6);
    }, [currentZone]);

    const handleSoilTypeChange = (event) => {
        const selectedSoil = event.target.value;
        setCurrentSoil(selectedSoil);

        if (selectedSoil === "All") {
            setFilteredCrops(crops);
        } else {
            const filtered = crops.filter(crop => crop['Soil Type']?.includes(selectedSoil));
            setFilteredCrops(filtered);
        }
    };

    const handleZoneChange = () => {
        alert("Only Zone 6 is available in the current version.");
        setCurrentZone(6);
    };

    const handleHover = (e, hover = true) => {
        e.target.style.borderColor = hover ? hoverEffect.borderColor : '#00ff00';
    };

    return (
        <Section>
            <SectionTitle>🌾 Farm Data</SectionTitle>
            <LocationInfo>
                <h3>📍 Current Location</h3>
                {errorLoc ? (
                    <p>{errorLoc}</p>
                ) : (
                    <>
                        <p><strong>Latitude:</strong> {location.lat ?? 'Detecting...'}</p>
                        <p><strong>Longitude:</strong> {location.lon ?? 'Detecting...'}</p>
                    </>
                )}

                <br />

                <label htmlFor="zone" style={labelStyle}>Zone</label>
                {loadingZones ? (
                    <p>Loading zones...</p>
                ) : (
                    <select
                        id="zone"
                        value={currentZone}
                        onChange={handleZoneChange}
                        style={selectStyle}
                        onMouseOver={(e) => handleHover(e, true)}
                        onMouseOut={(e) => handleHover(e, false)}
                    >
                        {zones.map((zone) => (
                            <option key={zone.ZoneId} value={zone.ZoneId}>
                                {zone.Name}
                            </option>
                        ))}
                    </select>
                )}

                <br /><br />

                <label htmlFor="soilType" style={labelStyle}>Soil Type</label>
                {loadingSoils ? (
                    <p>Loading soils...</p>
                ) : (
                    <select
                        id="soilType"
                        value={currentSoil}
                        onChange={handleSoilTypeChange}
                        style={selectStyle}
                        onMouseOver={(e) => handleHover(e, true)}
                        onMouseOut={(e) => handleHover(e, false)}
                    >
                        <option value="All">All</option>
                        {soils.map((soil, idx) => (
                            <option key={idx} value={soil}>
                                {soil}
                            </option>
                        ))}
                    </select>
                )}
            </LocationInfo>

            {loading ? (
                <p style={{ color: '#b2ffb2' }}>🔄 Loading crop recommendations...</p>
            ) : (
                <DataItem>
                    <SectionTitle>✅ Recommended Crops & Plants</SectionTitle>
                    {filteredCrops.length > 0 ? (
                        <CropList crops={filteredCrops} />
                    ) : (
                        <p style={{ color: '#ffcc00' }}>⚠️ No crops found for the selected soil type.</p>
                    )}
                </DataItem>
            )}
        </Section>
    );
};

export default FarmData;


