import { useState, useEffect } from "react";
import BaseHeader from "../../partials/BaseHeader";
import BaseFooter from "../../partials/BaseFooter";
import { Link } from "react-router-dom";
import Rater from "react-rater";
import "react-rater/lib/react-rater.css";
import apiInstance from "../../utils/axios";
function Index() {
  const [courses, setCourses] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const fetchCourse = async () => {
    setIsLoading(true);
    try {
      await apiInstance.get(`course/course-list/`).then((response) => {
        setCourses(response.data);
        setIsLoading(false);
        console.log("data", response.data);
      });
    } catch (error) {
      console.error("Error fetching courses:", error);
    }
  };
  useEffect(() => {
    fetchCourse();
  }, []);
  return (
    <>
      <BaseHeader />

      <section className="py-lg-8 py-5">
        {/* container */}
        <div className="container my-lg-8">
          {/* row */}
          <div className="row align-items-center">
            {/* col */}
            <div className="col-lg-6 mb-6 mb-lg-0">
              <div>
                {/* heading */}
                <h5 className="text-dark mb-4">
                  <i className="fe fe-check icon-xxs icon-shape bg-light-success text-success rounded-circle me-2" />
                  Most trusted education platform
                </h5>
                {/* heading */}
                <h1 className="display-3 fw-bold mb-3">
                  Grow your skills and advance career
                </h1>
                {/* para */}
                <p className="pe-lg-10 mb-5">
                  Start, switch, or advance your career with more than 5,000
                  courses, Professional Certificates, and degrees from
                  world-class universities and companies.
                </p>
                {/* btn */}
                <a href="#" className="btn btn-primary fs-4 text-inherit ms-3">
                  Join Free Now <i className="fas fa-plus"></i>
                </a>
                <a
                  href="https://www.youtube.com/watch?v=Nfzi7034Kbg"
                  className="btn btn-outline-success fs-4 text-inherit ms-3"
                >
                  Watch Demo <i className="fas fa-video"></i>
                </a>
              </div>
            </div>
            {/* col */}
            <div className="col-lg-6 d-flex justify-content-center">
              {/* images */}
              <div className="position-relative">
                <img
                  src="https://geeksui.codescandy.com/geeks/assets/images/background/acedamy-img/girl-image.png"
                  alt="girl"
                  className="end-0 bottom-0"
                />
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="pb-8">
        <div className="container mb-lg-8">
          {/* row */}
          <div className="row mb-5">
            <div className="col-md-6 col-lg-3 border-top-md border-top pb-4  border-end-md">
              {/* text */}
              <div className="py-7 text-center">
                <div className="mb-3">
                  <i className="fe fe-award fs-2 text-info" />
                </div>
                <div className="lh-1">
                  <h2 className="mb-1">316,000+</h2>
                  <span>Qualified Instructor</span>
                </div>
              </div>
            </div>
            <div className="col-md-6 col-lg-3 border-top-md border-top border-end-lg">
              {/* icon */}
              <div className="py-7 text-center">
                <div className="mb-3">
                  <i className="fe fe-users fs-2 text-warning" />
                </div>
                {/* text */}
                <div className="lh-1">
                  <h2 className="mb-1">1.8 Billion+</h2>
                  <span>Course enrolments</span>
                </div>
              </div>
            </div>
            <div className="col-md-6 col-lg-3 border-top-lg border-top border-end-md">
              {/* icon */}
              <div className="py-7 text-center">
                <div className="mb-3">
                  <i className="fe fe-tv fs-2 text-primary" />
                </div>
                {/* text */}
                <div className="lh-1">
                  <h2 className="mb-1">41,000+</h2>
                  <span>Courses in 42 languages</span>
                </div>
              </div>
            </div>
            <div className="col-md-6 col-lg-3 border-top-lg border-top">
              {/* icon */}
              <div className="py-7 text-center">
                <div className="mb-3">
                  <i className="fe fe-film fs-2 text-success" />
                </div>
                {/* text */}
                <div className="lh-1">
                  <h2 className="mb-1">179,000+</h2>
                  <span>Online Videos</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="mb-5">
        <div className="container mb-lg-8 ">
          <div className="row mb-5 mt-3">
            {/* col */}
            <div className="col-12">
              <div className="mb-6">
                <h2 className="mb-1 h1">🔥Most Popular Courses</h2>
                <p>
                  These are the most popular courses among Geeks Courses
                  learners worldwide in year 2022
                </p>
              </div>
            </div>
          </div>
          <div className="row">
            <div className="col-md-12">
              <div className="row row-cols-1 row-cols-md-2 row-cols-lg-4 g-4">
                <div className="col">
                  {courses.map((course) => (
                    <div className="card card-hover">
                      <Link to={`/course-detail/slug/`}>
                        <img
                          src={course.image}
                          alt="course"
                          className="card-img-top"
                          style={{
                            width: "100%",
                            height: "200px",
                            objectFit: "cover",
                          }}
                        />
                      </Link>
                      <div className="card-body">
                        <div className="d-flex justify-content-between align-items-center mb-3">
                          <span className="badge bg-info">{course.level}</span>
                          <span className="badge bg-success">
                            {course.language}
                          </span>
                          <a href="#" className="fs-5">
                            <i className="fas fa-heart text-danger align-middle" />
                          </a>
                        </div>
                        <h4 className="mb-2 text-truncate-line-2 ">
                          <Link
                            to={`/course-detail/slug/`}
                            className="text-inherit text-decoration-none text-dark fs-5"
                          >
                            {course.title}
                          </Link>
                        </h4>
                        <small>By: {course.teacher.full_name}</small> <br />
                        <small>
                          {course.students.length} Student
                          {course.students.length > 1 && "s"}
                        </small>
                        <br />
                        <div className="lh-1 mt-3 d-flex">
                          <span className="align-text-top">
                            <span className="fs-6">
                              <Rater total={5} rating={course.average_rating} />
                            </span>
                          </span>
                          <span className="text-warning">4.5</span>
                          <span className="fs-6 ms-2">
                            ({course.reviews.length} Review
                            {course.reviews.length > 1 && "s"})
                          </span>
                        </div>
                      </div>
                      {/* Card Footer */}
                      <div className="card-footer">
                        <div className="row align-items-center g-0">
                          <div className="col">
                            <h5 className="mb-0">${course.price}</h5>
                          </div>
                          <div className="col-auto">
                            <button
                              type="button"
                              className="text-inherit text-decoration-none btn btn-primary me-2"
                            >
                              <i className="fas fa-shopping-cart text-primary text-white" />
                            </button>
                            <Link
                              to={""}
                              className="text-inherit text-decoration-none btn btn-primary"
                            >
                              Enroll Now{" "}
                              <i className="fas fa-arrow-right text-primary align-middle me-2 text-white" />
                            </Link>
                          </div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
              <nav className="d-flex mt-5">
                <ul className="pagination">
                  <li className="">
                    <button className="page-link me-1">
                      <i className="ci-arrow-left me-2" />
                      Previous
                    </button>
                  </li>
                </ul>
                <ul className="pagination">
                  <li key={1} className="active">
                    <button className="page-link">1</button>
                  </li>
                </ul>
                <ul className="pagination">
                  <li className={`totalPages`}>
                    <button className="page-link ms-1">
                      Next
                      <i className="ci-arrow-right ms-3" />
                    </button>
                  </li>
                </ul>
              </nav>
            </div>
          </div>
        </div>
      </section>

      <section className="my-8 py-lg-8">
        {/* container */}
        <div className="container">
          {/* row */}
          <div className="row align-items-center bg-primary gx-0 rounded-3 mt-5">
            {/* col */}
            <div className="col-lg-6 col-12 d-none d-lg-block">
              <div className="d-flex justify-content-center pt-4">
                {/* img */}
                <div className="position-relative">
                  <img
                    src="https://geeksui.codescandy.com/geeks/assets/images/png/cta-instructor-1.png"
                    alt="image"
                    className="img-fluid mt-n8"
                  />
                  <div className="ms-n8 position-absolute bottom-0 start-0 mb-6">
                    <img
                      src="https://geeksui.codescandy.com/geeks/assets/images/svg/dollor.svg"
                      alt="dollor"
                    />
                  </div>
                  {/* img */}
                  <div className="me-n4 position-absolute top-0 end-0">
                    <img
                      src="https://geeksui.codescandy.com/geeks/assets/images/svg/graph.svg"
                      alt="graph"
                    />
                  </div>
                </div>
              </div>
            </div>
            <div className="col-lg-5 col-12">
              <div className="text-white p-5 p-lg-0">
                {/* text */}
                <h2 className="h1 text-white">Become an instructor today</h2>
                <p className="mb-0">
                  Instructors from around the world teach millions of students
                  on Geeks. We provide the tools and skills to teach what you
                  love.
                </p>
                <a href="#" className="btn bg-white text-dark fw-bold mt-4">
                  Start Teaching Today <i className="fas fa-arrow-right"></i>
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="bg-gray-200 pt-8 pb-8 mt-5">
        <div className="container pb-8">
          {/* row */}
          <div className="row mb-lg-8 mb-5">
            <div className="offset-lg-1 col-lg-10 col-12">
              <div className="row align-items-center">
                {/* col */}
                <div className="col-lg-6 col-md-8">
                  {/* rating */}
                  <div>
                    <div className="mb-3">
                      <span className="lh-1">
                        <span className="align-text-top ms-2">
                          <i className="fas fa-star text-warning"></i>
                          <i className="fas fa-star text-warning"></i>
                          <i className="fas fa-star text-warning"></i>
                          <i className="fas fa-star text-warning"></i>
                          <i className="fas fa-star text-warning"></i>
                        </span>
                        <span className="text-dark fw-semibold">4.5/5.0</span>
                      </span>
                      <span className="ms-2">(Based on 3265 ratings)</span>
                    </div>
                    {/* heading */}
                    <h2 className="h1">What our students say</h2>
                    <p className="mb-0">
                      Hear from
                      <span className="text-dark">teachers</span>,
                      <span className="text-dark">trainers</span>, and
                      <span className="text-dark">leaders</span>
                      in the learning space about how Geeks empowers them to
                      provide quality online learning experiences.
                    </p>
                  </div>
                </div>
                <div className="col-lg-6 col-md-4 text-md-end mt-4 mt-md-0">
                  {/* btn */}
                  <a href="#" className="btn btn-primary">
                    View Reviews
                  </a>
                </div>
              </div>
            </div>
          </div>
          {/* row */}
          <div className="row">
            {/* col */}
            <div className="col-md-12">
              <div className="position-relative">
                {/* controls */}
                {/* slider */}
                <div className="sliderTestimonial">
                  {/* item */}
                  <div className="row">
                    <div className="col-lg-4">
                      <div className="item">
                        <div className="card">
                          <div className="card-body text-center p-6">
                            {/* img */}
                            <img
                              src="../../assets/images/avatar/avatar-1.jpg"
                              alt="avatar"
                              className="avatar avatar-lg rounded-circle"
                            />
                            <p className="mb-0 mt-3">
                              “The generated lorem Ipsum is therefore always
                              free from repetition, injected humour, or words
                              etc generate lorem Ipsum which looks racteristic
                              reasonable.”
                            </p>
                            {/* rating */}
                            <div className="lh-1 mb-3 mt-4">
                              <span className="fs-6 align-top">
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                              </span>
                              <span className="text-warning">5</span>
                              {/* text */}
                            </div>
                            <h3 className="mb-0 h4">Gladys Colbert</h3>
                            <span>Software Engineer at Palantir</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="col-lg-4">
                      <div className="item">
                        <div className="card">
                          <div className="card-body text-center p-6">
                            {/* img */}
                            <img
                              src="../../assets/images/avatar/avatar-1.jpg"
                              alt="avatar"
                              className="avatar avatar-lg rounded-circle"
                            />
                            <p className="mb-0 mt-3">
                              “The generated lorem Ipsum is therefore always
                              free from repetition, injected humour, or words
                              etc generate lorem Ipsum which looks racteristic
                              reasonable.”
                            </p>
                            {/* rating */}
                            <div className="lh-1 mb-3 mt-4">
                              <span className="fs-6 align-top">
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                              </span>
                              <span className="text-warning">5</span>
                              {/* text */}
                            </div>
                            <h3 className="mb-0 h4">Gladys Colbert</h3>
                            <span>Software Engineer at Palantir</span>
                          </div>
                        </div>
                      </div>
                    </div>
                    <div className="col-lg-4">
                      <div className="item">
                        <div className="card">
                          <div className="card-body text-center p-6">
                            {/* img */}
                            <img
                              src="../../assets/images/avatar/avatar-1.jpg"
                              alt="avatar"
                              className="avatar avatar-lg rounded-circle"
                            />
                            <p className="mb-0 mt-3">
                              “The generated lorem Ipsum is therefore always
                              free from repetition, injected humour, or words
                              etc generate lorem Ipsum which looks racteristic
                              reasonable.”
                            </p>
                            {/* rating */}
                            <div className="lh-1 mb-3 mt-4">
                              <span className="fs-6 align-top">
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                                <svg
                                  xmlns="http://www.w3.org/2000/svg"
                                  width={11}
                                  height={11}
                                  fill="currentColor"
                                  className="bi bi-star-fill text-warning"
                                  viewBox="0 0 16 16"
                                >
                                  <path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.282.95l-3.522 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z" />
                                </svg>
                              </span>
                              <span className="text-warning">5</span>
                              {/* text */}
                            </div>
                            <h3 className="mb-0 h4">Gladys Colbert</h3>
                            <span>Software Engineer at Palantir</span>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <BaseFooter />
    </>
  );
}

export default Index;
