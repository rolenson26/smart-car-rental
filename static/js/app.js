// ---- Navigation ----
function showSection(name) {
  document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
  document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
  document.getElementById('section-' + name).classList.add('active');
  document.getElementById('nav-' + name).classList.add('active');
  if (name === 'cars') loadCars();
  if (name === 'rent') loadRentCars();
  if (name === 'return') loadReturnCars();
}

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.remove('hidden');
  setTimeout(() => t.classList.add('hidden'), 3000);
}

function setMsg(id, msg, type) {
  const el = document.getElementById(id);
  el.textContent = msg;
  el.className = 'msg ' + type;
}

// ---- Cars ----
const catClass = { SUV: 'cat-suv', Economy: 'cat-economy', Sedan: 'cat-sedan', Luxury: 'cat-luxury' };
const catIcon = { SUV: '🚙', Economy: '🚗', Sedan: '🏎️', Luxury: '💎' };

async function loadCars() {
  const res = await fetch('/api/cars');
  const cars = await res.json();
  const grid = document.getElementById('cars-grid');

  grid.innerHTML = cars.map(c => `
    <div class="car-card">
      <img src="${c.image}" class="car-img" alt="${c.model}">

      <div class="car-name">${c.brand} ${c.model}</div>

      <span class="car-category ${catClass[c.category] || ''}">
        ${c.category}
      </span>

      <div class="car-price">
        ₹${c.price.toLocaleString()}
        <span>/ day</span>
      </div>

      <span class="avail-badge ${c.available ? 'avail-yes' : 'avail-no'}">
        ${c.available ? '✔ Available' : '✘ Rented'}
      </span>
    </div>
  `).join('');
}

// ---- Register ----
async function registerCustomer() {
  const name = document.getElementById('reg-name').value.trim();
  const phone = document.getElementById('reg-phone').value.trim();
  const license = document.getElementById('reg-license').value.trim();
  if (!name || !phone || !license) { setMsg('reg-msg', 'All fields required.', 'error'); return; }
  const res = await fetch('/api/register', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ name, phone, license })
  });
  const data = await res.json();
  setMsg('reg-msg', data.message, data.success ? 'success' : 'error');
  if (data.success) { document.getElementById('reg-name').value = ''; document.getElementById('reg-phone').value = ''; document.getElementById('reg-license').value = ''; }
}

// ---- Rent ----
let allCars = [];
let pendingBill = null;

async function loadRentCars() {
  const res = await fetch('/api/cars');
  allCars = await res.json();
  const sel = document.getElementById('rent-car');
  sel.innerHTML = allCars.filter(c => c.available).map(c =>
    `<option value="${c.id}">ID ${c.id} — ${c.brand} ${c.model} (₹${c.price}/day)</option>`
  ).join('');
}

document.addEventListener('DOMContentLoaded', () => {
  // Payment method toggle
  document.querySelectorAll('input[name="payment"]').forEach(r => {
    r.addEventListener('change', e => {
      document.getElementById('upi-field').classList.toggle('hidden', e.target.value !== 'UPI');
      document.getElementById('card-field').classList.toggle('hidden', e.target.value !== 'Card');
    });
  });

  // Card number formatting
  document.getElementById('rent-card').addEventListener('input', e => {
    let v = e.target.value.replace(/\D/g, '').substring(0, 16);
    e.target.value = v.match(/.{1,4}/g)?.join(' ') || v;
  });

  loadCars();
});

async function previewBill() {
  const name = document.getElementById('rent-name').value.trim();
  const carId = parseInt(document.getElementById('rent-car').value);
  const days = parseInt(document.getElementById('rent-days').value);
  const coupon = document.getElementById('rent-coupon').value.trim().toUpperCase();
  const payment = document.querySelector('input[name="payment"]:checked').value;

  if (!name || !carId || !days || days < 1) { setMsg('rent-msg', 'Please fill all fields.', 'error'); return; }

  const car = allCars.find(c => c.id === carId);
  const base = car.price * days;
  const tax = base * 0.18;
  let total = base + tax;
  let discount = 0;

  if (coupon === 'SAVE10') discount += total * 0.10;

  const preview = document.getElementById('bill-preview');
  preview.classList.remove('hidden');
  preview.innerHTML = `
    <div class="bill-row"><span>Car</span><span>${car.brand} ${car.model}</span></div>
    <div class="bill-row"><span>Days</span><span>${days}</span></div>
    <div class="bill-row"><span>Base Rent</span><span>₹${base.toLocaleString()}</span></div>
    <div class="bill-row"><span>GST (18%)</span><span>₹${tax.toFixed(2)}</span></div>
    ${coupon === 'SAVE10' ? `<div class="bill-row discount"><span>Coupon (SAVE10)</span><span>-₹${(total * 0.10).toFixed(2)}</span></div>` : ''}
    <div class="bill-row"><em style="color:#888;font-size:0.8rem;">*Registered customer 5% discount applied at confirmation</em></div>
    <div class="bill-row total"><span>Estimated Total</span><span>₹${(total - discount).toFixed(2)}+</span></div>
  `;

  pendingBill = { name, car_id: carId, days, coupon, payment_method: payment };
  document.getElementById('confirm-btn').classList.remove('hidden');
  setMsg('rent-msg', '', '');
}

async function confirmBooking() {
  const payment = document.querySelector('input[name="payment"]:checked').value;

  if (payment === 'Card') {
    const card = document.getElementById('rent-card').value.replace(/\s/g, '');
    if (card.length !== 16) { setMsg('rent-msg', 'Invalid card number. Must be 16 digits.', 'error'); return; }
  }

  const res = await fetch('/api/book', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(pendingBill)
  });
  const data = await res.json();

  if (!data.success) { setMsg('rent-msg', data.message, 'error'); return; }

  const b = data.booking;
  document.getElementById('receipt').classList.remove('hidden');
  document.getElementById('receipt').innerHTML = `
    <h3>🚗 Smart Car Rental</h3>
    <div class="subtitle">Payment Receipt</div>
    <div class="receipt-row"><span>Customer</span><span>${b.name}</span></div>
    <div class="receipt-row"><span>Car</span><span>${b.car_name}</span></div>
    <div class="receipt-row"><span>Days</span><span>${b.days}</span></div>
    <div class="receipt-row"><span>Base Rent</span><span>₹${b.base.toLocaleString()}</span></div>
    <div class="receipt-row"><span>GST (18%)</span><span>₹${b.tax.toFixed(2)}</span></div>
    <div class="receipt-row" style="color:#2e7d32"><span>Discount</span><span>-₹${b.discount.toFixed(2)}</span></div>
    <div class="receipt-row receipt-total"><span>Total Paid</span><span>₹${b.total.toLocaleString()}</span></div>
    <div class="receipt-row"><span>Payment Mode</span><span>${b.payment_method}</span></div>
    <div class="receipt-row"><span>Date</span><span>${b.date}</span></div>
    <div class="receipt-status">✔ Payment Successful</div>
    <div class="booking-id">Booking ID: ${b.booking_id}</div>
  `;

  document.getElementById('bill-preview').classList.add('hidden');
  document.getElementById('confirm-btn').classList.add('hidden');
  document.getElementById('rent-name').value = '';
  document.getElementById('rent-coupon').value = '';
  document.getElementById('rent-days').value = 1;
  setMsg('rent-msg', '', '');
  toast('🎉 Car booked successfully!');
}

// ---- Return ----
async function loadReturnCars() {
  const res = await fetch('/api/cars');
  const cars = await res.json();
  const sel = document.getElementById('return-car');
  const rented = cars.filter(c => !c.available);
  sel.innerHTML = rented.length
    ? rented.map(c => `<option value="${c.id}">ID ${c.id} — ${c.brand} ${c.model}</option>`).join('')
    : '<option value="">No cars currently rented</option>';
}

async function returnCar() {
  const carId = parseInt(document.getElementById('return-car').value);
  const lateDays = parseInt(document.getElementById('late-days').value) || 0;
  if (!carId) { setMsg('return-msg', 'No car selected.', 'error'); return; }
  const res = await fetch('/api/return', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ car_id: carId, late_days: lateDays })
  });
  const data = await res.json();
  if (data.success) {
    const fine = data.fine > 0 ? ` Late fine: ₹${data.fine}` : ' No fine.';
    setMsg('return-msg', 'Car returned successfully!' + fine, 'success');
    loadReturnCars();
    toast('Car returned!');
  } else {
    setMsg('return-msg', data.message, 'error');
  }
}

// ---- Admin ----
async function adminLogin() {
  const pass = document.getElementById('admin-pass').value;
  const res = await fetch('/api/admin/login', {
    method: 'POST', headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ password: pass })
  });
  const data = await res.json();
  if (data.success) {
    document.getElementById('admin-login-box').classList.add('hidden');
    document.getElementById('admin-panel').classList.remove('hidden');
    loadAdminData();
  } else {
    setMsg('admin-login-msg', data.message, 'error');
  }
}

async function adminLogout() {
  await fetch('/api/admin/logout', { method: 'POST' });
  document.getElementById('admin-login-box').classList.remove('hidden');
  document.getElementById('admin-panel').classList.add('hidden');
  document.getElementById('admin-pass').value = '';
}

async function loadAdminData() {
  const res = await fetch('/api/admin/data');
  const data = await res.json();

  const activeBookings = data.bookings.filter(b => b.active).length;
  document.getElementById('admin-stats').innerHTML = `
    <div class="stat-card"><div class="stat-label">Total Income</div><div class="stat-value">₹${data.total_income.toLocaleString()}</div></div>
    <div class="stat-card"><div class="stat-label">Total Bookings</div><div class="stat-value">${data.bookings.length}</div></div>
    <div class="stat-card"><div class="stat-label">Active Rentals</div><div class="stat-value">${activeBookings}</div></div>
    <div class="stat-card"><div class="stat-label">Registered Users</div><div class="stat-value">${data.users.length}</div></div>
  `;

  document.getElementById('tab-bookings').innerHTML = data.bookings.length ? `
    <table class="data-table">
      <thead><tr><th>Booking ID</th><th>Customer</th><th>Car</th><th>Days</th><th>Total</th><th>Payment</th><th>Date</th><th>Status</th></tr></thead>
      <tbody>${data.bookings.map(b => `
        <tr>
          <td><strong>${b.booking_id}</strong></td>
          <td>${b.name}</td>
          <td>${b.car_name}</td>
          <td>${b.days}</td>
          <td>₹${b.total.toLocaleString()}</td>
          <td>${b.payment_method}</td>
          <td>${b.date}</td>
          <td><span style="color:${b.active ? '#2e7d32' : '#888'}">${b.active ? '● Active' : '✔ Returned'}</span></td>
        </tr>`).join('')}
      </tbody>
    </table>` : '<p style="color:#888;padding:1rem">No bookings yet.</p>';

  document.getElementById('tab-cars-status').innerHTML = `
    <table class="data-table">
      <thead><tr><th>ID</th><th>Brand</th><th>Model</th><th>Category</th><th>Price/Day</th><th>Status</th></tr></thead>
      <tbody>${data.cars.map(c => `
        <tr>
          <td>${c.id}</td><td>${c.brand}</td><td>${c.model}</td><td>${c.category}</td>
          <td>₹${c.price.toLocaleString()}</td>
          <td><span style="color:${c.available ? '#2e7d32' : '#c62828'}">${c.available ? '✔ Available' : '✘ Rented'}</span></td>
        </tr>`).join('')}
      </tbody>
    </table>`;

  document.getElementById('tab-users').innerHTML = data.users.length ? `
    <table class="data-table">
      <thead><tr><th>Name</th><th>Phone</th><th>License</th></tr></thead>
      <tbody>${data.users.map(u => `<tr><td>${u.name}</td><td>${u.phone}</td><td>${u.license}</td></tr>`).join('')}
      </tbody>
    </table>` : '<p style="color:#888;padding:1rem">No users registered.</p>';
}

function switchTab(tab) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  document.querySelectorAll('.tab-content').forEach(c => c.classList.add('hidden'));
  event.target.classList.add('active');
  document.getElementById('tab-' + tab).classList.remove('hidden');
}