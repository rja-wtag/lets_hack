import "@/App.css";
import MainMenu from "@/components/menu";
import { Routes, Route } from "react-router-dom";
import Home from "@/pages/home";
import { ThemeProvider } from "@/components/theme-provider";
import { ModeToggle } from "./components/mode-toggle";
import Posts from "@/components/post";

function App() {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <div className="relative">
        <MainMenu />
        <ModeToggle />
      </div>
      <div>
        <Posts />
      </div>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </ThemeProvider>
  );
}

export default App;
