import React from "react";
import ReactDOM from "react-dom/client";
import CapteursList from "./CapteursList";

const rootEl = document.getElementById("capteurs-root");
if (rootEl) {
  const root = ReactDOM.createRoot(rootEl);
  root.render(<CapteursList />);
}
