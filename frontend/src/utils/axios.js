import axios from "axios";

const apiInstance = axios.create({
  baseURl: "http://localhost:8000/",
  timeout: 5000,
  headers: {
    "Content-Type": "application/json",
    Accept: "application/json",
  },
});
export default apiInstance;
