import StudentList from './components/StudentList';

function App() {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <div className="max-w-3xl mx-auto bg-gray-900 shadow-md rounded-xl p-6">
        <h1 className="text-3xl font-bold mb-6 text-center text-blue-400">Student Management</h1>
        <StudentList />
      </div>
    </div>
  );
}

export default App;
