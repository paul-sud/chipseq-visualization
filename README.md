# chipseq-visualization

# Installation

Install Docker and [`docker-compose`](https://docs.docker.com/compose/). On MacOS this can be accomplished by simply installing [Docker Desktop](https://docs.docker.com/docker-for-mac/install/).

Create `.env` file in the repo root, see [this template](./backend/corr_end/.env.example). You can create a secret key using the following one-liner:

```bash
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'
```

## AWS Setup (local development only)

Configure the AWS CLI, assuming you already [installed it](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html) and [set up your default credentials](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html#cli-configure-quickstart-config). Edit `.aws/credentials` in your home directory to add the following profile (you should have a `default` profile in there after initial configuration).

```
[aditya-lambda-cli]
region = us-west-2
output = json
role_arn = "{ADITYA-LAMBDA-CLI ROLE_ARN - AWS CHERRY LAB ACCESS REQUIRED HERE}"
source_profile = default
```

In production, you will rely IAM Roles, for example for [EC2](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html). Containers inherit IAM Role from the host instance.

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
