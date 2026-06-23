// ── API endpoints ─────────────────────────────────────────────
const API_CHAT    = '/api/chat';
const API_EXPLAIN = '/api/explain';

// ── DOM refs ──────────────────────────────────────────────────
const messagesEl   = document.getElementById('messages');
const messageInput = document.getElementById('message');
const sendBtn      = document.getElementById('send');
const productsEl   = document.getElementById('products');
const resultsLabel = document.getElementById('resultsLabel');
const loadingState = document.getElementById('loadingState');
const emptyState   = document.getElementById('emptyState');

// ── State ─────────────────────────────────────────────────────
let products = [];

// ── Helpers ───────────────────────────────────────────────────
function inr(n) {
  if (!n && n !== 0) return '';
  return '₹' + Number(n).toLocaleString('en-IN');
}

function platformIcon(p) {
  return {flipkart:'🛒',amazon:'📦',myntra:'👗',ajio:'✨',meesho:'💰'}[p] || '🔗';
}

function platformColor(p) {
  return {flipkart:'#2878ff',amazon:'#ff9900',myntra:'#ff3c78',ajio:'#7c5cfc',meesho:'#00d4aa'}[p] || '#888';
}

// ── Platform table ────────────────────────────────────────────
function renderPlatforms(platforms) {
  if (!platforms) return '';
  const entries = Object.entries(platforms);
  if (!entries.length) return '';

  let lowest = null;
  entries.forEach(([,d]) => {
    const v = d && d.price ? Number(d.price) : null;
    if (v && (lowest === null || v < lowest)) lowest = v;
  });

  const rows = entries.map(([name, data]) => {
    const price = data && data.price ? Number(data.price) : null;
    const url   = data && data.url   ? data.url : '#';
    const isLow = price !== null && price === lowest;
    return `
      <div class="platform-row${isLow ? ' lowest' : ''}">
        <span class="platform-icon" style="color:${platformColor(name)}">${platformIcon(name)}</span>
        <span class="platform-name">${name.charAt(0).toUpperCase() + name.slice(1)}</span>
        <span class="platform-price${isLow ? ' best' : ''}">${price ? inr(price) : '<span class="na">N/A</span>'}${isLow ? '<span class="lowest-badge">BEST</span>' : ''}</span>
        ${price ? `<a class="platform-link" href="${url}" target="_blank" rel="noopener">Visit →</a>` : '<span class="na">—</span>'}
      </div>`;
  }).join('');

  return `<div class="platform-table">
    <div class="platform-table-header">💰 Price Comparison</div>
    ${rows}
  </div>`;
}

// ── Product card ──────────────────────────────────────────────
function buildCard(product, rank) {
  const tags = (product.tags || []).slice(0, 4);
  const whyRecommended = product.why_recommended || '';
  const aiScore = product.ai_score || 0;
  const bestPlatform = product.best_platform || '';
  const bestPrice = product.best_price || product.price_inr || null;

  return `
    <article class="product-card">
      <div class="card-top">
        <div class="card-meta">
          <div class="card-name">${product.name || 'Unknown Product'}</div>
        </div>
        <div class="card-rank">${rank < 10 ? '0' + rank : rank}</div>
      </div>

      ${tags.length ? `
      <div class="card-tags">
        ${tags.map(t => `<span class="tag">${t}</span>`).join('')}
      </div>` : ''}

      ${aiScore ? `
      <div class="ai-score-row">
        <span class="ai-score-label">AI Score</span>
        <div class="ai-score-bar-bg">
          <div class="ai-score-bar" style="width:${aiScore}%"></div>
        </div>
        <span class="ai-score-val">${aiScore}/100</span>
      </div>` : ''}

      <div class="card-price-row">
        <div class="card-price">${bestPrice ? inr(bestPrice) : ''}</div>
        ${bestPlatform ? `<span class="best-platform-chip">🏆 ${bestPlatform.charAt(0).toUpperCase() + bestPlatform.slice(1)}</span>` : ''}
      </div>

      ${whyRecommended ? `
      <div class="why-box">
        <div class="why-label">💡 Why Recommended</div>
        <div class="why-text">${whyRecommended}</div>
      </div>` : ''}

      ${renderPlatforms(product.platforms)}

      <div class="card-actions">
        <button class="btn btn-accent" data-action="why" data-title="${encodeURIComponent(product.name || '')}">
          💡 Why this?
        </button>
      </div>
    </article>`;
}

// ── Render products ───────────────────────────────────────────
function renderProducts() {
  if (!products.length) {
    productsEl.innerHTML = '';
    emptyState.style.display = 'flex';
    return;
  }
  emptyState.style.display = 'none';
  productsEl.innerHTML = products.map((p, i) => buildCard(p, i + 1)).join('');
  attachCardListeners();
}

// ── Card action listeners ─────────────────────────────────────
function attachCardListeners() {
  productsEl.querySelectorAll('button[data-action]').forEach(btn => {
    btn.onclick = () => {
      const { action, title } = btn.dataset;
      if (action === 'why') explainProduct(decodeURIComponent(title));
    };
  });
}

// ── Messages ──────────────────────────────────────────────────
function addMsg(role, text) {
  const el = document.createElement('div');
  el.className = 'msg ' + role;
  el.innerHTML = typeof text === 'string' ? text : JSON.stringify(text);
  messagesEl.appendChild(el);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

// ── Typing indicator ──────────────────────────────────────────
function addTyping() {
  const el = document.createElement('div');
  el.className = 'msg assistant typing-msg';
  el.id = 'typingIndicator';
  el.innerHTML = '<div class="typing-dots"><span></span><span></span><span></span></div>';
  messagesEl.appendChild(el);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function removeTyping() {
  const el = document.getElementById('typingIndicator');
  if (el) el.remove();
}

// ── Explain product ───────────────────────────────────────────
async function explainProduct(title) {
  addMsg('user', `💡 Why this? ${title}`);
  addTyping();
  try {
    const res  = await fetch(API_EXPLAIN, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ product_name: title }),
    });
    const data = await res.json();
    removeTyping();
    const reply = data.reply;
    addMsg('assistant', typeof reply === 'string' ? reply : JSON.stringify(reply));
  } catch (e) {
    removeTyping();
    addMsg('error', String(e));
  }
}

// ── Send message ──────────────────────────────────────────────
async function sendMessage(text) {
  if (!text) return;
  addMsg('user', text);
  messageInput.value = '';
  messageInput.style.height = 'auto';
  sendBtn.disabled = true;
  sendBtn.innerHTML = '<div class="send-spinner"></div>';
  loadingState.style.display = 'flex';
  emptyState.style.display = 'none';

  try {
    const res = await fetch(API_CHAT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    });
    if (!res.ok) { addMsg('error', `Server error: ${res.status}`); return; }

    const data  = await res.json();
    const reply = data.reply;

    if (reply && typeof reply === 'object' && Array.isArray(reply.products)) {
      const count = reply.products.length;
      const summary = reply.query_summary || text;
      resultsLabel.textContent = `${count} result${count !== 1 ? 's' : ''} for "${summary}"`;
      addMsg('assistant', `Found <strong>${count}</strong> recommendation${count !== 1 ? 's' : ''} for you. Check the results panel!`);
      products = reply.products;
      renderProducts();
    } else {
      const txt = typeof reply === 'string' ? reply : JSON.stringify(reply);
      addMsg('assistant', txt);
    }
  } catch (e) {
    addMsg('error', '❌ ' + String(e));
  } finally {
    sendBtn.disabled = false;
    sendBtn.innerHTML = '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>';
    loadingState.style.display = 'none';
  }
}

// ── Quick search from landing ─────────────────────────────────
function quickSearch(query) {
  document.getElementById('landingInput').value = query;
  startApp(query);
}
window.quickSearch = quickSearch;

function startApp(query) {
  document.getElementById('landing').style.display = 'none';
  document.getElementById('appShell').style.display = 'flex';
  document.getElementById('topSearch').value = query;
  sendMessage(query);
}
window.startApp = startApp;

function quickChat(msg) {
  messageInput.value = msg;
  sendMessage(msg);
}
window.quickChat = quickChat;

// ── Initialize ────────────────────────────────────────────────
function init() {
  // Send button
  sendBtn.addEventListener('click', () => {
    const text = messageInput.value.trim();
    if (text) sendMessage(text);
  });

  messageInput.addEventListener('keydown', e => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      const text = messageInput.value.trim();
      if (text) sendMessage(text);
    }
  });

  // Auto-resize textarea
  messageInput.addEventListener('input', () => {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 100) + 'px';
  });

  // Landing search
  document.getElementById('landingSearch').addEventListener('click', () => {
    const q = document.getElementById('landingInput').value.trim();
    if (q) startApp(q);
  });
  document.getElementById('landingInput').addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      const q = e.target.value.trim();
      if (q) startApp(q);
    }
  });

  // Top bar search
  document.getElementById('topSearchBtn').addEventListener('click', () => {
    const q = document.getElementById('topSearch').value.trim();
    if (q) sendMessage(q);
  });
  document.getElementById('topSearch').addEventListener('keydown', e => {
    if (e.key === 'Enter') {
      const q = e.target.value.trim();
      if (q) sendMessage(q);
    }
  });

  // Back to landing
  document.getElementById('backBtn').addEventListener('click', () => {
    document.getElementById('appShell').style.display = 'none';
    document.getElementById('landing').style.display = 'flex';
    products = [];
    messagesEl.innerHTML = '';
    productsEl.innerHTML = '';
    resultsLabel.textContent = 'Showing results';
    emptyState.style.display = 'flex';
  });

  renderProducts();
}

init();
