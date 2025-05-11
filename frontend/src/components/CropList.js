import React from 'react';
import { LocationInfo, divStyle } from '../styles';

const CropList = (props) => {
    const groupedCrops = props.crops.reduce((acc, crop) => {
        if (!acc[crop['Crop Type']]) {
            acc[crop['Crop Type']] = [];
        }
        acc[crop['Crop Type']].push(crop);
        return acc;
    }, {});

    return (
        <div>
            {Object.keys(groupedCrops).map((type, idx) => (
                <div key={idx} style={{ marginBottom: '30px' }}>
                    <LocationInfo>
                        <h2 style={{ color: '#00ff00', textAlign: 'center' }}>{type}</h2>
                        <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-around' }}>
                            {groupedCrops[type].map((crop, index) => (
                                <div 
                                    key={index} 
                                    style={divStyle}
                                    onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
                                    onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
                                >
                                    <h3 style={{ color: '#00ff00' }}>{index + 1}. {crop['Crop Name']}</h3>
                                    <p><strong>Water Requirements:</strong> {crop['Water Requirements']} L</p>
                                    <p><strong>Soil pH Level:</strong> {crop['Soil pH Level']}</p>
                                    <p><strong>Soil Type:</strong> {crop['Soil Type']}</p>
                                    <p><strong>Sunshine Hours:</strong> {crop['Sunshine Hours']}</p>
                                    <p><strong>Watering Schedule:</strong> {crop['Watering Schedule']}</p>
                                    <p><strong>Irrigation Schedules:</strong> {crop['Irrigation Schedules']}</p>
                                    <p><strong>Fertilizer Schedules:</strong> {crop['Fertilizer Schedules']}</p>
                                    <p><strong>Season:</strong> {crop['Season']}</p>
                                    
                                    <h4>Growth Stages:</h4>
                                    <ul>
                                        {crop['Growth Stage'].map((stage, stageIndex) => (
                                            <li key={stageIndex} style={{ color: '#b2ffb2' }}>
                                                <strong>{stage.Stage}</strong>: {stage['Start Date']} ({stage.Duration} Days)
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            ))}
                        </div>
                    </LocationInfo>
                </div>
            ))}
        </div>
    );
};

export default CropList;
