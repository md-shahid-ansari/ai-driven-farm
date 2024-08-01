import React from 'react';
import {LocationInfo} from '../styles';

const CropList = (props) => {
    // Group crops by type
    const groupedCrops = props.recommended_crops.reduce((acc, crop) => {
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
                    <LocationInfo><h2 style={{ color: '#333', textAlign: 'center' }}>{type}</h2>
                    <div style={{ display: 'flex', flexWrap: 'wrap', justifyContent: 'space-around' }}>
                        {groupedCrops[type].map((crop, index) => (
                            <div 
                                key={index} 
                                style={{ 
                                    border: '1px solid #ccc', 
                                    borderRadius: '10px',
                                    padding: '20px', 
                                    margin: '10px', 
                                    width: '300px', 
                                    boxShadow: '0px 4px 6px rgba(0, 0, 0, 0.1)',
                                    backgroundColor: '#f9f9f9',
                                    transition: 'transform 0.05s',
                                }}
                                onMouseEnter={(e) => e.currentTarget.style.transform = 'scale(1.05)'}
                                onMouseLeave={(e) => e.currentTarget.style.transform = 'scale(1)'}
                            >
                                <h3 style={{ color:'green' }}>{index + 1}. {crop['Crop Name']}</h3>
                                {/* <p><strong>Type:</strong> {crop['Crop Type']}</p> */}
                                <p><strong>Water Requirements:</strong> {crop['Water Requirements']} L</p>
                                <p><strong>Temperature:</strong> {crop['Temperature']}°C</p>
                                <p><strong>Soil pH Level:</strong> {crop['Soil pH Level']}</p>
                                <p><strong>Planting Dates:</strong> {crop['Planting Dates']}</p>
                                <p><strong>Harvesting Dates:</strong> {crop['Harvesting Dates']}</p>
                                <p><strong>Irrigation Schedules:</strong> {crop['Irrigation Schedules']}</p>
                                <p><strong>Fertilizer Schedules:</strong> {crop['Fertilizer Schedules']}</p>
                            </div>
                        ))}
                    </div></LocationInfo>
                </div>
            ))}
        </div>
    );
};

export default CropList;
