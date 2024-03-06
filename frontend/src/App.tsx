import "./App.css";
import TemperatureComponent from "./components/Temperature";

function App() {

  return (
    <>
      <h1>Flask Project</h1>
      <p className="read-the-docs">
        This is the home page of my flask project
      </p>
      <TemperatureComponent/>
    </>
  );
}

export default App;
