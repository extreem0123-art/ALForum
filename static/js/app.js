// App state
const state = {
  schedule: null,
  speakers: null,
  faq: null,
  venue: null,
  currentDay: 0,
  tg: null
};

// Initialize app
document.addEventListener('DOMContentLoaded', async () => {
  try {
    // Initialize Telegram WebApp
    initTelegram();
    
    // Load data
    await loadData();
    
    // Render initial state
    renderSchedule();
    renderSpeakers();
    renderFAQ();
    renderVenue();
    
    // Set up event listeners
    setupEventListeners();
    
  } catch (error) {
    console.error('App initialization failed:', error);
    showError('Ошибка загрузки приложения. Пожалуйста, обновите страницу.');
  }
});

// Telegram WebApp initialization
function initTelegram() {
  try {
    if (window.Telegram && window.Telegram.WebApp) {
      state.tg = window.Telegram.WebApp;
      state.tg.ready();
      state.tg.expand();
      state.tg.setHeaderColor("#0a0a0f");
      state.tg.setBackgroundColor("#0a0a0f");
      
      // Check if running in Telegram
      if (!state.tg.isExpanded) {
        state.tg.expand();
      }
    } else {
      console.warn('Telegram WebApp not available');
      // Show warning for non-Telegram environments
      const warning = document.createElement('div');
      warning.className = 'error-message';
      warning.textContent = 'Приложение работает только в Telegram WebApp';
      document.body.insertBefore(warning, document.body.firstChild);
    }
  } catch (error) {
    console.error('Telegram initialization failed:', error);
  }
}

// Data loading
async function loadData() {
  try {
    const [scheduleRes, speakersRes, faqRes, venueRes] = await Promise.all([
      fetch('./data/schedule.json'),
      fetch('./data/speakers.json'),
      fetch('./data/faq.json'),
      fetch('./data/venue.json')
    ]);
    
    if (!scheduleRes.ok || !speakersRes.ok || !faqRes.ok || !venueRes.ok) {
      throw new Error('Failed to load data');
    }
    
    state.schedule = await scheduleRes.json();
    state.speakers = await speakersRes.json();
    state.faq = await faqRes.json();
    state.venue = await venueRes.json();
    
  } catch (error) {
    console.error('Data loading failed:', error);
    throw error;
  }
}

// Event listeners
function setupEventListeners() {
  // Navigation
  window.switchPage = (name, btn) => {
    document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.nav-btn').forEach(b => b.classList.remove('active'));
    document.getElementById('page-' + name).classList.add('active');
    btn.classList.add('active');
    window.scrollTo(0, 0);
  };
  
  // Schedule day switching
  window.switchDay = (idx, btn) => {
    state.currentDay = idx;
    document.querySelectorAll('.day-tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.schedule-day').forEach(d => d.classList.remove('active'));
    btn.classList.add('active');
    document.getElementById('day-' + idx).classList.add('active');
    renderSchedule();
  };
  
  // FAQ toggle
  window.toggleFaq = (btn) => {
    const item = btn.closest('.faq-item');
    const isOpen = item.classList.contains('open');
    document.querySelectorAll('.faq-item').forEach(i => i.classList.remove('open'));
    if (!isOpen) item.classList.add('open');
  };
  
  // Map navigation
  window.openMaps = () => {
    const url = state.venue.maps_url;
    if (state.tg && state.tg.openLink) {
      state.tg.openLink(url);
    } else {
      window.open(url, '_blank');
    }
  };
}

// Render functions
function renderSchedule() {
  if (!state.schedule) return;
  
  const event = state.schedule.event;
  const day = state.schedule.days[state.currentDay];
  
  // Update hero section
  updateHero(event);
  
  // Update stats
  updateStats(event.stats);
  
  // Render day tabs
  renderDayTabs(state.schedule.days);
  
  // Render schedule
  renderDaySchedule(day);
}

function updateHero(event) {
  const heroLabel = document.querySelector('.hero-label');
  const heroTitle = document.querySelector('.hero h1');
  const heroDate = document.querySelector('.hero-meta-item:nth-child(1)');
  const heroLocation = document.querySelector('.hero-meta-item:nth-child(2)');
  
  if (heroLabel) heroLabel.textContent = '⚡ Конференция 2026';
  if (heroTitle) {
    heroTitle.innerHTML = event.name.replace('ALFA', '<span>ALFA</span>');
  }
  if (heroDate) {
    const dateIcon = heroDate.querySelector('svg');
    heroDate.innerHTML = dateIcon.outerHTML + event.date;
  }
  if (heroLocation) {
    const locationIcon = heroLocation.querySelector('svg');
    heroLocation.innerHTML = locationIcon.outerHTML + event.location + 
      '<span class="live-badge"><span class="pulse-dot"></span>Live</span>';
  }
}

function updateStats(stats) {
  const statNums = document.querySelectorAll('.stat-num');
  const statLabels = document.querySelectorAll('.stat-label');
  
  if (statNums[0]) statNums[0].textContent = stats.talks;
  if (statNums[1]) statNums[1].textContent = stats.speakers;
  if (statNums[2]) statNums[2].textContent = stats.days;
  
  if (statLabels[0]) statLabels[0].textContent = 'Докладов';
  if (statLabels[1]) statLabels[1].textContent = 'Спикеров';
  if (statLabels[2]) statLabels[2].textContent = 'День';
}

function renderDayTabs(days) {
  const container = document.querySelector('.day-tabs');
  if (!container || !days) return;
  
  container.innerHTML = '';
  days.forEach((day, index) => {
    const btn = document.createElement('button');
    btn.className = `day-tab ${index === 0 ? 'active' : ''}`;
    btn.textContent = day.name;
    btn.onclick = () => window.switchDay(index, btn);
    container.appendChild(btn);
  });
}

function renderDaySchedule(day) {
  const container = document.getElementById('day-' + day.id);
  if (!container || !day) return;
  
  container.innerHTML = '';
  
  day.events.forEach((event, index) => {
    const timeSlot = document.createElement('div');
    timeSlot.className = 'time-slot';
    if (index > 0) timeSlot.style.marginTop = '8px';
    
    // Time column
    const timeCol = document.createElement('div');
    timeCol.className = 'time-col';
    
    const timeText = document.createElement('div');
    timeText.className = 'time-text';
    timeText.textContent = event.time;
    
    const timeDot = document.createElement('div');
    timeDot.className = 'time-dot';
    if (event.type === 'keynote') timeDot.style.background = 'var(--accent)';
    if (event.type === 'break') timeDot.style.background = 'var(--muted)';
    
    const timeLine = document.createElement('div');
    timeLine.className = 'time-line';
    
    timeCol.appendChild(timeText);
    timeCol.appendChild(timeDot);
    timeCol.appendChild(timeLine);
    
    // Event card
    const eventCard = document.createElement('div');
    eventCard.className = `event-card ${event.type} ${event.type === 'break' ? 'break' : ''}`;
    eventCard.style.marginBottom = '0';
    
    // Event tag
    const eventTag = document.createElement('span');
    eventTag.className = `event-tag tag-${event.type}`;
    
    switch(event.type) {
      case 'keynote':
        eventTag.textContent = 'Keynote';
        break;
      case 'talk':
        eventTag.textContent = 'Доклад';
        break;
      case 'workshop':
        eventTag.textContent = 'Воркшоп';
        break;
      case 'break':
        eventTag.textContent = 'Перерыв';
        break;
    }
    
    // Event title
    const eventTitle = document.createElement('div');
    eventTitle.className = 'event-title';
    eventTitle.textContent = event.title;
    
    // Event room
    const eventRoom = document.createElement('div');
    eventRoom.className = 'event-room';
    eventRoom.textContent = event.room || '';
    
    // Speaker info
    const eventSpeaker = document.createElement('div');
    eventSpeaker.className = 'event-speaker';
    
    if (event.speaker) {
      const speakerAva = document.createElement('div');
      speakerAva.className = 'speaker-ava-placeholder';
      speakerAva.textContent = getInitials(event.speaker.name);
      
      const speakerName = document.createElement('span');
      speakerName.className = 'speaker-name';
      speakerName.textContent = `${event.speaker.name} · ${event.speaker.company}`;
      
      eventSpeaker.appendChild(speakerAva);
      eventSpeaker.appendChild(speakerName);
    }
    
    eventCard.appendChild(eventTag);
    eventCard.appendChild(eventRoom);
    eventCard.appendChild(eventTitle);
    if (event.speaker) eventCard.appendChild(eventSpeaker);
    
    timeSlot.appendChild(timeCol);
    timeSlot.appendChild(eventCard);
    container.appendChild(timeSlot);
  });
  
  // Add bottom spacing
  const spacer = document.createElement('div');
  spacer.style.height = '20px';
  container.appendChild(spacer);
}

function renderSpeakers() {
  if (!state.speakers) return;
  
  const container = document.querySelector('.speakers-grid');
  if (!container) return;
  
  container.innerHTML = '';
  
  state.speakers.forEach(speaker => {
    const card = document.createElement('div');
    card.className = `speaker-card ${speaker.featured ? 'featured' : ''}`;
    
    if (speaker.featured) {
      // Featured speaker layout
      const photo = document.createElement('div');
      photo.className = 'speaker-photo';
      photo.style.backgroundImage = `url(${speaker.avatar})`;
      photo.textContent = speaker.avatar.includes('dicebear') ? getInitials(speaker.name) : '';
      
      const info = document.createElement('div');
      
      if (speaker.badge) {
        const badge = document.createElement('div');
        badge.className = 'speaker-badge';
        badge.textContent = speaker.badge;
        info.appendChild(badge);
      }
      
      const name = document.createElement('div');
      name.className = 'speaker-card-name';
      name.textContent = speaker.name;
      
      const role = document.createElement('div');
      role.className = 'speaker-card-role';
      role.textContent = speaker.company;
      
      const topics = document.createElement('div');
      topics.className = 'speaker-topics';
      speaker.topics.forEach(topic => {
        const pill = document.createElement('span');
        pill.className = 'topic-pill';
        pill.textContent = topic;
        topics.appendChild(pill);
      });
      
      info.appendChild(name);
      info.appendChild(role);
      info.appendChild(topics);
      
      card.appendChild(photo);
      card.appendChild(info);
    } else {
      // Regular speaker layout
      const photo = document.createElement('div');
      photo.className = 'speaker-photo';
      photo.style.backgroundImage = `url(${speaker.avatar})`;
      photo.textContent = speaker.avatar.includes('dicebear') ? getInitials(speaker.name) : '';
      
      const name = document.createElement('div');
      name.className = 'speaker-card-name';
      name.textContent = speaker.name;
      
      const role = document.createElement('div');
      role.className = 'speaker-card-role';
      role.textContent = speaker.company;
      
      const topics = document.createElement('div');
      topics.className = 'speaker-topics';
      speaker.topics.forEach(topic => {
        const pill = document.createElement('span');
        pill.className = 'topic-pill';
        pill.textContent = topic;
        topics.appendChild(pill);
      });
      
      card.appendChild(photo);
      card.appendChild(name);
      card.appendChild(role);
      card.appendChild(topics);
    }
    
    container.appendChild(card);
  });
  
  // Add bottom spacing
  const spacer = document.createElement('div');
  spacer.style.height = '20px';
  container.parentNode.appendChild(spacer);
}

function renderFAQ() {
  if (!state.faq) return;
  
  const container = document.querySelector('.faq-list');
  if (!container) return;
  
  container.innerHTML = '';
  
  state.faq.forEach((item, index) => {
    const faqItem = document.createElement('div');
    faqItem.className = 'faq-item';
    
    const question = document.createElement('button');
    question.className = 'faq-q';
    question.onclick = () => window.toggleFaq(question);
    
    const qText = document.createElement('span');
    qText.textContent = item.question;
    
    const icon = document.createElement('span');
    icon.className = 'faq-icon';
    icon.textContent = '+';
    
    question.appendChild(qText);
    question.appendChild(icon);
    
    const answer = document.createElement('div');
    answer.className = 'faq-a';
    
    const answerInner = document.createElement('div');
    answerInner.className = 'faq-a-inner';
    answerInner.textContent = item.answer;
    
    answer.appendChild(answerInner);
    
    faqItem.appendChild(question);
    faqItem.appendChild(answer);
    
    container.appendChild(faqItem);
  });
}

function renderVenue() {
  if (!state.venue) return;
  
  const venueName = document.querySelector('.venue-name');
  const venueAddress = document.querySelector('.venue-address');
  const transportGrid = document.querySelector('.transport-grid');
  const mapBtn = document.querySelector('.map-btn');
  
  if (venueName) venueName.textContent = state.venue.name;
  if (venueAddress) venueAddress.textContent = state.venue.address;
  
  if (transportGrid) {
    transportGrid.innerHTML = '';
    state.venue.transport.forEach(transport => {
      const item = document.createElement('div');
      item.className = 'transport-item';
      
      const icon = document.createElement('div');
      icon.className = 'transport-icon';
      icon.textContent = transport.icon;
      
      const title = document.createElement('div');
      title.className = 'transport-title';
      title.textContent = transport.title;
      
      const desc = document.createElement('div');
      desc.className = 'transport-desc';
      desc.textContent = transport.description;
      
      item.appendChild(icon);
      item.appendChild(title);
      item.appendChild(desc);
      
      transportGrid.appendChild(item);
    });
  }
  
  if (mapBtn) {
    mapBtn.onclick = window.openMaps;
  }
}

// Utility functions
function getInitials(name) {
  return name
    .split(' ')
    .map(word => word[0])
    .join('')
    .toUpperCase()
    .slice(0, 2);
}

function showError(message) {
  const errorDiv = document.createElement('div');
  errorDiv.className = 'error-message';
  errorDiv.textContent = message;
  
  const main = document.querySelector('main') || document.body;
  main.insertBefore(errorDiv, main.firstChild);
}

// Loading state
function showLoading() {
  const loading = document.createElement('div');
  loading.className = 'loading';
  loading.innerHTML = '<div class="spinner"></div>';
  document.body.appendChild(loading);
}

function hideLoading() {
  const loading = document.querySelector('.loading');
  if (loading) loading.remove();
}