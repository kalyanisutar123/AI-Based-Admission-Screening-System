/* ============================================================
   app.js — Shared utilities: navbar, theme, auth, API helpers
   ============================================================ */

const API_BASE = "/api";   // Use relative path — works on any host/port

// ── Theme ──────────────────────────────────────────────────────────────────────
function initTheme() {
  const saved = localStorage.getItem("theme") || "light";
  document.documentElement.setAttribute("data-theme", saved);
  updateThemeToggle(saved);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
  updateThemeToggle(next);
}

function updateThemeToggle(theme) {
  const knob = document.querySelector(".theme-toggle-knob");
  if (knob) knob.textContent = theme === "dark" ? "🌙" : "☀️";
}

// ── Toast ──────────────────────────────────────────────────────────────────────
function showToast(message, type = "info", duration = 3500) {
  let container = document.getElementById("toast-container");
  if (!container) {
    container = document.createElement("div");
    container.id = "toast-container";
    document.body.appendChild(container);
  }
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerHTML = `<strong>${type === "success" ? "✓" : type === "error" ? "✗" : "ℹ"}</strong> ${message}`;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.style.transform = "translateX(120%)";
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// ── Session helpers ────────────────────────────────────────────────────────────
// FIX: session now stores { username, role } — login.html saves username from input
function getSession() {
  try { return JSON.parse(localStorage.getItem("admitiq_session") || "null"); }
  catch { return null; }
}
function setSession(data) { localStorage.setItem("admitiq_session", JSON.stringify(data)); }
function clearSession()   { localStorage.removeItem("admitiq_session"); }
function isLoggedIn()     { return !!getSession(); }
function isAdmin()        { const s = getSession(); return s && s.role === "admin"; }

// ── Build Navbar ───────────────────────────────────────────────────────────────
function buildNavbar() {
  const nav = document.getElementById("main-navbar");
  if (!nav) return;
  const session = getSession();
  const page = window.location.pathname.split("/").pop() || "index.html";

  nav.innerHTML = `
    <a href="index.html" class="navbar-brand">
      <span class="logo-icon">🎓</span>
      AdmitIQ
    </a>
    <ul class="navbar-nav" id="nav-links">
      <li><a href="index.html"    class="nav-link ${page === 'index.html'    || page === '' ? 'active' : ''}">Home</a></li>
      <li><a href="colleges.html" class="nav-link ${page === 'colleges.html'              ? 'active' : ''}">Colleges</a></li>
      <li><a href="form.html"     class="nav-link ${page === 'form.html'                  ? 'active' : ''}">Apply Now</a></li>
      ${session && session.role === "admin"
        ? `<li><a href="admin.html" class="nav-link ${page === 'admin.html' ? 'active' : ''}">Admin</a></li>`
        : ""}
    </ul>
    <div class="navbar-actions">
      <button class="theme-toggle" onclick="toggleTheme()" title="Toggle theme" aria-label="Toggle theme">
        <span class="theme-toggle-knob">☀️</span>
      </button>
      ${session
        ? `<span class="text-sm text-muted">Hi, <strong>${session.username}</strong></span>
           <button class="btn btn-ghost" onclick="logout()" style="font-size:.85rem;padding:.4rem .8rem">Logout</button>`
        : `<a href="login.html"           class="btn btn-outline" style="font-size:.85rem;padding:.4rem .9rem">Login</a>
           <a href="login.html#register"  class="btn btn-primary" style="font-size:.85rem;padding:.4rem .9rem">Register</a>`
      }
    </div>`;
  updateThemeToggle(document.documentElement.getAttribute("data-theme"));
}

// ── Logout ─────────────────────────────────────────────────────────────────────
async function logout() {
  try { await fetch(`${API_BASE}/logout`, { method: "POST" }); }
  catch (_) { /* ignore network errors — still clear local session */ }
  clearSession();
  window.location.href = "index.html";
}

// ── Password visibility toggle ─────────────────────────────────────────────────
function togglePassword(inputId, btn) {
  const input = document.getElementById(inputId);
  if (!input) return;
  if (input.type === "password") {
    input.type = "text";
    btn.textContent = "🙈";
  } else {
    input.type = "password";
    btn.textContent = "👁️";
  }
}

// ── API helpers ────────────────────────────────────────────────────────────────
async function apiPost(endpoint, body) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
    credentials: "same-origin",
  });
  return res.json();
}

async function apiGet(endpoint) {
  const res = await fetch(`${API_BASE}${endpoint}`, {
    credentials: "same-origin",
  });
  return res.json();
}

// ── Form validation helpers ────────────────────────────────────────────────────
function showError(id, msg) {
  const el = document.getElementById(id);
  if (el) { el.textContent = msg; el.classList.add("show"); }
}
function clearError(id) {
  const el = document.getElementById(id);
  if (el) { el.textContent = ""; el.classList.remove("show"); }
}
function clearAllErrors() {
  document.querySelectorAll(".form-error").forEach(el => {
    el.textContent = "";
    el.classList.remove("show");
  });
}

// ── Init on every page ─────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  buildNavbar();
});