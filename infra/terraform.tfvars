vpc_id = "vpc-xxxxxxx"

# Copy this file outside version control and supply real environment-specific IDs.
public_subnets = ["subnet-aaaa", "subnet-bbbb"]
private_subnets = ["subnet-cccc", "subnet-dddd"]
image_tag = "replace-with-immutable-image-tag"
bucket_arn = "arn:aws:s3:::replace-me"
dynamodb_table_arns = ["arn:aws:dynamodb:eu-west-2:123456789012:table/Commentpayloads"]
secret_arns = {
  OPENAI_API_KEY = "arn:aws:secretsmanager:eu-west-2:123456789012:secret:outreach/openai"
  WEBHOOK_SIGNING_SECRET = "arn:aws:secretsmanager:eu-west-2:123456789012:secret:outreach/webhook"
}

certificate_arn = "arn:aws:acm:xxxxxxxxxx"
