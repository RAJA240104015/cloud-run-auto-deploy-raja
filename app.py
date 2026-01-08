# cloudbuild.yaml
options:
  logging: CLOUD_LOGGING_ONLY
  substitutionOption: ALLOW_LOOSE

substitutions:
  _REGION: 'us-central1'

steps:
  # Step 1: Memulai Build Docker Image
  - id: 'Start Build'
    name: 'gcr.io/cloud-builders/docker'
    args:
      [
        'build',
        '-t', 'gcr.io/$PROJECT_ID/cloud-run-app:${BRANCH_NAME}-${SHORT_SHA}',
        '.'
      ]
    waitFor: ['-']
    entrypoint: 'bash'
    env:
      - 'BRANCH_NAME=$BRANCH_NAME'
      - 'SHORT_SHA=$SHORT_SHA'

  # Step 2: Push Docker Image ke Google Container Registry
  - id: 'Push Image'
    name: 'gcr.io/cloud-builders/docker'
    args:
      [
        'push',
        'gcr.io/$PROJECT_ID/cloud-run-app:${BRANCH_NAME}-${SHORT_SHA}'
      ]
    waitFor: ['Start Build']

  # Step 3: Deploy ke Cloud Run
  - id: 'Deploy Cloud Run'
    name: 'gcr.io/google.com/cloudsdktool/cloud-sdk'
    entrypoint: 'gcloud'
    args:
      [
        'run', 'deploy', 'cloud-run-app',
        '--image', 'gcr.io/$PROJECT_ID/cloud-run-app:${BRANCH_NAME}-${SHORT_SHA}',
        '--region', '$_REGION',
        '--platform', 'managed',
        '--allow-unauthenticated'
      ]
    waitFor: ['Push Image']

images:
  - 'gcr.io/$PROJECT_ID/cloud-run-app:${BRANCH_NAME}-${SHORT_SHA}'
