const map = L.map('map').setView([49.07, -123.88], 12);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

const markers = {};
const zones = [
  {name:'Airport Restricted Zone', lat:49.05497, lon:-123.86986, radius:1800},
  {name:'Power Facility', lat:49.07500, lon:-123.89000, radius:1200},
];
zones.forEach(z => {
  L.circle([z.lat,z.lon], {radius:z.radius}).addTo(map).bindPopup(z.name);
});

function iconFor(level) {
  return L.divIcon({
    className: '',
    html: `<div style="background:white;color:black;border-radius:12px;padding:3px 6px;border:2px solid black">${level}</div>`
  });
}

async function explain(trackId) {
  const res = await fetch('/api/v1/analyst/explain', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body:JSON.stringify({track_id: trackId})
  });
  const data = await res.json();
  alert(`${data.summary}\n\nWhy: ${data.why}\n\nRecommendation: ${data.recommendation}`);
}

async function refresh() {
  const res = await fetch('/api/v1/cop/tracks');
  const tracks = await res.json();
  document.getElementById('status').innerText = `${tracks.length} active tracks`;
  const panel = document.getElementById('panel');
  panel.innerHTML = '';
  tracks.forEach(t => {
    if (!markers[t.id]) {
      markers[t.id] = L.marker([t.lat, t.lon], {icon: iconFor(t.threat_level)}).addTo(map);
    }
    markers[t.id].setLatLng([t.lat, t.lon]);
    markers[t.id].bindPopup(`${t.label}<br>${t.threat_level} ${t.threat_score}/100<br>${t.explanation}`);
    const div = document.createElement('div');
    div.className = `track ${t.threat_level}`;
    div.innerHTML = `
      <strong>${t.label}</strong><br/>
      Type: ${t.object_type}<br/>
      Threat: ${t.threat_level} ${t.threat_score}/100<br/>
      Confidence: ${Math.round(t.confidence*100)}%<br/>
      Sources: ${t.sources.join(', ')}<br/>
      <small>${t.explanation}</small><br/>
      <button onclick="explain('${t.id}')">Why this alert?</button>
    `;
    panel.appendChild(div);
  });
}
setInterval(refresh, 2500);
refresh();
