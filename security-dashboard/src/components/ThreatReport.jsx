function ThreatReport({ log }) {
    // If no log has been selected yet, show a placeholder instead of crashing.
    // This is a common React pattern called a "guard clause" —
    // handle the empty/null case early and return before using the data.
    if (!log) {
        return (
            <div className="threat-report empty">
                <p>Select a log from the table to see details</p>
            </div>
        );
    }

    return (
        <div className="threat-report">
            <h3>Log Details</h3>
            <p><strong>IP:</strong> {log.ip}</p>
            <p><strong>User:</strong> {log.userId}</p>
            <p><strong>Rule triggered:</strong> {log.rule_triggered || "None"}</p>

            {/* Conditional rendering: only show the AI report section
          if ai_report actually has a value. The && operator means
          "render the right side only if the left side is truthy". */}
            {log.ai_report && (
                <div className="ai-report">
                    <h4>AI Analysis</h4>
                    {/* white-space: pre-wrap in CSS will respect the newlines
              already in the text, so we don't need to parse markdown. */}
                    <pre className="ai-report-text">{log.ai_report}</pre>
                </div>
            )}
        </div>
    );
}

export default ThreatReport;