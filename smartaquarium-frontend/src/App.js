import CapteursList from "./CapteursList";
import AlertsList from "./AlertsList";

function App() {
  return (
    <div className="App">
      <h1>Capteurs</h1>
      <CapteursList />

      <h1>Alertes actives</h1>
      <AlertsList />
    </div>
  );
}

export default App;
