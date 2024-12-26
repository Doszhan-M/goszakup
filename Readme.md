# GosZakup Bot  


# Description

The project is designed to participate in government procurement tenders. It automates authentication, application submission, and document management on the procurement platform.

## Key Features

### Authentication:
- Performed via EDS (Electronic Digital Signature) using NCALayer.

### Tender Management:
- Checking the current status of a tender.
- Automated application submission.
- Cancellation of previously submitted applications.

### Document Handling:
- Generation, signing, and uploading of mandatory documents.
- Application status verification.

## Project Structure

### Root Directory:
- **docker-compose.yml**: Configuration for running the application in Docker.
- **requirements.txt**: Project dependencies.
- **Readme.md**: Instructions for working with the project.

### Directories:
- **tender_pw/**:
  - **app/**: Code for tender management, APIs, and business logic.
  - **Dockerfile**: Application containerization.
- **signer/**:
  - Manages EDS and interacts with NCALayer via gRPC.
- **dashboard/**:
  - Django application for monitoring and tender management.
- **scripts/**:
  - Utilities for setting up the environment, running services, and working with NCALayer.


## [Control](readme/control.md)

## [URLs](readme/urls.md)

## [Installation](readme/install.md)

## [Procedure for participation in the tender](readme/tender.md)

## [Pritunl on Debian 11](readme/pritunl.md)
