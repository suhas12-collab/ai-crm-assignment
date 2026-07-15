import { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [form, setForm] = useState({
    doctor_name: "",
    hospital: "",
    interaction_type: "",
    interaction_date: "",
    interaction_time: "",
    discussion: "",
    follow_up: "",
  });

  const [chat, setChat] = useState("");
  const [reply, setReply] = useState("");
  const [interactions, setInteractions] = useState([]);
  const API_BASE = "http://127.0.0.1:8000";

  useEffect(() => {
    fetchInteractions();
  }, []);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const fetchInteractions = async () => {
    try {
      const res = await axios.get(`${API_BASE}/interactions`);
      setInteractions(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  const saveInteraction = async () => {
    try {
      await axios.post(`${API_BASE}/interactions`, form);

      alert("✅ Interaction Saved Successfully");

      fetchInteractions();

      setForm({
        doctor_name: "",
        hospital: "",
        interaction_type: "",
        interaction_date: "",
        interaction_time: "",
        discussion: "",
        follow_up: "",
      });
    } catch (err) {
      console.log(err);
      alert("❌ Error Saving Interaction");
    }
  };

  const askAI = async () => {
    try {
      const res = await axios.post(`${API_BASE}/chat`, {
        message: chat,
      });

      setReply(res.data.response);
    } catch (err) {
      console.log(err);
      alert("❌ AI Error");
    }
  };

  const uniqueDoctors = new Set(interactions.map((i) => i.doctor_name)).size;
  const uniqueHospitals = new Set(interactions.map((i) => i.hospital)).size;

  return (
    <div className="container">
      <h1 className="title">🏥 AI CRM Dashboard</h1>

      {/* Statistics */}
      <div className="stats">
        <div className="stat-card">
          <h3>👨‍⚕️ Doctors</h3>
          <h2>{uniqueDoctors}</h2>
        </div>

        <div className="stat-card">
          <h3>🏥 Hospitals</h3>
          <h2>{uniqueHospitals}</h2>
        </div>

        <div className="stat-card">
          <h3>📝 Interactions</h3>
          <h2>{interactions.length}</h2>
        </div>
      </div>

      {/* Main Dashboard */}
      <div className="dashboard">
        {/* Left Card */}
        <div className="card">
          <h2>👨‍⚕️ Log Doctor Interaction</h2>

          <input
            type="text"
            placeholder="Doctor Name"
            name="doctor_name"
            value={form.doctor_name}
            onChange={handleChange}
          />

          <input
            type="text"
            placeholder="Hospital"
            name="hospital"
            value={form.hospital}
            onChange={handleChange}
          />

          <input
            type="text"
            placeholder="Interaction Type"
            name="interaction_type"
            value={form.interaction_type}
            onChange={handleChange}
          />

          <input
            type="date"
            name="interaction_date"
            value={form.interaction_date}
            onChange={handleChange}
          />

          <input
            type="time"
            name="interaction_time"
            value={form.interaction_time}
            onChange={handleChange}
          />

          <textarea
            placeholder="Discussion"
            name="discussion"
            value={form.discussion}
            onChange={handleChange}
          />

          <input
            type="text"
            placeholder="Follow Up"
            name="follow_up"
            value={form.follow_up}
            onChange={handleChange}
          />

          <button onClick={saveInteraction}>
            💾 Save Interaction
          </button>
        </div>

        {/* Right Card */}
        <div className="card">
          <h2>🤖 AI Assistant</h2>

          <textarea
            placeholder="Ask AI anything..."
            value={chat}
            onChange={(e) => setChat(e.target.value)}
          />

          <button onClick={askAI}>
            🚀 Ask AI
          </button>

          <div className="response">
            <strong>AI Response</strong>
            <hr />
            {reply || "Your AI response will appear here..."}
          </div>
        </div>
      </div>

      {/* Interaction History */}
      <div className="card" style={{ marginTop: "30px" }}>
        <h2>📋 Interaction History</h2>

        <table className="history-table">
          <thead>
            <tr>
              <th>Doctor</th>
              <th>Hospital</th>
              <th>Type</th>
              <th>Date</th>
            </tr>
          </thead>

          <tbody>
            {interactions.length > 0 ? (
              interactions.map((item) => (
                <tr key={item.id}>
                  <td>{item.doctor_name}</td>
                  <td>{item.hospital}</td>
                  <td>{item.interaction_type}</td>
                  <td>{item.interaction_date}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="4">No interactions found.</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default App;