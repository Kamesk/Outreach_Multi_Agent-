from services.s3_service import S3Service
from services.linkedin_upload_service import LinkedInUploadService
from services.linkedin_post_service import LinkedInPostService
from utils.logger import get_logger

logger = get_logger("orchestrator")


class PostingOrchestrator:

    def __init__(self, settings):
        self.settings = settings
        self.s3 = S3Service()

    def execute(self):

        key = self.s3.get_next_object(
            self.settings.BUCKET_NAME,
            self.settings.PREFIX
        )

        if not key:
            return "No approved post to process."

        data = self.s3.read_json(self.settings.BUCKET_NAME, key)

        content = data.get("text", "")
        image_url = data.get("image_url", "")

        asset_urn = LinkedInUploadService.upload_image(
            image_url,
            self.settings.ACCESS_TOKEN,
            self.settings.ORG_ID
        )

        LinkedInPostService.create_post(
            content,
            asset_urn,
            self.settings.ACCESS_TOKEN,
            self.settings.ORG_ID
        )

        self.s3.delete(self.settings.BUCKET_NAME, key)

        return f"Posted content from {key}"
