const retrievalUrl = "../outputs/sample_retrieval_results.json";
const briefUrl = "../outputs/sample_ceo_departure_answer.md";

const els = {
  runMeta: document.querySelector("#run-meta"),
  analogCount: document.querySelector("#analog-count"),
  analogList: document.querySelector("#analog-list"),
  pathwayGrid: document.querySelector("#pathway-grid"),
  evidenceList: document.querySelector("#evidence-list"),
  analystBrief: document.querySelector("#analyst-brief"),
  limitList: document.querySelector("#limit-list"),
};

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function sentenceCase(value) {
  const text = String(value).replaceAll("_", " ");
  return text.charAt(0).toUpperCase() + text.slice(1);
}

function renderAnalogs(cases) {
  els.analogCount.textContent = `${cases.length} cases`;
  els.analogList.innerHTML = cases
    .map((item) => {
      const reasons = item.selection_reasons
        .map((reason) => `<li>${escapeHtml(reason)}</li>`)
        .join("");

      return `
        <article class="analog-card">
          <div class="analog-top">
            <div>
              <div class="company">${escapeHtml(item.company)}</div>
              <div class="ticker">${escapeHtml(item.ticker)} · ${escapeHtml(item.sector)}</div>
            </div>
            <div class="score">Score ${escapeHtml(item.score)}</div>
          </div>
          <p class="meta-line">${escapeHtml(item.departure_type)} · ${escapeHtml(item.observed_pathway)}</p>
          <ul class="reason-list">${reasons}</ul>
        </article>
      `;
    })
    .join("");
}

function renderPathways(pathways) {
  els.pathwayGrid.innerHTML = pathways
    .map((item) => {
      const cases = item.companies
        .map((company) => `<span class="case-chip">${escapeHtml(company)}</span>`)
        .join("");

      return `
        <article class="pathway-card">
          <h3>${escapeHtml(sentenceCase(item.pathway))}</h3>
          <p>${escapeHtml(item.interpretation)}</p>
          <div class="case-chip-row" aria-label="${escapeHtml(item.pathway)} companies">${cases}</div>
        </article>
      `;
    })
    .join("");
}

function renderEvidence(cases) {
  els.evidenceList.innerHTML = cases
    .map(
      (item) => `
        <div class="source-item">
          <strong>${escapeHtml(item.company)}</strong>
          <a href="${escapeHtml(item.source_url)}" target="_blank" rel="noreferrer">
            Source reference
          </a>
        </div>
      `,
    )
    .join("");
}

function renderLimitations(limitations) {
  els.limitList.innerHTML = limitations.map((item) => `<li>${escapeHtml(item)}</li>`).join("");
}

function renderMarkdown(markdown) {
  const lines = markdown.split("\n");
  const html = [];
  let listOpen = false;

  function closeList() {
    if (listOpen) {
      html.push("</ul>");
      listOpen = false;
    }
  }

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) {
      closeList();
      continue;
    }

    if (trimmed.startsWith("# ")) {
      closeList();
      html.push(`<h1>${escapeHtml(trimmed.slice(2))}</h1>`);
    } else if (trimmed.startsWith("## ")) {
      closeList();
      html.push(`<h2>${escapeHtml(trimmed.slice(3))}</h2>`);
    } else if (trimmed.startsWith("- ")) {
      if (!listOpen) {
        html.push("<ul>");
        listOpen = true;
      }
      html.push(`<li>${escapeHtml(trimmed.slice(2))}</li>`);
    } else {
      closeList();
      html.push(`<p>${escapeHtml(trimmed)}</p>`);
    }
  }

  closeList();
  els.analystBrief.innerHTML = html.join("");
}

function renderError(error) {
  const message = `
    <div class="error">
      Dashboard data did not load. Serve the repository root with
      <code>python3 -m http.server 8000</code> and open
      <code>http://localhost:8000/dashboard/</code>.
      <br />
      ${escapeHtml(error.message)}
    </div>
  `;
  els.runMeta.textContent = "Data load failed";
  els.analogList.innerHTML = message;
}

async function loadDashboard() {
  try {
    const [retrievalResponse, briefResponse] = await Promise.all([
      fetch(retrievalUrl),
      fetch(briefUrl),
    ]);

    if (!retrievalResponse.ok) {
      throw new Error(`Could not load ${retrievalUrl}`);
    }
    if (!briefResponse.ok) {
      throw new Error(`Could not load ${briefUrl}`);
    }

    const retrieval = await retrievalResponse.json();
    const brief = await briefResponse.text();

    renderAnalogs(retrieval.retrieved_cases);
    renderPathways(retrieval.observed_pathways);
    renderEvidence(retrieval.retrieved_cases);
    renderLimitations(retrieval.limitations);
    renderMarkdown(brief);

    els.runMeta.textContent = `${retrieval.retrieved_cases.length} analogs · ${retrieval.observed_pathways.length} pathways`;
  } catch (error) {
    renderError(error);
  }
}

loadDashboard();
