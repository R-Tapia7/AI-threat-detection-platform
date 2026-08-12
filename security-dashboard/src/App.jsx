import { useState, useEffect } from "react";
import { fetchResults } from "./api/securityApi";
import MetricsBar from "./components/MetricsBar";
import LogsTable from "./components/LogsTable";
import ThreatReport from "./components/ThreatReport";
import "./App.css";

function App() {
  // useState creates a piece of state — a value that React tracks.
  // When it changes, React automatically re-renders the component.
  // 'results' is the current value, 'setResults' is the function to update it.
  const [results, setResults] = useState([]);

  // 'selectedLog' tracks which row the user clicked in the table,
  // so ThreatReport knows what to display.
  const [selectedLog, setSelectedLog] = useState(null);

  // useEffect runs side effects — things that happen outside
  // the normal render flow, like fetching data or setting timers.
  useEffect(() => {
    // This function calls Python and updates the state with the response.
    async function loadResults() {
      try {
        const data = await fetchResults();
        setResults(data);
      } catch (error) {
        console.error("Failed to fetch results:", error);
      }
    }

    loadResults(); // Run once immediately when the component mounts

    // setInterval repeats a function every N milliseconds.
    // This is what makes the dashboard feel "real-time" — it's polling
    // Python every 3 seconds for new data.
    const interval = setInterval(loadResults, 3000);

    // The function returned by useEffect is a "cleanup" function.
    // React calls it when the component unmounts, to avoid memory leaks
    // (otherwise the interval would keep running forever in the background).
    return () => clearInterval(interval);
  }, []); // Empty array means: run this effect only once, on mount

  return (
    <div className="app">
      <header className="app-header">
        <h1>Security Analytics Dashboard</h1>
      </header>

      <MetricsBar results={results} />

      <div className="main-content">
        <LogsTable results={results} onSelectLog={setSelectedLog} />
        <ThreatReport log={selectedLog} />
      </div>
    </div>
  );
}

export default App;
