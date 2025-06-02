import os
import logging


import anthropic
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader, select_autoescape

# configure logging
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# load template environment
jinja = Environment(
    loader=FileSystemLoader("prompts"),
    autoescape=select_autoescape(["html", "xml"]),
)
tag_list_template = jinja.get_template("tag-list.txt")
tagging_template = jinja.get_template("summary-tagging.txt")

tags = ["poetry", "ocean", "nature"]

tag_list_prompt = ""
if tags:
    tag_list_prompt = tag_list_template.render(
        tag_list=", ".join(tags)
    )
document_content = "todo"
tagging_prompt = tagging_template.render(
    tag_list_prompt=tag_list_prompt,
    document_content=document_content
)
print(tagging_prompt)

# load_dotenv()
# model = os.getenv("MODEL", "claude-opus-4-20250514")
# logger.debug(f"using model: {model}")

# client = anthropic.Anthropic()

# message = client.messages.create(
#     model=model,
#     max_tokens=1000,
#     temperature=1,
#     system="You are a world-class poet. Respond only with short poems.",
#     messages=[
#         {
#             "role": "user",
#             "content": [{"type": "text", "text": "Why is the ocean salty?"}],
#         }
#     ],
# )
# print(message.content)
