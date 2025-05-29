function send(command) {
    fetch('/command', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ command })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById('status').innerText = "✅ " + data.status;
    })
    .catch(err => {
        console.error(err);
        document.getElementById('status').innerText = "❌ Error sending command";
    });
}
