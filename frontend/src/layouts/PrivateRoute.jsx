import { useEffect, useState } from "react";
import { Navigate } from "react-dom";
import { useAuthStore } from "../Store/auth";

const PrivateRoute = ({ children }) => {
  const loggedIn = useAuthStore((state) => state.isLoggedIn)();
  return loggedIn ? <>{children}</> : <Navigate to="/login/" />;
};
export default PrivateRoute;
