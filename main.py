import asyncio
import logging
import os

import rasa.utils.io
from rasa.cli import train
from rasa.core.agent import Agent
from rasa.core.interpreter import NaturalLanguageInterpreter
from rasa.core.utils import AvailableEndpoints
from rasa.model import get_model, get_model_subdirectories
from rasa.shared.constants import DEFAULT_MODELS_PATH
from rasa.shared.nlu.interpreter import RegexInterpreter
from rasa.shared.utils.cli import print_error
from rasa.shared.utils.io import read_config_file
from rasa.shared.utils.validation import validate_yaml_schema

logger = logging.getLogger(__name__)

async def load_agent(model_path: str) -> Agent:
    logger.debug(f"Loading agent model from '{model_path}'...")

    try:
        model_path = get_model(model_path)
        zipped_model = await rasa.utils.io.read_zip_file(model_path)
        fingerprint = await rasa.utils.io.get_model_fingerprint(zipped_model)
        model_path = os.path.join(model_path, DEFAULT_MODELS_PATH)

        if os.path.exists(model_path):
            domain = await rasa.utils.io.read_yaml_file(os.path.join(model_path, "domain.yml"))
            validate_yaml_schema(domain, "domain")

            nlu = await NaturalLanguageInterpreter.create(
                os.path.join(model_path, "nlu"),
                endpoint=AvailableEndpoints.read_endpoints(model_path),
            )

            agent = Agent.load(
                model_path,
                interpreter=nlu,
                generator=RegexInterpreter(),
                action_endpoint=AvailableEndpoints.read_endpoints(model_path).action,
                fingerprint=fingerprint,
            )

            logger.debug(f"Successfully loaded agent model from '{model_path}'.")
            return agent

        else:
            raise ValueError(f"No domain file found in '{model_path}'.")
    except Exception as e:
        logger.exception(f"Failed to load agent model from '{model_path}': {e}")
        raise

async def handle_user_input(user_input: str, agent: Agent) -> str:
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, agent.handle_text, user_input)
        responses = [r.get("text") for r in result]
        return "\n".join(responses)
    except Exception as e:
        logger.exception(f"Failed to handle user input: {e}")
        return ""

async def main():
    # Train the model
    train.run(
        domain="domain.yml",
        config="config.yml",
        training_files="data/",
        output_path="models/",
    )

    # Load the model
    model_subdirectories = get_model_subdirectories("models")
    model_path = os.path.join("models", max(model_subdirectories))
    agent = await load_agent(model_path)

    # Chat loop
    while True:
        user_input = input("You: ")
        if not user_input:
            break
        response = await handle_user_input(user_input, agent)
        print(f"Bot: {response}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
