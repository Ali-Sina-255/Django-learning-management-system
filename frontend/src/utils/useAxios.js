import axios from "axios";
import {
  getRefreshToken,
  isAccessTokenExpired,
  setAuthUser,
  setUser,
} from "./auth";
import { apiBaseUrl } from "./constants";
import Cookie from "js-cookie";

const useAxios = () => {
  const accessToken = Cookie.get("access_token");
  const refreshToken = Cookie.get("refresh_token");
  const axiosInstance = axios.create({
    baseURL: apiBaseUrl,
    headers: { Authorization: `Bearer ${accessToken}` },
  });
  axiosInstance.interceptors.request.use(async (req) => {
    if (!isAccessTokenExpired) {
      return req;
    }
    const response = await getRefreshToken(refreshToken);
    setAuthUser(response.access, response.refresh);
    req.headers.Authorization = `Bearer ${response.data?.access}`;
    return req;
  });
  return axiosInstance;
};

export default useAxios;
