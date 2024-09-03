import axios from "axios";
import React, { useEffect, useState } from "react";
import { Link, useMatch, useNavigate } from "react-router-dom";

const AdminDashboard = () => {
  const token = sessionStorage.getItem("token");
  const id = sessionStorage.getItem("id");
  const [previewUrl, setPreviewUrl] = useState();
  const [selectedOption, setSelectedOption] = useState("");
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  // const navigate = useNavigate();

  const useLogout = () => {
    const logout = () => {
      sessionStorage.removeItem("token");
      sessionStorage.removeItem("id");
      sessionStorage.removeItem("zone");
      navigate("/");
    };
    return logout;
  };

  if (!token) {
    // navigate("/login");
  }

  useEffect(() => {
    const fetchUser = async () => {
      try {

      } catch (error) {
        console.error("Error fetching user data:", error);
      }
    };

    fetchUser();
  }, [id]);

  return (
    <div
      dir="rtl"
      className="min-h-screen flex flex-col bg-gradient-to-br from-red-900 via-red-700 to-red-400"
    >
      {/* Navbar */}
      <nav
        dir="ltr"
        className="bg-red-950 text-white p-4 flex justify-between items-center"
      >
        <div className="text-xl font-bold">
          <img src='' alt="Logo" className=" size-14" />
        </div>
        <div>
          <p className="animate-pulse opacity-0 duration-100 sm:text-xl md:text-2xl lg:text-4xl gradient-text">
            به دشبورد سیستم خوش آمدید
          </p>
        </div>

        <div className="relative">
          <img
            src={previewUrl}
            alt="Profile"
            className="rounded-full w-14 h-14 cursor-pointer"
            onClick={() => setDropdownOpen(!dropdownOpen)}
          />
          {dropdownOpen && (
            <div className="z-20 absolute right-0 mt-2 w-48 bg-white rounded-md shadow-lg py-1">
              <Link
                to={`/profile/${id}`}
                className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
              >
                <button>بازدید از پروفایل</button>
              </Link>
              <Link
                onClick={useLogout()}
                className="block px-4 py-2 text-gray-700 hover:bg-gray-100"
              >
                <button>خروج از دشبورد</button>
              </Link>
            </div>
          )}
        </div>
      </nav>

      <div className="flex flex-grow flex-col md:flex-row">
        {/* Hamburger Menu for Mobile */}
        <div className="bg-red-950 text-white p-4 md:hidden flex justify-between items-center">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="text-xl font-bold"
          >
            ☰
          </button>
        </div>

        {/* Sidebar */}
        <aside
          className={`bg-red-700 text-white w-full md:w-1/4 p-4 transform ${
            sidebarOpen
              ? "translate-x-0 "
              : "hidden md:flex lg:flex -translate-x-full"
          } hi md:translate-x-0 transition-transform duration-300 ease-in-out`}
        >
          <ul>
            <li
              className={`p-2 cursor-pointer ${
                selectedOption === "CreateAppointment" && "bg-red-600"
              }`}
              onClick={() => setSelectedOption("CreateAppointment")}
            >
              نوبت دهی
            </li>
            <li
              className={`p-2 cursor-pointer ${
                selectedOption === "CreateAccount" && "bg-red-600"
              }`}
              onClick={() => setSelectedOption("CreateAccount")}
            >
              ایجاد حساب کاربری جدید
            </li>
            <li
              className={`p-2 cursor-pointer mt-2 ${
                selectedOption === "DeleteAccount" && "bg-red-600"
              }`}
              onClick={() => setSelectedOption("DeleteAccount")}
            >
              حذف حساب کاربری
            </li>
            <li
              className={`p-2 cursor-pointer mt-2 ${
                selectedOption === "report" && "bg-red-600"
              }`}
              onClick={() => setSelectedOption("report")}
            >
              گزارشات
            </li>
            <li
              className={`p-2 cursor-pointer mt-2 ${
                selectedOption === "users" && "bg-red-600"
              }`}
              onClick={() => setSelectedOption("users")}
            >
              کارمندان زون
            </li>
          </ul>
        </aside>

        {/* Main Content */}
        <main className="flex-grow bg-gray-100 p-4">
          {selectedOption === "CreateAccount" ? (
            <section className="dir-rtl">
              <h2 className="text-xl font-semibold mb-4">
                ایجاد حساب کاربری جدید
              </h2>
              <RegisterUser id={id} />
            </section>
          ) : selectedOption === "DeleteAccount" ? (
            <section>
              <h2 className="text-xl font-semibold mb-4">حذف حساب کاربری</h2>
              <DeleteUser id={id} />
            </section>
          ) : selectedOption === "CreateAppointment" ? (
            <section>
              <h2 className="text-xl font-semibold mb-4">نوبت دهی</h2>
              <CreateAppointment id={id} />
            </section>
          ) : selectedOption === "report" ? (
            <section>
              <h2 className="text-xl font-semibold mb-4">گزارشات</h2>
              <Reporting id={id} />
            </section>
          ): selectedOption === "users" ? (
            <section>
              <h2 className="text-xl font-semibold mb-4">گزارشات</h2>
              <UsersInZone />
            </section>
          ) : (
            <section></section>
          )}
        </main>
      </div>
    </div>
  );
};

export default AdminDashboard;
