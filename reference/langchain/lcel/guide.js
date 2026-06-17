async function initGuideSearch() {
  const input = document.getElementById("guide-search");
  const countEl = document.getElementById("search-count");
  const cards = [...document.querySelectorAll("[data-guide-item]")];

  if (!input || cards.length === 0) {
    return;
  }

  let index = [];
  try {
    const res = await fetch("guide_index.json");
    index = (await res.json()).items || [];
  } catch (_) {
    index = [];
  }

  function filter() {
    const q = input.value.trim().toLowerCase();
    let visible = 0;

    cards.forEach((card) => {
      const tags = (card.dataset.tags || "").toLowerCase();
      const title = (card.dataset.title || "").toLowerCase();
      const body = card.textContent.toLowerCase();
      const match = !q || title.includes(q) || tags.includes(q) || body.includes(q);
      card.dataset.hidden = match ? "false" : "true";
      if (match) visible += 1;
    });

    if (countEl) {
      countEl.textContent = q ? `${visible} of ${cards.length}` : `${cards.length} items`;
    }
  }

  input.addEventListener("input", filter);
  filter();
}