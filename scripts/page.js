(function () {
  var links = Array.prototype.slice.call(document.querySelectorAll('a[data-n]'));
  var box = document.getElementById('lightbox');
  var img = document.getElementById('lb-img');
  var info = document.getElementById('lb-info');
  var bar = document.getElementById('lb-bar');
  var cur = -1, opener = null;

  function show(i) {
    cur = (i + links.length) % links.length;
    var a = links[cur];
    img.width = +a.dataset.w; img.height = +a.dataset.h;
    img.src = a.href;
    img.alt = 'Frame ' + a.dataset.n + ', ' + a.dataset.chapter;
    info.textContent = 'frame ' + a.dataset.n + ' · ' + a.dataset.chapter + ' · ' + (cur + 1) + ' of ' + links.length;
    bar.style.width = ((cur + 1) / links.length * 100) + '%';
    [cur - 1, cur + 1].forEach(function (j) {
      new Image().src = links[(j + links.length) % links.length].href;
    });
    history.replaceState(null, '', '#f' + a.dataset.n);
  }
  function open(i) {
    opener = document.activeElement;
    box.hidden = false;
    if (!box.open) { try { box.show(); } catch (e) { box.setAttribute('open', ''); } }
    document.body.classList.add('lb-open');
    show(i);
    document.getElementById('lb-close').focus();
  }
  function close() {
    box.hidden = true; box.removeAttribute('open');
    document.body.classList.remove('lb-open');
    img.removeAttribute('src');
    history.replaceState(null, '', location.pathname + location.search);
    if (opener && opener.focus) opener.focus();
  }

  links.forEach(function (a, i) {
    a.addEventListener('click', function (e) { e.preventDefault(); open(i); });
  });
  document.getElementById('lb-close').addEventListener('click', close);
  document.getElementById('lb-prev').addEventListener('click', function () { show(cur - 1); });
  document.getElementById('lb-next').addEventListener('click', function () { show(cur + 1); });
  document.addEventListener('keydown', function (e) {
    if (box.hidden) return;
    if (e.key === 'ArrowLeft') show(cur - 1);
    else if (e.key === 'ArrowRight') show(cur + 1);
    else if (e.key === 'Escape') { e.preventDefault(); close(); }
    else if (e.key === 'Home') show(0);
    else if (e.key === 'End') show(links.length - 1);
  });
  var x0 = null;
  box.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  box.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0; x0 = null;
    if (Math.abs(dx) > 40) show(cur + (dx < 0 ? 1 : -1));
  });

  var m = /^#f(\d{4})$/.exec(location.hash);
  if (m) {
    for (var i = 0; i < links.length; i++) if (links[i].dataset.n === m[1]) { open(i); break; }
  }

  // current chapter highlight
  if ('IntersectionObserver' in window) {
    var idx = {};
    document.querySelectorAll('.index a').forEach(function (a) { idx[a.dataset.target] = a; });
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) {
          Object.keys(idx).forEach(function (k) { idx[k].classList.remove('active'); });
          idx[e.target.id].classList.add('active');
        }
      });
    }, { rootMargin: '-30% 0px -60% 0px' });
    document.querySelectorAll('.chapter').forEach(function (s) { io.observe(s); });
  }
})();
