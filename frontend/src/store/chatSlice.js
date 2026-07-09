import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { sendChatMessage } from "../services/api";
import { applyAIData } from "./interactionSlice";

export const sendMessage = createAsyncThunk(
  "chat/sendMessage",
  async (message, { dispatch, rejectWithValue }) => {
    try {
      const data = await sendChatMessage(message);

      if (data.database_result && !data.database_result.error) {
        dispatch(applyAIData(data.database_result));
      }

      return data;
    } catch (err) {
      console.log("FULL ERROR:", err);
      console.log("RESPONSE:", err.response);
      console.log("DATA:", err.response?.data);
      return rejectWithValue(
        err.response?.data?.detail ||
        err.message ||
        "Something went wrong. Please try again."
      );
    }
  }
);

const chatSlice = createSlice({
  name: "chat",
  initialState: {
    messages: [],
    loading: false,
    error: null,
  },
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(sendMessage.pending, (state, action) => {
        state.loading = true;
        state.error = null;
        state.messages.push({ role: "user", text: action.meta.arg });
      })
      .addCase(sendMessage.fulfilled, (state, action) => {
        state.loading = false;
        state.messages.push({
          role: "ai",
          text: action.payload.ai_response,
          selected_tool: action.payload.selected_tool,
        });
      })
      .addCase(sendMessage.rejected, (state, action) => {
        state.loading = false;
        state.error = action.payload;
        state.messages.push({ role: "ai", text: `⚠️ ${action.payload}` });
      });
  },
});

export default chatSlice.reducer;