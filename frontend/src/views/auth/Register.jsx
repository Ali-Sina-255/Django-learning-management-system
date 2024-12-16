import React, { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import BaseHeader from "../../partials/BaseHeader";
import BaseFooter from "../../partials/BaseFooter";
import Swal from "sweetalert2";

import apiInstance from "../../utils/axios";
import { register } from "../../utils/auth";
// frontend / src / utils / auth.js;
function Register() {
  const [fullName, setFullName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [password2, setPassword2] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const navigate = useNavigate();
  const handelSubmittedForm = async (e) => {
    e.preventDefault();
    setIsLoading(true);
    const { error } = await register(fullName, email, password, password2);
    if (error) {
      alert(error.response.email);
      alert(error.response.fullName);
    } else {
      navigate("/");
      alert("registration was  successful, you have been logged in!");
    }
  };
  return (
    <>
      <BaseHeader />

      <section
        className="container d-flex flex-column vh-100"
        style={{ marginTop: "150px" }}
      >
        <div className="row align-items-center justify-content-center g-0 h-lg-100 py-8">
          <div className="col-lg-5 col-md-8 py-8 py-xl-0">
            <div className="card shadow">
              <div className="card-body p-6">
                <div className="mb-4">
                  <h1 className="mb-1 fw-bold">Sign up</h1>
                  <span>
                    Already have an account?
                    <Link to="/login/" className="ms-1">
                      Sign In
                    </Link>
                  </span>
                </div>
                {/* Form */}
                <form
                  className="needs-validation"
                  noValidate=""
                  onSubmit={handelSubmittedForm}
                >
                  {/* Username */}
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">
                      Full Name
                    </label>
                    <input
                      type="text"
                      id="full_name"
                      className="form-control"
                      name="full_name"
                      placeholder="John Doe"
                      required=""
                      onChange={(e) => setFullName(e.target.value)}
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="email" className="form-label">
                      Email Address
                    </label>
                    <input
                      type="email"
                      id="email"
                      className="form-control"
                      name="email"
                      placeholder="johndoe@gmail.com"
                      required=""
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </div>

                  {/* Password */}
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                      Password
                    </label>
                    <input
                      type="password"
                      id="password"
                      className="form-control"
                      name="password"
                      placeholder="**************"
                      required=""
                      onChange={(e) => setPassword(e.target.value)}
                    />
                  </div>
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                      Confirm Password
                    </label>
                    <input
                      type="password"
                      id="password"
                      className="form-control"
                      name="password"
                      placeholder="**************"
                      required=""
                      onChange={(e) => setPassword2(e.target.value)}
                    />
                  </div>
                  <div>
                    <div className="d-grid">
                      <button type="submit" className="btn btn-primary">
                        Sign Up <i className="fas fa-user-plus"></i>
                      </button>
                    </div>
                  </div>
                </form>
              </div>
            </div>
          </div>
        </div>
      </section>

      <BaseFooter />
    </>
  );
}

export default Register;
