import Header from "../components/Header";
import InteractionForm from "../components/InteractionForm";
import AIChat from "../components/AIChat";

function Dashboard() {
  return (
    <div className="min-h-screen bg-gray-100">
      <Header />

      <div className="flex h-[calc(100vh-70px)] p-4 gap-4">

        {/* Left Side */}
        <div className="w-2/3 bg-white rounded-xl shadow-md p-5 overflow-auto">
          <InteractionForm />
        </div>

        {/* Right Side */}
        <div className="w-1/3 bg-white rounded-xl shadow-md">
          <AIChat />
        </div>

      </div>
    </div>
  );
}

export default Dashboard;