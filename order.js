(() => {
  const source = window.DEBUT_MENU;
  if (!source?.sections) return;
  const assetPrefix = document.body.dataset.assetPrefix ?? '../';
  const excluded = new Set(['deals', 'add-ons']);
  const dishes = source.sections.flatMap(section => excluded.has(section.id) ? [] : section.items.map((item, index) => ({
    ...item, section: section.title, sectionId: section.id,
    id: `${section.id}-${String(index + 1).padStart(2, '0')}`,
    image: `${assetPrefix}images/generated/${section.id}-${String(index + 1).padStart(2, '0')}.webp`,
    thumbnail: `${assetPrefix}images/generated/thumbs/${section.id}-${String(index + 1).padStart(2, '0')}.webp`
  }))).filter(item => typeof item.price === 'number' && Number.isFinite(item.price));
  const $ = id => document.getElementById(id);
  const money = amount => '$' + amount.toFixed(2);
  const image = $('featured-image');
  const cartButton = $('open-cart');
  const drawer = $('cart-drawer');
  const backdrop = $('cart-backdrop');
  const rail = $('dish-rail');
  const filters = $('category-filters');
  const search = $('dish-search');
  const taxRate = 0.13;
  const storageKey = 'debut-pickup-cart-v1';
  let active = 0;
  let category = 'all';
  let switchTimer;
  let previousFocus;
  let lastWheel = 0;
  let cart = {};
  try {
    const saved = JSON.parse(localStorage.getItem(storageKey) || '{}');
    for (const [id, count] of Object.entries(saved)) {
      if (dishes.some(d => d.id === id) && Number.isInteger(count) && count > 0 && count <= 99) cart[id] = count;
    }
  } catch (_) { cart = {}; }
  const ingredientMap = {
    'appetizers-01': ['BUTTER CHICKEN', 'CHEESE CURDS', 'GOLDEN FRIES'],
    'appetizers-02': ['GRILLED CHICKEN', 'BELL PEPPERS', 'MELTED CHEESE'],
    'appetizers-03': ['NASHVILLE CHICKEN', 'COOL SLAW', 'SLICED PICKLE'],
    'flavours-east-06': ['TENDER CHICKEN', 'TOMATO CREAM', 'WARM SPICES'],
    'grills-mains-03': ['GRILLED SALMON', 'ROASTED POTATOES', 'BROCCOLI'],
    'pasta-05': ['GARLIC SHRIMP', 'PENNE PASTA', 'CREAM SAUCE']
  };
  function callouts(dish) {
    const container = $('ingredient-callouts');
    container.replaceChildren();
    const names = ingredientMap[dish.id];
    if (!names) return;
    const positions = [{left:'1%',top:'26%'},{left:'70%',top:'16%'},{left:'72%',top:'68%'}];
    names.forEach((name, i) => {
      const label = document.createElement('span');
      label.className = 'callout ' + (i === 0 ? 'left' : 'right');
      label.textContent = name;
      Object.assign(label.style, positions[i]);
      label.style.animationDelay = `${i * .1}s`;
      container.append(label);
    });
  }
  function renderFeatured() {
    const dish = dishes[active];
    image.src = dish.image;
    image.alt = `Illustration of ${dish.name}`;
    $('featured-category').textContent = dish.section.toUpperCase();
    $('featured-name').textContent = dish.name;
    $('featured-description').textContent = dish.description;
    $('featured-price').textContent = money(dish.price);
    $('dish-position').textContent = `${String(active + 1).padStart(2, '0')} / ${String(dishes.length).padStart(2, '0')}`;
    $('add-featured').setAttribute('aria-label', `Add ${dish.name} to order`);
    const tags = $('featured-tags');
    tags.replaceChildren();
    (dish.tags || []).forEach(tag => { const el = document.createElement('span'); el.textContent = tag; tags.append(el); });
    callouts(dish);
    rail.querySelectorAll('button[data-item-id]').forEach(button => {
      const selected = button.dataset.itemId === dish.id;
      button.classList.toggle('active', selected);
      button.setAttribute('aria-current', selected ? 'true' : 'false');
    });
  }
  function selectDish(index, animate = true) {
    const next = (index + dishes.length) % dishes.length;
    if (next === active && image.src) return;
    clearTimeout(switchTimer);
    const shouldAnimate = animate && !matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (shouldAnimate) {
      const old = image.cloneNode();
      old.removeAttribute('id');
      old.className = 'featured-image rolling-out plate-ghost';
      $('plate-scene').append(old);
      setTimeout(() => old.remove(), 480);
    }
    active = next;
    renderFeatured();
    image.classList.remove('rolling-in');
    if (shouldAnimate) {
      void image.offsetWidth;
      image.classList.add('rolling-in');
      switchTimer = setTimeout(() => image.classList.remove('rolling-in'), 550);
    }
  }
  function renderFilters() {
    const options = [['all','All dishes'], ...source.sections.filter(s => !excluded.has(s.id)).map(s => [s.id,s.title])];
    options.forEach(([id, label]) => {
      const button = document.createElement('button');
      button.type = 'button'; button.textContent = label;
      button.classList.toggle('active', id === category);
      button.addEventListener('click', () => { category = id; renderRail(); renderFiltersState(); });
      button.dataset.category = id; filters.append(button);
    });
  }
  function renderFiltersState() { filters.querySelectorAll('button').forEach(b => b.classList.toggle('active', b.dataset.category === category)); }
  function renderRail() {
    rail.replaceChildren();
    const query = search.value.trim().toLocaleLowerCase();
    const visible = dishes.filter(d => (category === 'all' || d.sectionId === category) && (!query || `${d.name} ${d.description} ${d.section}`.toLocaleLowerCase().includes(query)));
    if (!visible.length) { const empty = document.createElement('p'); empty.className='empty-result'; empty.textContent='No dishes match your search.'; rail.append(empty); return; }
    visible.forEach(dish => {
      const button = document.createElement('button'); button.type='button'; button.dataset.itemId=dish.id;
      const thumb=document.createElement('img'); thumb.src=dish.thumbnail; thumb.alt=''; thumb.loading='lazy'; thumb.decoding='async'; thumb.width=320; thumb.height=320;
      const copy=document.createElement('span'); const name=document.createElement('strong'); name.textContent=dish.name; const price=document.createElement('small'); price.textContent=`${dish.section} · ${money(dish.price)}`;
      copy.append(name,price); button.append(thumb,copy);
      button.classList.toggle('active', dishes[active].id === dish.id);
      button.addEventListener('click', () => { selectDish(dishes.indexOf(dish)); $('order-main').scrollIntoView({behavior:'smooth'}); });
      rail.append(button);
    });
  }
  function saveCart() { try { localStorage.setItem(storageKey, JSON.stringify(cart)); } catch (_) {} }
  function renderCart() {
    const list=$('cart-items'); list.replaceChildren();
    let subtotal=0, count=0;
    dishes.forEach(dish => {
      const qty=cart[dish.id] || 0; if (!qty) return;
      subtotal += Math.round(dish.price * 100) * qty; count += qty;
      const row=document.createElement('div'); row.className='cart-item';
      const img=document.createElement('img'); img.src=dish.thumbnail; img.alt=''; img.width=320; img.height=320;
      const info=document.createElement('div'); const name=document.createElement('strong'); name.textContent=dish.name; const price=document.createElement('small'); price.textContent=money(dish.price * qty); info.append(name,price);
      const quantity=document.createElement('div'); quantity.className='quantity-control';
      const minus=document.createElement('button'); minus.type='button'; minus.textContent='−'; minus.setAttribute('aria-label',`Decrease ${dish.name} quantity`); minus.addEventListener('click',()=>changeQuantity(dish.id,-1));
      const number=document.createElement('span'); number.textContent=qty;
      const plus=document.createElement('button'); plus.type='button'; plus.textContent='+'; plus.setAttribute('aria-label',`Increase ${dish.name} quantity`); plus.addEventListener('click',()=>changeQuantity(dish.id,1));
      quantity.append(minus,number,plus); row.append(img,info,quantity); list.append(row);
    });
    if (!count) { const empty=document.createElement('p'); empty.className='cart-empty'; empty.textContent='Your order is empty. Choose a dish to begin.'; list.append(empty); }
    const tax=Math.round(subtotal*taxRate);
    $('cart-count').textContent=count; $('cart-subtotal').textContent=money(subtotal/100); $('cart-tax').textContent=money(tax/100); $('cart-total').textContent=money((subtotal+tax)/100);
    $('order-form').querySelector('button[type=submit]').disabled=!count;
  }
  function changeQuantity(id, delta) {
    const next=Math.min(99,Math.max(0,(cart[id]||0)+delta));
    if (next) cart[id]=next; else delete cart[id];
    saveCart(); renderCart();
  }
  function flyToCart() {
    if (matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const plate=image.getBoundingClientRect();
    const visibleHeight=Math.max(0,Math.min(plate.bottom,innerHeight)-Math.max(plate.top,0));
    const start=visibleHeight>=Math.min(160,plate.height*.4)?plate:$('add-featured').getBoundingClientRect();
    const end=cartButton.getBoundingClientRect();
    const size=Math.min(190,Math.max(96,start.width*.36));
    const x=start.left+start.width/2-size/2,y=start.top+start.height/2-size/2;
    const dx=end.left+end.width/2-(x+size/2),dy=end.top+end.height/2-(y+size/2);
    const clone=image.cloneNode();
    clone.removeAttribute('id');
    clone.className='fly-dish';
    Object.assign(clone.style,{left:`${x}px`,top:`${y}px`,width:`${size}px`,height:`${size}px`});
    document.body.append(clone);
    const flight=clone.animate([
      {transform:'translate(0,0) scale(1) rotate(0deg)',opacity:1},
      {transform:`translate(${dx*.48}px,${dy*.5-75}px) scale(.7) rotate(20deg)`,opacity:1,offset:.52},
      {transform:`translate(${dx}px,${dy}px) scale(.14) rotate(50deg)`,opacity:0}
    ],{duration:850,easing:'cubic-bezier(.4,0,.2,1)',fill:'forwards'});
    flight.onfinish=()=>{clone.remove();cartButton.animate([{transform:'scale(1)'},{transform:'scale(1.18)'},{transform:'scale(1)'}],{duration:250,easing:'ease-out'});};
  }
  function openCart() { previousFocus=document.activeElement; backdrop.hidden=false; drawer.classList.add('open'); drawer.setAttribute('aria-hidden','false'); document.body.style.overflow='hidden'; $('close-cart').focus(); }
  function closeCart() { drawer.classList.remove('open'); drawer.setAttribute('aria-hidden','true'); backdrop.hidden=true; document.body.style.overflow=''; previousFocus?.focus(); }
  $('dish-prev').addEventListener('click',()=>selectDish(active-1)); $('dish-next').addEventListener('click',()=>selectDish(active+1));
  document.addEventListener('keydown', event => { if (event.key==='Escape' && drawer.classList.contains('open')) closeCart(); if (drawer.classList.contains('open') || /INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName || '')) return; if (event.key==='ArrowRight' || event.key==='ArrowLeft') { event.preventDefault(); selectDish(active+(event.key==='ArrowRight'?1:-1)); } });
  $('plate-scene').addEventListener('wheel',event=>{ if(Math.abs(event.deltaY)<8 || Date.now()-lastWheel<700)return; event.preventDefault(); lastWheel=Date.now(); selectDish(active+(event.deltaY>0?1:-1)); },{passive:false});
  let touchStartX=0, touchStartY=0;
  $('plate-scene').addEventListener('touchstart',event=>{touchStartX=event.changedTouches[0].screenX;touchStartY=event.changedTouches[0].screenY;},{passive:true});
  $('plate-scene').addEventListener('touchend',event=>{const dx=event.changedTouches[0].screenX-touchStartX,dy=event.changedTouches[0].screenY-touchStartY;if(Math.abs(dx)>55&&Math.abs(dx)>Math.abs(dy)*1.4)selectDish(active+(dx<0?1:-1));},{passive:true});
  $('add-featured').addEventListener('click',()=>{ changeQuantity(dishes[active].id,1); flyToCart(); $('live-message').textContent=`${dishes[active].name} added to order`; });
  cartButton.addEventListener('click',openCart); $('close-cart').addEventListener('click',closeCart); backdrop.addEventListener('click',closeCart);
  drawer.addEventListener('keydown',event=>{ if(event.key!=='Tab')return; const focusables=[...drawer.querySelectorAll('button:not(:disabled),input,select,textarea,a[href]')].filter(el=>el.getClientRects().length); const first=focusables[0],last=focusables.at(-1); if(event.shiftKey && document.activeElement===first){event.preventDefault();last.focus()}else if(!event.shiftKey && document.activeElement===last){event.preventDefault();first.focus()} });
  search.addEventListener('input',renderRail); renderFilters(); renderRail(); renderFeatured(); renderCart();
  if (location.hash === '#cart') openCart();
  const dateInput=$('order-form').elements.date;
  const today=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Toronto',year:'numeric',month:'2-digit',day:'2-digit'}).format(new Date());
  dateInput.min=today;
  const maxDate=new Date(Date.now()+14*86400000);
  dateInput.max=new Intl.DateTimeFormat('en-CA',{timeZone:'America/Toronto',year:'numeric',month:'2-digit',day:'2-digit'}).format(maxDate);
  const select=$('order-form').elements.time;
  for(let minutes=12*60;minutes<=21*60;minutes+=30){const option=document.createElement('option');const h=Math.floor(minutes/60),m=minutes%60;option.value=`${String(h).padStart(2,'0')}:${String(m).padStart(2,'0')}`;option.textContent=new Intl.DateTimeFormat('en-CA',{hour:'numeric',minute:'2-digit'}).format(new Date(2020,0,1,h,m));select.append(option)}
  $('order-form').addEventListener('submit',async event=>{
    event.preventDefault();
    const form=event.currentTarget;
    const submitButton=form.querySelector('button[type="submit"]');
    if(submitButton.disabled || !Object.keys(cart).length || !form.reportValidity())return;
    const ref='DB-'+Date.now().toString(36).toUpperCase().slice(-7);
    const subtotal=dishes.reduce((sum,d)=>sum+Math.round(d.price*100)*(cart[d.id]||0),0);
    const tax=Math.round(subtotal*taxRate);
    const total=subtotal+tax;
    const items=dishes.filter(d=>cart[d.id]).map(d=>({name:d.name,quantity:cart[d.id],unit_price:money(d.price),line_total:money(d.price*cart[d.id])}));
    const lines=items.map(d=>`${d.quantity} × ${d.name} — ${d.line_total}`);
    const name=form.elements.name.value.trim(),email=form.elements.email.value.trim(),phone=form.elements.phone.value.trim();
    const date=form.elements.date.value,time=form.elements.time.value,notes=form.elements.notes.value.trim();
    const message=[`Pickup request ${ref}`,'',...lines,'',`Subtotal: ${money(subtotal/100)}`,`Estimated HST (13%): ${money(tax/100)}`,`Estimated total: ${money(total/100)}`,'',`Name: ${name}`,`Email: ${email}`,`Phone: ${phone}`,`Preferred pickup: ${date} at ${time}`,`Notes: ${notes || 'None'}`,'','Please reply to confirm availability, final pricing, and pickup time.'].join('\n');
    const subject=`Début pickup request ${ref}`;
    $('email-link').href=`mailto:info@debutbar.ca?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(message)}`;
    const status=$('order-status');
    status.hidden=false; status.dataset.kind='ok'; status.textContent='Sending your pickup request…';
    $('email-link').hidden=true;
    submitButton.disabled=true;
    submitButton.innerHTML='SENDING…';
    try {
      const response=await fetch(form.action,{
        method:'POST',
        headers:{'Content-Type':'application/json',Accept:'application/json'},
        body:JSON.stringify({name,email,phone,date,time,notes,reference:ref,request_type:'Pickup order',items,subtotal:money(subtotal/100),estimated_hst:money(tax/100),estimated_total:money(total/100),message,_subject:subject})
      });
      if(!response.ok)throw new Error(`Formspree returned ${response.status}`);
      $('request-reference').textContent=`Reference ${ref} · Estimated total ${money(total/100)}`;
      status.hidden=true; form.hidden=true; $('request-result').hidden=false;
      cart={}; saveCart(); renderCart(); form.reset();
      $('live-message').textContent=`Pickup request ${ref} sent`;
    } catch (_) {
      status.dataset.kind='error';
      status.textContent='Could not send your request. Try again, use Email instead, or call +1 942 883 3288.';
      $('email-link').hidden=false;
      submitButton.disabled=false;
      submitButton.innerHTML='PLACE PICKUP REQUEST <span>↗</span>';
    }
  });
  $('new-request').addEventListener('click',()=>{$('request-result').hidden=true;$('order-form').hidden=false});
})();
