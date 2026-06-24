# QHUB

QHUB is a quantum notebook workspace MVP for launching, editing, and running
quantum computing notebooks through a web-first interface. It brings together a
SaaS-style dashboard, notebook management, device visibility, queued jobs,
credits, and a guided notebook experience for quantum workflows.

The public repository contains only the deployed static web artifact for the
QHUB MVP. The application source code, backend runtime materials, product notes,
and development history are maintained privately by QANTLabs.

## Live App

Use QHUB here:

https://qantlabs.github.io/QHUB/

## What QHUB Demonstrates

- A hosted quantum notebook dashboard experience.
- Notebook creation, template selection, and interactive notebook views.
- Device and job surfaces for quantum runtime workflows.
- Billing/credit, settings, and authentication flows for a SaaS product shell.
- A responsive public MVP frontend backed by local mock clients for evaluation.

## Repository Contents

This repository is deploy-only. It contains the compiled GitHub Pages output:

- `index.html`
- `404.html`
- `.nojekyll`
- compiled JavaScript, CSS, font, and media assets under `assets/`
- public static files such as `favicon.svg`

It does not contain the TypeScript/React source code, Jupyter backend/runtime
source, notebooks, Docker configuration, or internal project documents.

## License

QHUB is proprietary software owned by QANTLabs. The public deployment artifact
is provided for viewing and evaluation only. No rights are granted to copy,
modify, redistribute, host, resell, commercialize, reverse engineer, or create
derivative works from QHUB without prior written permission from QANTLabs.

For licensing or partnership enquiries, contact QANTLabs.
