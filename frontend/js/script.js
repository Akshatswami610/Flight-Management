// Format currency
function formatCurrency(amount) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
  }).format(amount)
}

// Format time
function formatTime(time) {
  return new Date(`2024-01-01 ${time}`).toLocaleTimeString("en-IN", {
    hour: "2-digit",
    minute: "2-digit",
    hour12: true,
  })
}

// Show loading state
function showLoading(element, show = true) {
  if (show) {
    element.innerHTML = '<div class="loading"></div> Loading...'
    element.style.textAlign = "center"
  } else {
    element.innerHTML = ""
  }
}

// Show status message with auto-dismiss
function showStatus(message, type = "info", duration = 5000) {
  const statusDiv = document.getElementById("status")
  if (statusDiv) {
    statusDiv.innerHTML = `<div class="status ${type}">${message}</div>`
    if (duration > 0) {
      setTimeout(() => {
        statusDiv.innerHTML = ""
      }, duration)
    }
  }
}

// Validate email
function validateEmail(email) {
  const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  return re.test(email)
}

// Validate name
function validateName(name) {
  return name.trim().length >= 3
}

// Set active nav link
function setActiveNav(page) {
  document.querySelectorAll(".nav-links a").forEach((link) => {
    link.classList.remove("active")
  })
  document.querySelector(`.nav-links a[href="${page}"]`)?.classList.add("active")
}

// Format date for display
function formatDate(dateString) {
  return new Date(dateString).toLocaleDateString("en-IN", {
    year: "numeric",
    month: "long",
    day: "numeric",
  })
}

// Format time for display
function formatDateTime(dateString) {
  return new Date(dateString).toLocaleString("en-IN", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  })
}

// Debounce function for input validation
function debounce(func, delay) {
  let timeoutId
  return (...args) => {
    clearTimeout(timeoutId)
    timeoutId = setTimeout(() => func(...args), delay)
  }
}

// Local storage with expiration
const Storage = {
  set: (key, value, expirationMinutes = null) => {
    const data = {
      value,
      timestamp: Date.now(),
      expiration: expirationMinutes ? Date.now() + expirationMinutes * 60000 : null,
    }
    localStorage.setItem(key, JSON.stringify(data))
  },
  get: (key) => {
    const data = JSON.parse(localStorage.getItem(key))
    if (!data) return null
    if (data.expiration && Date.now() > data.expiration) {
      localStorage.removeItem(key)
      return null
    }
    return data.value
  },
  remove: (key) => localStorage.removeItem(key),
}
