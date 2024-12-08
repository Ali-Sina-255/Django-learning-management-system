import { useAuthStore } from "../store/auth"; // Assuming you have a custom store
import axios from "./axios";
import jwt_decode from "jwt-decode"; // Correct import statement
import Cookie from "js-cookie";
import Swal from "sweetalert2";

export const login = async (email, password) => {
  try {
    const { data, status } = await axios.post("user/login/", {
      email,
      password,
    });

    if (status === 200) {
      // If successful, store the auth tokens
      setAuthUser(data.access, data.refresh);
      Swal.fire({
        title: "Login Successful!",
        icon: "success",
        confirmButtonText: "OK",
      });

      return { data, error: null };
    }
  } catch (error) {
    // Handle any errors
    return {
      data: null,
      error: error.response?.data?.detail || "Something went wrong",
    };
  }
};

export const register = async (
  first_name,
  last_name,
  email,
  password,
  password2
) => {
  try {
    const { data, status } = await axios.post("user/register/", {
      first_name,
      last_name,
      email,
      password,
      password2,
    });
    await login(email, password);
    alert("User registration was successfully");
  } catch (error) {
    return {
      data: null,
      error: error.response.data?.detail || "something want wrong",
    };
  }
};

export const logout = () => {
  Cookie.remove("access_token");
  Cookie.remove("refresh_token");
  useAuthStore.getState().setUser(null);
  alert("you have been logged out successfully");
};
export const setUser = async () => {
  const access_token = Cookie.get("access_token");
  const refresh_token = Cookie.get("refresh_token");
  if (!access_token || !refresh_token) {
    alert("Token is does not exist");
    return;
  }
  if (isAccessTokenExpired(access_token)) {
    const response = getRefreshToken(access_token);
    setAuthUser(data.access, response.refresh);
  } else {
    setAuthUser(access_token, refresh_token);
  }
};

export const setAuthUser = (access_token, refresh_token) => {
  Cookie.set("access_token", access_token, {
    expires: 1,
    secure: true,
  });
  Cookie.set("refresh_token", refresh_token, {
    expires: 7,
    secure: true,
  });

  const user = jwt_decode(access_token) ?? null;
  if (user) {
    useAuthStore.getState().setUser(user);
  }
  setAuthUser().getState().setLoading();
};

export const getRefreshToken = async () => {
  const refresh_token = Cookie.get("refresh_token");
  const response = await axios.post(`api/auth/jwt/refresh`, {
    refresh: refresh_token,
  });
  return response.data;
};

export const isAccessTokenExpired = (access_token) => {
  try {
    const decoded = jwt_decode(access_token);
    return decoded.exp < Date.now() / 1000;
  } catch (error) {
    console.log(error);
    return true;
  }
};
