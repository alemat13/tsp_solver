import React, { useEffect, useState } from "react";
import Map from "./components/Map";
import ParameterBox from "./components/ParameterBox";
import "./App.css";

function App() {
  const API_HOST =
    process.env.NODE_ENV === "production" ? "" : "http://localhost:5000";
  const API_ENDPOINT = `${API_HOST}/api/calculate`;
  const [positions, setPositions] = useState([
    "48.8606, 2.3376",
    "48.8530, 2.3499",
    "48.8738, 2.2950",
    "48.8867, 2.3431",
    "48.8600, 2.3267",
    "48.8698, 2.3075",
    "48.8635, 2.3274",
    "48.8462, 2.3447",
    "48.8656, 2.3212",
    "48.8556, 2.3158",
    "",
  ]);
  const [route, setRoute] = useState({
    optimal_route: [],
    route: [],
    openrouteservice_data: {},
  });
  const [parameters, setParameters] = useState({
    api_key: "",
    profile: "foot-walking",
    population_size: 1000,
    num_generations: 300
  });

  // function that validate GPS coordinates user input
  // const validateGPS = (input) => {
  //   const regex = /^-?([1-8]?[1-9]|[1-9]0)\.{1}\d{1,6}/;
  //   return regex.test(input);
  // };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Save parameters to local storage
    localStorage.setItem("parameters", JSON.stringify(parameters));

    try {
      const response = await fetch(API_ENDPOINT, {
        method: "POST",
        body: JSON.stringify({
          positions: positionsObj,
          parameters,
        }),
        headers: {
          "Content-type": "application/json",
        },
      });
      const data = await response.json();
      setRoute(data);
    } catch (error) {
      console.error("Error optimizing positions:", error);
    }
  };

  useEffect((parameters) => {
    // Load parameters from local storage and set it to state
    const storedParameters = JSON.parse(localStorage.getItem("parameters"));
    if (storedParameters) {
      setParameters(storedParameters);
    }
  }, []);

  const positionsObj = positions
    .filter((e) => e !== "")
    .map((p) => p.split(",").map((e) => parseFloat(e)));

  const handleChange = (e, index) => {
    const newPositions = [...positions];
    newPositions[index] = e.target.value;
    setPositions(newPositions);
  };

  const handlePaste = (e, index) => {
    e.preventDefault();
    const pastedTxt = e.clipboardData.getData("text");
    const newPositionsList = pastedTxt.split(/\r?\n/).filter((e) => e !== "");
    setPositions((prev) => [
      ...prev.slice(0, index),
      ...newPositionsList,
      ...prev.slice(index + 1),
    ]);
  };

  return (
    <div>
      <ParameterBox parameters={parameters} setParameters={setParameters} />
      <h1>Optimize GPS Positions</h1>
      <form onSubmit={handleSubmit}>
        <label>Enter GPS Positions:</label>
        {positions.map((position, index) => (
          <div key={index}>
            <input
              key={index}
              type="text"
              value={position}
              onChange={(e) => handleChange(e, index)}
              onPaste={(e) => handlePaste(e, index)}
            />
            <button
              type="button"
              onClick={(e, index) => {
                setPositions([...positions].splice(index));
                console.log(index);
              }}
            >
              X
            </button>
          </div>
        ))}
        <button type="button" onClick={() => setPositions([...positions, ""])}>
          Add Position
        </button>
        <button type="submit">Optimize Positions</button>
        <button type="button" onClick={() => setPositions([])}>
          Clear
        </button>
      </form>
      <div>
        <h2>Optimized Positions:</h2>
        <ul>
          {route["optimal_route"].map(([lat, lon], index) => (
            <li key={index}>
              {lat}, {lon}
            </li>
          ))}
        </ul>
        <Map positions={positionsObj} route={route["route"]} />
      </div>
    </div>
  );
}

export default App;
