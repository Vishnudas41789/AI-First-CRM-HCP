import { createSlice } from "@reduxjs/toolkit";

const initialState = {
  hcp_name: "",
  interaction_type: "Meeting",
  interaction_date: "",
  interaction_time: "",
  attendees: "",
  topics_discussed: "",
  materials_shared: "",
  samples_distributed: "",
  sentiment: "",
  outcome: "",
  follow_up_actions: "",
};

const interactionSlice = createSlice({
  name: "interaction",
  initialState,
  reducers: {
    setField: (state, action) => {
      const { field, value } = action.payload;
      state[field] = value;
    },
    // Called automatically whenever the backend returns a database_result
    applyAIData: (state, action) => {
      const data = action.payload || {};
      Object.keys(data).forEach((key) => {
        if (!(key in state)) return;
        let value = data[key];
        if (value === null || value === undefined || value === "") return;

        if (key === "sentiment") {
          const v = String(value).toLowerCase();
          if (v.includes("positive")) value = "Positive";
          else if (v.includes("negative")) value = "Negative";
          else if (v.includes("neutral")) value = "Neutral";
        }

        state[key] = value;
      });
    },
    resetForm: () => initialState,
  },
});

export const { setField, applyAIData, resetForm } = interactionSlice.actions;
export default interactionSlice.reducer;