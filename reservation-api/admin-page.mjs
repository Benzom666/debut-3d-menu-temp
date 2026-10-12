export const adminPage = `<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Reservations · Début</title>
<style>
:root{color-scheme:dark;font-family:Arial,sans-serif;background:#111411;color:#efe9db}
*{box-sizing:border-box}body{margin:0}a{color:inherit}button,select{font:inherit}button{cursor:pointer}
header{padding:23px clamp(24px,5vw,80px);display:flex;align-items:center;justify-content:space-between;border-bottom:1px solid #34382f}
.brand{font:30px Georgia,serif;letter-spacing:.08em;text-decoration:none}.brand span{display:block;font:9px Arial,sans-serif;letter-spacing:.25em;color:#d8b161;margin-top:4px}
.signout{font-size:12px;letter-spacing:.1em;text-decoration:none;text-transform:uppercase;border-bottom:1px solid #d8b161;padding-bottom:6px}
main{max-width:1500px;margin:auto;padding:70px clamp(24px,5vw,80px) 100px}
.eyebrow{font-size:11px;letter-spacing:.22em;color:#d8b161;text-transform:uppercase;font-weight:700}
h1{font:clamp(52px,7vw,96px)/.95 Georgia,serif;letter-spacing:-.06em;margin:18px 0 25px}
.intro{color:#b6b7ae;max-width:620px;line-height:1.6;margin:0 0 50px}
.toolbar{display:flex;align-items:center;justify-content:space-between;gap:20px;border-top:1px solid #41463c;border-bottom:1px solid #41463c;padding:16px 0;margin-bottom:12px}
.toolbar label{font-size:12px;color:#c5c4b9}.toolbar select{margin-left:12px;background:#1d221c;color:#efe9db;border:1px solid #5a604f;padding:10px 35px 10px 12px}
.toolbar button,.actions button{background:transparent;color:#d8b161;border:1px solid #806e48;padding:9px 13px;font-size:11px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}
.toolbar button:hover,.actions button:hover{background:#d8b161;color:#111411}.toolbar button:focus-visible,.actions button:focus-visible,select:focus-visible,a:focus-visible{outline:2px solid #d8b161;outline-offset:3px}
.status{min-height:28px;color:#c5c4b9;font-size:13px}.grid{display:grid;grid-template-columns:125px minmax(180px,1fr) minmax(180px,1fr) 90px minmax(170px,1.2fr) minmax(190px,1.2fr);gap:16px;align-items:start}
.head{padding:17px 0;color:#aaac9f;font-size:10px;letter-spacing:.15em;text-transform:uppercase;border-bottom:1px solid #41463c}
.row{padding:24px 0;border-bottom:1px solid #34382f;font-size:13px;line-height:1.5}.row strong{display:block;font:23px Georgia,serif;font-weight:400}.row small{display:block;color:#aaa99e}.row a{display:block;text-decoration:none;overflow-wrap:anywhere}.row a:hover{color:#d8b161}.row .note{color:#c5c4b9;white-space:pre-wrap;overflow-wrap:anywhere}
.state{display:inline-block;margin-top:8px;color:#d8b161;font-size:10px;text-transform:uppercase;letter-spacing:.1em}.actions{display:flex;flex-wrap:wrap;gap:7px}.actions button{padding:7px 9px;font-size:9px}.actions button[disabled]{opacity:.45;cursor:default}
.empty{padding:55px 0;color:#b6b7ae}
@media(max-width:900px){.head{display:none}.row{grid-template-columns:1fr 1fr;gap:18px 24px}.row>div:first-child{grid-column:1/-1}.row>div:last-child{grid-column:1/-1}.row strong{font-size:20px}}
@media(max-width:540px){main{padding-top:50px}.row{grid-template-columns:1fr}.row>div{grid-column:1/-1}.toolbar{align-items:flex-start;flex-direction:column}}
</style></head><body>
<header><a class="brand" href="/admin">DÉBUT<span>BAR & RESTAURANT</span></a><a class="signout" href="/signout-with-chatgpt?return_to=%2Fadmin">Sign out ↗</a></header>
<main><p class="eyebrow">STAFF DESK</p><h1>Reservations</h1><p class="intro">Review requests and update their status after contacting the guest. A request is not confirmed until the team replies.</p>
<div class="toolbar"><label for="filter">Show <select id="filter"><option value="all">All requests</option><option value="pending">Pending</option><option value="confirmed">Confirmed</option><option value="cancelled">Cancelled</option></select></label><button id="refresh" type="button">Refresh ↻</button></div>
<p class="status" id="status" role="status" aria-live="polite"></p><div class="grid head" aria-hidden="true"><span>DATE</span><span>GUEST</span><span>CONTACT</span><span>PARTY</span><span>REQUEST</span><span>STATUS</span></div><div id="list"></div>
</main><script>
const list=document.getElementById('list');const status=document.getElementById('status');const filter=document.getElementById('filter');let rows=[];
function cell(text,cls){const el=document.createElement('div');if(cls)el.className=cls;el.textContent=text??'';return el}
function link(label,href){const el=document.createElement('a');el.href=href;el.textContent=label;return el}
function render(){list.replaceChildren();const shown=rows.filter(row=>filter.value==='all'||row.status===filter.value);if(!shown.length){list.append(cell('No reservations in this view.','empty'));return}
for(const row of shown){const article=document.createElement('article');article.className='grid row';const date=cell('');const strong=document.createElement('strong');strong.textContent=row.reservation_date;date.append(strong,cell(row.reservation_time));
const guest=cell('');const guestName=document.createElement('strong');guestName.textContent=row.name;guest.append(guestName,cell('Requested '+new Date(row.created_at).toLocaleString()));
const contact=cell('');contact.append(link(row.email,'mailto:'+row.email),link(row.phone,'tel:'+row.phone));
const party=cell(String(row.guests));const note=cell(row.message||'—','note');const controls=cell('');const current=cell(row.status,'state');controls.append(current);const actions=cell('','actions');
for(const next of ['pending','confirmed','cancelled']){const button=document.createElement('button');button.type='button';button.textContent=next;button.disabled=row.status===next;button.addEventListener('click',()=>update(row,next,button));actions.append(button)}controls.append(actions);article.append(date,guest,contact,party,note,controls);list.append(article)}}
async function load(){status.textContent='Loading reservations…';try{const response=await fetch('/api/admin/reservations',{cache:'no-store'});if(response.status===401){location.assign('/signin-with-chatgpt?return_to=%2Fadmin');return}if(!response.ok)throw Error('Could not load reservations');rows=(await response.json()).reservations;render();status.textContent=rows.length+' recent requests'}catch(error){status.textContent=error.message}}
async function update(row,next,button){button.disabled=true;status.textContent='Saving status…';try{const response=await fetch('/api/admin/reservations/'+encodeURIComponent(row.id),{method:'PATCH',headers:{'content-type':'application/json'},body:JSON.stringify({status:next})});if(!response.ok)throw Error('Could not update status');row.status=next;render();status.textContent='Status updated. Contact the guest to confirm.'}catch(error){button.disabled=false;status.textContent=error.message}}
filter.addEventListener('change',render);document.getElementById('refresh').addEventListener('click',load);load();
</script></body></html>`;
