 import React, {useState} from "react";
 
 export default function SearchBar({onSearch, loading}) {

    const [query, setQuery] = useState("");

    const handleSearch = () => {
        if (query.trim() && !loading){

            onSearch(query);

            setQuery("");
        }
    };
 }