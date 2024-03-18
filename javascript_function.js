// Assuming msg.payload contains the temperature value as a string
let temperature = parseFloat(msg.payload);
let threshold = flow.get("temperatureThreshold") || 30; // Default threshold of 30
let conversion = 'celsius'; // The different options are: 'fahrenheit', 'kelvin', 'celsius'

// Define actions
let actions = [
    { function: "check_temperature", args: { threshold: threshold } },
    { function: "convert_temperature", args: { conversion: conversion } }
];

// Add temperature and actions to payload
msg.payload = {
    rawData: {
        temperature: temperature,
    },
    actions: actions
};

return msg;
