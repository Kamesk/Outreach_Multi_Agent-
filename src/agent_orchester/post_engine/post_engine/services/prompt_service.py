import yaml

class PromptService:

    @staticmethod
    def load_prompt(path: str):
        with open(path, "r") as f:
            data = yaml.safe_load(f)

        return (
            data["generate_post"]["system"],
            data["generate_post"]["user"],
            data["generate_image"]["prompt"]
        )