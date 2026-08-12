// In React, a component is just a function that returns JSX (HTML-like syntax).
// This component receives 'results' as a prop — data passed down from the parent.
// Props are React's way of passing data from parent components to children.
function MetricsBar({ results }) {

    // Plain JavaScript array methods to count each threat level.
    // .filter() returns only the items matching the condition,
    // .length gives us the count.
    const total = results.length;
    const critical = results.filter((r) => r.threat_level === "CRITICAL").length;
    const suspicious = results.filter((r) => r.threat_level === "SUSPICIOUS").length;
    const safe = results.filter((r) => r.threat_level === "SAFE").length;

    return (
        <div className="metrics-bar">
            <div className="metric-card">
                <span className="metric-value">{total}</span>
                <span className="metric-label">Total Logs</span>
            </div>
            <div className="metric-card critical">
                <span className="metric-value">{critical}</span>
                <span className="metric-label">Critical</span>
            </div>
            <div className="metric-card suspicious">
                <span className="metric-value">{suspicious}</span>
                <span className="metric-label">Suspicious</span>
            </div>
            <div className="metric-card safe">
                <span className="metric-value">{safe}</span>
                <span className="metric-label">Safe</span>
            </div>
        </div>
    );
}

export default MetricsBar;