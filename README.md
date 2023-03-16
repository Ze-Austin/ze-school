<!-- Back to Top Navigation Anchor -->
<a name="readme-top"></a>

<!-- Project Shields -->
<div align="center">

  [![Contributors][contributors-shield]][contributors-url]
  [![Forks][forks-shield]][forks-url]
  [![Stargazers][stars-shield]][stars-url]
  [![Issues][issues-shield]][issues-url]
  [![MIT License][license-shield]][license-url]
  [![Twitter][twitter-shield]][twitter-url]
</div>

<!-- Project Name -->
<div align="center">
  <h1>Ze School</h1>
</div>

<div>
  <p align="center">
    <a href="https://github.com/Ze-Austin/ze-school#readme"><strong>Explore the Docs »</strong></a>
    <br />
    <a href="https://github.com/Ze-Austin/ze-school/blob/main/images/Ze_School_Full_Page.png">View Demo</a>
    ·
    <a href="https://github.com/Ze-Austin/ze-school/issues">Report Bug</a>
    ·
    <a href="https://github.com/Ze-Austin/ze-school/issues">Request Feature</a>
  </p>
</div>

---

<!-- Table of Contents -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-ze-school">About Ze School</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li><a href="#lessons-learned">Lessons Learned</a></li>
    <li><a href="#usage">Usage</a></li>    
    <li><a href="#sample">Sample</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
  <p align="right"><a href="#readme-top">back to top</a></p>
</details>

---

<!-- About the Project -->
## About Ze School

Ze School is a REST API which enables school staff to register accounts and manage student data on the PythonAnywhere-powered web app. CRUD operations can be carried out on the student data, with an easy-to-use Swagger UI setup for testing and integration with the front end.

Students have limited access to the app, as a student can only change their profile details and view their profile, courses, grades and CGPA.

This student management API was built with Python's Flask-RESTX by <a href="https://www.github.com/Ze-Austin">Ze Austin</a> during Backend Engineering live classes at <a href="https://altschoolafrica.com/schools/engineering">AltSchool Africa</a>.

<p align="right"><a href="#readme-top">back to top</a></p>

### Built With:

![Python][python]
![Flask][flask]
![SQLite][sqlite]

<p align="right"><a href="#readme-top">back to top</a></p>

---
<!-- Lessons from the Project -->
## Lessons Learned

Creating this API helped me learn and practice:
* API Development with Python
* App Deployment with PythonAnywhere
* Testing with pytest and Insomnia
* Documentation
* Debugging
* Routing
* Database Management
* Internet Security
* User Authentication
* User Authorization

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- GETTING STARTED -->
## Usage

To use this API, follow these steps:

1. Open the PythonAnywhere web app on your browser: https://zeaustin.pythonanywhere.com

2. Create an admin or student account:
    - Click 'admin' to reveal a dropdown menu of administration routes, then register an admin account via the '/admin/register' route
    - Click 'students' to reveal a dropdown menu of student routes, then register a student account via the '/students/register' route

3. Sign in via the '/auth/login' route to generate a JWT token. Copy this access token without the quotation marks

4. Scroll up to click 'Authorize' at top right. Enter the JWT token in the given format, for example:
   ```
   Bearer this1is2a3rather4long5hex6string
   ```

5. Click 'Authorize' and then 'Close'

6. Now authorized, you can create, view, update and delete students, courses, grades and admins via the many routes in 'students', 'courses' and 'admin'. You can also get:
    - All students taking a course
    - All courses taken by a student
    - A student's grades in percentage (eg: 84.8%) and letters (eg: A)
    - A student's CGPA, calculated based on all grades from all courses they are taking

7. When you're done, click 'Authorize' at top right again to then 'Logout'

**Note:** When using this API in production, please [fork this repo](https://github.com/Ze-Austin/ze-school) and uncomment the `@admin_required()` decorator in line 51 of [the admin views file](https://github.com/Ze-Austin/ze-school/blob/main/api/admin/views.py). This will ensure that students and other users will not be authorized to access the admin creation route after the first admin is registered.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Sample Screenshot -->
## Sample

<br />

[![Ze School Screenshot][ze-school-screenshot]](https://github.com/Ze-Austin/ze-school/blob/main/images/Ze_School_Full_Page.png)

<br/>

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- License -->
## License

Distributed under the MIT License. See <a href="https://github.com/Ze-Austin/ze-school/blob/main/LICENSE">LICENSE</a> for more information.

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Contact -->
## Contact

Dr Austin Wopara - [@Ze_Austin](https://twitter.com/Ze_Austin) - austinwopara@gmail.com

Project Link: [Ze School](https://github.com/Ze-Austin/ze-school)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Acknowledgements -->
## Acknowledgements

This project was made possible by:

* [AltSchool Africa School of Engineering](https://altschoolafrica.com/schools/engineering)
* [Caleb Emelike's Flask Lessons](https://github.com/CalebEmelike)

<p align="right"><a href="#readme-top">back to top</a></p>

---

<!-- Markdown Links & Images -->
[contributors-shield]: https://img.shields.io/github/contributors/Ze-Austin/ze-school.svg?style=for-the-badge
[contributors-url]: https://github.com/Ze-Austin/ze-school/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Ze-Austin/ze-school.svg?style=for-the-badge
[forks-url]: https://github.com/Ze-Austin/ze-school/network/members
[stars-shield]: https://img.shields.io/github/stars/Ze-Austin/ze-school.svg?style=for-the-badge
[stars-url]: https://github.com/Ze-Austin/ze-school/stargazers
[issues-shield]: https://img.shields.io/github/issues/Ze-Austin/ze-school.svg?style=for-the-badge
[issues-url]: https://github.com/Ze-Austin/ze-school/issues
[license-shield]: https://img.shields.io/github/license/Ze-Austin/ze-school.svg?style=for-the-badge
[license-url]: https://github.com/Ze-Austin/ze-school/blob/main/LICENSE.txt
[twitter-shield]: https://img.shields.io/badge/-@ze_austin-1ca0f1?style=for-the-badge&logo=twitter&logoColor=white&link=https://twitter.com/ze_austin
[twitter-url]: https://twitter.com/ze_austin
[ze-school-screenshot]: https://github.com/Ze-Austin/ze-school/blob/main/images/Ze_School_Full_Page.png
[python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[flask]: https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white
[sqlite]: https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white