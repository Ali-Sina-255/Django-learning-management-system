import axios from "axios";
import { apiBaseUrl } from "./constants";

const apiInstance = axios.create({
  baseURL: apiBaseUrl,
  timeout: 1000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});
export default apiInstance;
