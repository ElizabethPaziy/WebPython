import { useEffect, useState } from 'react';
import { getStudents, deleteStudent } from '../api/student';
import StudentForm from './StudentForm';
import { Pencil, Trash2 } from 'lucide-react';

const StudentList = () => {
    const [students, setStudents] = useState([]);
    const [editing, setEditing] = useState(null);

    const fetchStudents = async () => {
        const res = await getStudents();
        setStudents(res.data.students);
    };

    useEffect(() => {
        fetchStudents();
    }, []);

    const handleDelete = async (id) => {
        await deleteStudent(id);
        fetchStudents();
    };

    return (
        <div className="min-h-screen bg-gray-950 text-white p-4">
            <StudentForm onSuccess={fetchStudents} editing={editing} setEditing={setEditing} />

            <div className="mt-8 grid gap-4">
                {students.map((student) => (
                    <div
                        key={student.id}
                        className="flex justify-between items-start p-4 bg-gray-800 shadow-md rounded-xl border border-gray-700"
                    >
                        <div>
                            <h3 className="text-xl font-semibold">{student.name}</h3>
                            <p className="text-gray-400 text-sm">📧 {student.email}</p>
                            <p className="text-gray-400 text-sm">📘 Курс: {student.course}</p>
                            <p className="text-green-400 font-medium">🎓 GPA: {student.gpa}</p>
                        </div>

                        <div className="flex gap-3">
                            <button
                                onClick={() => setEditing(student)}
                                className="flex items-center gap-1 text-blue-400 hover:text-blue-500 transition"
                                title="Редагувати"
                            >
                                <Pencil size={18} />
                                <span className="hidden sm:inline">Редагувати</span>
                            </button>
                            <button
                                onClick={() => handleDelete(student.id)}
                                className="flex items-center gap-1 text-red-400 hover:text-red-500 transition"
                                title="Видалити"
                            >
                                <Trash2 size={18} />
                                <span className="hidden sm:inline">Видалити</span>
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default StudentList;
