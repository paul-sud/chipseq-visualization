# chipseq-visualization

# Installation

Install Docker and [`docker-compose`](https://docs.docker.com/compose/). On MacOS this can be accomplished by simply installing [Docker Desktop](https://docs.docker.com/docker-for-mac/install/).

Create `.env` file in the repo root, see [this template](./backend/corr_end/.env.example)

## Backend Setup

1. Configure AWS CLI, assuming you already installed and set up default your credentials. Edit `.aws/credentials` in your home directory to add the following profile.

```
[aditya-lambda-cli]
region = us-west-2
output = json
role_arn = "{ADITYA-LAMBDA-CLI ROLE_ARN - AWS CHERRY LAB ACCESS REQUIRED HERE}"
source_profile = default
```

# Running the application

Run the following command. This may take a while on the first go since it will build images.

```bash
docker-compose up
```

Before hitting any endpoints run the following to create tables:
```bash
docker-compose run backend python corr_end/manage.py migrate
```

Frontend will be accessible on http://localhost:3000/ and backend on http://localhost:8000/

# Troubleshooting (Cherry Lab Members With Access to Cherry Lab AWS only)

Occasionally, if the correlations request to the back end fails or if multiple requests are submitted at once, the AWS lambda function might crash. Go to the SQS page and check "jaccard3-success" and "jaccard3-failure" and "jaccard3-unprocessed"; make sure all 3 SQS queues are cleared before submitting a new request.
