import React, { useState } from 'react';
import axios from 'axios';

function UserRegistration() {
    // State to hold form values
    const [formData, setFormData] = useState({
        full_name: '',
        email: '',
        password: '',
        password2: ''
    });

    // State to handle success or error messages
    const [message, setMessage] = useState('');

    // Handle input changes
    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    // Handle form submission
    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            // Post the form data to the registration endpoint
            const res = await axios.post('http://localhost:8000/apis/user/register/', formData);
            // Handle success (you can navigate or display a success message)
            setMessage('User registered successfully!');
            setFormData({
                full_name: '',
                email: '',
                password: '',
                password2: ''
            })
        } catch (err) {
            // Handle error (display error message)
            setMessage('Registration failed. Please try again.');
            console.error(err);
        }
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-6 border border-gray-300 rounded-lg shadow-lg">
            <h1 className="text-2xl font-bold mb-4">Register New User</h1>
            {message && <p className="mb-4 text-center">{message}</p>}
            <form onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label htmlFor="full_name" className="block text-gray-700 text-left">Full Name</label>
                    <input
                        type="text"
                        name="full_name"
                        id="full_name"
                        value={formData.full_name}
                        onChange={handleChange}
                        className="mt-1 block w-full p-2 border border-gray-300 rounded-lg"
                        required
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="email" className="block text-gray-700 text-left">Email</label>
                    <input
                        type="email"
                        name="email"
                        id="email"
                        value={formData.email}
                        onChange={handleChange}
                        className="mt-1 block w-full p-2 border border-gray-300 rounded-lg"
                        required
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="password" className="block text-gray-700 text-left">Password</label>
                    <input
                        type="password"
                        name="password"
                        id="password"
                        value={formData.password}
                        onChange={handleChange}
                        className="mt-1 block w-full p-2 border border-gray-300 rounded-lg"
                        required
                    />
                </div>
                <div className="mb-4">
                    <label htmlFor="password2" className="block text-gray-700 text-left">Confirm Password</label>
                    <input
                        type="password"
                        name="password2"
                        id="password2"
                        value={formData.password2}
                        onChange={handleChange}
                        className="mt-1 block w-full p-2 border border-gray-300 rounded-lg"
                        required
                    />
                </div>
                <button
                    type="submit"
                    className="w-full bg-blue-500 text-white p-2 rounded-lg hover:bg-blue-600 transition duration-200"
                >
                    Register
                </button>
            </form>
        </div>
    );
}

export default UserRegistration;
