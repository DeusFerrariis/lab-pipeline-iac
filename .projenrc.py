from projen.awscdk import AwsCdkPythonApp

project = AwsCdkPythonApp(
    author_email="cleghornw04@proton.me",
    author_name="Will C IV",
    cdk_version="2.1.0",
    module_name="lab_pipeline_iac",
    name="lab-pipeline-iac",
    poetry=True,
    version="0.1.0",
)

project.synth()