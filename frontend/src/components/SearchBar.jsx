 import React, {useState} from "react";
 
 export default function SearchBar({onSearch, loading}) {

    const [query, setQuery] = useState("");

    const handleSearch = () => {
        if (query.trim() && !loading){

            onSearch(query);

            setQuery("");
        }
    };

    return(
        <div
            style ={{
                padding: "20px",
                
                textAlign: "center",

                borderBottom: "2px solid #ddd"
            }}
            
        >
            {/*header*/}
            <h1>Research Agent</h1>

            <p>Enter your research query to get real-time results</p>

            <div
                style = {{
                    display: "flex",

                    justifyContent: "center",

                    gap: "10px"
                }}
            >

            <input

                type = "text"

                placeholder="Enter your search query:"

                value = {query}

                onChange={(e) => setQuery(e.target.value)}

                onKeyPress={(e) => e.key === "Enter" && handleSearch()}

                disabled = {loading}

                style = {{
                    width: "400px",
                    padding: "10px",
                    fontSize: "16px",
                    borderRadius: "5px",
                    border: "1px solid #ccc",
                    opacity: loading ? 0.6 : 1,
                }}
            />
            <button
                onClick = {handleSearch}

                disabled = {loading}

                style = {{
                    padding: "10px 20px",
                    fontSize: "16px",
                    backgroundColor: loading ? "#ccc" : "#007bff",
                    color: "white",
                    border: "none",
                    borderRadius: "5px",
                    cursor: loading ? "not-allowed" : "pointer",
                }}
            >
                {loading ? "Searching..": "Search"}
                
            </button>
        </div>
    </div>
    );
 }