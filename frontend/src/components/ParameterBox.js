import React, { useState } from "react";

function ParameterBox({ parameters, setParameters }) {
  const [showParametersBox, setShowParametersBox] = useState(false);
  const profiles = ["foot-walking", "cycling-regular", "driving-car"]

  return (
    <>
      <button onClick={() => setShowParametersBox(!showParametersBox)}>
        {showParametersBox ? "Hide" : "Show"} Parameters
      </button>
      {showParametersBox && (
        <>
          <div>
            <label>API Key:</label>
            <input
              type="text"
              value={parameters["api_key"]}
              onChange={(e) => setParameters({...parameters, api_key: e.target.value })}
            />
          </div>
          <div>
            <label>Traveling mode</label>
            <select
              value={parameters["profile"]}
              onChange={(e) => setParameters({...parameters, profile: e.target.value })}>
              {profiles.map((p) => (
                <option key={p} value={p}>
                  {p}
                </option>
              ))}
              </select>
          </div>
        </>
      )}
    </>
  );
}

export default ParameterBox;
