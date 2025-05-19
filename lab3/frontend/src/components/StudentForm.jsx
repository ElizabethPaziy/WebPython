import { useState, useEffect } from 'react';
import { createStudent, updateStudent } from '../api/student';

const initialForm = {
    name: '',
    email: '',
    course: '',
    gpa: '',
};

const StudentForm = ({ onSuccess, editing, setEditing }) => {
    const [form, setForm] = useState(initialForm);

    useEffect(() => {
        setForm(editing || initialForm);
    }, [editing]);

    const handleChange = (e) => {
        const { name, value } = e.target;
        setForm((prev) => ({ ...prev, [name]: value }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (editing) {
            await updateStudent(editing.id, form);
            setEditing(null);
        } else {
            await createStudent(form);
        }
        setForm(initialForm);
        onSuccess();
    };

    return (
        <div className="max-w-md mx-auto bg-gray-900 text-white shadow-lg rounded-xl p-6 border border-gray-700">
            <h2 className="text-2xl font-semibold mb-4 text-center">
                {editing ? 'Редагувати студента' : 'Додати нового студента'}
            </h2>
            <form onSubmit={handleSubmit} className="space-y-4">
                {[
                    { name: 'name', label: 'Імʼя' },
                    { name: 'email', label: 'Електронна пошта' },
                    { name: 'course', label: 'Курс' },
                    { name: 'gpa', label: 'Середній бал (GPA)' }
                ].map(({ name, label }) => (
                    <div key={name} className="flex flex-col">
                        <label htmlFor={name} className="text-sm font-medium text-gray-300 mb-1">
                            {label}
                        </label>
                        <input
                            id={name}
                            name={name}
                            type={name === 'gpa' ? 'number' : 'text'}
                            step={name === 'gpa' ? '0.1' : undefined}
                            max={name === 'gpa' ? '100.0' : undefined}
                            value={form[name]}
                            onChange={handleChange}
                            placeholder={`Введіть ${label.toLowerCase()}`}
                            className="bg-gray-800 border border-gray-600 text-white rounded-lg px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                            required
                        />
                    </div>
                ))}

                <div className="flex justify-between mt-6">
                    <button
                        type="submit"
                        className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200"
                    >
                        {editing ? 'Оновити студента' : 'Створити студента'}
                    </button>
                </div>

                {editing && (
                    <button
                        type="button"
                        onClick={() => setEditing(null)}
                        className="w-full mt-2 bg-gray-600 text-white py-2 rounded-lg hover:bg-gray-500 transition-colors duration-200"
                    >
                        Скасувати
                    </button>
                )}
            </form>
        </div>
    );
};

export default StudentForm;
