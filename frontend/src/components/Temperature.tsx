import React, { useState } from "react";
import { getTemperatureByDateRange } from "../api/temperature";

interface TemperatureData {
  region: string;
  country: string;
  state: string;
  city: string;
  year: string;
  month: string;
  day: string;
  avg_temperature: number;
}

const TemperatureComponent = () => {
  const [temperatureData, setTemperatureData] = useState<TemperatureData[]>([]);
  const [startDate, setStartDate] = useState("2000-01-01");
  const [endDate, setEndDate] = useState("2000-01-01");
  const [warningMessage, setWarningMessage] = useState("");

  const handleStartDateChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const newStartDate = event.target.value;
    setStartDate(newStartDate);
    if (warningMessage) {
      setWarningMessage("");
    }
  };

  const handleEndDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const newEndDate = event.target.value;
    setEndDate(newEndDate);
    if (warningMessage) {
      setWarningMessage("");
    }
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (endDate < startDate) {
      setWarningMessage("End date cannot be before the start date.");
    } else {
      getTemperatureByDateRange(startDate, endDate)
        .then((data) => {
          setTemperatureData(data);
        })
        .catch((error) => {
          console.error("Error fetching temperature data:", error);
        });
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            gap: "2em",
            flexDirection: "row",
            alignItems: "baseline",
          }}
        >
          <label
            style={{
              marginBottom: "20px",
              marginRight: "20px",
              display: "block",
            }}
          >
            Start Date:
            <input
              type="date"
              value={startDate}
              onChange={handleStartDateChange}
              style={{ marginLeft: "2em" }}
            />
          </label>
          <label
            style={{
              marginBottom: "20px",
              display: "block",
            }}
          >
            End Date:
            <input
              type="date"
              value={endDate}
              onChange={handleEndDateChange}
              style={{ marginLeft: "2em" }}
            />
          </label>
          <button type="submit" disabled={warningMessage !== ""}>
            Submit
          </button>
        </div>
        {warningMessage && <p style={{ color: "red" }}>{warningMessage}</p>}
      </form>
      {temperatureData.map((item, index) => (
        <div
          key={index}
          style={{
            display: "flex",
            justifyContent: "space-between",
            borderBottom: "1px solid #ccc",
            paddingBottom: "10px",
            marginBottom: "10px",
          }}
        >
          <p>Region: {item.region}</p>
          <p>Country: {item.country}</p>
          {item.state && <p>State: {item.state}</p>}
          <p>City: {item.city}</p>
          <p>
            Date: {item.year}-{item.month}-{item.day}
          </p>
          <p>Average Temperature: {item.avg_temperature}°F</p>
        </div>
      ))}
    </div>
  );
};

export default TemperatureComponent;
