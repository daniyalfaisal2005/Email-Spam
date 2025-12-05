"""
Email Spam Detection System - Web-based GUI with Tabs
Run: python web_gui_tabbed.py
Then open: http://localhost:5000 in your browser
"""

from flask import Flask, render_template_string, request, jsonify, send_file
import json
import os
import sys
from datetime import datetime
from io import StringIO

# Add project root to path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from data.email_parser import EmailParser
from core.directed_graph import DirectedEmailGraph
from detection.spam_scorer import SpamScorer
from detection.spam_classifier import SpamClassifier
import algorithms.metrics.network_metrics as network_metrics
import algorithms.shortest_paths as shortest_paths

app = Flask(__name__)
current_data = None


# HTML Template
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Email Spam Detection System</title>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/chart.js@3.9.1/dist/chart.min.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.3);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .header p { font-size: 1.1em; opacity: 0.9; }
        .subtitle { font-size: 0.95em; opacity: 0.85; margin-top: 8px; }
        
        /* Tab Navigation */
        .tab-container {
            display: flex;
            border-bottom: 2px solid #dee2e6;
            background: #f8f9fa;
            padding: 0;
        }
        
        .tab-button {
            flex: 1;
            padding: 18px 20px;
            border: none;
            background: transparent;
            cursor: pointer;
            font-size: 1em;
            font-weight: 500;
            color: #666;
            border-bottom: 3px solid transparent;
            transition: all 0.3s;
            text-align: center;
        }
        
        .tab-button:hover {
            background: #e9ecef;
            color: #667eea;
        }
        
        .tab-button.active {
            color: #667eea;
            border-bottom-color: #667eea;
            background: white;
        }
        
        /* Tab Content */
        .tab-content {
            display: none;
            animation: fadeIn 0.3s;
        }
        
        .tab-content.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        
        .content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 25px;
        }
        
        .content.full-grid {
            grid-template-columns: 1fr;
        }
        
        .content.single-col {
            grid-template-columns: 1fr;
        }
        
        .panel {
            background: #f8f9fa;
            border-radius: 8px;
            padding: 20px;
            border: 1px solid #dee2e6;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .panel h2 {
            color: #667eea;
            margin-bottom: 15px;
            font-size: 1.3em;
            border-bottom: 2px solid #667eea;
            padding-bottom: 10px;
        }
        
        .form-group {
            margin-bottom: 15px;
        }
        
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 500;
            color: #333;
            font-size: 0.95em;
        }
        
        select, input, textarea {
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1em;
        }
        
        button {
            background: #667eea;
            color: white;
            padding: 12px 20px;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1em;
            font-weight: 500;
            width: 100%;
            transition: background 0.3s;
        }
        
        button:hover { background: #764ba2; }
        button:disabled { background: #ccc; cursor: not-allowed; }
        
        .stat {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 12px 18px;
            margin: 5px;
            border-radius: 5px;
            text-align: center;
            min-width: 100px;
            font-size: 0.95em;
        }
        
        .stat-number { font-size: 1.6em; font-weight: bold; }
        .stat-label { font-size: 0.85em; opacity: 0.9; }
        
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
            font-size: 0.95em;
        }
        
        th, td {
            padding: 10px;
            text-align: left;
            border-bottom: 1px solid #ddd;
        }
        
        th {
            background: #667eea;
            color: white;
            font-weight: 600;
        }
        
        tr:hover { background: #f5f5f5; }
        
        .spam { color: #dc3545; font-weight: bold; }
        .suspicious { color: #ff9800; font-weight: bold; }
        .legitimate { color: #28a745; font-weight: bold; }
        
        .loading {
            text-align: center;
            padding: 20px;
            color: #667eea;
            font-weight: 500;
        }
        
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .success { color: #28a745; }
        .error { color: #dc3545; }
        
        /* Graph visualization styling */
        #network {
            width: 100%;
            height: 600px;
            border: 1px solid #ddd;
            border-radius: 5px;
            background: white;
        }
        
        .graph-legend {
            margin-top: 15px;
            font-size: 0.9em;
        }
        
        .legend-item {
            display: inline-block;
            margin-right: 20px;
            margin-bottom: 8px;
        }
        
        .legend-color {
            display: inline-block;
            width: 15px;
            height: 15px;
            border-radius: 50%;
            margin-right: 5px;
            vertical-align: middle;
        }
        
        /* Chart container */
        .chart-container {
            position: relative;
            height: 300px;
            margin-top: 15px;
        }
        
        .metrics-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            margin-top: 15px;
        }
        
        .metric-box {
            background: white;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #667eea;
        }
        
        .metric-label {
            font-size: 0.85em;
            color: #666;
            margin-bottom: 5px;
        }
        
        .metric-value {
            font-size: 1.5em;
            font-weight: bold;
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Email Spam Detection System</h1>
            <p>Advanced Graph Theory Application with Network Visualization</p>
            <div class="subtitle">Graph Algorithms: Dijkstra • MST • Centrality • Connected Components • Vertex Coloring</div>
        </div>
        
        <!-- Tab Navigation -->
        <div class="tab-container">
            <button class="tab-button active" onclick="switchTab('data')">📁 Data & Load</button>
            <button class="tab-button" onclick="switchTab('visualization')">🕸️ Network Graph</button>
            <button class="tab-button" onclick="switchTab('analysis')">📊 Analysis</button>
            <button class="tab-button" onclick="switchTab('threats')">⚠️ Threats</button>
            <button class="tab-button" onclick="switchTab('pathfinder')">🛣️ Dijkstra</button>
        </div>
        
        <!-- TAB 1: Data & Load -->
        <div id="data" class="tab-content active">
            <div class="content single-col">
                <div class="panel">
                    <h2>📁 Load Dataset</h2>
                    <div class="form-group">
                        <label>Select Sample Dataset:</label>
                        <select id="dataset">
                            <option value="demo" selected>🔍 Demo (Small - 13 emails, 1 Spammer)</option>
                            <option value="legitimate">✓ Legitimate (16 emails, 1 Suspicious)</option>
                            <option value="broadcast">📡 Broadcast Spam (13 emails, 1 Heavy Spammer)</option>
                            <option value="ring">🔄 Ring Spam (14 emails, 1 Suspicious)</option>
                            <option value="combined">📦 All Combined (25 emails, Spam + Suspicious)</option>
                        </select>
                    </div>
                    <button onclick="loadDataset()">🔄 Load Dataset</button>
                    <div id="loadStatus" style="margin-top: 15px;"></div>
                </div>
                
                <div class="panel">
                    <h2>📊 Quick Statistics</h2>
                    <div id="stats"></div>
                </div>
                
                <div class="panel">
                    <h2>📈 Classification Breakdown</h2>
                    <div class="chart-container">
                        <canvas id="classificationChart"></canvas>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- TAB 2: Network Visualization -->
        <div id="visualization" class="tab-content">
            <div class="content full-grid">
                <div class="panel">
                    <h2>🕸️ Email Network Graph Visualization</h2>
                    <p style="font-size: 0.9em; color: #666; margin-bottom: 10px;">
                        Nodes = Email addresses | Edges = Email connections | Colors = Classification | Size = Threat Score
                    </p>
                    <div id="network"></div>
                    <div class="graph-legend">
                        <div class="legend-item"><div class="legend-color" style="background: #dc3545;"></div><strong>Spam</strong> (score ≥ 80)</div>
                        <div class="legend-item"><div class="legend-color" style="background: #ff9800;"></div><strong>Suspicious</strong> (40-80)</div>
                        <div class="legend-item"><div class="legend-color" style="background: #28a745;"></div><strong>Legitimate</strong> (< 40)</div>
                        <div class="legend-item" style="margin-top: 8px;"><span style="font-size: 0.8em; color: #666;">● Larger nodes = Higher threat score | Arrows = Email direction</span></div>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- TAB 3: Analysis -->
        <div id="analysis" class="tab-content">
            <div class="content">
                <div class="panel">
                    <h2>🔍 Graph Theory Metrics</h2>
                    <div id="metrics"></div>
                </div>
            </div>
        </div>
        
        <!-- TAB 4: Top Threats -->
        <div id="threats" class="tab-content">
            <div class="content full-grid">
                <div class="panel">
                    <h2>⚠️ Top Threat Candidates</h2>
                    <p style="font-size: 0.85em; color: #666; margin-bottom: 15px;">Email addresses ranked by spam detection score (Degree Ratio: out-degree / in-degree)</p>
                    <div id="topSpam"></div>
                </div>
            </div>
        </div>
        
        <!-- TAB 5: Dijkstra Pathfinder -->
        <div id="pathfinder" class="tab-content">
            <div class="content single-col">
                <div class="panel">
                    <h2>🛣️ Dijkstra Shortest Path Finder</h2>
                    <p style="font-size: 0.9em; color: #666; margin-bottom: 15px;">Find the shortest communication path between any two email addresses in the network.</p>
                    
                    <div style="background: #e7f3ff; border: 1px solid #b3d9ff; padding: 12px; border-radius: 5px; margin-bottom: 15px; font-size: 0.9em;">
                        <strong>💡 Tip:</strong> Use arrow keys to navigate text fields. Examples: <code>spammer1@example.com</code>, <code>alice@example.com</code>
                    </div>
                    
                    <div class="form-group">
                        <label>Source Email:</label>
                        <input type="text" id="pathFrom" placeholder="e.g., spammer1@example.com" autocomplete="off">
                    </div>
                    <div class="form-group">
                        <label>Target Email:</label>
                        <input type="text" id="pathTo" placeholder="e.g., alice@example.com" autocomplete="off">
                    </div>
                    <button onclick="findPath()">🔗 Find Shortest Path</button>
                    <div id="pathResult" style="margin-top: 20px;"></div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let network = null;
        let classificationChart = null;
        
        function switchTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(tab => tab.classList.remove('active'));
            document.querySelectorAll('.tab-button').forEach(btn => btn.classList.remove('active'));
            
            // Show selected tab
            document.getElementById(tabName).classList.add('active');
            event.target.classList.add('active');
            
            // If switching to visualization, trigger graph update
            if (tabName === 'visualization') {
                setTimeout(() => {
                    if (network) network.fit();
                }, 100);
            }
        }
        
        function loadDataset() {
            const dataset = document.getElementById('dataset').value;
            document.getElementById('loadStatus').innerHTML = '<div class="loading"><div class="spinner"></div>Loading...</div>';
            
            fetch('/api/load-dataset/' + dataset)
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        document.getElementById('loadStatus').innerHTML = '<div class="success">✓ ' + data.message + '</div>';
                        updateDisplay();
                    } else {
                        document.getElementById('loadStatus').innerHTML = '<div class="error">✗ ' + data.error + '</div>';
                    }
                })
                .catch(e => document.getElementById('loadStatus').innerHTML = '<div class="error">✗ ' + e + '</div>');
        }
        
        function updateDisplay() {
            updateStats();
            updateClassificationChart();
            updateNetworkGraph();
            updateMetrics();
            updateTopSpam();
        }
        
        function updateStats() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    let html = '';
                    html += '<div class="stat"><div class="stat-number">' + data.total_nodes + '</div><div class="stat-label">Nodes</div></div>';
                    html += '<div class="stat"><div class="stat-number">' + data.total_emails + '</div><div class="stat-label">Emails</div></div>';
                    html += '<div class="stat"><div class="stat-number">' + data.spam + '</div><div class="stat-label">Spam</div></div>';
                    html += '<div class="stat"><div class="stat-number">' + data.suspicious + '</div><div class="stat-label">Suspicious</div></div>';
                    html += '<div class="stat"><div class="stat-number">' + data.legitimate + '</div><div class="stat-label">Legitimate</div></div>';
                    document.getElementById('stats').innerHTML = html;
                });
        }
        
        function updateClassificationChart() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    const ctx = document.getElementById('classificationChart').getContext('2d');
                    
                    if (classificationChart) {
                        classificationChart.destroy();
                    }
                    
                    classificationChart = new Chart(ctx, {
                        type: 'doughnut',
                        data: {
                            labels: ['Spam', 'Suspicious', 'Legitimate'],
                            datasets: [{
                                data: [data.spam, data.suspicious, data.legitimate],
                                backgroundColor: ['#dc3545', '#ff9800', '#28a745'],
                                borderColor: ['#bb2d3b', '#e67e22', '#20c997'],
                                borderWidth: 2
                            }]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            plugins: {
                                legend: { position: 'bottom', labels: { font: { size: 12 }, padding: 15 } }
                            }
                        }
                    });
                });
        }
        
        function updateNetworkGraph() {
            fetch('/api/graph-data')
                .then(r => r.json())
                .then(data => {
                    const nodes = new vis.DataSet(data.nodes);
                    const edges = new vis.DataSet(data.edges);
                    
                    const container = document.getElementById('network');
                    const graphData = { nodes: nodes, edges: edges };
                    
                    const options = {
                        physics: {
                            enabled: true,
                            barnesHut: { gravitationalConstant: -30000, centralGravity: 0.3, springLength: 200, springConstant: 0.04 },
                            maxVelocity: 50,
                            solver: 'barnesHut',
                            timestep: 0.5
                        },
                        interaction: {
                            hover: true,
                            tooltipDelay: 100,
                            navigationButtons: true,
                            keyboard: true
                        },
                        nodes: {
                            font: { size: 14, face: 'Tahoma', color: '#fff' },
                            borderWidth: 2,
                            borderWidthSelected: 3
                        },
                        edges: {
                            color: { color: '#999', highlight: '#667eea', opacity: 0.6 },
                            width: 1.5,
                            smooth: { type: 'continuous' },
                            arrows: { to: { enabled: true, scaleFactor: 0.5 } },
                            font: { size: 10 }
                        }
                    };
                    
                    if (network) {
                        network.destroy();
                    }
                    network = new vis.Network(container, graphData, options);
                });
        }
        
        function updateMetrics() {
            fetch('/api/metrics')
                .then(r => r.json())
                .then(data => {
                    let html = '<div class="metrics-grid">';
                    html += '<div class="metric-box"><div class="metric-label">Network Density</div><div class="metric-value">' + data.density.toFixed(4) + '</div></div>';
                    html += '<div class="metric-box"><div class="metric-label">Diameter</div><div class="metric-value">' + data.diameter + '</div></div>';
                    html += '<div class="metric-box"><div class="metric-label">Clustering Coeff</div><div class="metric-value">' + data.clustering.toFixed(4) + '</div></div>';
                    html += '<div class="metric-box"><div class="metric-label">Triangles</div><div class="metric-value">' + data.triangles + '</div></div>';
                    html += '</div>';
                    html += '<p style="margin-top: 15px; font-size: 0.9em; color: #666;"><strong>Interpretation:</strong> Network density indicates sparsity, diameter shows max distance, clustering coefficient reveals triangle structures.</p>';
                    document.getElementById('metrics').innerHTML = html;
                });
        }
        
        function updateTopSpam() {
            fetch('/api/top-spam')
                .then(r => r.json())
                .then(data => {
                    let html = '<table><tr><th>Email Address</th><th>Score</th><th>Classification</th></tr>';
                    data.slice(0, 15).forEach(row => {
                        let cls = row.score >= 80 ? 'spam' : row.score >= 40 ? 'suspicious' : 'legitimate';
                        html += '<tr><td style="font-size: 0.9em;">' + row.email + '</td><td>' + row.score.toFixed(1) + '</td><td class="' + cls + '">' + row.classification + '</td></tr>';
                    });
                    html += '</table>';
                    document.getElementById('topSpam').innerHTML = html;
                });
        }
        
        function findPath() {
            const from = document.getElementById('pathFrom').value;
            const to = document.getElementById('pathTo').value;
            
            if (!from || !to) {
                document.getElementById('pathResult').innerHTML = '<div class="error">✗ Enter both source and target emails</div>';
                return;
            }
            
            document.getElementById('pathResult').innerHTML = '<div class="loading"><div class="spinner"></div>Finding shortest path...</div>';
            
            fetch('/api/dijkstra', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({source: from, target: to})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    let html = '<div class="panel" style="background: #d4edda; border: 2px solid #28a745;">';
                    html += '<div class="success">✓ Path Found!</div>';
                    html += '<p><strong>Distance:</strong> ' + data.distance.toFixed(2) + '</p>';
                    html += '<p><strong>Number of Hops:</strong> ' + data.hops + ' hop' + (data.hops !== 1 ? 's' : '') + '</p>';
                    html += '<p style="word-break: break-all; margin-top: 15px;"><strong>Communication Route:</strong><br><span style="background: #f0f0f0; padding: 10px; border-radius: 5px; display: block; margin-top: 10px; font-size: 0.95em;">' + data.path.join(' → ') + '</span></p>';
                    html += '</div>';
                    document.getElementById('pathResult').innerHTML = html;
                } else if (data.reverse_path) {
                    let html = '<div class="panel" style="background: #fff3cd; border: 2px solid #ffc107;">';
                    html += '<div style="color: #ff9800;"><strong>⚠️ No direct path found</strong></div>';
                    html += '<p style="margin-top: 10px;"><strong>Reverse path exists:</strong></p>';
                    html += '<p><strong>Distance:</strong> ' + data.reverse_distance.toFixed(2) + '</p>';
                    html += '<p><strong>Hops:</strong> ' + data.reverse_hops + '</p>';
                    html += '<p style="word-break: break-all; margin-top: 15px;"><strong>Reverse Route:</strong><br><span style="background: #f0f0f0; padding: 10px; border-radius: 5px; display: block; margin-top: 10px; font-size: 0.95em;">' + data.reverse_path.join(' → ') + '</span></p>';
                    html += '<p style="margin-top: 15px; font-size: 0.9em;"><strong>💡 Tip:</strong> ' + data.suggestion + '</p>';
                    html += '</div>';
                    document.getElementById('pathResult').innerHTML = html;
                } else {
                    let html = '<div class="panel" style="background: #f8d7da; border: 2px solid #dc3545;">';
                    html += '<div class="error">✗ No communication path found</div>';
                    html += '<p style="margin-top: 10px;">' + data.message + '</p>';
                    if (data.all_nodes) {
                        html += '<p style="margin-top: 15px; font-size: 0.9em;"><strong>Available addresses (' + data.total_nodes + ' total):</strong><br>' + data.all_nodes + '</p>';
                    }
                    html += '</div>';
                    document.getElementById('pathResult').innerHTML = html;
                }
            })
            .catch(e => document.getElementById('pathResult').innerHTML = '<div class="error">✗ Error: ' + e + '</div>');
        }
        
        // Load on start
        window.onload = function() {
            loadDataset();
        };
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    """Main page"""
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/load-dataset/<name>')
def load_dataset(name):
    """Load sample dataset"""
    datasets = {
        'demo': 'data/datasets/demo_small.csv',
        'legitimate': 'data/datasets/legitimate.csv',
        'broadcast': 'data/datasets/mixed_with_broadcast.csv',
        'ring': 'data/datasets/mixed_with_ring.csv',
        'combined': 'data/datasets/all_combined.csv'
    }
    
    if name not in datasets:
        return jsonify({'error': 'Unknown dataset'}), 404
    
    file_path = datasets[name]
    if not os.path.exists(file_path):
        return jsonify({'error': 'Dataset not found'}), 404
    
    try:
        global current_data
        
        emails = EmailParser.parse_csv(file_path)
        graph = DirectedEmailGraph()
        graph.add_emails_batch(emails)
        
        scorer = SpamScorer(graph)
        scores = scorer.calculate_all_scores()
        
        classifier = SpamClassifier()
        classification = classifier.get_classification_summary(scores)
        
        nx_graph = graph.to_networkx()
        metrics = {
            'density': network_metrics.network_density(graph),
            'diameter': network_metrics.diameter(graph),
            'clustering': network_metrics.average_clustering_coefficient(graph),
            'triangles': network_metrics.number_of_triangles(graph),
        }
        
        current_data = {
            'graph': graph,
            'emails': emails,
            'scores': scores,
            'classification': classification,
            'metrics': metrics,
            'nx_graph': nx_graph
        }
        
        return jsonify({
            'success': True,
            'message': f'Loaded {name} dataset',
            'emails': len(emails),
            'nodes': len(scores)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats')
def get_stats():
    """Get statistics"""
    if current_data is None:
        return jsonify({'error': 'No data loaded'}), 400
    
    classification = current_data['classification']
    return jsonify({
        'total_emails': len(current_data['emails']),
        'total_nodes': len(current_data['scores']),
        'spam': classification['spam_count'],
        'suspicious': classification['suspicious_count'],
        'legitimate': classification['legitimate_count']
    })


@app.route('/api/top-spam')
def get_top_spam():
    """Get top spam candidates"""
    if current_data is None:
        return jsonify({'error': 'No data loaded'}), 400
    
    scores = current_data['scores']
    results = []
    
    for node, score in scores.items():
        classification = 'Spam' if score >= 80 else 'Suspicious' if score >= 40 else 'Legitimate'
        results.append({
            'email': node,
            'score': score,
            'classification': classification
        })
    
    results.sort(key=lambda x: x['score'], reverse=True)
    return jsonify(results[:15])


@app.route('/api/metrics')
def get_metrics():
    """Get network metrics"""
    if current_data is None:
        return jsonify({'error': 'No data loaded'}), 400
    
    metrics = current_data['metrics']
    return jsonify({
        'density': metrics['density'],
        'diameter': metrics['diameter'],
        'clustering': metrics['clustering'],
        'triangles': metrics['triangles']
    })


@app.route('/api/dijkstra', methods=['POST'])
def dijkstra():
    """Find shortest path"""
    if current_data is None:
        return jsonify({'error': 'No data loaded'}), 400
    
    try:
        data = request.json
        source = data.get('source').strip() if data.get('source') else None
        target = data.get('target').strip() if data.get('target') else None
        
        if not source or not target:
            return jsonify({'success': False, 'message': 'Please enter both source and target emails'}), 400
        
        graph = current_data['graph']
        nodes = graph.get_nodes()
        
        # Check if nodes exist
        if source not in nodes:
            return jsonify({'success': False, 'message': f'Source "{source}" not found in network. Available senders: {", ".join(nodes[:5])}...'}), 404
        if target not in nodes:
            return jsonify({'success': False, 'message': f'Target "{target}" not found in network. Available receivers: {", ".join(nodes[:5])}...'}), 404
        
        # Try forward path
        path, distance = shortest_paths.dijkstra_shortest_path(graph, source, target)
        
        if path:
            return jsonify({
                'success': True,
                'path': path,
                'distance': distance,
                'hops': len(path) - 1,
                'direction': 'forward'
            })
        
        # If no path found, try reverse direction
        path_reverse, distance_reverse = shortest_paths.dijkstra_shortest_path(graph, target, source)
        
        if path_reverse:
            # Reverse the path to show user perspective
            return jsonify({
                'success': False,
                'message': f'No direct path from {source} to {target}, but reverse path exists!',
                'reverse_path': path_reverse,
                'reverse_distance': distance_reverse,
                'reverse_hops': len(path_reverse) - 1,
                'suggestion': f'Try searching: {target} → {source}'
            })
        
        # No path in either direction
        all_nodes = ', '.join(nodes)
        return jsonify({
            'success': False,
            'message': f'No communication path between {source} and {target}. These nodes may be in different network clusters.',
            'all_nodes': all_nodes,
            'total_nodes': len(nodes)
        }), 404
            
    except Exception as e:
        import traceback
        print(f"Error in dijkstra: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


@app.route('/api/graph-data')
def get_graph_data():
    """Get graph visualization data"""
    if current_data is None:
        return jsonify({'nodes': [], 'edges': []}), 400
    
    try:
        graph = current_data['graph']
        scores = current_data['scores']
        
        # Color map for classifications
        def get_color(score):
            if score >= 80:
                return {'background': '#dc3545', 'border': '#bb2d3b'}  # Red - Spam
            elif score >= 40:
                return {'background': '#ff9800', 'border': '#e67e22'}  # Orange - Suspicious
            else:
                return {'background': '#28a745', 'border': '#20c997'}  # Green - Legitimate
        
        # Create nodes
        nodes = []
        max_score = max(scores.values()) if scores else 1
        min_score = min(scores.values()) if scores else 0
        
        for node, score in scores.items():
            # Node size based on spam score (higher score = bigger node)
            size = 20 + (score / max_score * 40) if max_score > 0 else 20
            color = get_color(score)
            
            nodes.append({
                'id': node,
                'label': node[:20],  # Truncate long names
                'title': f'{node}\nScore: {score:.1f}',
                'color': color,
                'size': size,
                'font': {'size': 12, 'face': 'Tahoma', 'color': '#fff'}
            })
        
        # Create edges from NetworkX graph
        edges = []
        nx_graph = graph.to_networkx()
        
        for source, target, data in nx_graph.edges(data=True):
            weight = data.get('weight', 1)
            edges.append({
                'from': source,
                'to': target,
                'weight': weight,
                'title': f'Weight: {weight}',
                'color': {'color': '#999999', 'opacity': 0.5},
                'width': min(weight * 2, 5)  # Edge width based on weight
            })
        
        return jsonify({
            'nodes': nodes,
            'edges': edges
        })
        
    except Exception as e:
        import traceback
        print(f"Error in get_graph_data: {str(e)}")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("\n" + "="*70)
    print("  EMAIL SPAM DETECTION SYSTEM - WEB INTERFACE")
    print("="*70)
    print("\n[OK] Flask server starting...")
    print("[OK] Open your browser to: http://localhost:5000")
    print("\nFeatures:")
    print("  • 5 Organized Tabs (Data, Graph, Analysis, Threats, Dijkstra)")
    print("  • Interactive email network visualization")
    print("  • Network metrics dashboard")
    print("  • Dijkstra shortest path finder")
    print("  • Real-time spam analysis")
    print("\n[INFO] Press Ctrl+C to stop\n")
    print("="*70 + "\n")
    
    app.run(debug=False, host='localhost', port=5000)
