//to be run from webstorm

const io = require('socket.io-client');

const socket = io('http://127.0.0.1:5000/engine');

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

socket.on('connect', () => {
    const requestCurrentMode = async () => {
        while (true) {
            await delay(1000);
            socket.emit('currentmode', 'Requesting current mode');
        }
    };

    requestCurrentMode();
});
let a = 0;
socket.on('currentmode', (msg) => {
    a++;
    console.log('Received current mode response from server:', msg, a);
});



socket.on('connected', (msg) => {
    console.log('Received connection message from Flask server:', msg);
});

socket.on('disconnect', () => {
    console.log('Disconnected from server');
});

socket.on('connect_error', (err) => {
    console.error('Connection error:', err);
});
