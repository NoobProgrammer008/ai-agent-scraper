import React, {useState, useEffect} from 'react';
import SearchBar from "./components/SearchBar";
import ProgressDisplay from "./components/ProgressDisplay";
import HistoryList from "./components/HistoryList";
import logo from './logo.svg';
import './App.css';


export default function App() {
  const [progress, setProgress] = useState(null);

  const [history, setHistory] = useState([]);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchHistory();
  }, []);
// ==================== FETCH HISTORY ====================
  const fetchHistory = async () => {

    try{
      const response = await fetch("http://localhost:8000/history");

      const data = await response.json();

      setHistory(data.history || []);

    } catch (error){
      console.error("Failed to fetch history:", error);
    }
  };
  // ==================== HANDLE SEARCH ====================
  
  const handleSearch = (query) => {

    setLoading(true);
    setProgress(null);

    const websocket = new WebSocket("ws://localhost:8000/ws/research");

    websocket.onopen = () =>{
      console.log("Connected to server");

      websocket.send(JSON.stringify({ query }));
    };

    websocket.onmessage = (event) => {
      const data = JSON.parse(event.data);

      console.log("Received:", data);

      setProgress(data);

      if(data.status === "completed" || data.status === "error") {
        
        setLoading(false);

        fetchHistory();
      }
    };

    websocket.onerror = (error) => {
      console.error("WebSocket error:", error);

      setProgress({
        status : "error",
        message: "Connection error"
      });

      setLoading(false);
    };

  };

  const handleExport = async (resultId) => {
    try{
      const response = await fetch(
        `http://localhost:8000/export/${resultId}`,

        {method: "POST"}
        
      );

      const blob = await response.blob();

      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");

      a.href = url;
      a.download = `research_${resultId}.csv`;
      a.click();

      window.URL.revokeObjectURL(url);
    }catch (error){
      console.error("Export Failure", error);
    }
  };

  const handleDelete = async (resultId) => {
    try{
      await fetch (`http://localhost:8000/results/${resultId}1`,{
        method: "DELETE"
      });
      fetchHistory();
    } catch (error){
      console.log("Delete Failed", error);
    }
  };

  return(
    <div className='app'>
      <SearchBar
        onSearch = {handleSearch}

        loading = {loading}
      />
      <ProgressDisplay
        progress = {progress}  
      />

      <HistoryList
        history = {history}

        onExport = {handleExport}

        onDelete = {handleDelete}
      />
    </div>
  );
}
