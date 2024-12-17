import axios from "axios";
import { API_BASE_URL } from "./constant";
const apiInstance = axios.create({
  baseURl: API_BASE_URL,
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});
export default apiInstance;
