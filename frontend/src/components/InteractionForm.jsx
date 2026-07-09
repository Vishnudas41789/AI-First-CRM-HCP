import { useDispatch, useSelector } from "react-redux";
import { setField } from "../store/interactionSlice";

function InteractionForm() {
  const dispatch = useDispatch();
  const form = useSelector((state) => state.interaction);

  const handleChange = (field) => (e) => {
    dispatch(setField({ field, value: e.target.value }));
  };

  return (
    <div>
      <h2 className="text-3xl font-bold mb-8">Log HCP Interaction</h2>

      <div className="grid grid-cols-2 gap-5">
        <div>
          <label className="font-semibold">HCP Name</label>
          <input
            type="text"
            placeholder="Search or select HCP..."
            className="w-full mt-2 border rounded-lg p-3"
            value={form.hcp_name}
            onChange={handleChange("hcp_name")}
          />
        </div>

        <div>
          <label className="font-semibold">Interaction Type</label>
          <select
            className="w-full mt-2 border rounded-lg p-3"
            value={form.interaction_type}
            onChange={handleChange("interaction_type")}
          >
            <option>Meeting</option>
            <option>Call</option>
            <option>Email</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-2 gap-5 mt-6">
        <div>
          <label className="font-semibold">Date</label>
          <input
            type="date"
            className="w-full mt-2 border rounded-lg p-3"
            value={form.interaction_date}
            onChange={handleChange("interaction_date")}
          />
        </div>

        <div>
          <label className="font-semibold">Time</label>
          <input
            type="time"
            className="w-full mt-2 border rounded-lg p-3"
            value={form.interaction_time}
            onChange={handleChange("interaction_time")}
          />
        </div>
      </div>

      <div className="mt-6">
        <label className="font-semibold">Attendees</label>
        <input
          type="text"
          placeholder="Enter names or search..."
          className="w-full mt-2 border rounded-lg p-3"
          value={form.attendees}
          onChange={handleChange("attendees")}
        />
      </div>

      <div className="mt-6">
        <label className="font-semibold">Topics Discussed</label>
        <textarea
          rows="5"
          placeholder="Enter key discussion points..."
          className="w-full mt-2 border rounded-lg p-3"
          value={form.topics_discussed}
          onChange={handleChange("topics_discussed")}
        ></textarea>
      </div>

      <div className="mt-8">
        <h3 className="text-xl font-semibold mb-3">
          Materials Shared / Samples Distributed
        </h3>
        <div className="grid grid-cols-2 gap-5">
          <div>
            <label className="font-semibold">Materials Shared</label>
            <input
              type="text"
              className="w-full mt-2 border rounded-lg p-3"
              value={form.materials_shared}
              onChange={handleChange("materials_shared")}
            />
          </div>
          <div>
            <label className="font-semibold">Samples Distributed</label>
            <input
              type="text"
              className="w-full mt-2 border rounded-lg p-3"
              value={form.samples_distributed}
              onChange={handleChange("samples_distributed")}
            />
          </div>
        </div>
      </div>

      <div className="mt-8">
        <h3 className="text-lg font-semibold">
          Observed / Inferred HCP Sentiment
        </h3>
        <div className="flex gap-8 mt-4">
          {["Positive", "Neutral", "Negative"].map((option) => (
            <label key={option} className="flex items-center gap-2">
              <input
                type="radio"
                name="sentiment"
                checked={form.sentiment === option}
                onChange={() =>
                  dispatch(setField({ field: "sentiment", value: option }))
                }
              />
              {option === "Positive" && "😊"}
              {option === "Neutral" && "😐"}
              {option === "Negative" && "😔"} {option}
            </label>
          ))}
        </div>
      </div>

      <div className="mt-8">
        <label className="font-semibold">Outcome</label>
        <textarea
          rows="4"
          placeholder="Key outcomes or agreements..."
          className="w-full mt-2 border rounded-lg p-3"
          value={form.outcome}
          onChange={handleChange("outcome")}
        ></textarea>
      </div>

      <div className="mt-8">
        <label className="font-semibold">Follow-up Actions</label>
        <textarea
          rows="4"
          placeholder="Next actions..."
          className="w-full mt-2 border rounded-lg p-3"
          value={form.follow_up_actions}
          onChange={handleChange("follow_up_actions")}
        ></textarea>
      </div>
    </div>
  );
}

export default InteractionForm;