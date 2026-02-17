// import React from "react";

// export default function HistoryList({ history, onExport, onDelete }) {
//   // Receive three props from App:
//   // history = array of past results
//   // onExport = function to call when exporting
//   // onDelete = function to call when deleting

//   // ==================== EARLY RETURN ====================
  
//   if (history.length === 0) {
//     return null;
//     // If no history, don't show anything
//   }

//   // ==================== RETURN JSX ====================
  
//   return (
//     <div style={{ padding: "20px", borderTop: "2px solid #ddd" }}>
//       {/* Header */}
//       <h2>
//         📜 Research History ({history.length})
//         {/* Show count of searches */}
//       </h2>

//       {/* Loop through history array */}
//       <div
//         style={{
//           display: "grid",
//           // Use CSS grid layout
          
//           gap: "10px",
//           // Space between items
//         }}
//       >
//         {history.map((item) => (
//           // map() = for each item in array, create JSX
//           // Returns array of JSX elements
          
//           <div
//             key={item.id}
//             // key = unique identifier for React
//             // Must be unique for each list item
//             // React uses it to track items
            
//             style={{
//               padding: "15px",
//               // Space inside
              
//               border: "1px solid #ddd",
//               // Light gray border
              
//               borderRadius: "5px",
//               // Rounded corners
              
//               backgroundColor: "#f9f9f9",
//               // Light gray background
              
//               display: "flex",
//               // Flexbox layout
              
//               justifyContent: "space-between",
//               // Space between content and buttons
              
//               alignItems: "center",
//               // Align vertically in middle
//             }}
//           >
//             {/* Left side: Query and timestamp */}
//             <div style={{ flex: 1 }}>
//               {/* flex: 1 = take available space */}
              
//               <strong style={{ fontSize: "16px" }}>
//                 {item.query}
//                 {/* Show search query */}
//               </strong>
              
//               <p style={{ margin: "5px 0", color: "#666", fontSize: "14px" }}>
//                 {new Date(item.timestamp).toLocaleString()}
//                 {/* Convert ISO timestamp to readable format
//                     "2024-02-09T10:30:00" → "2/9/2024, 10:30:00 AM"
//                     new Date() = create Date object from string
//                     toLocaleString() = convert to locale format
//                 */}
//               </p>
//             </div>

//             {/* Right side: Buttons */}
//             <div style={{ display: "flex", gap: "10px" }}>
//               {/* Flexbox to align buttons horizontally */}
              
//               {/* Export Button */}
//               <button
//                 onClick={() => onExport(item.id)}
//                 // When clicked, call parent's onExport
//                 // () => onExport(item.id) = arrow function
//                 // Necessary to pass parameter
//                 // Without arrow function, would call immediately
                
//                 style={{
//                   padding: "8px 15px",
//                   backgroundColor: "#27ae60",
//                   // Green
                  
//                   color: "white",
//                   border: "none",
//                   borderRadius: "5px",
//                   cursor: "pointer",
//                 }}
//               >
//                 📥 Export
//               </button>

//               {/* Delete Button */}
//               <button
//                 onClick={() => onDelete(item.id)}
//                 // When clicked, call parent's onDelete
                
//                 style={{
//                   padding: "8px 15px",
//                   backgroundColor: "#e74c3c",
//                   // Red
                  
//                   color: "white",
//                   border: "none",
//                   borderRadius: "5px",
//                   cursor: "pointer",
//                 }}
//               >
//                 🗑️ Delete
//               </button>
//             </div>
//           </div>
//         ))}
//       </div>
//     </div>
//   );
// }
import React from "react";

export default function HistoryList({ history, onExport, onDelete }) {
  if (history.length === 0) {
    return null;
  }

  return (
    <div style={{ padding: "20px", borderTop: "2px solid #ddd" }}>
      <h2>
        📜 Research History ({history.length})
      </h2>

      <div
        style={{
          display: "grid",
          gap: "10px",
        }}
      >
        {history.map((item) => (
          <div
            key={item.id}
            style={{
              padding: "15px",
              border: "1px solid #ddd",
              borderRadius: "5px",
              backgroundColor: "#f9f9f9",
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
            }}
          >
            <div style={{ flex: 1 }}>
              <strong style={{ fontSize: "16px" }}>
                {item.query}
              </strong>
              <p style={{ margin: "5px 0", color: "#666", fontSize: "14px" }}>
                {new Date(item.timestamp).toLocaleString()}
              </p>
            </div>

            <div style={{ display: "flex", gap: "10px" }}>
              <button
                onClick={() => onExport(item.id)}
                style={{
                  padding: "8px 15px",
                  backgroundColor: "#27ae60",
                  color: "white",
                  border: "none",
                  borderRadius: "5px",
                  cursor: "pointer",
                }}
              >
                📥 Export
              </button>

              <button
                onClick={() => onDelete(item.id)}
                style={{
                  padding: "8px 15px",
                  backgroundColor: "#e74c3c",
                  color: "white",
                  border: "none",
                  borderRadius: "5px",
                  cursor: "pointer",
                }}
              >
                🗑️ Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}