import os
from aws_cdk import CfnOutput
from aws_cdk import Stack
from aws_cdk import aws_codecommit as codecommit
from aws_cdk import aws_codepipeline as codepipeline
from aws_cdk import aws_codepipeline_actions as codepipeline_actions
from aws_cdk import aws_s3 as s3
from aws_cdk import aws_iam as iam
from aws_cdk import aws_codebuild as codebuild
from constructs import Construct


class LabPipelineStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        developer_group = iam.Group(self, "LabPipelineDeveloper")

        # Lab CDK Repository
        source_repo = codecommit.Repository(
            self, "LabRepository", repository_name="Lab-Pipeline-CDK-Repository"
        )
        clone_url_http = CfnOutput(
            self, "LabRepoCloneUrlHttp", value=source_repo.repository_clone_url_http
        )
        clone_url_ssh = CfnOutput(
            self, "LabRepoCloneUrlSsh", value=source_repo.repository_clone_url_ssh
        )
        source_repo.grant_pull_push(developer_group)

        # Deployment pipeline
        lab_pipeline = codepipeline.Pipeline(self, "LabPipeline")

        # Lab CDK Repository Source
        source_output = codepipeline.Artifact("SourceArtifact")

        source_stage = lab_pipeline.add_stage(stage_name="Source")
        source_action = codepipeline_actions.CodeCommitSourceAction(
            action_name="Source",
            output=source_output,
            repository=source_repo,
        )
        source_stage.add_action(source_action)

        # Archive Stage
        artifact_bucket = s3.Bucket(self, "LabPipelineArtifacts")

        deploy_action = codepipeline_actions.S3DeployAction(
            action_name="S3ArchiveSource",
            bucket=artifact_bucket,
            input=source_output,
        )
        deploy_stage = lab_pipeline.add_stage(stage_name="Deploy")
        deploy_stage.add_action(deploy_action)

        pl_project = codebuild.PipelineProject(
            self,
            "ArchiveS3Synth",
            build_spec=codebuild.BuildSpec.from_object({
                "version": "2.0",
                "phases": {
                    "install": {
                        "commands": [
                            "sh <(curl -L https://nixos.org/nix/install) --no-daemon",
                            "nix develop --extra-experimental-features flakes",
                        ],
                    },
                    "synth" : {
                        "commands": [
                            "cdk synth > synth-output.txt"
                        ],
                    },
                },
                "artifacts": {
                    "files": ["./synth-output.txt"],
                }
            }),
        )

        codebuild_action = codepipeline_actions.CodeBuildAction(
            action_name="CDKSynth",
            project=pl_project,
            input=source_output,
        )

        codebuild_stage = lab_pipeline.add_stage(stage_name="CDKSynthArchive")
        codebuild_stage.add_action(codebuild_action)
        # TODO: deploy to code build
        # TODO: codebuild save synth output to artifact bucket
