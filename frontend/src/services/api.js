import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000",
  headers: { "Content-Type": "application/json" },
});

export const sendChatMessage = async (message) => {
  const response = await api.post("/interaction/chat", { message });
  return response.data;
};

export default api;