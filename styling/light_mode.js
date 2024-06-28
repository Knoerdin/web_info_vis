function enforceLightMode() {
    // Remove theme switcher, disallowing dark mode.
    const switchButton = document.querySelector('.theme-switch-button');
    if (typeof switchButton !== 'undefined') {
      switchButton.remove();
    }
  
    // Enforce light mode, because that is when our story looks the best :)
    if (document.querySelector('html').getAttribute('data-theme') !== 'light') {
      // Switch theme right now.
      document.querySelector('html').setAttribute('data-theme', 'light')
  
      // Set light mode to be permanent for future visits.
      localStorage.setItem('mode', 'light');
      localStorage.setItem('theme', 'light');
  
    }
  }
  
  window.addEventListener('load', enforceLightMode);