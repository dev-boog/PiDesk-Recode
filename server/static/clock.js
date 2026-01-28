function updateClock() {
    const now = new Date();
            
    // Time formats
    const timeShort = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit' });
    const timeFull = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' });
            
    // Date formats
    const dayName = now.toLocaleDateString('en-GB', { weekday: 'long' });
    const dateShort = now.toLocaleDateString('en-GB', { day: 'numeric', month: 'short' });
    const dateFull = now.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
            
    // Update elements

    document.getElementById('clock-time').textContent = timeFull;
    document.getElementById('clock-date').textContent = dateFull;
}
        
updateClock();
setInterval(updateClock, 1000);