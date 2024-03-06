const baseURL = "http://localhost:5001/";

export const getTemperatureByDateRange = async (
  startDate: string,
  endDate: string
) => {
  const response = await fetch(
    `${baseURL}/temperature/range?start=${startDate}&end=${endDate}`
  );
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return response.json();
};

export const gettTemperatureById = async (id: number) => {
  const response = await fetch(`${baseURL}/temperature/${id}`);
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return response.json();
};

export const addTemperatureRecord = async (temperatureRecord: {
  region: string;
  country: string;
  state?: string;
  city: string;
  month: number;
  day: number;
  year: number;
  avg_temperature: number;
}) => {
  const response = await fetch(`${baseURL}/temperatures`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(temperatureRecord),
  });
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return response.json();
};

export const updateTemperatureRecordById = async (
  id: number,
  temperatureRecord: {
    region: string;
    country: string;
    state?: string;
    city: string;
    month: number;
    day: number;
    year: number;
    avg_temperature: number;
  }
) => {
  const response = await fetch(`${baseURL}/temperature/${id}`, {
    method: "PUT",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(temperatureRecord),
  });
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return response.json();
};

export const deleteTemperatureRecordById = async (id: number) => {
  const response = await fetch(`${baseURL}/temperature/${id}`, {
    method: "DELETE",
  });
  if (!response.ok) {
    throw new Error("Network response was not ok");
  }
  return response.json();
};
