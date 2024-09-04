import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function UserRegistration() {
    const navigate = useNavigate(); // Hook for navigation
    const [formData, setFormData] = useState({
        full_name: '',
        email: '',
        password: '',
        password2: ''
    });

    const [message, setMessage] = useState('');  // State for messages
    const [popupVisible, setPopupVisible] = useState(false); // State for popup visibility

    const handleChange = (e) => {
        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        try {
            const res = await axios.post('http://localhost:8000/apis/user/register/', formData);
            setMessage('User registered successfully!');
            setPopupVisible(true); // Show the popup
            setFormData({
                full_name: '',
                email: '',
                password: '',
                password2: ''
            });

            // Hide the popup after 3 seconds and navigate to /login
            setTimeout(() => {
                setPopupVisible(false);
                navigate('/login');
            }, 3000);

        } catch (err) {
            setMessage('Registration failed. Please try again.');
            setPopupVisible(true); // Show the popup

            // Hide the popup after 3 seconds
            setTimeout(() => {
                setPopupVisible(false);
            }, 3000);

            console.error(err);
        }
    };

    return (
        <div className="max-w-md mx-auto mt-10 p-6 border border-gray-300 rounded-lg shadow-lg">
            <h1 className="text-2xl font-bold mb-4">Register New User</h1>
            {popupVisible && (
                <div className={`fixed inset-x-0 top-0 p-4 ${message.includes('successfully') ? 'bg-green-500' : 'bg-red-500'} text-white text-center`}>
                    {message}
                </div>
            )}
            <form onSubmit={handleSubmit}>
                <div className="mb-4">
                    <label htmlFor="full_name" className="block text-gray-700 text-left">Full Name</label>
                    <input
                        type="text"
                        name="name"
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
