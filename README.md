<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<!-- <br />
<div align="center">
  <a href="https://github.com/giuseppesalvi/website-screenshot-and-code-getter">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a> -->

<h3 align="center">Website Screenshot And Code Getter</h3>

  <p align="center">
    This is a tool to get the screenshot and the html code of a given website URL
    <br />
    <!-- <a href="https://github.com/giuseppesalvi/website-screenshot-and-code-getter"><strong>Explore the docs »</strong></a> -->
    <!-- <br /> -->
    <br />
    <a href="https://github.com/giuseppesalvi/website-screenshot-and-code-getter">View Demo</a>
    ·
    <a href="https://github.com/giuseppesalvi/website-screenshot-and-code-getter/issues">Report Bug</a>
    ·
    <a href="https://github.com/giuseppesalvi/website-screenshot-and-code-getter/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

This project is a part of my Master's Degree thesis in Computer Engineering at Politecnico di Torino. 
The tool can automatically extract screenshots and code from websites while minimizing the noise in the extracted textual files and the number of resources. 

This automated pipeline can be utilized to generate a dataset comprising pairs of website code and images, which can be used for subsequent machine-learning tasks.

The main repository of the Thesis can be found at [webUI2ode](https://github.com/giuseppesalvi/webUI2code).
<!-- [![Product Name Screen Shot][product-screenshot]](https://example.com)
 -->
<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

[![Python][Python.org]][Python-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started


### Prerequisites

* python 3.9.13
  ```sh
  python3 --version 
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/giuseppesalvi/website-screenshot-and-code-getter.git
   ```
2. Install requirements 
- Python Dependencies:
    ```bash
    pip install -r requirements.txt
    ```
- Node Modules:
    ```bash
    npm install
    ```

- Clean HTML Tool (Global Installation):
    ```bash
    npm install clean-html -g
    ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- USAGE EXAMPLES -->
## Usage

<p align="right">(<a href="#readme-top">back to top</a>)</p>

A guide on how to run a complete extraction experiment is available [here](https://github.com/giuseppesalvi/website-screenshot-and-code-getter/blob/main/run_complete_experiment.md)
The tool can be used in several ways and some of the features can be disabled by not passing specific command line arguments.

### Command Line Arguments
- `--website` : specify the url of the website 
- `--website_list` : specify the path of the file with the list of website urls
- `--just_new` : process only the websites not already present in the result folder
- `--task` : specify the task (choices = `all`, `screenshot`, `code`, `stats`, `log`, default = `all`)
- `--batch` : max number of websites processed (default = `10`)

### Examples

#### Get the screenshot for the website www.google.com
```python main.py --website https://www.google.com --task screenshot```

#### Get the screenshot and the code for the first 5 websites in the list websites.txt
```python main.py --website_list websites.txt --batch 5```

#### Get the screenshot and the code for 10 new websites from the list in websites.txt
```python main.py --website_list websites.txt --just_new```

See the [open issues](https://github.com/giuseppesalvi/website-screenshot-and-code-getter/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what makes the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the GPL License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Giuseppe Salvi - s287583@studenti.polito.it 

Project Link: [https://github.com/giuseppesalvi/website-screenshot-and-code-getter](https://github.com/giuseppesalvi/website-screenshot-and-code-getter)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [sanitize-html](https://github.com/apostrophecms/sanitize-html)
* [tinycss2](https://pypi.org/project/tinycss2/)
* [clean-html](https://github.com/dave-kennedy/clean-html)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/giuseppesalvi/website-screenshot-and-code-getter.svg?style=for-the-badge
[contributors-url]: https://github.com/giuseppesalvi/website-screenshot-and-code-getter/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/giuseppesalvi/website-screenshot-and-code-getter.svg?style=for-the-badge
[forks-url]: https://github.com/giuseppesalvi/website-screenshot-and-code-getter/network/members
[stars-shield]: https://img.shields.io/github/stars/giuseppesalvi/website-screenshot-and-code-getter.svg?style=for-the-badge
[stars-url]: https://github.com/giuseppesalvi/website-screenshot-and-code-getter/stargazers
[issues-shield]: https://img.shields.io/github/issues/giuseppesalvi/website-screenshot-and-code-getter.svg?style=for-the-badge
[issues-url]: https://github.com/giuseppesalvi/website-screenshot-and-code-getter/issues
[license-shield]: https://img.shields.io/github/license/giuseppesalvi/website-screenshot-and-code-getter.svg?style=for-the-badge
[license-url]: https://github.com/giuseppesalvi/website-screenshot-and-code-getter/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/giuseppe-salvi-03239a248
[product-screenshot]: images/screenshot.png
[Next.js]: https://img.shields.io/badge/next.js-000000?style=for-the-badge&logo=nextdotjs&logoColor=white
[Next-url]: https://nextjs.org/
[React.js]: https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB
[React-url]: https://reactjs.org/
[Vue.js]: https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs&logoColor=4FC08D
[Vue-url]: https://vuejs.org/
[Angular.io]: https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white
[Angular-url]: https://angular.io/
[Svelte.dev]: https://img.shields.io/badge/Svelte-4A4A55?style=for-the-badge&logo=svelte&logoColor=FF3E00
[Svelte-url]: https://svelte.dev/
[Laravel.com]: https://img.shields.io/badge/Laravel-FF2D20?style=for-the-badge&logo=laravel&logoColor=white
[Laravel-url]: https://laravel.com
[Bootstrap.com]: https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white
[Bootstrap-url]: https://getbootstrap.com
[JQuery.com]: https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white
[JQuery-url]: https://jquery.com 
[Python-url]: https://www.python.org/
[Python.org]: https://img.shields.io/badge/Python-306998?style=for-the-badge&logo=python&logoColor=white 
