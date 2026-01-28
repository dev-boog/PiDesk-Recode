function updateClock() {
    const now = new Date();
            
    const timeFull = now.toLocaleTimeString('en-GB', { hour: '2-digit', minute: '2-digit', second: '2-digit' });      
    const dateFull = now.toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' });
            
    document.getElementById('clock-time').textContent = timeFull;
    document.getElementById('clock-date').textContent = dateFull;
}
        
updateClock();
setInterval(updateClock, 1000);