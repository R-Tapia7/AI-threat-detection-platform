import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8001";

const api = axios.create({
    baseURL: API_BASE_URL,
});

export async function fetchResults() {
    const response = await api.get("/analyze/results");
    return response.data; // axios wraps the response; .data is the actual JSON
}