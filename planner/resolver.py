import json
import re


REFERENCE_PATTERN = r"\{step_(\d+)\.result\}"


def resolve_arguments(arguments, results):

    text = json.dumps(arguments)

    def replace(match):

        index = int(match.group(1))

        if index >= len(results):
            raise ValueError(
                f"Unknown plan reference: {match.group(0)}"
            )

        return str(results[index])

    text = re.sub(
        REFERENCE_PATTERN,
        replace,
        text,
    )

    return json.loads(text)