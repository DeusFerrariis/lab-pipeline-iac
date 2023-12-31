import os
from aws_cdk import App, Environment
from lab_pipeline_iac.main import LabPipelineStack

# for development, use account/region from cdk cli
dev_env = Environment(
  account=os.getenv('CDK_DEFAULT_ACCOUNT'),
  region=os.getenv('CDK_DEFAULT_REGION')
)

app = App()
LabPipelineStack(app, "lab-pipeline-iac-dev", env=dev_env)
# MyStack(app, "lab-pipeline-iac-prod", env=prod_env)

app.synth()
