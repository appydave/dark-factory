/* Mochaccino Copy Kit — shared across dark-factory designs.
 *
 * Per-page config (set BEFORE this script loads):
 *   window.COPYKIT_CONFIG = { blocks: "<css selector>", title: "<page title>" };
 *
 * Behaviour:
 *   - injects a checkbox chip into each block matching `blocks`
 *   - floating toolbar: select-all · "Copy selected (N)" · "Copy all"
 *   - copies selected blocks to the clipboard as markdown (# title / ## section / text)
 *   - re-scans after async render (MutationObserver) so JS-rendered pages work too
 */
(function () {
  'use strict';

  var CFG   = window.COPYKIT_CONFIG || {};
  var SEL   = CFG.blocks || null;
  var TITLE = CFG.title || document.title || 'Mochaccino view';
  var bar, toast, busy = false, t;

  function blocks() {
    return SEL ? Array.prototype.slice.call(document.querySelectorAll(SEL)) : [];
  }

  function isDark(el) {
    var bg = getComputedStyle(el).backgroundColor || '';
    var m = bg.match(/\d+/g);
    if (!m) return false;
    var lum = (0.299 * m[0] + 0.587 * m[1] + 0.114 * m[2]);
    return lum < 90;
  }

  function labelFor(el, i) {
    if (el.getAttribute('data-copy-title')) return el.getAttribute('data-copy-title');
    var inner = el.querySelector(
      '.wf-name,.lens-label,.probe-title,.stage-name,.card-title,.design-title,' +
      '.hero-title,.med-verb,.section-label,.lineage-title,.converge-head,.xcard-head,' +
      '.verdict-head,h1,h2,h3,h4'
    );
    if (inner && inner.textContent.trim()) return inner.textContent.trim().replace(/\s+/g, ' ');
    var prev = el.previousElementSibling;
    while (prev) {
      if (/^H[2-4]$/.test(prev.tagName)) return prev.textContent.trim().replace(/\s+/g, ' ');
      if (prev.tagName === 'H1') break;
      prev = prev.previousElementSibling;
    }
    return 'Section ' + (i + 1);
  }

  function ensureChip(el) {
    if (el.querySelector(':scope > .copykit-chip')) return;
    if (getComputedStyle(el).position === 'static') el.style.position = 'relative';
    var lab = document.createElement('label');
    lab.className = 'copykit-chip' + (isDark(el) ? ' on-dark' : '');
    lab.setAttribute('title', 'Select this section for copy');
    var cb = document.createElement('input');
    cb.type = 'checkbox';
    cb.addEventListener('change', updateCount);
    lab.appendChild(cb);
    lab.addEventListener('click', function (e) { e.stopPropagation(); });
    el.appendChild(lab);
  }

  function cbOf(el) {
    var c = el.querySelector(':scope > .copykit-chip input');
    return c || null;
  }

  function checkedBlocks() {
    return blocks().filter(function (b) { var c = cbOf(b); return c && c.checked; });
  }

  function blockText(b) {
    // innerText is layout-aware (good line breaks); chip is a bare checkbox so adds nothing.
    var t = b.innerText || b.textContent || '';
    return t.replace(/[ \t]+\n/g, '\n').replace(/\n{3,}/g, '\n\n').trim();
  }

  function buildMarkdown(list) {
    var out = '# ' + TITLE + '\n\n';
    list.forEach(function (b, i) {
      out += '## ' + labelFor(b, i) + '\n' + blockText(b) + '\n\n';
    });
    return out.trim() + '\n';
  }

  function doCopy(text, label) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard.writeText(text).then(
        function () { showToast(label, text); },
        function () { legacyCopy(text, label); }
      );
    } else {
      legacyCopy(text, label);
    }
  }

  function legacyCopy(text, label) {
    var ta = document.createElement('textarea');
    ta.value = text;
    ta.style.position = 'fixed'; ta.style.top = '-9999px';
    document.body.appendChild(ta); ta.focus(); ta.select();
    try { document.execCommand('copy'); showToast(label, text); }
    catch (e) { window.prompt('Copy manually:', text); }
    ta.remove();
  }

  function showToast(label, text) {
    if (!toast) {
      toast = document.createElement('div');
      toast.className = 'copykit-toast';
      document.body.appendChild(toast);
    }
    var kb = Math.max(1, Math.round(text.length / 1024));
    toast.textContent = '✓ Copied ' + label + ' · ~' + kb + 'KB to clipboard';
    toast.classList.add('show');
    clearTimeout(toast._t);
    toast._t = setTimeout(function () { toast.classList.remove('show'); }, 2200);
  }

  function updateCount() {
    if (!bar) return;
    var total = blocks().length;
    var n = checkedBlocks().length;
    bar.querySelector('.ck-count').textContent = n + ' / ' + total + ' selected';
    var master = bar.querySelector('.ck-all input');
    if (master) master.checked = (n > 0 && n === total);
  }

  function buildBar(total) {
    if (bar) { updateCount(); return; }
    bar = document.createElement('div');
    bar.className = 'copykit-bar';
    bar.innerHTML =
      '<label class="ck-all"><input type="checkbox"> all</label>' +
      '<span class="ck-count">0 / ' + total + ' selected</span>' +
      '<button class="ck-copy">Copy selected</button>' +
      '<button class="ck-all-btn">Copy all</button>';
    document.body.appendChild(bar);

    bar.querySelector('.ck-all input').addEventListener('change', function (e) {
      var on = e.target.checked;
      blocks().forEach(function (b) { var c = cbOf(b); if (c) c.checked = on; });
      updateCount();
    });
    bar.querySelector('.ck-copy').addEventListener('click', function () {
      var list = checkedBlocks();
      if (!list.length) list = blocks();          // nothing ticked → copy everything
      doCopy(buildMarkdown(list), list.length + ' section' + (list.length > 1 ? 's' : ''));
    });
    bar.querySelector('.ck-all-btn').addEventListener('click', function () {
      var list = blocks();
      doCopy(buildMarkdown(list), 'all ' + list.length + ' sections');
    });
  }

  function mount() {
    if (busy) return;
    busy = true;
    var bs = blocks();
    bs.forEach(ensureChip);
    buildBar(bs.length);
    updateCount();
    setTimeout(function () { busy = false; }, 0);
  }

  function schedule() { clearTimeout(t); t = setTimeout(mount, 180); }

  if (document.readyState !== 'loading') mount();
  else document.addEventListener('DOMContentLoaded', mount);
  window.addEventListener('load', schedule);

  // JS-rendered pages (01/02/03) build their DOM after fetch — re-scan on mutations.
  if (window.MutationObserver) {
    new MutationObserver(function () { if (!busy) schedule(); })
      .observe(document.body, { childList: true, subtree: true });
  }
})();
