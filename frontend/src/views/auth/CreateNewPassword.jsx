import React, { useState } from "react";
import BaseHeader from "../../partials/BaseHeader";
import BaseFooter from "../../partials/BaseFooter";
import { useNavigate, useSearchParams } from "react-router-dom";
import apiInstance from "../../utils/axios";

function CreateNewPassword() {
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();

  const otp = searchParams.get("otp");
  const uuidb64 = searchParams.get("uuidb64");
  const refresh_token = searchParams.get("refresh_token");

  // Function to properly encode UUID to Base64 and ensure it's padded correctly
  const encodeUUID = (id) => {
    let base64 = btoa(id); // Base64 encode the string (ID)
    // Ensure the base64 string is padded properly
    while (base64.length % 4 !== 0) {
      base64 += "="; // Padding the base64 string
    }
    return base64;
  };

  // If you're encoding the user ID, you can pass it as follows:
  // Example: Let's assume we have a userId (you should replace it with actual userId)
  const userId = "2"; // Example user ID
  const encodedUUID = encodeUUID(userId); // Base64 encode it
  console.log("Encoded UUID: ", encodedUUID); // Ensure it's correctly logged

  // Handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();

    // Check if passwords match
    if (confirmPassword !== password) {
      alert("Passwords do not match");
    } else {
      setIsLoading(true);

      const data = {
        password,
        otp,
        uuidb64: encodedUUID,
        refresh_token,
      };

      // Make the API call to change the password
      apiInstance
        .post("user/password-change/", data) // Send data as JSON
        .then((response) => {
          console.log(response.data);
          alert("Password changed successfully"); // Alert the user
          navigate("/login"); // Redirect to the login page after success
        })
        .catch((error) => {
          console.error("Error changing password:", error);
          alert("Error: " + (error.response?.data?.message || error.message));
        })
        .finally(() => {
          setIsLoading(false); // Reset loading state after API call
        });
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
                  <h1 className="mb-1 fw-bold">Create New Password</h1>
                  <span>Choose a new password for your account</span>
                </div>
                <form
                  className="needs-validation"
                  noValidate=""
                  onSubmit={handleSubmit}
                >
                  <div className="mb-3">
                    <label htmlFor="password" className="form-label">
                      Enter New Password
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
                    <div className="invalid-feedback">
                      Please enter a valid password.
                    </div>
                  </div>

                  <div className="mb-3">
                    <label htmlFor="confirmPassword" className="form-label">
                      Confirm New Password
                    </label>
                    <input
                      type="password"
                      id="confirmPassword"
                      className="form-control"
                      name="confirmPassword"
                      placeholder="**************"
                      required=""
                      onChange={(e) => setConfirmPassword(e.target.value)}
                    />
                    <div className="invalid-feedback">
                      Please confirm the password correctly.
                    </div>
                  </div>

                  <div>
                    <div className="d-grid">
                      <button
                        type="submit"
                        className="btn btn-primary"
                        disabled={isLoading}
                      >
                        {isLoading ? "Saving..." : "Save New Password"}{" "}
                        <i className="fas fa-check-circle"></i>
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

export default CreateNewPassword;
