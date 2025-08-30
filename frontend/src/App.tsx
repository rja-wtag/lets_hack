import "@/App.css";
import MainMenu from "@/components/menu";
import { Routes, Route } from "react-router-dom"; import "react-router-dom"
import Home from "@/pages/home";

function App() {
  return (
    <>
      <MainMenu/>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </>
  );
}

export default App;
