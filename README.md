# TsibraBot

This project contains source code and supporting files for a serverless application that you can deploy with the SAM CLI. It includes the following files and folders.

- src - Code for the application's Lambda function.
- template.yaml - A template that defines the application's AWS resources.

### Resources
* AWS Lambda functions
* AWS API Gateway
* AWS CloudFormation
* SmallTalk service from Google Dialogflow.

## Configuration
It is assumed that you already have AWS and Google accounts.


### Update AWS IAM Permissions
* Go to `IAM` -> `Users` (choose your user). Select `Add permissions` -> add `AmazonAPIGatewayAdministrator`, `AmazonS3FullAccess`, `AWSCloudFormationFullAccess`;
* Select `Add inline policy` -> `JSON` and put follow:
 ```bash    
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "lambda:CreateFunction",
                "lambda:InvokeFunction",
                "iam:CreateRole",
                "iam:DeleteRole",
                "iam:AttachRolePolicy",
                "lambda:InvokeAsync",
                "lambda:GetFunctionConfiguration",
                "iam:PutRolePolicy",
                "lambda:UpdateAlias",
                "lambda:UpdateFunctionCode",
                "iam:PassRole",
                "iam:DetachRolePolicy",
                "lambda:AddPermission",
                "lambda:CreateAlias"
            ],
            "Resource": "*"
        }
    ]
}
```

### Dialogflow

* Go to https://dialogflow.cloud.google.com/
* Click `Create new agent`, fill in the required fields (set DEFAULT LANGUAGE = `ru`) and click `Create`
* Next: `Prebuilt Agents` -> `Small Tallk` -> `Import` -> `Create From Template`
* Choose your agent -> `Settings` and click on `Project ID` field, it should redirect you to gcloud platform. In main menu choose `IAM` -> `Service accounts` -> `Create service account`
* Fill in the required fields (In field `Select a role` choose `Basic` -> `Owner`) -> `Done`
* Select your service account (field `Email`) -> `Keys` -> `Add Key` -> `Create new key` -> `JSON`.

### Create your telegram bot
* Open Telegram app, search for @BotFather and start the chat.
* Send `/newbot` command and follow the instructions. After completing the initial steps, you’ll get your own TOKEN


## Deploy the sample application

* Clone repository
* Copy the contents of the downloaded file in json format to the `private_key.json` file

Install awscli
```bash 
pip install awscli
```
You need to configure your AWS credentials
```bash 
aws configure
```

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications

Install the SAM CLI
```bash 
pip install aws-sam-cli
```

Build your application with the `sam build` command.

```bash
$ sam build
```

The SAM CLI installs dependencies defined in `src/requirements.txt`, creates a deployment package, and saves it in the `.aws-sam/build` folder.

Deploy your application with the` sam deploy command.

```bash
$ sam deploy --guided --parameter-overrides 'TelegramToken=<you_telegram_bot_token>
```

### Set API WebHook
For APIGatevay to track bot activity - register a webhook via telegram api.
Go to the AWS Lambda console, select ApiGateway and copy path from it
Paste in yor browser
```bash
https://api.telegram.org/bot<you_telegram_bot_token>/setWebHook?url=<url_from_your_deployed_ApiGateway>
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name tsibraBot
```
