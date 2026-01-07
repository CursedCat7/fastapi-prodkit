# Security Policy

This is a personal, non-commercial side project maintained on a best-effort basis. While security reports are welcome, response times may vary.

## Supported Versions

Security fixes are provided on a best-effort basis for:

- The **latest release** published on PyPI, and
- The current `main` branch.

Older versions may not receive security fixes. When in doubt, please upgrade to the latest release and retest.

## Reporting a Vulnerability

If you believe you have found a security vulnerability in **fastapi-prodkit**, please report it responsibly.

### Please do not
- Open a public GitHub issue describing the vulnerability.
- Publish exploit code or detailed reproduction steps publicly before a fix is available.

### How to report
Please email the maintainer using the contact address listed on the maintainer’s GitHub profile:

- GitHub profile: https://github.com/CursedCat7


If you cannot access the profile email, you may use: **CursedCat7@users.noreply.github.com**

When emailing, please use the subject line:
**[SECURITY] fastapi-prodkit vulnerability report**


### What to include
To help with triage, please include:
- A clear description of the issue and potential impact
- Affected versions and environment details (Python/FastAPI/Starlette versions)
- Minimal reproduction steps or a proof-of-concept (PoC), if available
- Any known mitigations or suggested fixes

## Response Expectations

Because this project is maintained in spare time, I cannot guarantee:
- A specific acknowledgement time,
- Fix timelines,
- Backports to older versions, or
- Coordinated disclosure dates.

If the issue is severe, I will prioritize it as much as reasonably possible. In some cases, I may recommend mitigation steps or a workaround while a fix is being developed.

## Disclosure

I aim to follow responsible disclosure practices:
- I will generally avoid public discussion of details until a fix is released.
- After a patch is available, I may publish brief release notes describing the issue at a high level.

## User Responsibilities and Risk

`fastapi-prodkit` affects logging, error handling, and optional observability integrations. You are responsible for evaluating and operating this software securely in your environment, including but not limited to:

- Avoid logging sensitive data (credentials, tokens, PII) in headers and bodies.
- Keep `include_error_details_in_response=False` in production to reduce information leakage.
- Restrict access to `/metrics` and any tracing/export endpoints where appropriate.
- Review optional integrations for data egress, authentication, and network exposure.

## Disclaimer (No Warranty / Limitation of Liability)

This project is provided on an **"AS IS"** basis, without warranties or conditions of any kind, express or implied. Use of this project is at your own risk.

To the maximum extent permitted by applicable law, the maintainer(s) shall not be liable for any claim, damages, or other liability arising from, out of, or in connection with the software or the use or other dealings in the software. You assume full responsibility for any security risks, configuration choices, and operational outcomes resulting from the use of this project.

## Credits

Responsible disclosure is appreciated. If you would like to be credited in release notes, please mention it in your report (or request anonymity).