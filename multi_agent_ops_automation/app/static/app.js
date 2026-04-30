document.getElementById('metricForm').addEventListener('submit', async (e)=>{
  e.preventDefault();
  const data = Object.fromEntries(new FormData(e.target).entries());
  ['cpu','memory','disk','error_rate','latency_ms'].forEach(k=>data[k]=Number(data[k]));
  const res = await fetch('/api/metrics',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});
  const json = await res.json();
  document.getElementById('result').textContent = JSON.stringify(json,null,2);
});
async function startScheduler(){const r=await fetch('/api/scheduler/start',{method:'POST'});alert((await r.json()).message)}
async function stopScheduler(){const r=await fetch('/api/scheduler/stop',{method:'POST'});alert((await r.json()).message)}
