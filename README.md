<h1 align="center">
  <a href="https://github.com/mobilemike/alpha">
    <!-- Please provide path to your logo here -->
    <img src="docs/images/alpha.png" alt="Logo" width="100" height="100">
  </a>
</h1>

<div align="center">
  Alpha McBottington
  <br />
  <br />
  <a href="https://github.com/mobilemike/alpha/issues/new?assignees=&labels=bug&template=01_BUG_REPORT.md&title=bug%3A+">Report a Bug</a>
  ·
  <a href="https://github.com/mobilemike/alpha/issues/new?assignees=&labels=enhancement&template=02_FEATURE_REQUEST.md&title=feat%3A+">Request a Feature</a>
  ·
  <a href="https://github.com/mobilemike/alpha/discussions">Ask a Question</a>
</div>

<div align="center">
<br />

[![Project license](https://img.shields.io/github/license/mobilemike/alpha.svg?style=flat-square)](LICENSE)

[![Pull Requests welcome](https://img.shields.io/badge/PRs-welcome-ff69b4.svg?style=flat-square)](https://github.com/mobilemike/alpha/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22)
[![code with love by mobilemike](https://img.shields.io/badge/%3C%2F%3E%20with%20%E2%99%A5%20by-mobilemike-ff1414.svg?style=flat-square)](https://github.com/mobilemike)

</div>

<details open="open">
<summary>Table of Contents</summary>

- [About](#about)
  - [Built With](#built-with)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Roadmap](#roadmap)
- [Support](#support)
- [Project assistance](#project-assistance)
- [Contributing](#contributing)
- [Authors & contributors](#authors--contributors)
- [Security](#security)
- [License](#license)

</details>

---

## About

This project creates an AI chat bot named Alpha that can:

- Receive messages from BlueBubbles (iMessage) via webhooks
- Process messages using Google's Gemini AI model
- Send automated responses back through BlueBubbles
- Handle typing indicators and message events

## Features

- 🤖 AI-powered responses using Google Gemini
- 📱 Seamless iMessage integration
- ⌨️ Typing indicator support
- 🔒 Secure webhook handling
- 📝 Comprehensive logging
- ⚡ Fast response times

### Built With

- BlueBubbles
- FastAPI
- Google Gemini
- Pydantic
- HTTPX
- Structlog

## Getting Started

### Prerequisites

- Python 3.12+
- BlueBubbles server setup
- Google AI API key
- Environment variables properly configured

### Installation

1. Clone the repository:

    ```bash
    git clone <repository-url>
    cd alpha
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Create a `.env` file with the following variables:

    ```properties
    GOOGLE_AI_API_KEY=<your-google-ai-api-key>
    BB_URL=<your-bluebubbles-server-url>
    BB_PASSWORD=<your-bluebubbles-password>
    ENVIRONMENT=<development/production>

## Usage

1. Start the FastAPI server:

    ```bash
    uvicorn app.core:app --reload
    ```

2. Configure BlueBubbles to send webhooks to your server endpoint:

    ```text
    http://<your-server>/webhook
    ```

The bot will automatically:

- Receive incoming messages
- Generate responses using Gemini AI
- Send responses back through iMessage

## Roadmap

See the [open issues](https://github.com/mobilemike/alpha/issues) for a list of proposed features (and known issues).

- [Top Feature Requests](https://github.com/mobilemike/alpha/issues?q=label%3Aenhancement+is%3Aopen+sort%3Areactions-%2B1-desc) (Add your votes using the 👍 reaction)
- [Top Bugs](https://github.com/mobilemike/alpha/issues?q=is%3Aissue+is%3Aopen+label%3Abug+sort%3Areactions-%2B1-desc) (Add your votes using the 👍 reaction)
- [Newest Bugs](https://github.com/mobilemike/alpha/issues?q=is%3Aopen+is%3Aissue+label%3Abug)

## Support

Reach out to the maintainer at one of the following places:

- [GitHub Discussions](https://github.com/mobilemike/alpha/discussions)
- Contact options listed on [this GitHub profile](https://github.com/mobilemike)

## Project assistance

If you want to say **thank you** or/and support active development of Alpha McBottington:

- Add a [GitHub Star](https://github.com/mobilemike/alpha) to the project.
- Tweet about the Alpha McBottington.
- Write interesting articles about the project on [Dev.to](https://dev.to/), [Medium](https://medium.com/) or your personal blog.

Together, we can make Alpha McBottington **better**!

## Contributing

First off, thanks for taking the time to contribute! Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make will benefit everybody else and are **greatly appreciated**.

Please read [our contribution guidelines](docs/CONTRIBUTING.md), and thank you for being involved!

## Authors & contributors

The original setup of this repository is by [Mike Karolow](https://github.com/mobilemike).

For a full list of all authors and contributors, see [the contributors page](https://github.com/mobilemike/alpha/contributors).

## Security

Alpha McBottington follows good practices of security, but 100% security cannot be assured.
Alpha McBottington is provided **"as is"** without any **warranty**. Use at your own risk.

_For more information and to report security issues, please refer to our [security documentation](docs/SECURITY.md)._

## License

This project is licensed under the **MIT license**.

See [LICENSE](LICENSE) for more information.
