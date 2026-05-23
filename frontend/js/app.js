// frontend/js/app.js — Fully API-driven dashboard

const API_BASE = window.location.origin; // works when served by FastAPI
let sentimentChartInstance = null;

// ==================== BOOT & NAVIGATION ====================
document.addEventListener('DOMContentLoaded', () => {
    // 1. Initial Load
    loadDashboard();

    // 2. Selectors logic
    document.getElementById('gameSelector').addEventListener('change', () => loadDashboard());
    document.getElementById('dateSelector').addEventListener('change', () => loadDashboard());

    // 3. Sidebar Navigation Logic
    const navItems = document.querySelectorAll('.nav-item');
    navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            // Remove active from all nav items
            navItems.forEach(n => n.classList.remove('active'));
            // Add active to clicked nav item
            item.classList.add('active');

            // Hide all views
            document.querySelectorAll('.view-section').forEach(view => {
                view.classList.remove('active');
            });

            // Show target view
            const targetId = item.getAttribute('data-target');
            document.getElementById(targetId).classList.add('active');
        });
    });
});

function getSelectedGame() { return document.getElementById('gameSelector').value; }
function getSelectedDays() { return document.getElementById('dateSelector').value; }

async function loadDashboard() {
    const game = getSelectedGame();
    const days = getSelectedDays();
    await Promise.all([
        loadStats(game, days),
        loadLogs(game, days),
        loadChart(game, days),
    ]);
    renderMockHeatmap();
}

// ==================== KPI CARDS ====================
async function loadStats(game, days) {
    let url = `${API_BASE}/api/dashboard/stats?days=${days}`;
    if (game) url += `&game=${game}`;

    try {
        const res = await fetch(url);
        const d = await res.json();

        document.getElementById('kpiTotal').textContent = d.total_posts.toLocaleString();
        document.getElementById('kpiTotalSub').textContent = game ? `Filtered: ${game}` : 'All competitors combined';

        const s = d.avg_sentiment;
        document.getElementById('kpiSentiment').textContent = (s >= 0 ? '+' : '') + s.toFixed(2);
        document.getElementById('kpiSentiment').className = 'kpi-value ' + (s > 0.2 ? 'text-green' : s < -0.2 ? 'text-red' : '');
        document.getElementById('kpiSentimentSub').textContent = s > 0.2 ? 'Leaning Positive' : s < -0.2 ? 'Leaning Negative' : 'Neutral';

        document.getElementById('kpiChurn').textContent = d.churn_count;
        document.getElementById('kpiChurnSub').textContent = `${Math.round(d.churn_count / (d.total_posts || 1) * 100)}% of total posts`;

        document.getElementById('kpiLoyalty').textContent = d.loyalty_count;
        document.getElementById('kpiLoyaltySub').textContent = `${Math.round(d.loyalty_count / (d.total_posts || 1) * 100)}% of total posts`;
    } catch (e) {
        console.error('Stats fetch failed', e);
        document.getElementById('kpiTotal').textContent = '—';
    }
}

// ==================== AUDIT TABLE ====================
async function loadLogs(game, days) {
    let url = `${API_BASE}/api/dashboard/logs?limit=40&days=${days}`;
    if (game) url += `&game=${game}`;

    const tbody = document.getElementById('auditTableBody');

    try {
        const res = await fetch(url);
        const logs = await res.json();

        if (!logs.length) {
            tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:30px; color:#718096;">No data for this filter.</td></tr>';
            return;
        }

        tbody.innerHTML = '';
        logs.forEach(row => {
            const tagClass = getTagClass(row.category);
            const gameName = { lostark: 'Lost Ark', tl: 'TL', black: 'Black Desert', aion2: 'Aion 2' }[row.game_name] || row.game_name;

            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>
                    <span class="score-value" style="color:${row.score > 0 ? 'var(--success)' : row.score < 0 ? 'var(--danger)' : 'var(--text-main)'}">${row.score > 0 ? '+' + row.score : row.score}</span>
                    <span class="vote-count">▲ ${row.upvotes.toLocaleString()}</span>
                </td>
                <td style="font-weight:600; font-size:12px;">${gameName}</td>
                <td><span class="tag ${tagClass}">${row.category}</span></td>
                <td><div class="snippet">"${row.text}"</div></td>
                <td class="reasoning">${row.reasoning}</td>
                <td style="font-weight:600; font-size:13px; white-space:nowrap;">${row.signal}</td>
            `;
            tbody.appendChild(tr);
        });
    } catch (e) {
        console.error('Logs fetch failed', e);
        tbody.innerHTML = '<tr><td colspan="6" style="text-align:center; padding:30px; color:#e53e3e;">⚠ Backend API not running. Start server first.</td></tr>';
    }
}

function getTagClass(category) {
    const map = {
        'Combat_Mechanics': 'tag-combat',
        'Monetization': 'tag-mtx',
        'Server_Stability': 'tag-server',
        'Graphics_Optimization': 'tag-graphics',
    };
    return map[category] || 'tag-combat';
}

// ==================== CHART ====================
async function loadChart(game, days) {
    let url = `${API_BASE}/api/dashboard/sentiment-trend?days=${days}`;
    if (game) url += `&game=${game}`;

    try {
        const res = await fetch(url);
        const data = await res.json();

        const labels = data.map(d => d.category.replace('_', ' '));
        const scores = data.map(d => d.avg_score);
        const counts = data.map(d => d.count);

        const colors = scores.map(s => s > 0 ? 'rgba(56, 161, 105, 0.8)' : 'rgba(229, 62, 62, 0.8)');
        const borders = scores.map(s => s > 0 ? '#38a169' : '#e53e3e');

        // Destroy old chart if exists
        if (sentimentChartInstance) sentimentChartInstance.destroy();

        const ctx = document.getElementById('sentimentChart').getContext('2d');
        sentimentChartInstance = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Avg Sentiment',
                    data: scores,
                    backgroundColor: colors,
                    borderColor: borders,
                    borderWidth: 1,
                    borderRadius: 6,
                    barPercentage: 0.5,
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                indexAxis: 'y',
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            afterLabel: (ctx) => `${counts[ctx.dataIndex]} posts analyzed`
                        }
                    }
                },
                scales: {
                    x: {
                        min: -1, max: 1,
                        grid: { color: '#e2e8f0' },
                        ticks: { color: '#718096', font: { family: "'Inter', sans-serif" } }
                    },
                    y: {
                        grid: { display: false },
                        ticks: { color: '#1a202c', font: { family: "'Inter', sans-serif", weight: '600' } }
                    }
                }
            }
        });
    } catch (e) {
        console.error('Chart fetch failed', e);
    }
}

// ==================== MOCK HEATMAP GEN ====================
function renderMockHeatmap() {
    const container = document.getElementById('heatmapContainer');
    if(!container) return;
    
    // Generate dummy heatmap data based on currently selected game
    const topics = ["Combat Balance", "P2W MTX", "Server Lag", "Graphics Optimization", "Event Rewards", "New Raid"];
    let html = "";
    
    topics.forEach(topic => {
        // Random sentiment score between -1 and 1
        const score = (Math.random() * 2 - 1);
        
        let color;
        if(score > 0.5) color = "#38a169"; // Green
        else if (score > 0) color = "#68d391"; // Light Green
        else if (score > -0.5) color = "#fc8181"; // Light Red
        else color = "#e53e3e"; // Red
        
        html += `
            <div class="heat-box" style="background-color: ${color};">
                <div style="font-size: 14px; margin-bottom: 5px; opacity: 0.9;">${topic}</div>
                <div style="font-size: 24px; font-weight: bold;">${score > 0 ? '+'+score.toFixed(2) : score.toFixed(2)}</div>
            </div>
        `;
    });
    
    container.innerHTML = html;
}
