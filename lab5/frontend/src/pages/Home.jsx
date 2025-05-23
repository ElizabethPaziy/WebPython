import { useState, useEffect } from "react";
import api from "../api";
import Note from "../components/Note";
import "../styles/Home.css";

function Home() {
    const [notes, setNotes] = useState([]);
    const [content, setContent] = useState("");
    const [title, setTitle] = useState("");
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isEditing, setIsEditing] = useState(false);
    const [editNoteId, setEditNoteId] = useState(null);

    useEffect(() => {
        getNotes();
    }, []);

    const getNotes = () => {
        api
            .get("/api/notes/")
            .then((res) => res.data)
            .then((data) => {
                setNotes(data);
                console.log(data);
            })
            .catch((err) => alert(err));
    };

    const deleteNote = (id) => {
        api
            .delete(`/api/notes/delete/${id}/`)
            .then((res) => {
                if (res.status === 204) alert("Note deleted!");
                else alert("Failed to delete note.");
                getNotes();
            })
            .catch((error) => alert(error));
    };

    const startEdit = (note) => {
        setTitle(note.title);
        setContent(note.content);
        setEditNoteId(note.id);
        setIsEditing(true);
    };

    const resetForm = () => {
        setTitle("");
        setContent("");
        setEditNoteId(null);
        setIsEditing(false);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        setIsSubmitting(true);
        const payload = { content, title };

        if (isEditing && editNoteId !== null) {
            api
                .put(`/api/notes/update/${editNoteId}/`, payload)
                .then((res) => {
                    if (res.status === 200) alert("Note updated!");
                    else alert("Failed to update note.");
                    resetForm();
                    getNotes();
                })
                .catch((err) => alert(err))
                .finally(() => setIsSubmitting(false));
        } else {
            api
                .post("/api/notes/", payload)
                .then((res) => {
                    if (res.status === 201) alert("Note created!");
                    else alert("Failed to make note.");
                    resetForm();
                    getNotes();
                })
                .catch((err) => alert(err))
                .finally(() => setIsSubmitting(false));
        }
    };

    return (
        <div>
            <div>
                <h2>Notes</h2>
                {notes.map((note) => (
                    <Note
                        note={note}
                        onDelete={deleteNote}
                        onEdit={startEdit}
                        key={note.id}
                    />
                ))}
            </div>
            <h2>{isEditing ? "Edit Note" : "Create a Note"}</h2>
            <form onSubmit={handleSubmit}>
                <label htmlFor="title">Title:</label>
                <br />
                <input
                    type="text"
                    id="title"
                    name="title"
                    required
                    onChange={(e) => setTitle(e.target.value)}
                    value={title}
                    disabled={isSubmitting}
                />
                <label htmlFor="content">Content:</label>
                <br />
                <textarea
                    id="content"
                    name="content"
                    required
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                    disabled={isSubmitting}
                ></textarea>
                <br />
                <input
                    type="submit"
                    value={isSubmitting ? "Submitting..." : isEditing ? "Update Note" : "Create Note"}
                    disabled={isSubmitting}
                />
                {isEditing && (
                    <button type="button" onClick={resetForm} disabled={isSubmitting}>
                        Cancel
                    </button>
                )}
            </form>
        </div>
    );
}

export default Home;
