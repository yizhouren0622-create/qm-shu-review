(function () {
  "use strict";
  const root = document.querySelector('.formula-guide');
  if (!root) return;
  const activeLink = document.querySelector('.site-links a[data-page="formulas.html"]');
  if (activeLink) {
    activeLink.classList.add('is-active');
    activeLink.setAttribute('aria-current', 'page');
  }
  const siteTop = document.querySelector('.site-top');
  const menuButton = document.querySelector('.site-menu-btn');
  if (siteTop && menuButton) {
    menuButton.addEventListener('click', () => {
      menuButton.setAttribute('aria-expanded', String(siteTop.classList.toggle('open')));
    });
    for (const link of siteTop.querySelectorAll('.site-links a')) {
      link.addEventListener('click', () => {
        siteTop.classList.remove('open');
        menuButton.setAttribute('aria-expanded', 'false');
      });
    }
  }
      const guide = root.querySelector('.guide');
      const input = root.querySelector('input');
      const select = root.querySelector('select');
      const buttons = [...root.querySelectorAll('[data-filter]')];
      const articles = [...root.querySelectorAll('article')];
      const expand = root.querySelector('.expand');
      let filter = 'all';
      const refresh = () => {
        const query = input.value.trim().toLocaleLowerCase();
        let count = 0;
        for (const card of articles) {
          const chapter = card.closest('.chapter').dataset.chapter;
          const show = (filter === 'all' || chapter === filter) && (!query || card.dataset.search.includes(query));
          card.hidden = !show;
          if (show) count++;
        }
        for (const chapter of root.querySelectorAll('.chapter')) chapter.hidden = ![...chapter.querySelectorAll('article')].some(card => !card.hidden);
        root.querySelector('.empty').hidden = count > 0;
        root.querySelector('.results').textContent = select.value === 'zh' ? `显示 ${count} / ${articles.length} 组公式` : select.value === 'en' ? `${count} of ${articles.length} formula groups` : `${count} / ${articles.length} 组公式 · formula groups`;
        const visible = articles.filter(card => !card.hidden);
        const allOpen = visible.length > 0 && visible.every(card => card.querySelector('details').open);
        expand.disabled = visible.length === 0;
        expand.textContent = allOpen ? (select.value === 'zh' ? '收起全部例题' : select.value === 'en' ? 'Close all examples' : '收起全部例题 / Close all examples') : (select.value === 'zh' ? '展开全部例题' : select.value === 'en' ? 'Open all examples' : '展开全部例题 / Open all examples');
        expand.setAttribute('aria-expanded',String(allOpen));
      };
      input.addEventListener('input',refresh);
      select.addEventListener('change',() => { guide.dataset.view = select.value; refresh(); });
      for (const button of buttons) button.addEventListener('click',() => {
        filter = button.dataset.filter;
        for (const other of buttons) other.setAttribute('aria-pressed',String(other === button));
        refresh();
      });
      expand.addEventListener('click',() => {
        const visible = articles.filter(card => !card.hidden);
        const open = !visible.every(card => card.querySelector('details').open);
        for (const card of visible) card.querySelector('details').open = open;
        refresh();
      });
      for (const details of root.querySelectorAll('details')) details.addEventListener('toggle',refresh);
      refresh();
})();
