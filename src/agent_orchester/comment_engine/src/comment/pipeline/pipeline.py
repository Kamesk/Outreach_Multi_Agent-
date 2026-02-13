from src.components.stage_1_data_ingestion import DataIngestion
from src.components.stage_2_mongodb_saver import MongoSaver
from src.components.stage_3_model_llm import LLMModel
from src.components.stage_4_response_poster import ResponsePoster

class Pipeline:
    def __init__(self):
        self.ingestor = DataIngestion()
        self.saver = MongoSaver()
        self.llm = LLMModel()
        self.poster = ResponsePoster()

    def run_all_stages(self):
        posts = self.ingestor.fetch_posts()
        for post in posts:
            comments = self.ingestor.fetch_comments(post_id=post["id"])
            for comment in comments:
                comment_id = comment["id"]
                text = comment["text"]
                self.saver.save_comment({"comment_id": comment_id, "text": text})
                feedback = self.llm.get_feedback(text)
                self.poster.update_db_with_response(comment_id, feedback)
                self.poster.post_response(comment_id, feedback)