import { useEffect } from "react";
import { Navigate } from "react-dom";
import { userAuthStore } from "../Store/auth";

const PrivateRoute = ({ children }) => {
  const loggedIn = userAuthStore((state) => state.isLoggedIn)();
  return loggedIn ? <>{children}</> : <Navigate to="/login/" />;
};
export default PrivateRoute;
