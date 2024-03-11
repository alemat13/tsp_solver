import React, { useState } from "react";

function ParameterBox({ parameters, setParameters }) {
  const [showParametersBox, setShowParametersBox] = useState(false);
  
  return (
    <>
      <button onClick={() => setShowParametersBox(!showParametersBox)}>
        {showParametersBox ? "Hide" : "Show"} Parameters
      </button>
      {showParametersBox && (
        <div>
          <label>API Key:</label>
          <input
            type="text"
            value={parameters["api_key"]}
            onChange={(e) => setParameters({ api_key: e.target.value })}
          />
        </div>
      )}
    </>
  );
}

export default ParameterBox;
