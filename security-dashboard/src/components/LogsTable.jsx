// This component also receives 'results', plus a function 'onSelectLog'.
// Passing a function as a prop lets the child notify the parent
// when something happens (here: when the user clicks a row).
function LogsTable({ results, onSelectLog }) {
    return (
        <div className="logs-table-container">
            <table className="logs-table">
                <thead>
                    <tr>
                        <th style={{ textAlign: 'center' }}>IP</th>
                        <th style={{ textAlign: 'center' }}>User</th>
                        <th style={{ textAlign: 'center' }}>Action</th>
                        <th style={{ textAlign: 'center' }}>Status</th>
                        <th style={{ textAlign: 'center' }}>Threat Level</th>
                    </tr>
                </thead>
                <tbody>
                    {/* .map() transforms each item in the array into a JSX element.
              React requires a unique 'key' prop on list items so it can
              efficiently track which rows changed, were added, or removed. */}
                    {results.map((log) => (
                        <tr
                            key={log.logId}
                            // Clicking a row calls the function passed by the parent,
                            // sending this specific log up to be shown in the report panel.
                            onClick={() => onSelectLog(log)}
                            // Template literal to build a dynamic className —
                            // adds a CSS class based on the threat level for color coding.
                            className={`log-row ${log.threat_level.toLowerCase()}`}
                        >
                            <td>{log.ip}</td>
                            <td>{log.userId}</td>
                            <td>{log.action}</td>
                            <td>{log.status}</td>
                            <td>
                                <span className={`badge ${log.threat_level.toLowerCase()}`}>
                                    {log.threat_level}
                                </span>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default LogsTable;