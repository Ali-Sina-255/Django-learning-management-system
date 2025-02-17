import { useAuthStore } from "../Store/auth";
import axios from "axios";
import jwt_decode from "jwt-decode";
import Cookies from "js-cookie";
const baseURl = "http://localhost:8000/";
// login user
export const login = async (email, password) => {
  try {
    const { data, status } = await axios.post(`${baseURl}/user/login/`, {
      email,
      password,
    });
    if (status === 200) {
      setAuthUser(data.access, data.refresh);
      alert("Login successfully!");
    }
    return { data, error: null };
  } catch (error) {
    console.error(error);
    const errorMessage = error.response?.data?.detail || "Something went wrong";
    return {
      data: null,
      error: errorMessage,
    };
  }
};

// Register User
export const register = async (full_name, email, password, password2) => {
  try {
    const { data } = await axios.post(`${baseURl}/user/register/`, {
      full_name,
      email,
      password,
      password2,
    });
    await login(email, password);
    alert("Registration was successfully.");
    return { data, error: null };
  } catch (error) {
    console.log(error);
    return {
      data: null,
      error: error.response.data?.detail || "Something went wrong",
    };
  }
};
// logout user

export const logout = () => {
  // Remove the tokens from cookies
  Cookies.remove("access_token");
  Cookies.remove("refresh_token");

  // Set the user data to null in the store
  useAuthStore.getState().setUser(null);

  // Optionally, you can call the setLoading function to set loading to false after logout
  useAuthStore.getState().setLoading(false);
};

export const setUser = async () => {
  const access_token = Cookies.get("access_token");
  const refresh_token = Cookies.get("refresh_token");
  if (!access_token || !refresh_token) {
    alert("Token Does not exist!!");
    return;
  }
  //   IsAccessTokenExpire is not defined
  if (isAccessTokenExpired(access_token)) {
    // getRefreshToken is not defined yet
    const response = getRefreshToken(refresh_token);
    // setAuthUser  is not defined yet
    setAuthUser(response.access, response.refresh_token);
  } else {
    setAuthUser(access_token, refresh_token);
  }
};

export const setAuthUser = (access_token, refresh_token) => {
  // Set the access and refresh tokens in cookies with expiration times
  Cookies.set("access_token", access_token, {
    expires: 1, // Access token expires in 1 day
    secure: true, // Secure flag for HTTPS
  });

  Cookies.set("refresh_token", refresh_token, {
    expires: 7, // Refresh token expires in 7 days
    secure: true, // Secure flag for HTTPS
  });

  const user = jwt_decode(access_token) ?? null;

  if (user) {
    useAuthStore.getState().setUser(user);
  }

  useAuthStore.getState().setLoading(false);
};

export const getRefreshToken = async () => {
  const refresh_token = Cookies.get("refresh_token");
  const response = await axios.post(`${baseURl}user/token/refresh/`, {
    refresh: refresh_token,
  });
  return response.data;
};

export const isAccessTokenExpired = (access_token) => {
  try {
    const decodedToken = jwt_decode(access_token);
    return decodedToken.exp < Date.now() / 1000;
  } catch (error) {
    console.log(error);
    return true;
  }
};
