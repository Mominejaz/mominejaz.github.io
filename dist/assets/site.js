(() => {
  const menuButton = document.querySelector('.menu-button');
  const navigation = document.querySelector('#site-nav');
  const year = document.querySelector('#year');
  if (year) year.textContent = new Date().getFullYear();
  if (menuButton && navigation) {
    menuButton.addEventListener('click', () => { const open = navigation.classList.toggle('open'); menuButton.setAttribute('aria-expanded', String(open)); menuButton.textContent = open ? 'Close' : 'Menu'; });
    navigation.querySelectorAll('a').forEach((link) => link.addEventListener('click', () => { navigation.classList.remove('open'); menuButton.setAttribute('aria-expanded', 'false'); menuButton.textContent = 'Menu'; }));
  }
  const revealItems = document.querySelectorAll('.reveal');
  if ('IntersectionObserver' in window && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const observer = new IntersectionObserver((entries) => entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add('visible'); observer.unobserve(entry.target); } }), { threshold: 0.12 });
    revealItems.forEach((item) => observer.observe(item));
  } else revealItems.forEach((item) => item.classList.add('visible'));
  const filters = document.querySelectorAll('[data-filter]'); const projects = document.querySelectorAll('[data-category]'); const count = document.querySelector('#project-count');
  filters.forEach((filter) => filter.addEventListener('click', () => { const category = filter.dataset.filter; let visible = 0; filters.forEach((button) => button.setAttribute('aria-pressed', String(button === filter))); projects.forEach((project) => { const show = category === 'all' || project.dataset.category === category; project.classList.toggle('is-hidden', !show); if (show) visible += 1; }); if (count) count.textContent = `Showing ${visible} project${visible === 1 ? '' : 's'}`; }));
  const sections = [...document.querySelectorAll('main section[id]')]; const navLinks = [...document.querySelectorAll('nav a[href^="#"]')];
  if ('IntersectionObserver' in window && navLinks.length) { const navObserver = new IntersectionObserver((entries) => entries.forEach((entry) => { if (!entry.isIntersecting) return; navLinks.forEach((link) => link.classList.toggle('active', link.getAttribute('href') === `#${entry.target.id}`)); }), { rootMargin: '-35% 0px -55% 0px', threshold: 0 }); sections.forEach((section) => navObserver.observe(section)); }
})();
