import axios from 'axios';

const API_URL = 'http://localhost:8000/student/';

export const getStudents = () => axios.get(API_URL);
export const getStudent = (id) => axios.get(`${API_URL}/${id}`);
export const createStudent = (data) => axios.post(API_URL, data);
export const updateStudent = (id, data) => axios.put(`${API_URL}${id}`, data);
export const deleteStudent = (id) => axios.delete(`${API_URL}${id}`);
