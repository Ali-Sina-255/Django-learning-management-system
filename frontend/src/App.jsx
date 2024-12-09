import { Route, Routes, BrowserRouter } from "react-router-dom";
import MainWrapper from "./layouts/MainWrapper";
import PrivateRoute from "./layouts/PriviteRoute";

import Register from "../src/views/auth/Register";
function App() {
  return (
    <BrowserRouter>
      <MainWrapper>
        <Routes>
          <Route />
        </Routes>
      </MainWrapper>
    </BrowserRouter>
  );
}

export default App;
